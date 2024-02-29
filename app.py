import streamlit as st
import pandas as pd
import pickle
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhNDAwZWU4MWU1MWYwNTIxM2JjMGE4ZTVkNjNiOThlMyIsInN1YiI6IjY1ZGY1NjQxOThmMWYxMDE3ZDk5ZjUwMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Y7LppybcaFoTEQ_JhmEJKSFYPhgrgImsZie9lqvJLH4"
}
    response = requests.get("https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id), headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# Load movie data and similarity matrix
movies_dict = pickle.load(open('MovieData\movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('MovieData\similarity.pkl', 'rb'))

# Set page title and background color
st.set_page_config(page_title='Movie Recommender System', page_icon="🎬", layout="wide", initial_sidebar_state="expanded")
st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(to right, #833ab4, #fd1d1d, #fcb045) !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page title and description
st.title('Movie Recommender System')
st.write("Welcome to the Movie Recommender System! Select a movie from the dropdown menu and click 'Recommend' to find similar movies.")

# Movie selection dropdown
selected_movie_name = st.selectbox('Select a Movie', movies['title'].values)

# Recommendation button
if st.button('Recommend'):
    with st.spinner('Finding Recommendations...'):
        names, posters = recommend(selected_movie_name)
    
    # Display recommended movies and posters in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for name, poster, col in zip(names, posters, cols):
        with col:
            st.write(name)
            st.image(poster, use_column_width=True)

# Footer
st.write("---")
st.write("Made with ❤️ by Tanmay")


    