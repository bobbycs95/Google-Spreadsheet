#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 11:47:42 2022
Focus on getting all the entities that are enlisted in Indonesia's Government Regulation
After getting the data through API Request, we will focus on cleaning the data to get 
more clear entity name 
"""

import requests
import json
import pandas as pd

judul = []
dummy = "0"

# Scraping Part 

for i in range(0,991,10):
  
  # Define URL 
  url = 'https://api.hukum.io/v3/search/regulations/_msearch'
  i = str(i)
  
  # Define your Payload/Request Body or another parameter for request into API
  payload = '{"preference":"searchResult"}\n{"query":{"bool":{"must":[{"bool":{"must":[{"match":{}},{"bool":{"should":[{"terms":{"language":["id"]}}]}},{"bool":{"should":[{"terms":{"hierarchy.key.keyword":["Peraturan Lembaga/Badan"]}}]}}]}}]}},"size":10,"aggs":{"hierarchy.key.keyword":{"terms":{"field":"hierarchy.key.keyword","size":3,"order":{"_key":"desc"}}}},"_source":{"includes":["*"],"excludes":[]},"from":0,"sort":[{"_score":{"order":"desc"}}]}'
  payload_new = payload.replace(str(dummy),str(i))

  # Define headers used to request
  headers = {
          'Content-Type': 'application/x-ndjson',
          'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hdXRoOjgwXC9hdXRoIiwiYXVkIjoicHVibGljIiwiaWF0IjoxNTMxODIzNzUyLCJuYmYiOjE1MzE4MjM3NTIsImV4cCI6MTUzOTU5OTc4MjAsInN1YiI6IjViNDI2MGNhNTQxNmJiMWFlODg0MjY2YiJ9.WnnOw3PaSC2RiK9AO8L5yao3JIyCqmtlzq57ZGygVDZygScG2iqPU13AoA5TNnunDYucVY5_ZtaDSvhGAjGiiBiAgJU48qwaz5ApuQ8lgIcSQnmi4Jg8pv9zC6nkg1JbpX14gjVUTz5lzc55FdLL4uURFbbqoz2vnw3504Lsk0DSr7q5FJ6U3hIAheVm3MFMVs_EWh_mTRJIw8jHfH_QMaE_CXZfgwHhY58BbB4VK8WzUHRoPpdKKG-yOlvJN0FBKS2Z60MjmeInrK5BnZcfkXHwQDvulFQ3rIk31NNBqpA75jhSdsY4AYXGAceYBWT_ozJfuCM34Upfi55Xe-93Sw'
      }

  # Start request to API
  response = requests.post(url, headers=headers, data=payload_new).json()

  data = json.dumps(response, indent=4)

  python_obj = json.loads(data)

  for j in range(0,10):
    judul.append(python_obj["responses"][0]["hits"]["hits"][j]["_source"]["title"])

# Cleaning Part

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
# print(stopwords.words('indonesian'))

# Setting the New Stopwords
stopwords = ["Tahun","Rancangan","Peraturan","Nomor","Pedoman","TAHUN","Kepala","Keputusan"]
for m in range (0,200,1):
  stopwords.append(str(m)) 
for n in range (1950,2023,1):
  stopwords.append(str(n)) 
new_stopwords = set(stopwords)

# Removing the words from Title that Contains the new Stopwords
judul_new = [' '.join([w for w in s.split() if w not in new_stopwords]) for s in judul]

# Removing Duplicate Value after Removing the Stopwords
judul_clean = []
[judul_clean.append(x) for x in judul_new if x not in judul_clean] 

# Removing Words that contains specific character (/)
def remove_words(in_list, char_list):
    new_list = []
    for line in in_list:
        new_words = ' '.join([word for word in line.split() if not any([phrase in word for phrase in char_list])])
        new_list.append(new_words)
    return new_list

words = ["/","-","0",".",":","("]
judul_clean = remove_words(judul_clean,words)

#Once again, Remove Duplicate Value after Removing the Unnecessary Words
judul_clean2 = []
[judul_clean2.append(x) for x in judul_clean if x not in judul_clean2] 
judul_clean2

# Creating the DataFrame to view all the Entity

df = pd.DataFrame(judul_clean2)
df.rename(columns={0:"Lembaga"},inplace=True)
df.show()