#!/usr/bin/env python
# coding: utf-8

# In[186]:


# Momenton Data Challenge
import pandas as pd
import numpy as np

encoding='latin1'


# In[187]:


# Create dataframe from movies.dat file 
# Assign column names. Extract year from dat file and create list of movie genres.

movies_df=pd.read_csv('https://raw.githubusercontent.com/momenton/momenton-code-test-movietweetings/master/snapshots/100K/movies.dat',sep='::',engine='python',header=None,encoding=encoding)
movies_df.columns=['movie_id','movie_name','genre']
movies_df["release_year"]=movies_df['movie_name'].str.extract('.*\(([0-9]*)\).*')
movies_df['genre']=movies_df['genre'].str.split('|')
del movies_df['movie_name']


# In[188]:


# Create dataframe from ratings.dat file 
# Assign column names and delete unnecessary columns.

ratings_df=pd.read_csv('https://raw.githubusercontent.com/momenton/momenton-code-test-movietweetings/master/snapshots/100K/ratings.dat',sep = '::',engine='python',header=None,encoding=encoding)
ratings_df.columns=["user_id","movie_id","rating","rating_ts"]
del ratings_df['rating_ts']


# In[189]:


# Join ratings_df with movies_df based on "movie_id" to get the genre and year associated with each movie_id
# Group the dataframe on genre and release_year to get the count of all movie ratings based on Genre and year.

movie_ratings_merge_df=ratings_df.merge(movies_df, on='movie_id', how='inner')
movie_ratings_merge_df=movie_ratings_merge_df.explode('genre').dropna()
movie_insights_df=movie_ratings_merge_df.groupby(['genre','release_year'],as_index=False)['rating'].count()


# In[190]:


# Derive insights to get the list of popular genres based on year for the past decade [10 years]

movie_insights_pivot=movie_insights_df.pivot(index='release_year',columns='genre', values='rating')
movie_insights_pivot[-10:].plot(figsize=(20,10), grid=True)

