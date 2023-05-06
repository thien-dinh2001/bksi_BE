# -*- coding: utf-8 -*-
"""BKSI_search_engine.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ttyB-zjhEtC_pqCVmLdXr9hGCb7oxV1g


# Word Embedding

Install library
"""

"""Import library"""

import math
import pandas as pd
import nltk
import numpy as np
from sklearn.decomposition import TruncatedSVD
from underthesea import word_tokenize, pos_tag
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import csv
import regex as re
import os
import sys

"""Preprocessing"""

def loaddicchar():
  dic = {}
  char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
      '|')
  charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
      '|')
  for i in range(len(char1252)):
      dic[char1252[i]] = charutf8[i]
  return dic
dicchar = loaddicchar()

def covert_unicode(txt):
  return re.sub(
    r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
    lambda x: dicchar[x.group()], txt)

# stopword_text = open("/content/stopword_77.txt", "r", encoding='utf-8')
# stopword_text = stopword_text.read().replace("_", " ")
# stopword_text = covert_unicode(stopword_text)
stopword_list = [] #stopword_text.split("\n")

def preprocess(document):
  data = covert_unicode(document)
  data = data.replace(',', " ")
  data = data.replace('.', " ")
  data = data.replace('.\n', " ")
  data = data.replace('!', " ")
  data = data.replace('@', " ")
  data = data.replace(':', " ")
  data = data.replace('(', " ")
  data = data.replace(')', " ")
  data = data.replace('[', " ")
  data = data.replace(']', " ")
  data = data.replace('{', " ")
  data = data.replace('}', " ")
  
  for stopword in stopword_list:
    data = data.replace(' ' + stopword + ' ', ' ')
  data = word_tokenize(data)
  for i in range(len(data)):
    data[i] = data[i].lower()
    #print("data", data[i], "\n")
  return data

"""Get data"""

document_names = []
# đổi lại path
path = "D:/project/BKSI/BKSI_refurbishment/Data"
os.chdir(path)
documents = []
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
      data = f.read()
      documents.append(preprocess(data))
      f.close()
files = []
listOfFiles = []
for (dirpath, dirnames, filenames) in os.walk(path):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]
# for file in os.listdir():
for file in listOfFiles:
    # Check whether file is in text format or not
    if file.endswith(".txt"):
        file_path = f"{file}"
        files.append(file) 
        x = file_path.split("/")[-1]
        document_names.append(x.split('\\')[1] + ' - ' + x.split('\\')[2]) 
        # call read text file function
        read_text_file(file_path)

"""Corpus vocabulary"""

corpus = {}
indexer = {}
token_id = {}
avg_length = 0
# calculate corpus vocabulary

for i in range(len(documents)):
    avg_length += len(documents[i])
    for token in documents[i]:
        if token not in corpus.keys():
            corpus[token] = 1
            token_id[token] = len(corpus) - 1
            indexer[token] = [i]
            # indexer[token] = [document_paths[i]]

        else:
            if i not in indexer[token]:
                corpus[token] += 1
                indexer[token].append(i)
                # indexer[token].append(document_paths[i])

avg_length /= len(documents)

# with open('/content/indexer.csv', 'w') as csvfile:
#     for key in indexer.keys():
#         csvfile.write("%s, %s\n" % (key, indexer[key]))

"""Calculate tf_idf"""
                     
def tf_idf(article):
  freq = np.zeros(len(corpus))
  expand = []
  expand_id = {}
  for token in article:
    if token in corpus.keys():
      freq[token_id[token]] += 1
    else:
      if token in expand_id.keys():
        expand[expand_id[token]] += 1
      # xử lý trường hợp không có => có quan trọng không, vì nếu corpus nhiều thì những trường hợp này sẽ rất ít và không có ý nghĩa
      else:
        expand_id[token] = len(expand)
        expand.append(1)

  expand = np.array(expand)
  if (len(article) != 0):
    # Normal tf-idf
    # Begin
    freq = freq / len(article)
  for token in corpus.keys():
    if corpus[token] != 0:
      freq[token_id[token]] /= corpus[token]      
  return freq

"""Vectorize"""

docs = []
for article in documents:
  docs.append(tf_idf(article=article))

documents_vector = np.array(docs)



# Wordnet

"""# Query handle

Query enrichment
"""

def enrichment(query):
  result = preprocess(query)
  # result = synset(result)
  return result

"""# Select candidate documents

Select candidate documents
"""

def candidates(query):
  documents_id = []
  for token in query:
    if token in indexer.keys():
      documents_id = list(set(indexer[token])| set(documents_id))
  return documents_id

"""# Scoring

TruncatedSVD
"""

def truncated(query, documents):
  # truncated vector
  np.insert(documents, 0, query, 0)
  svd = TruncatedSVD(n_components=226)
  svd.fit(documents) 
  return svd.transform(documents)

"""Cosine similarity"""

def cosine_sim_func(query, candidates):
    documents = []
    for i in candidates:
      documents.append(documents_vector[i])
    #truncated
    # docs = truncated(tf_idf(query), documents)
    # query = docs[0]
    # documents = docs[1:]
    # query_vector = np.reshape(query, (1,-1))
    #normal query
    query_vector = tf_idf(query)
    query_vector = np.reshape(query_vector, (1, -1))
    sim_matrix = cosine_similarity(query_vector, documents)
    sim_matrix = np.reshape(sim_matrix, (-1,))
    # sim_list = np.where(sim_matrix >= 0.01, sim_matrix, 0)
    sim_list = (-sim_matrix).argsort()
    result = []
    if len(candidates) < 10:
      for i in range(len(candidates)):
        if sim_matrix[sim_list[i]] > 0.2:
          result.append(document_names[candidates[sim_list[i]]])
    else:
      for i in range(10):
        if sim_matrix[sim_list[i]] > 0.2:
          result.append(document_names[candidates[sim_list[i]]])
    return result