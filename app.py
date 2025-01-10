import pickle
import pandas as pd
import streamlit as st
import requests


def fetch_poster(movie_id):
    # Request to TMDB API
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=cb9006c20b31ff1cf407e7f4b9c03459'.format(movie_id))

    # Convert response to JSON
    data = response.json()

    # # Debugging: Print the whole API response to check if poster_path exists
    # st.text(str(data))

    # Check if the poster_path exists in the response
    if 'poster_path' in data and data['poster_path'] is not None:
        # If poster_path exists, return the full URL
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        # If poster_path doesn't exist or is None, return a placeholder image
        return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        fetch_poster(i[0])
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', "rb"))

# custom CSS for cursor
st.markdown("""
    <style>
    .streamlit-expanderHeader, .stSelectbox, .stSelectbox div {
        cursor: pointer;
    }
     .stImage {
        cursor: pointer;
    </style>
""", unsafe_allow_html=True)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)

    st.markdown("<br>", unsafe_allow_html=True)

    # loop to create 5 columns to display the recommended movies and their posters in a row
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.text(names[i])