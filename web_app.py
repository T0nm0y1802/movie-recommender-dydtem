from flask import Flask, render_template, request
import pandas as pd
import pickle
import requests

app = Flask(__name__)

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


# Load movie data and similarity matrix
movies_dict = pickle.load(open('MovieData/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('MovieData/similarity.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html', movies=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    movies_dict = pickle.load(open('MovieData/movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('MovieData/similarity.pkl', 'rb'))

    selected_movie_name = request.form['movie']
    movie_index = movies[movies['title'] == selected_movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))


    
    recommendations = zip(recommended_movies, recommended_movies_poster)
    return render_template('recommendation.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
 
