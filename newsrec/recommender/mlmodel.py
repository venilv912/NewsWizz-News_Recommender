#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import math
import time
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances


# In[2]:


news = pd.read_json("E:/News_Recc/newsrec/recommender/latest_dataset.json", lines = True)


# In[3]:


news = news[news['date'] >= pd.Timestamp(2020,1,1)]


# In[4]:


news.shape


# In[5]:


#news.sort_values('headline',inplace=True, ascending=False)
#duplicated_articles_series = news.duplicated('headline', keep = False)
#news = news[~duplicated_articles_series]
#print("Total number of articles after removing duplicates:", news.shape[0])


# In[6]:


news.index = range(news.shape[0])


# In[7]:


news["day and month"] = news["date"].dt.strftime("%a") + "_" + news["date"].dt.strftime("%b")


# In[8]:


news.index = range(news.shape[0])
news.index.shape[0]


# In[9]:


news.info()


# In[10]:


news_temp = news.copy()


# In[11]:


stop_words = set(stopwords.words('english'))


# In[12]:


for i in range(len(news_temp["headline"])):
    string = ""
    for word in news_temp["headline"][i].split():
        word = ("".join(e for e in word if e.isalnum()))
        word = word.lower()
        if not word in stop_words:
          string += word + " "  
    news_temp.at[i,"headline"] = string.strip()


# In[13]:


lemmatizer = WordNetLemmatizer()


# In[14]:


for i in range(len(news_temp["headline"])):
    string = ""
    for w in word_tokenize(news_temp["headline"][i]):
        string += lemmatizer.lemmatize(w,pos = "v") + " "
    news_temp.at[i, "headline"] = string.strip()


# In[15]:


tfidf_headline_vectorizer = TfidfVectorizer(min_df = 0.0)
tfidf_headline_features = tfidf_headline_vectorizer.fit_transform(news_temp['headline'])


# In[16]:


def tfidf_based_model(row_index, num_similar_items):
    couple_dist = pairwise_distances(tfidf_headline_features,tfidf_headline_features[row_index])
    indices = np.argsort(couple_dist.ravel())[0:num_similar_items]

    df = pd.DataFrame({'original_index': indices, 'publish_date': news['date'][indices].values,
               'headline':news['headline'][indices].values,
                 'link':news['link'][indices].values})
    #print("="*30,"Queried article details","="*30)
    #print('headline : ',news['headline'][indices[0]])
    #print("\n","="*25,"Recommended articles : ","="*23)
    
    list_of_lists=df.dropna().values.tolist()
    return list_of_lists

tfidf_based_model(4156, 11)


# In[ ]:




