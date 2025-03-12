import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Carrega o conjunto de treinamento usando a pandas
data = pd.read_csv('data1_train.csv')

# Faz o mapeamento das classes pelo label A, B ou C, atribuindo 0, 1 ou 2 respectivamente para facilitar
data['CLASS'] = data['CLASS'].map({'A': 0, 'B': 1, 'C': 2})

# Separa os dados de entrada (caracteristicas) e os rótulos (classes)
# X -> características, Y -> classes.
X = data[['A1', 'A2', 'A3', 'A4']].values.T  # Transposição para alinhar o formato dos dados.
Y = data['CLASS'].values

# Normaliza os dados de entrada (X) dividindo pelo maior valor de cada característica.
# A normalização ajuda a padronizar os dados para a rede aprender melhor.
X = X / X.max(axis=1, keepdims=True)


m = X.shape[1]  # Quantidade total de exemplares
data_dev_split = int(0.2 * m)  # Define 20% do total para validação (80% para treinamento) de modo a avaliar a performance da rede
X_dev, Y_dev = X[:, :data_dev_split], Y[:data_dev_split]  # Dados de validação
X_train, Y_train = X[:, data_dev_split:], Y[data_dev_split:]  # Dados de treinamento
m_train = X_train.shape[1]  # Quantidade de exemplares de treino

# Inicializa os parâmetros da rede (pesos e vieses).
def init_params():
    # Atribui pesos e vieses aleatórios para a camada oculta (10 neurônios) e para a camada de saida (3 neurônios).
    W1 = np.random.rand(10, 4) - 0.5  # Pesos para a primeira camada
    b1 = np.random.rand(10, 1) - 0.5  # Vieses para a primeira camada
    W2 = np.random.rand(3, 10) - 0.5  # Pesos para a camada de saída
    b2 = np.random.rand(3, 1) - 0.5  # Vieses para a camada de saída
    return W1, b1, W2, b2

# Técnica de Dropout, inclui ruido para que a rede dependa menos de neurônios específicos de modo a evitar o overfitting e generalizar melhor
def dropout(A, p=0.2):
    # p é a probabilidade de desativar um neurônio, 20% dos neurônios serão desativados.
    mask = np.random.rand(*A.shape) > p  # Máscara para aplicar dropout
    A = A * mask  # Desativa os neurônios
    A = A / p  # Ajuste para manter a escala da saída
    return A

# Função de ativação ReLU (Unidade Linear Retificada) para introduzir não-linearidade (decide se um neurônio deve ser ativado ou não).
def ReLU(Z):
    return np.maximum(Z, 0)  # Define valores negativos como zero

# Função de ativação softmax (força a saída da rede a representar a probabilidade dos dados serem de uma das classes definidas).
def softmax(Z):
    A = np.exp(Z) / np.sum(np.exp(Z), axis=0, keepdims=True)
    return A

# Calcula as ativações da rede usando as entradas e os parâmetros.
def forward_prop(W1, b1, W2, b2, X, apply_dropout=True, p=0.2):
    # Primeira etapa, camada oculta
    Z1 = W1.dot(X) + b1  # Z1 é a entrada linear para os neurônios da primeira camada, obtida multiplicando as entradas (X) pelos pesos (W1) e adicionando um valor de viés (b1).
    A1 = ReLU(Z1)  #  ReLU para introduzir transformação não linear convertendo valores negativos para zero
    if apply_dropout:
        A1 = dropout(A1, p=p)  # Dropout para evitar overfitting
    # Segunda etapa, camada de saída
    Z2 = W2.dot(A1) + b2  # Z2 é a entrada linear para a camada de saída que representa as somas ponderadas dos neurônios da camada anterior.
    A2 = softmax(Z2)  # Softmax converte os valores de Z2 para indicar a probabilidade de cada exemplar de entrada pertencer a cada classe (A, B ou C)
    return Z1, A1, Z2, A2

# Derivada da função ReLU para a fase de backpropagation.
def ReLU_deriv(Z):
    return Z > 0  # Define a derivada como 1 para valores positivos e 0 para negativos

# Converte os rótulos 0, 1 e 2 das classes em vetores para facilitar o cálculo do erro durante o treinamento.
def one_hot(Y):
    one_hot_Y = np.zeros((Y.size, Y.max() + 1)) # Matriz de zeros em que cada linha é uma classe
    one_hot_Y[np.arange(Y.size), Y] = 1 # Para cada exemplar de treinamneto, coloca 1 na coluna correspondente a classe correta, transformando cada rótulo em um vetor (com uma posição 1)
    return one_hot_Y.T # Retorna transposta para facilitar outras operações

# Backpropagation calcula os gradientes para ajustar os parâmetros da rede.
def backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y):
    m = X.shape[1] # Número de exemplares
    one_hot_Y = one_hot(Y)  # Converte rótulos Y para o formato onehot para cacular o erro de saída
    dZ2 = A2 - one_hot_Y  # Erro da camada de saída
    dW2 = 1 / m * dZ2.dot(A1.T)  # Gradiente dos pesos da camada de saída (quanto cada peso contribui para o erro)
    db2 = 1 / m * np.sum(dZ2, axis=1, keepdims=True)  # Gradiente dos vieses da camada de saída
    dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)  # Erro da camada oculta, propagando o erro de saída para trás usando a derivada da ReLu (ajusta valores positivos)
    dW1 = 1 / m * dZ1.dot(X.T)  # Gradiente dos pesos da camada oculta
    db1 = 1 / m * np.sum(dZ1, axis=1, keepdims=True)  # Gradiente dos vieses da camada oculta
    return dW1, db1, dW2, db2

# Atualiza os parâmetros da rede utilizando os gradientes e uma taxa de aprendizado (alpha).
def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    # Ajusta os pesos e vieses da camada oculta (W1 e b1) e da camada de saída (W2 e b2) tendo como base os gradientes calculados e na taxa de aprendizado alpha
    W1 = W1 - alpha * dW1  # Atualiza os pesos W1
    b1 = b1 - alpha * db1  # Atualiza os vieses b1
    W2 = W2 - alpha * dW2  # Atualiza os pesos W2
    b2 = b2 - alpha * db2  # Atualiza os vieses b2
    return W1, b1, W2, b2

# Retorna as previsões da rede, em que para cada exemplar identifica a classe com maior probabilidade e retorna o índice da classe para cada entrada.
def get_predictions(A2):
    return np.argmax(A2, axis=0)

# Faz o cálculo da acurácia das previsões, comparando as previsões com os valores reais (Y), calculando quantas vezes a rede previu corretamente
def get_accuracy(predictions, Y):
    return np.sum(predictions == Y) / Y.size

# Função de treinamento da rede neural, que executa várias iterações do gradiente descendente.
def gradient_descent(X, Y, alpha, iterations):
    W1, b1, W2, b2 = init_params()  # Inicializa os pesos e vieses
    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)  # Propagação para frente para calcular a saída da rede
        dW1, db1, dW2, db2 = backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y)  # Propagação para trás calculando o erro e os ajustes necessários
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)  # Atualiza os pesos e vieses
        if i % 10 == 0: # A cada 10 iterações calcula e exibe acurácia
            predictions = get_predictions(A2)
            accuracy = get_accuracy(predictions, Y)
            print(f"Iteração: {i}, Acurácia: {accuracy:.3f}")
    return W1, b1, W2, b2

############################## Treinamento do modelo

# Treina a rede neural com os dados de treino.
W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 0.1, 500)

############################## Testa o modelo com dados de teste

# Carrega e normaliza os dados de teste.
test_data = pd.read_csv('data1_test.csv')
X_test = test_data[['A1', 'A2', 'A3', 'A4']].values.T
X_test = X_test / X_test.max(axis=1, keepdims=True)  # Normalização

# Faz previsões no conjunto de teste.
def make_predictions(X, W1, b1, W2, b2):
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, X)
    predictions = get_predictions(A2)
    return predictions

# Gera as previsões para os dados de teste.
test_predictions = make_predictions(X_test, W1, b1, W2, b2)

############################## Printa tabela do DataFrame com predições no terminal

# Adiciona a coluna de previsões ao DataFrame de teste.
test_data['PREDICTIONS'] = test_predictions

# Faz o mapeamento dos valores numéricos das previsões de volta para as classes A, B ou C.
test_data['PREDICTIONS'] = test_data['PREDICTIONS'].map({0: 'A', 1: 'B', 2: 'C'})

# Printa o DataFrame atualizado com as previsões.
print(test_data)

############################## Plota as predições

# Define mapa de cores do gráfico.
color_map = {'A': 'orange', 'B': 'blue', 'C': 'green'}

# Cria um gráfico
fig, ax = plt.subplots(figsize=(10, 6))

# Plota as predições com as cores para cada classe e contorno para facilitar a distinção.
for label, color in color_map.items():
    subset = test_data[test_data['PREDICTIONS'] == label]
    ax.scatter(subset['A1'], subset['A2'], facecolors='none', edgecolors=color, label=f'Pred {label}', linewidth=1.5)

ax.set_title("Predições")
ax.legend()
plt.show()
