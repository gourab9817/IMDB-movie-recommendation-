# -*- coding: utf-8 -*-
"""moviereco.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1deBeWhx7Xm_XUjMouNt1GzQJwQxc-0NC
"""





import numpy as np
import pandas as pd
import ast

movies='/content/drive/MyDrive/Movie recomendation/tmdb_5000_movies.csv'
credits='/content/drive/MyDrive/Movie recomendation/tmdb_5000_credits.csv'

movie=pd.read_csv(movies)
credit=pd.read_csv(credits)

movie.head(1)

credit.head(1)



# credit.head(1)["cast"].values

movie= movie.merge(credit,on="title")

movie.head(1)

movie.info()

"""genre
id
keyword
title
overview
original language
"""

# Genres
# id
# keywords
# original language
# overview
# title
# cast
# crew

movie=movie[['movie_id','title','overview','genres','keywords','cast','crew']]

movie.head(1)

movie.isnull().sum()

movie.dropna(inplace=True)

movie.duplicated().sum()

movie.iloc[0].genres

# [{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]
# ['Action','Advanture','Fantasy','Science Fiction']
# For that we have to write a function which collects all the tags from the genres and make a simple list
# secondly we have to look that after taking out the list from genres column it forms a string of list ,  and we have to convert it into list

# Here is the function which will extract the tags from the genres column
# And there is a predefined function which can change string of list into list only
# we have to import ast  and the function is [ast.literal_eval()]

def convert(obj):
  L=[]
  for i in ast.literal_eval(obj):
    L.append(i['name'])
  return L

movie['genres'].apply(convert)

movie['genres']=movie['genres'].apply(convert)

movie.head(1)

movie.iloc[0].keywords

movie['keywords'].apply(convert)

movie['keywords']=movie['keywords'].apply(convert)

movie.head(1)

movie['cast'][0]

def convert2(obj):
  L=[]
  counter=0
  for i in ast.literal_eval(obj):
    if counter != 5:
      L.append(i['name'])
      counter +=1
    else:
      break
  return L

movie['cast'].apply(convert2)

movie['cast']=movie['cast'].apply(convert2)



movie['cast'][0]

movie.head(1)

movie['crew'][0]

# fetch director
def fetch_director(obj):
  L=[]
  for i in ast.literal_eval(obj):
    if i['job'] == 'Director':
       L.append(i['name'])
       break
  return L

movie['crew'].apply(fetch_director)

movie['crew']=movie['crew'].apply(fetch_director)

movie.head(1)

# convert movie overview cloumn from string to list
movie['overview'].apply(lambda x:x.split())

movie['overview']=movie['overview'].apply(lambda x:x.split())

movie.head()

# Remove a space from string  eg: sam worthington to samworthington. and it will be applicable for genres, keywords,cast,crew
movie['genres'].apply(lambda x:[i.replace(" ","") for i in x])

movie['genres']=movie['genres'].apply(lambda x:[i.replace(" ","") for i in x])

movie['keywords'].apply(lambda x:[i.replace(" ","") for i in x])

movie['keywords']=movie['keywords'].apply(lambda x:[i.replace(" ","") for i in x])

movie['cast'].apply(lambda x:[i.replace(" ","") for i in x])

movie['cast']=movie['cast'].apply(lambda x:[i.replace(" ","") for i in x])

movie['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movie['crew']=movie['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movie.head()

movie['tags']=movie['overview']+movie['genres']+movie['keywords']+movie['cast']+movie['crew']

movie.head(1)

new_df=movie[['movie_id','title','tags']]

new_df

# convert tags column elements from list to string
new_df["tags"].apply(lambda x:" ".join(x))

new_df["tags"]=new_df["tags"].apply(lambda x:" ".join(x))

new_df['tags'][0]

new_df["tags"].apply(lambda x:x.lower())

# converted into lowercase
new_df["tags"]=new_df["tags"].apply(lambda x:x.lower())

new_df.head()

import nltk

from nltk.stem.porter import PorterStemmer
ps= PorterStemmer()

def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

new_df["tags"]=new_df["tags"].apply(stem)

new_df["tags"][0]

from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features=5000, stop_words="english")

vectors = cv.fit_transform(new_df['tags']).toarray()

feature_names = cv.get_feature_names_out()

feature_names

len(feature_names)

from sklearn.metrics.pairwise import cosine_similarity

similarity=cosine_similarity(vectors)

similarity.shape

sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:7]

# The error you're encountering indicates that you're trying to iterate over a numpy.float64 object, which is not iterable. This typically happens when the 'distances' variable is a scalar rather than an iterable object like a list or an array. To resolve this, ensure that 'distances' is a list or an array before attempting to iterate over it.

# Here's a modified version of your code with potential fixes:

def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]

    # Check if distances is a scalar, and if so, convert it to a list
    if isinstance(distances, np.float64):
        distances = [distances]

    # Now, proceed with sorting and printing the top recommendations
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

    # Assuming 'movies_list' is defined somewhere in your code
    for k in movies_list:
        print(new_df.iloc[k[0]].title)

    return movie_index

# Call the function

recommend("Rockaway")

sk=new_df.to_excel('tmdb 5000 movies filtered dataset.xlsx', index=False)

sk

import pickle

pickle.dump(new_df,open("movies.pkl","wb"))

pickle.dump(similarity,open('similarity.pkl','wb'))

pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb'))