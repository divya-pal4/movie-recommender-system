import numpy as np
import pandas as pd
import ast
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

ps = PorterStemmer()

base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct path to datasets
credits_path = os.path.join(base_dir, '..', 'datasets', 'credits.csv')
movies_path = os.path.join(base_dir, '..', 'datasets', 'movies.csv')

# Load CSVs
credits = pd.read_csv(credits_path)
movies = pd.read_csv(movies_path)

movies = movies.merge(credits, on='title')
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
import ast


def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

movies.dropna(inplace=True)

movies['genres'] = movies['genres'].apply(convert)

movies['keywords'] = movies['keywords'].apply(convert)

ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')



def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L
movies['cast'] = movies['cast'].apply(convert)

movies['cast'] = movies['cast'].apply(lambda x:x[0:3])


def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L


movies['crew'] = movies['crew'].apply(fetch_director)


def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1


movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)


movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new = movies.drop(columns=['overview','genres','keywords','cast','crew'])
new['tags'] = new['tags'].apply(lambda x: " ".join(x))

# import nltk
# from nltk.stem.porter import PorterStemmer
def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

new['tags']=new['tags'].apply(stem)



# from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vector = cv.fit_transform(new['tags']).toarray()

cv.get_feature_names_out()
# from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vector)
new[new['title'] == 'The Lego Movie'].index[0]



def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_titles = []
    for i in distances[1:6]:
        recommended_titles.append(new.iloc[i[0]].title)
    return recommended_titles


# import pickle
base_dire = os.path.dirname(os.path.abspath(__file__))

# Build path to ../models/
movie_list_path = os.path.join(base_dire, '..', 'models', 'movie_list.pkl')
similarity_path = os.path.join(base_dire, '..', 'models', 'similarity.pkl')

with open(movie_list_path, 'wb') as f:
    pickle.dump(new, f)

with open(similarity_path, 'wb') as f:
    pickle.dump(similarity, f)


# import nltk
nltk.download('stopwords')