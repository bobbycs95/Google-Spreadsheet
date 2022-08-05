#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 13:54:56 2022
"""

import requests
import json
import pandas as pd
import re

# This section is to generate each lawyer's code from the Json File

judul = []

for i in range(1,57,1):
  url = f'https://api.justika.com/lawyer/?page={i}'
  # Define headers used to request
  headers = {
            'Content-Type': 'application/json',
  }

  response = requests.get(url, headers=headers).json()
  data = json.dumps(response, indent=4)
  python_obj = json.loads(data)

  try:
    for j in range(0,10):
        judul.append((python_obj["results"][j]["code"]))
  except:
    pass
    
# This section is to insert each lawyer's code to the url, to generate json data for each lawyers in
# the next section

link = []
for j in judul:
  string = f"https://api.justika.com/lawyer/{j}/review/?page=1&page_size=5&score=3"
  link.append(string)

# This section is to get the 3-Stars feedback, order type, and post date from each lawyers

feedback = []
order_type = []
post_date = []

for k in link:
  r = requests.get(k,headers=headers).json()
  data = json.dumps(r, indent=4)
  python_obj_2 = json.loads(data)

  for x in python_obj_2["results"]:
    feedback.append(x["feedback"])
    order_type.append(x["order_type"])
    post_date.append(x["post_date"])

# This section is to generate the Feedback, order type, and post date and compile it in a dataframe

df = pd.DataFrame(feedback)
df["order_type"] = order_type
df["post_date"] = post_date
df.rename(columns={0:"Score_3"},inplace=True)
df = df[df["Score_3"]!=""].dropna()
df = df.replace("|","",regex=True)
df

# This is the Sentiment Analysis section

import matplotlib.pyplot as plt
import nltk
nltk.download('stopwords') #download stopwords library dari NLP
from nltk.corpus import stopwords #untuk membuat stopwords
from wordcloud import WordCloud, STOPWORDS #untuk membuat wordcloud

# Removes all special characters and numericals leaving the alphabets
def clean(text):
    text = re.sub('[^A-Za-z]+', ' ', text)
    return text

df["Score_3_New"] = df["Score_3"].apply(clean)

# Uncomment this first to generate the csv file. Then, I modify the language using Google Sheets formula
# =GOOGLETRANSLATE() because I haven't found python code to translate the language from Indonesian to English. 
# df.to_csv("translate.csv")

# After translated, reupload the csv file. I use a different name (same file, but added the translated part) call translation.csv
df1 = pd.read_csv("translation.csv")
df1

# This section is to tokenize each words, and checking the most occur words, by plotting it to Wordcloud.

comment_words = ''
stopwords = set(STOPWORDS)

for val in df1.Score_3_New:
     
    # typecaste each val to string
    val = str(val)
 
    # split the value
    tokens = val.split()
     
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "

# new_words = [' '.join([w for w in s.split() if w not in new_stopwords]) for s in comment_words]

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
# plot the WordCloud image                      
plt.figure(figsize = (10, 10), facecolor = None)
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0) 
plt.show() 

# Using textblob to do a simple Sentiment Analysis

from textblob import TextBlob
# function to calculate subjectivity
def getSubjectivity(review):
    return TextBlob(review).sentiment.subjectivity
    # function to calculate polarity
def getPolarity(review):
    return TextBlob(review).sentiment.polarity

# function to analyze the reviews
def analysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

fin_data = pd.DataFrame(df1[['Score_3_New', 'Translate','order_type',"post_date"]])
fin_data['Polarity'] = fin_data['Translate'].apply(getPolarity) 
fin_data['Analysis'] = fin_data['Polarity'].apply(analysis)

df2 = pd.DataFrame()
df2 = pd.merge(df1,fin_data, how='right',left_on = 'Score_3_New', right_on = 'Score_3_New')
df2 = df2.drop(["Unnamed: 0","order_type_x","Score_3_New","Translate_x","Translate_y","Polarity","post_date_y"],axis=1).dropna()

df2.rename(columns={"order_type_y":"Order_Type","post_date_x":"Post_Date"},inplace=True)
df2.to_csv("Analisa.csv")
df2