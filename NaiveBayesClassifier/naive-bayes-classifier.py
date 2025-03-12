import numpy as np
import random 
from math import sqrt, pi, exp, log
from itertools import chain 
from random import randrange

def read_data():
  file = open('house-votes-84.data')
  file_lines = file.readlines()
  dataset = []

  for line in file_lines:
    attributes = line.strip('\n').split(',')
    dataset.append(attributes)

  return dataset

def to_numbers(data): 
  for i in range(len(data)):
    if data[i] == 'y':
      data[i] = 2
    elif data[i] == 'n':
      data[i] = 1
    elif data[i] == '?':
      data[i] = 0

  return data 

def gaussian_probability(x, mean, stdev):
  exponential = exp(-(pow(x-mean, 2)/(2*pow(stdev, 2))))
  return (1/(sqrt(2*pi)*stdev))*exponential

def train(dataset):
  dataset_by_class = dict({'democrat': [], 'republican': []})

  for i in range(len(dataset)):
    class_value = dataset[i][0]  
    row = dataset[i][1:17]
    dataset_by_class[class_value].append(row)

  summaries = dict({'democrat': [], 'republican': []})
  
  for class_value, rows in dataset_by_class.items():
    for column in zip(*rows):
      summaries[class_value].append([np.mean(column), np.std(column), len(column)])

  return summaries

def predict_probabilities(summaries, row, total_rows):
  probabilities = dict()
  
  for class_value, class_summaries in summaries.items():
    class_probability = summaries[class_value][0][2]/float(total_rows)
    probability = 0
    gaussian_probabilities_sum = 0
  
    for i in range(len(class_summaries)):
      mean, stdev, _count = class_summaries[i]
      gaussian_probabilities_sum += log(gaussian_probability(row[i], mean, stdev))
      probability = log(class_probability) + gaussian_probabilities_sum

    probabilities[class_value] = probability
  
  return probabilities

def predict(summaries, dataset, total_rows):
  predictions = []

  for row in dataset:
    predicted_probabilities = predict_probabilities(summaries, row[1:17], total_rows) 
    prediction = {k:v for k,v in predicted_probabilities.items() if v == max(predicted_probabilities.values())}
    predictions.append(prediction)

  return predictions

def predictions_accuracy(accurates, predictions):
  correct = 0

  for accurate, prediction in zip(accurates, predictions):
    accurate_class = accurate[0]
    predicted_class = list(prediction.keys())[0]

    if predicted_class == accurate_class:
      correct+=1

  return correct/float(len(predictions))

def folds_to_dataset(folds):
  dataset = sum(folds, [])
  for i in range(len(dataset)):
    dataset[i] = to_numbers(dataset[i])

  return dataset

def cross_validation_split(dataset, n_folds):
  dataset_copy = list(dataset)
  folds = []
  fold_size = int(len(dataset_copy)/n_folds)

  for _ in range(n_folds):
    sample = random.sample(dataset_copy, fold_size)
    folds.append(sample)
    for x in sample:
      dataset_copy.remove(x)

  return folds

def naive_bayes(train_dataset, test_dataset):
  summaries = train(train_dataset)
  predictions = predict(summaries, test_dataset, len(train_dataset))
  accuracy = predictions_accuracy(test_dataset, predictions)

  return accuracy

def main():
  n_folds = 10
  dataset = read_data()
  folds = cross_validation_split(dataset, n_folds)
  accuracies = []

  for fold in folds:
    train_folds = list(folds)
    train_folds.remove(fold)
    train_dataset = folds_to_dataset(train_folds)

    test_fold = fold
    test_dataset = folds_to_dataset([test_fold])

    accuracy = naive_bayes(train_dataset, test_dataset)
    print('Accuracy:', accuracy)
    accuracies.append(accuracy)

  print('Mean of accuracies:', np.mean(accuracies))

if __name__== "__main__":
  main()
