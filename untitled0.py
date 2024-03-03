# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12B9vltDM5sz7wf30evNay5FYL-slrcYD
"""

import nltk
nltk.download('stopwords')
nltk.download("punkt")

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
import chardet

# Detect file encoding
with open('customer_feedback.csv', 'rb') as file:
    result = chardet.detect(file.read())
file_encoding = result['encoding']

# Load Amazon reviews data from CSV with detected encoding
feedback_data = pd.read_csv('customer_feedback.csv', encoding=file_encoding)

# Split data into training and testing sets
reviews = list(feedback_data['Comments'])  # Replace 'YourColumnName' with the actual column name
sentiments = list(feedback_data['Review Title'])

# Shuffle the data
documents = list(zip(reviews, sentiments))
random.shuffle(documents)

# Prepare stopwords
nltk.download('stopwords')

# Get the most common 3000 words as features
all_words = set()
stop_words = set(stopwords.words('english'))
for review, _ in documents:
    words = word_tokenize(review.lower())
    words = [w for w in words if w.isalpha() and w not in stop_words]
    all_words.update(words)

word_features = list(all_words)[:3000]

# Function to extract features from the text
def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

# Extract features from the text
featuresets = [(find_features(word_tokenize(review.lower())), sentiment) for review, sentiment in documents]

# Split the data into training and testing sets
training_set = featuresets[:int(len(featuresets)*0.8)]
testing_set = featuresets[int(len(featuresets)*0.8):]

# Train a Naive Bayes classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)

# Test the classifier on the testing set
print("Naive Bayes accuracy:", nltk.classify.accuracy(classifier, testing_set))

# Test the classifier on custom feedback
custom_feedback = "good quality"
custom_feedback_tokens = word_tokenize(custom_feedback.lower())
custom_feedback_set = find_features(custom_feedback_tokens)
print("Custom feedback sentiment:", classifier.classify(custom_feedback_set))

