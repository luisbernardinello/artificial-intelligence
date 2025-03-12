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
	def __init__(self, attribute=None, branches=[], classification=None):
		self.attribute = attribute
		self.branches = dict(branches)
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
	positives_count =  (df['Class'] == classes[1]).sum()
	total_count = negatives_count + positives_count

	p1 = negatives_count/total_count
	p2 = positives_count/total_count

	entropy = get_entropy([p1, p2])
	return entropy

def information_gain(df, attributes, attribute):
	attribute_values = df[attribute].unique()
	gain = class_entropy(df)

	for value in attribute_values:
		probabilities = []
		attribute_rows = df.loc[df[attribute] == value]
		attribute_rows_count = attribute_rows.shape[0]

		for class_value in classes:
			class_attribute_rows = attribute_rows.loc[attribute_rows['Class'] == class_value]
			rows_count = class_attribute_rows.shape[0]
			probability = rows_count/attribute_rows_count
			probabilities.append(probability) 

		gain -= get_entropy(probabilities)

	return gain

def attribute_names():
	columns = list(column_names)
	columns.pop(0)
	return columns 

def greatest_information_gain(df, attributes):
	greatest_gain = -math.inf
	greatest_gain_attribute = ''
	
	for attribute in attributes:
		gain = information_gain(df, attributes, attribute)
		if gain > greatest_gain:
			greatest_gain = gain
			greatest_gain_attribute = attribute

	return greatest_gain_attribute

def max_class(df):
	negatives_count = (df['Class'] == classes[0]).sum()
	positives_count = (df['Class'] == classes[1]).sum()

	classification = classes[0] if negatives_count > positives_count else classes[1]
	return classification

def has_same_class(df):
	class_values = df['Class'].unique()
	return len(class_values) == 1

def id3(df, allowed_attributes):
	root = Node()

	if has_same_class(df) or len(allowed_attributes) == 0 or df.shape[0] <= K:
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

			if rows.shape[0] == 0:
				classification = max_class(df)
				child_node.classification = classification
			else:
				child_node = id3(rows, child_attributes)

			root.branches[attribute_value] = child_node
	return root

def predict(row, attributes, root):
	node = root
	attribute_value = row[node.attribute]
	attributes.remove(node.attribute)

	while True:
		child = node.branches[attribute_value]
		if len(attributes) == 0 or len(child.branches) == 0 or child.attribute == None:
			return child.classification

		attribute_value = row[child.attribute]
		node = child

	return node.classification

def get_predictions_accuracy(df, root):
	correct = 0
	for _index, row in df.iterrows():
		real_class = row['Class']
		prediction = predict(row, attribute_names(), root)
		if real_class == prediction:
			correct+=1

	return correct/float(df.shape[0])

def split_folds(df):
	folds = []
	fold_size = int(df.shape[0]/10)

	for i in range(10):
		rows = df.sample(n=fold_size)
		folds.append(rows)
		for index, row in folds[i].iterrows():
			df.drop(index)

	return folds

def main():
	data = read_data()
	df = pd.DataFrame(data, columns=column_names)
	set_attributes(df)
	folds = split_folds(df)
	accuracies = []

	for index, fold in enumerate(folds):
		train_folds = list(folds)
		del train_folds[index]
		test = fold.copy()
		train = pd.concat(train_folds)
	
		root = id3(train, attribute_names())
		accuracy = get_predictions_accuracy(test, root)
		print('Accuracy:', accuracy)
		accuracies.append(accuracy)

	print('Mean of accuracies:', np.mean(accuracies))


if __name__== "__main__":
	main()

