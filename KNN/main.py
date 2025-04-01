import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import time


def euclidean_distance(data, test):
    """
    Calcula a distância euclidiana entre um conjunto de dados e um exemplo de teste.
    Implementação vetorizada para maior eficiência.
    """
    return np.sqrt(np.sum((data - test)**2, axis=1))

def most_common(lst):
    """
    Retorna o elemento mais comum de uma lista.
    Utilizada para determinar a classe mais frequente entre os vizinhos.
    """
    unique_values, counts = np.unique(lst, return_counts=True)
    return unique_values[np.argmax(counts)]

class KNeighborsClassifier:
    """
    Implementação otimizada do algoritmo K-Nearest Neighbors para classificação.
    
    Parâmetros:
    -----------
    k : int, default=3
        Número de vizinhos a considerar para classificação.
    weights : str, default='uniform'
        Método de ponderação: 'uniform' (todos os vizinhos têm o mesmo peso) ou 
        'distance' (pesos proporcionais ao inverso da distância).
    """
    
    def __init__(self, k=3, weights='uniform'):
        self.k = k
        self.weights = weights
        self.X_train = None
        self.y_train = None
        
    def fit(self, X_train, y_train):
        """
        Armazena os dados de treinamento para classificação posterior.
        
        Parâmetros:
        -----------
        X_train : array-like, shape (n_samples, n_features)
            Conjunto de dados de treinamento.
        y_train : array-like, shape (n_samples,)
            Classes correspondentes aos dados de treinamento.
            
        Retorno:
        --------
        self : object
            Retorna a instância do classificador.
        """
        self.X_train = np.array(X_train)
        self.y_train = np.array(y_train)
        return self
    
    def predict(self, X_test):
        """
        Prediz classes para múltiplas amostras.
        
        Parâmetros:
        -----------
        X_test : array-like, shape (n_samples, n_features)
            Dados para predição.
            
        Retorno:
        --------
        y_pred : array, shape (n_samples,)
            Classes preditas.
        """
        predictions = []
        X_test = np.array(X_test)
        
        for x in X_test:
            # Calcula a distância euclidiana entre x e todos os exemplos de treinamento
            distances = euclidean_distance(self.X_train, x)
            
            # Pega os índices dos k vizinhos mais próximos
            nearest_indices = np.argsort(distances)[:self.k]
            nearest_labels = self.y_train[nearest_indices]
            
            if self.weights == 'uniform':
                predictions.append(most_common(nearest_labels))
            else:
                nearest_distances = distances[nearest_indices]
                # Evitar divisão por zero
                nearest_distances = np.maximum(nearest_distances, 1e-10)
                weights = 1.0 / nearest_distances
                
                classes = np.unique(self.y_train)
                class_weights = np.zeros(len(classes))
                
                for i, cls in enumerate(classes):
                    mask = nearest_labels == cls
                    class_weights[i] = np.sum(weights[mask])
                
                predictions.append(classes[np.argmax(class_weights)])
                
        return np.array(predictions)
    
    def evaluate(self, X_test, y_test, verbose=True):
        """
        Avalia o desempenho do classificador.
        
        Parâmetros:
        -----------
        X_test : array-like, shape (n_samples, n_features)
            Dados de teste.
        y_test : array-like, shape (n_samples,)
            Classes verdadeiras.
        verbose : bool, default=True
            Se True, imprime relatório detalhado.
            
        Retorno:
        --------
        accuracy : float
            Acurácia do modelo.
        """
        start_time = time()
        y_pred = self.predict(X_test)
        prediction_time = time() - start_time
        
        accuracy = np.mean(y_pred == y_test)
        
        if verbose:
            print(f"Acuracia: {accuracy:.4f}")
            print(f"Tempo de predicao: {prediction_time:.4f} segundos")
            
            classes = np.unique(np.concatenate((y_test, y_pred)))
            n_classes = len(classes)
            conf_matrix = np.zeros((n_classes, n_classes), dtype=int)
            
            for i in range(len(y_test)):
                true_idx = np.where(classes == y_test[i])[0][0]
                pred_idx = np.where(classes == y_pred[i])[0][0]
                conf_matrix[true_idx, pred_idx] += 1
                
            print("\nMatriz de Confusão:")
            print(conf_matrix)
            
        return accuracy

def cross_validate(model, X, y, k_folds=5):
    """
    Realiza validação cruzada k-fold para avaliar o modelo.
    
    Parâmetros:
    -----------
    model : objeto
        Modelo com métodos fit e predict.
    X : array-like
        Dados de características.
    y : array-like
        Classes correspondentes.
    k_folds : int, default=5
        Número de divisões para validação cruzada.
        
    Retorno:
    --------
    cv_scores : list
        Lista com acurácias para cada fold.
    """
    X = np.array(X)
    y = np.array(y)
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    fold_size = len(X) // k_folds
    
    cv_scores = []
    
    for i in range(k_folds):
        test_indices = indices[i * fold_size:(i + 1) * fold_size]
        train_indices = np.setdiff1d(indices, test_indices)
        
        X_train_fold, X_test_fold = X[train_indices], X[test_indices]
        y_train_fold, y_test_fold = y[train_indices], y[test_indices]
        
        model.fit(X_train_fold, y_train_fold)
        accuracy = model.evaluate(X_test_fold, y_test_fold, verbose=False)
        cv_scores.append(accuracy)
        
        print(f"Fold {i+1}: Acuracia = {accuracy:.4f}")
    
    print(f"\nAcuracia media: {np.mean(cv_scores):.4f} (±{np.std(cv_scores):.4f})")
    return cv_scores

if __name__ == "__main__":
    print("Carregando dados")
    data_train = pd.read_csv("data1_train.csv")
    data_test = pd.read_csv("data1_test_labeled.csv")
    
    # Separa os dados
    X_train = np.array(data_train.iloc[:, :-1])
    y_train = np.array(data_train.iloc[:, -1])
    X_test = np.array(data_test.iloc[:, :-1])
    y_test = np.array(data_test.iloc[:, -1])
    
    print(f"Dimensões dos dados de treinamento: {X_train.shape}")
    print(f"Dimensões dos dados de teste: {X_test.shape}")
    print(f"Classes: {np.unique(y_train)}")
    
    # Valores de k a testar
    k_values = [1, 3, 5, 11, 45, 95]
    weights_options = ['uniform', 'distance']
    
    # Dicionários para armazenar resultados
    results = {
        'uniform': {'k': k_values, 'accuracy': []},
        'distance': {'k': k_values, 'accuracy': []}
    }
    
    # Testando diferentes configurações
    print("\n=== Avaliação de Diferentes Configurações do KNN ===")
    best_accuracy = 0
    best_config = {'k': None, 'weights': None}
    
    for weights in weights_options:
        print(f"\n-- Metodo de ponderacao: {weights} --")
        
        for k in k_values:
            print(f"\nAvaliando k={k}:")
            knn = KNeighborsClassifier(k=k, weights=weights)
            knn.fit(X_train, y_train)
            accuracy = knn.evaluate(X_test, y_test, verbose=False)
            results[weights]['accuracy'].append(accuracy)
            
            print(f"Acuracia para k={k}, weights='{weights}': {accuracy:.4f}")
            
            # Atualiza a melhor configuração
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_config = {'k': k, 'weights': weights}
    
    # Exibindo a melhor configuração
    print(f"\n=== Melhor Configuracao ===")
    print(f"k = {best_config['k']}, weights = '{best_config['weights']}'")
    print(f"Acuracia: {best_accuracy:.4f}")
    
    # Validação cruzada para a melhor configuração
    print("\n=== Validacao Cruzada para a Melhor Configuracao ===")
    best_knn = KNeighborsClassifier(k=best_config['k'], weights=best_config['weights'])
    cv_scores = cross_validate(best_knn, np.concatenate((X_train, X_test)), 
                              np.concatenate((y_train, y_test)), k_folds=5)
    
    # Avaliação final com a melhor configuração
    print("\n=== Avaliacao Final ===")
    final_knn = KNeighborsClassifier(k=best_config['k'], weights=best_config['weights'])
    final_knn.fit(X_train, y_train)
    final_knn.evaluate(X_test, y_test, verbose=True)
    
    # Gráfico de resultados
    plt.figure(figsize=(12, 8))
    
    for weights in weights_options:
        plt.plot(k_values, results[weights]['accuracy'], 
                marker='o', linestyle='-', label=f'weights="{weights}"')
    
    plt.xlabel("Valor de k")
    plt.ylabel("Acuracia")
    plt.title("Acuracia do KNN para diferentes valores de k e metodos de ponderacao")
    plt.xticks(k_values)
    plt.grid(True)
    plt.legend()
    
    # Destacando a melhor configuração
    best_idx = k_values.index(best_config['k'])
    best_y = results[best_config['weights']]['accuracy'][best_idx]
    plt.scatter([best_config['k']], [best_y], color='red', s=100, 
                label=f'Melhor: k={best_config["k"]}, weights="{best_config["weights"]}"')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('knn_performance.png', dpi=300)
    plt.show()