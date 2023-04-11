"""
    This script is focus on creating Sentiment Analysis and Topic Analysis
    for Spotify. The data is taken from Free Kaggle Dataset : 
    https://www.kaggle.com/datasets/mfaaris/spotify-app-reviews-2022?resource=download
"""

import pandas as pd
import nltk 
nltk.download('stopwords')
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import string
from autocorrect import Speller # spelling removal
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def cleaning(text):
    # aposthropes list
    Apos_dict={"'s":" is","n't":" not","'m":" am","'ll":" will",
            "'d":" would","'ve":" have","'re":" are"}
    
    # replace the aposthropes
    for key,value in Apos_dict.items():
        if key in text:
            text=text.replace(key,value)

    # changing all cases to lower cases
    text = text.lower()
    
    # autocorrect mispell english words
    spell = Speller(lang='en')
    # spell check
    text = spell(text)

    # import english stopwords list from nltk
    stopwords_eng = stopwords.words('english')
    text_tokens = text.split()
    text_list =[]

    #remove stopwords
    for word in text_tokens:
        if word not in stopwords_eng:
            text_list.append(word)

    clean_tweet=[]
    #remove symbols
    for word in text_list:
        if word not in string.punctuation:
            clean_tweet.append(word)

    cleans = " ".join(kata for kata in clean_tweet)
    return cleans

# Preparing the dataset, import the data from the reviews.csv
# only pick the review and rating column

df = pd.read_csv('reviews.csv')
df = df[df["Time_submitted"] >= "2022-07-01"]
df = df[["Review","Rating"]]
df = df[~df["Review"].isnull()]

# We will separate the positive (rating >=3) and negative (rating <3) reviews
# and will do analysis for both of them
df_pos = df[df["Rating"]>=3]
df_neg = df[df["Rating"]<3]

def positive_sentiment():
    # Cleaning the review data, create a new column contains the clean text called 
    # 'review_clean'
    df_pos["review_clean"] = df_pos["Review"].apply(cleaning)

    # Sentiment Analysis : 
    # Creating the sid model first, then calculate the compound score 
    sid = SentimentIntensityAnalyzer()
    df_pos["SentimentScore"] = df_pos["review_clean"].apply(lambda review:sid.polarity_scores(review))
    df_pos["compound"] = df_pos["SentimentScore"].apply(lambda d:d['compound'])
    df_pos["sentiment"] = df_pos["compound"].apply(lambda x: 'Positive' if x>=0 else 'Negative')
    df_pos["starLabel"] = df_pos["Rating"].apply(lambda sym: {1:"Negative",2:"Negative",3:"Positive",4:"Positive",5:"Positive"}.get(sym,' '))

    # Checking the accuracy of the Sentiment Model
    print("Classification Report for Positive : ", classification_report(df_pos["starLabel"],df_pos["sentiment"]))
    print(confusion_matrix(df_pos["starLabel"],df_pos["sentiment"]))
    return df_pos

def negative_sentiment():
    # Cleaning the review data, create a new column contains the clean text called 
    # 'review_clean'
    df_neg["review_clean"] = df_neg["Review"].apply(cleaning)

    # Sentiment Analysis : 
    # Creating the sid model first, then calculate the compound score 
    sid = SentimentIntensityAnalyzer()
    df_neg["SentimentScore"] = df_neg["review_clean"].apply(lambda review:sid.polarity_scores(review))
    df_neg["compound"] = df_neg["SentimentScore"].apply(lambda d:d['compound'])
    df_neg["sentiment"] = df_neg["compound"].apply(lambda x: 'Positive' if x>=0 else 'Negative')
    df_neg["starLabel"] = df_neg["Rating"].apply(lambda sym: {1:"Negative",2:"Negative",3:"Positive",4:"Positive",5:"Positive"}.get(sym,' '))

    # Checking the accuracy of the Sentiment Model
    print("Classification Report for Negative : ", classification_report(df_neg["starLabel"],df_neg["sentiment"]))
    print(confusion_matrix(df_neg["starLabel"],df_neg["sentiment"]))
    return df_neg

def topic_analysis(df,number_of_topic,number_of_words):
    # Count the words in each comments, make document type matrix (dtm)
    cv = CountVectorizer(max_df = 0.9,min_df = 2,stop_words = 'english')
    dtm = cv.fit_transform(df["review_clean"])

    # Make a LDA with (#number_of_topic) topics
    LDA = LatentDirichletAllocation(n_components = number_of_topic,random_state = 42)
    LDA.fit(dtm)

    # For each topic (#number_of_topic), print the top (#number_of_words) words
    words = []
    for i,topic in enumerate(LDA.components_):
        print(f"The top {number_of_words} words for topic #{i}")
        words_in_topic = [cv.get_feature_names_out()[index] for index in topic.argsort()[-number_of_words:]]
        print(words_in_topic)
        string = ", ".join(x for x in words_in_topic)
        words.append(string)
        print("\n")

    # Getting the Match Key for Original Table (with topic number as the Match Key)
    topic_results = LDA.transform(dtm)
    df["topic"] = topic_results.argmax(axis=1)

    # Creating the topic dataframe
    df1 = pd.DataFrame(words).reset_index()
    df1.rename(columns={0:"words"},inplace=True)

    return df1

# Assign the positive and negative sentiment to each df_positive and df_negative
df_positive = positive_sentiment()
df_negative = negative_sentiment()

# Creating new dataframe to contains the top topic for each sentiment
positive_topic = topic_analysis(df_positive,number_of_topic = 5,number_of_words = 10)
negative_topic = topic_analysis(df_negative,number_of_topic = 5,number_of_words = 10)

# Print the topic
print(positive_topic)
print(negative_topic)