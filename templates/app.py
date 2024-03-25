from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Load data and models
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))

# Ensure that movies_dict is a dictionary with 'title' and other relevant columns
# Adjust the code accordingly based on the structure of movies_dict

# Example assumption: movies_dict has a 'title' key
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html', movie_titles=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    selected_movie = request.form['selected_movie']
    recommendations = recommend(selected_movie)
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
