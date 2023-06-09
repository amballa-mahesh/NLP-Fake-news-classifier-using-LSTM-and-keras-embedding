# -*- coding: utf-8 -*-
"""NLP Fake news classifer using LSTM and keras embedding.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZzbinssMzgd5ALkfZsPWypqxKr2kEOIN
"""

from google.colab import drive
drive.mount('/content/mydrive')

import pandas as pd

"""Reading Data using Pandas"""

df = pd.read_csv('/content/mydrive/MyDrive/Fake News Data/train.csv')

df.head()

df.shape

df.isnull().sum()

"""Removing null values"""

df.dropna(axis =0,inplace=True)
df.reset_index(inplace=True)

df.shape

df.head()

import re
import tqdm
import string
from tqdm import tqdm
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import stopwords 
from nltk import word_tokenize,sent_tokenize
from nltk.stem import PorterStemmer

"""Stop words creation"""

stops = stopwords.words('english')
lm = WordNetLemmatizer()
ps = PorterStemmer()

stops.remove('no')
stops.remove('not')
stops.remove('nor')

stops

x = df['title']

"""Text Cleaning and creating the word corpus"""

from nltk.corpus.reader import wordlist
corpus = []
for i in tqdm(range(0,x.shape[0])):
  text = re.sub(r"didn't", "did not", x[i])
  text = re.sub(r"don't", "do not", text)
  text = re.sub(r"won't", "will not", text)
  text = re.sub(r"can't", "can not", text)
  text = re.sub(r"wasn't", "do not", text)
  text = re.sub(r"should't", "should not", text)
  text = re.sub(r"could't", "could not", text)  
  text = re.sub(r"\'ve", " have", text)
  text = re.sub(r"\'m", " am", text)
  text = re.sub(r"\'ll", " will", text)
  text = re.sub(r"\'re", " are", text)
  text = re.sub(r"\'s", " is", text)
  text = re.sub(r"\'d", " would", text)
  text = re.sub(r"\'t", " not", text)
  text = re.sub(r"\'m", " am", text)
  text = re.sub(r"n\'t", " not", text)
  text = re.sub('[^a-zA-Z]',' ',text)
  text = text.lower()
  text = text.split()
  text = [ps.stem(word) for word in text if word not in stops]
  text = ' '.join(text)
  corpus.append(text)
word_corpus = []
for sent in tqdm(corpus):
  sent_token = sent_tokenize(sent)
  for sen in sent_token:
    words = word_tokenize(sen)
  word_corpus.append(words)

import tensorflow

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dropout,Dense, LSTM,Bidirectional
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import one_hot

"""Vocabulary Size """

voc_size = 5000

corpus[0:1]

"""Creating the text into onehot representation"""

one_hot_rep = [one_hot(sent,voc_size) for sent in corpus]

word_len = [len(word_corpus[i]) for i in range(len(word_corpus))]
max(word_len)

"""Pad the Onehot vectors"""

emmbedded_sents = pad_sequences(one_hot_rep,maxlen = max(word_len),padding ='pre')

emmbedded_sents[0]

X = emmbedded_sents
y = df['label']

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(X,y,test_size = 0.2,random_state = 123,stratify=y)

"""Creation to Model using LSTM or Bidirectional LSTM(Output dimention means size of each word in vector representation.)"""

model = Sequential()
model.add(Embedding(output_dim = 40,input_dim = voc_size,input_length =max(word_len)))
model.add(Bidirectional(LSTM(100)))
model.add(Dropout(rate =0.2))
model.add(Dense(1,activation = 'sigmoid'))
print(model.summary())

model.compile(optimizer= 'adam',loss='binary_crossentropy',metrics ='accuracy')

model.fit(x_train,y_train,epochs =20,verbose=1,batch_size=60,validation_data=(x_test,y_test))

import numpy as np

y_pred = np.round(model.predict(x_test),0)

"""Testing the Model"""

from sklearn.metrics import confusion_matrix,classification_report

print(confusion_matrix(y_test,y_pred))

print(classification_report(y_test,y_pred))