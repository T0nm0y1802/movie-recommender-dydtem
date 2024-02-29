import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhNDAwZWU4MWU1MWYwNTIxM2JjMGE4ZTVkNjNiOThlMyIsInN1YiI6IjY1ZGY1NjQxOThmMWYxMDE3ZDk5ZjUwMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Y7LppybcaFoTEQ_JhmEJKSFYPhgrgImsZie9lqvJLH4"
}
    response = requests.get("https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id), headers=headers)
    data=response.json()
    return "https://image.tmdb.org/t/p/original"+data['poster_path']

similarity=pickle.load(open('MovieData\similarity.pkl','rb'))

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

movies_dict=pickle.load(open('MovieData\movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

st.title('Movie Recommeder System')

selected_movie_name=st.selectbox(
    'Enter Movie',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    coll, col2, col3 ,col4, col5= st.columns(5)
    with coll:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])    
    