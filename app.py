import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[movie_index])),reverse=True,key = lambda x: x[1])[1:6]
    movies_list_1=sorted(list(enumerate(similarity_1[movie_index])),reverse=True,key = lambda x: x[1])[1:6]
    list_1=[]
    list_2=[]
    recommended_movie_posters = []
    for i in movies_list:
        list_1.append(movies.iloc[i[0]].title)
    for j in movies_list_1:
        list_2.append(movies.iloc[j[0]].title)
    final_list=list(set(list_1+list_2))
    for k in final_list:
        movie_id = movies._get_value(movies[movies['title']==k].index[0],'id')
        recommended_movie_posters.append(fetch_poster(movie_id))
    return final_list,recommended_movie_posters

st.title('Movie Recommender System')
st.markdown("<div style='text-align: right;font-size: 20px;'>Created by Mukesh Tiwary</div><hr><br><br>",
            unsafe_allow_html=True)
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
similarity_1 = pickle.load(open('similarity_1.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)


if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    l=len(recommended_movie_names)
    st.markdown("<div style='text-align: center;font-size: 50px;'>RECOMMENDED MOVIES</div><hr><br><br>",
                unsafe_allow_html=True)
    for i in range(1,l+1,1):
        st.markdown(f"<span style='font-size: 38px;'> {i}.{recommended_movie_names[i-1]}</span>", unsafe_allow_html=True)
        st.image(recommended_movie_posters[i-1], width=475)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)




