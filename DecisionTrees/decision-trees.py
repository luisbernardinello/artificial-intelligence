import math
import pandas as pd 
import random
import numpy as np

column_names = [
    'Class',
    'age',
    'menopause',
    'tumor-size',
    'inv-nodes',
    'node-caps',
    'deg-malig',
    'breast',
    'breast-quad',
    'irradiat'
]

classes = ['no-recurrence-events', 'recurrence-events']

attributes = dict()

K = 4

class Node(object):
    def __init__(self, attribute=None, branches=None, classification=None):
        self.attribute = attribute
        self.branches = branches if branches is not None else {}
        self.classification = classification

def set_attributes(df):
    for column in column_names:
        values = df[column].unique()
        attributes[column] = values

def read_data():
    file = open('breast-cancer.data')
    file_lines = file.readlines()
    dataset = []

    for line in file_lines:
        attributes = line.strip('\n').split(',')
        dataset.append(attributes)

    return dataset

def get_entropy(probabilities):
    entropy = 0
    for prob in probabilities:
        entropy += -prob*math.log(prob, 2) if prob > 0 else 0

    return entropy

def class_entropy(df):
    negatives_count = (df['Class'] == classes[0]).sum()
    positives_count = (df['Class'] == classes[1]).sum()
    total_count = negatives_count + positives_count
    
    if total_count == 0:
        return 0
        
    p1 = negatives_count/total_count
    p2 = positives_count/total_count

    entropy = get_entropy([p1, p2])
    return entropy

def information_gain(df, attribute):
    attribute_values = df[attribute].unique()
    total_rows = df.shape[0]
    entropy_before = class_entropy(df)
    entropy_after = 0
    
    for value in attribute_values:
        subset = df[df[attribute] == value]
        subset_size = subset.shape[0]
        subset_weight = subset_size / total_rows
        subset_entropy = class_entropy(subset)
        entropy_after += subset_weight * subset_entropy
        
    return entropy_before - entropy_after

def attribute_names():
    columns = list(column_names)
    columns.pop(0) 
    return columns 

def greatest_information_gain(df, allowed_attributes):
    greatest_gain = -math.inf
    greatest_gain_attribute = ''
    
    for attribute in allowed_attributes:
        gain = information_gain(df, attribute)
        if gain > greatest_gain:
            greatest_gain = gain
            greatest_gain_attribute = attribute

    return greatest_gain_attribute

def max_class(df):
    if df.empty:
        return classes[0] 
        
    negatives_count = (df['Class'] == classes[0]).sum()
    positives_count = (df['Class'] == classes[1]).sum()

    classification = classes[0] if negatives_count >= positives_count else classes[1]
    return classification

def has_same_class(df):
    class_values = df['Class'].unique()
    return len(class_values) == 1

def id3(df, allowed_attributes):
    root = Node()

    if df.empty or has_same_class(df) or len(allowed_attributes) == 0 or df.shape[0] <= K:
        classification = max_class(df)
        root.classification = classification
        return root
    else:
        best_attribute = greatest_information_gain(df, allowed_attributes)
        root.attribute = best_attribute
        child_attributes = list(allowed_attributes)
        child_attributes.remove(best_attribute)
        attribute_values = attributes[best_attribute]

        for attribute_value in attribute_values:
            rows = df.loc[df[best_attribute] == attribute_value]
            child_node = Node()

            if rows.empty:
                classification = max_class(df)
                child_node.classification = classification
            else:
                child_node = id3(rows, child_attributes)

            root.branches[attribute_value] = child_node
    return root

def predict(row, root):
    node = root
    
    while node.classification is None:
        attribute = node.attribute
        value = row[attribute]
        
        if value not in node.branches:
            return max_class(pd.DataFrame([row]))
            
        node = node.branches[value]
        
    return node.classification

def get_predictions_accuracy(df, root):
    correct = 0
    for _index, row in df.iterrows():
        real_class = row['Class']
        prediction = predict(row, root)
        if real_class == prediction:
            correct += 1

    return correct/float(df.shape[0])

def split_folds(df, num_folds=10):
    df_copy = df.copy()
    df_copy = df_copy.sample(frac=1, random_state=42).reset_index(drop=True)
    
    folds = []
    fold_size = len(df_copy) // num_folds
    
    for i in range(num_folds):
        start_idx = i * fold_size
        end_idx = start_idx + fold_size if i < num_folds - 1 else len(df_copy)
        fold = df_copy.iloc[start_idx:end_idx].copy()
        folds.append(fold)
        
    return folds

def main():
    data = read_data()
    df = pd.DataFrame(data, columns=column_names)
    set_attributes(df)
    num_folds = 10
    folds = split_folds(df, num_folds)
    accuracies = []

    for index in range(num_folds):
        test = folds[index]
        train_folds = [folds[i] for i in range(num_folds) if i != index]
        train = pd.concat(train_folds)
    
        root = id3(train, attribute_names())
        accuracy = get_predictions_accuracy(test, root)
        print(f'Fold {index+1} Accuracy: {accuracy:.4f}')
        accuracies.append(accuracy)

    print('Mean of accuracies:', np.mean(accuracies))
    print('Std of accuracies:', np.std(accuracies))


if __name__== "__main__":
    main()