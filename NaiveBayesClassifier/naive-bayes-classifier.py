import pandas as pd
import numpy as np
import random
from math import sqrt, pi, exp, log
from itertools import chain

class NaiveBayesClassifier:
    def __init__(self):
        self.summaries = None
        self.classes = None
        self.total_rows = 0
    
    def read_data(self, filepath='house-votes-84.data'):
        """
        Lê os dados do arquivo usando pandas e retorna um DataFrame
        """
        # Cria nomes de colunas para o dataset
        cols = ['class'] + [f'attribute_{i}' for i in range(1, 17)]
        
        # Lê o arquivo como um DataFrame pandas
        df = pd.read_csv(filepath, header=None, names=cols)
        return df
    
    def preprocess_data(self, df):
        """
        Pré-processa os dados convertendo y/n/? para valores numéricos
        """
        # Cria uma cópia para não modificar o original
        df_processed = df.copy()
        
        # Mapeamento para conversão
        mapping = {'y': 2, 'n': 1, '?': 0}
        
        # Aplica o mapeamento a todas as colunas exceto a classe
        for col in df_processed.columns[1:]:
            df_processed[col] = df_processed[col].map(mapping)
            
        return df_processed
    
    def gaussian_probability(self, x, mean, stdev):
        """
        Calcula a probabilidade gaussiana
        """
        if stdev == 0:  # Evita divisão por zero
            return 0.0
            
        exponent = exp(-(pow(x - mean, 2) / (2 * pow(stdev, 2))))
        return (1 / (sqrt(2 * pi) * stdev)) * exponent
    
    def train(self, df):
        """
        Treina o modelo usando o DataFrame fornecido
        """
        # Dicionário para armazenar estatísticas por classe
        self.summaries = {}
        self.classes = df['class'].unique()
        self.total_rows = len(df)
        
        # Separa o DataFrame por classe
        for class_value in self.classes:
            self.summaries[class_value] = []
            class_data = df[df['class'] == class_value].iloc[:, 1:]  # Exclui coluna de classe
            
            # Calcula estatísticas para cada atributo
            for column in class_data:
                col_data = class_data[column]
                self.summaries[class_value].append([
                    col_data.mean(),
                    col_data.std(), 
                    len(col_data)
                ])
                
        return self.summaries
    
    def predict_probabilities(self, row):
        """
        Calcula a probabilidade de uma linha pertencer a cada classe
        """
        probabilities = {}
        
        for class_value, class_summaries in self.summaries.items():
            # Probabilidade a priori da classe
            class_probability = class_summaries[0][2] / float(self.total_rows)
            gaussian_probabilities_sum = 0
            
            # Soma os logaritmos das probabilidades para evitar underflow
            for i, feature_value in enumerate(row):
                mean, stdev, _ = class_summaries[i]
                gaussian_prob = self.gaussian_probability(feature_value, mean, stdev)
                # Use log para evitar valores muito pequenos
                if gaussian_prob > 0:  # Evita log(0)
                    gaussian_probabilities_sum += log(gaussian_prob)
                else:
                    # Penalidade para probabilidade zero
                    gaussian_probabilities_sum += log(1e-10)
                    
            # Log da probabilidade a priori + soma dos logs das probabilidades condicionais
            probabilities[class_value] = log(class_probability) + gaussian_probabilities_sum
            
        return probabilities
    
    def predict(self, df):
        """
        Prediz a classe para todas as linhas no DataFrame
        """
        predictions = []
        for _, row in df.iterrows():
            # Usa apenas atributos (sem a classe)
            feature_values = row.iloc[1:].values
            probabilities = self.predict_probabilities(feature_values)
            
            # Encontra a classe com maior probabilidade
            best_class = max(probabilities, key=probabilities.get)
            predictions.append(best_class)
            
        return predictions
    
    def evaluate(self, df, predictions):
        """
        Avalia a precisão das predições
        """
        true_classes = df['class'].values
        correct = sum(1 for true, pred in zip(true_classes, predictions) if true == pred)
        accuracy = correct / len(predictions)
        return accuracy
    
    def cross_validation_split(self, df, n_folds=10):
        """
        Divide o DataFrame em n_folds para validação cruzada
        """
        df_shuffled = df.sample(frac=1, random_state=42) 
        folds = []
        fold_size = len(df) // n_folds
        
        for i in range(n_folds):
            start_idx = i * fold_size
            end_idx = (i + 1) * fold_size if i < n_folds - 1 else len(df)
            fold = df_shuffled.iloc[start_idx:end_idx].reset_index(drop=True)
            folds.append(fold)
            
        return folds
    
    def cross_validate(self, df, n_folds=10):
        """
        Executa validação cruzada e retorna a média das acurácias
        """
        df_processed = self.preprocess_data(df)
        folds = self.cross_validation_split(df_processed, n_folds)
        accuracies = []
        
        for i in range(n_folds):
            # Constrói conjunto de treino com todos os folds exceto o atual
            train_data = pd.concat([folds[j] for j in range(n_folds) if j != i])
            test_data = folds[i]
            
            # Treina o modelo
            self.train(train_data)
            
            # Faz previsões
            predictions = self.predict(test_data)
            
            # Calcula acurácia
            accuracy = self.evaluate(test_data, predictions)
            accuracies.append(accuracy)
            print(f'Fold {i+1}: Acuracia = {accuracy:.4f}')
            
        mean_accuracy = np.mean(accuracies)
        print(f'Acuracia Media: {mean_accuracy:.4f}')
        return mean_accuracy

def main():
    classifier = NaiveBayesClassifier()
    
    data = classifier.read_data()
    
    classifier.cross_validate(data, n_folds=10)

if __name__ == "__main__":
    main()