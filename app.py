
import streamlit as st
import pickle

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"

)

# -----------------------------
# Load files
# -----------------------------
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies_df['title'].values


# -----------------------------
# Recommendation function
# -----------------------------
def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:8]

    recommend_movies = []
    for i in movie_list:
        recommend_movies.append(movies_df.iloc[i[0]]['title'])

    return recommend_movies


# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
    <style>
    .movie-card {
        padding: 15px;
        border-radius: 15px;
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        text-align: center;
        margin: 10px;
        color: #000000;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        transition: transform 0.2s ease;
    }

    .movie-card:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)


# -----------------------------
# Title
# -----------------------------
st.markdown('<p class="title">🎬 Movie Recommendation System</p>', unsafe_allow_html=True)


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("⚙️ Settings")
selected_movie_name = st.sidebar.selectbox(
    'Choose a movie',
    movies_list
)

num_recommendations = st.sidebar.slider(
    "Number of recommendations",
    3, 10, 7
)


# -----------------------------
# Recommend Button
# -----------------------------
if st.sidebar.button('🎯 Recommend'):
    recommendations = recommend(selected_movie_name)

    st.subheader(f"Top recommendations for **{selected_movie_name}**:")

    # Display in columns (cards layout)
    cols = st.columns(3)

    for i, movie in enumerate(recommendations[:num_recommendations]):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="movie-card">
                    <h4>🎥 {movie}</h4>
                </div>
            """, unsafe_allow_html=True)


# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Made with ❤️ by Sahil")
