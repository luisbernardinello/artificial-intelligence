import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#  Calcula a distância euclidiana entre um conjunto de dados e um exemplo de teste
def euclidean_distance(data, test):
    distance = np.sqrt(np.sum((data - test)**2, axis=1))
    return distance

# Retorna o elemento mais comum de uma lista (determina a classe mais frequente entre os vizinhos)
def most_common(lst):
    return max(set(lst), key=lst.count)

# Classe K-NN
class KNeighborsClassifier:
    def __init__(self, k=3): # K eh o numero de vizinhos
        self.k = k
        self.X_train = None
        self.y_train = None
    
    # Simula o treinamento (armazena os dados de treinamento)
    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    # Faz a predição
    def predict(self, X_test):
        neighbors = []
        for x in X_test:
            # calcula a distância euclidiana para o exemplo de teste
            distances = euclidean_distance(self.X_train, x)
            # ordena os exemplos de treinamento de acordo com a distância para o exemplo de teste
            y_sorted = [y for _, y in sorted(zip(distances, self.y_train))]
            # adiciona na lista neighbors somente os k vizinhos mais próximos
            neighbors.append(y_sorted[:self.k])
        return list(map(most_common, neighbors))

    # Avaliar o desempenho do K-NN
    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        accuracy = sum(y_pred == y_test) / len(y_test)
        return accuracy

# dados de treinamento e teste
data_train = pd.read_csv("data1_train.csv")
data_test = pd.read_csv("data1_test_labeled.csv")

# Separando os dados de treinamento entre atributos preditivos e classe
X_train = np.array(data_train.iloc[:, :-1])
y_train = np.array(data_train.iloc[:, -1])

# Separando os dados de teste entre atributos preditivos e classe
X_test = np.array(data_test.iloc[:, :-1])
y_test = np.array(data_test.iloc[:, -1])

# k que serão testados
k_values = [1, 3, 5, 11, 45, 95]
accuracies = []

# Executa o KNN para cada valor de k e calcula a acurácia
for k in k_values:
    knn = KNeighborsClassifier(k=k)
    knn.fit(X_train, y_train)
    accuracy = knn.evaluate(X_test, y_test)
    accuracies.append(accuracy)
    print(f"Acurácia para k={k}: {accuracy:.4f}")

# Plota o gráfico de acurácia em função dos valores de k
plt.figure(figsize=(10, 6))
plt.plot(k_values, accuracies, marker='o', linestyle='-', color='b')
plt.xlabel("valor de k")
plt.ylabel("acurácia")
plt.title("Gráfico da acurácia do K-NN para diferentes valores de k")
plt.xticks(k_values)
plt.grid(True)
plt.show()
