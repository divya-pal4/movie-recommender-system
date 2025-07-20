import pickle
import streamlit as st
import requests
import os

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    try:
        data = requests.get(url, timeout=5)
        data.raise_for_status()
        data = data.json()
        poster_path = data.get('poster_path')
        if not poster_path:
            return None
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except Exception as e:
        return None

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error('Selected movie not found in database.')
        return [], []
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        recommended_movie_posters.append(poster if poster else "https://via.placeholder.com/500x750?text=No+Poster")
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

try:
    movies = pickle.load(open('./models/movie_list.pkl','rb'))
    similarity = pickle.load(open('./models/similarity.pkl','rb'))
except FileNotFoundError:
    st.error('Model files not found. Please ensure movie_list.pkl and similarity.pkl exist in the models directory.')
    st.stop()
except Exception as e:
    st.error(f'Error loading model files: {e}')
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    if len(recommended_movie_names) < 5:
        st.warning('Less than 5 recommendations found. Please try another movie.')
    else:
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            col.text(recommended_movie_names[idx])
            col.image(recommended_movie_posters[idx])
            if recommended_movie_posters[idx] == "https://via.placeholder.com/500x750?text=No+Poster":
                col.caption("No poster available")