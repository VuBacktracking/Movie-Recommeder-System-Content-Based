'''Streamlit Documentation: https://docs.streamlit.io/'''

import streamlit as st
import pickle
import requests
from streamlit.components.v1 import components

movies = pickle.load(open("Data/movies_list.pkl", "rb"))
# similarity_matrix = pickle.load(open("Data/similarity_ct.pkl", "rb"))
similarity_matrix = pickle.load(open("Data/similarity_tf.pkl", "rb"))
top_10_movies = pickle.load(open("Data/top_10_movies.pkl", "rb"))

movie_titles = movies["title"].values

tmdb_image_path = "https://image.tmdb.org/t/p/w500"
# This is my own api key on TMDB website, you can get your own api key on https://www.themoviedb.org
# After getting api key, replace your api key with mine to run.
api_key = "YOUR_API_KEY"

def get_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US")
    data = response.json()
    return tmdb_image_path + data["poster_path"]

# we only need id of the movie to fetch the poster of that movie
def recommend_movie(movie_name, n_movies):
    # index of movie
    pos_movie = movies[movies["title"] == movie_name].index[0]
    # similarity vector
    similarity = similarity_matrix[pos_movie]
    # N similar movies
    pos_movies_list = sorted(list(enumerate(similarity)), reverse=True, key=lambda x: x[1])[1:n_movies+1]
    
    # index of similar movies
    recommendation_movie_pos = [pos_movie[0] for pos_movie in pos_movies_list] 
    # fetch the poster and the title of each movie
    recommendation_title = []
    recommendation_poster = []
    for i in recommendation_movie_pos:
        # Append title to the list
        title = movies.iloc[i].title
        recommendation_title.append(title)
        
        # Append poster path
        movie_id = movies.iloc[i].movie_id
        recommendation_poster.append(get_poster(movie_id))

    return recommendation_title, recommendation_poster, recommendation_movie_pos


# Load custom CSS
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title
st.markdown('''<b class = 'title'>
                Movie Recommender System
            </b>''', 
            unsafe_allow_html=True)

# Top 10 movies header
st.markdown('''<h2 class = 'header-10-movies'>
                Top 10 Highest Rating Movies
            </h2>''',
            unsafe_allow_html=True)

# Image Carousel Component
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")
imageUrls = [get_poster(id) for id in top_10_movies.values]
selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)
if selectedImageUrl is not None:
    st.image(selectedImageUrl)

# Selected Movie
option = st.selectbox( "Type and select a movie to get recommendation",
                        movie_titles,
                        index=None,
                        placeholder="Select a movie...",
                    )

# Number of movies to recommend
n_movies = st.slider("Insert the number of movies for recommendation", min_value=1, max_value=20)

if st.button("Recommend"):
    titles, posters, recommended_pos = recommend_movie(option, n_movies)
    # for movie in recommendations:
    #     st.write(movie)
    ncols = 5
    nrows = (n_movies - 1) // ncols + 1  # Calculate the number of rows
    
    # Create the columns for the grid
    cols = [st.columns(ncols) for _ in range(nrows)]
    
    # Loop to add content to the columns
    for i in range(nrows):
        for j in range(ncols):
            index = i * ncols + j  # Calculate the index in the 'titles' and 'posters' lists
            if index < n_movies:  # Make sure the index is within the range of available recommendations
                cols[i][j].image(posters[index])
                cols[i][j].write(f''' <p class='custom-text'>
                                        {titles[index]}
                                    </p>''', unsafe_allow_html=True)
                
                # Average Vote
                vote_avg = movies.iloc[recommended_pos[index]].vote_average
                cols[i][j].write(f'<b class = "rate-count">Rating</b>:<b> {vote_avg}</b>',unsafe_allow_html=True)
                
                # Vote count
                vote_count = movies.iloc[recommended_pos[index]].vote_count
                cols[i][j].write(f'<b class = "rate-count">Vote Count</b>:<b> {vote_count}</b>',unsafe_allow_html=True)
            else:
                cols[i][j].empty()  # If there are no more recommendations, leave the column empty

# st-emotion-cache-4ail08 e1nzilvr5 select..
