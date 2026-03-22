from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
import base64
import cv2
import numpy as np
import requests
import time
from deepface import DeepFace

app = Flask(__name__)

movies = pd.read_csv("movies.csv")

# TMDb API Configuration
TMDB_API_KEY = "fd51106fd282dbbf7997e1067fff840d"  # Replace with your actual TMDb API key
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Emoji mapping for emotions
emotion_emoji_map = {
    "happy": "😊",
    "sad": "😢", 
    "angry": "😠",
    "fear": "😨",
    "surprise": "😮",
    "neutral": "😐",
    "disgust": "🤢"
}

# Cache for TMDb data to avoid rate limiting
tmdb_cache = {}
cache_time = {}
CACHE_DURATION = 300  # 5 minutes cache

def get_tmdb_movie_data(movie_title):
    """Fetch movie data from TMDb API"""
    current_time = time.time()
    
    # Check cache first
    if movie_title in tmdb_cache:
        if current_time - cache_time.get(movie_title, 0) < CACHE_DURATION:
            return tmdb_cache[movie_title]
    
    # Check if TMDb API key is configured
    if TMDB_API_KEY == "YOUR_TMDB_API_KEY" or not TMDB_API_KEY:
        return {"rating": "N/A", "review": "Please configure TMDb API key in app.py"}
    
    try:
        # Search for movie
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": movie_title,
            "language": "en-US",
            "page": 1
        }
        
        response = requests.get(search_url, params=params)
        if response.status_code != 200:
            return {"rating": "N/A", "review": "Error connecting to TMDb API"}
        
        search_data = response.json()
        if not search_data.get("results"):
            return {"rating": "N/A", "review": "Movie not found in TMDb database"}
        
        # Get the first result
        movie_id = search_data["results"][0]["id"]
        
        # Get movie details
        details_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        details_params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US"
        }
        
        details_response = requests.get(details_url, params=details_params)
        if details_response.status_code != 200:
            return {"rating": "N/A", "review": "Error fetching movie details from TMDb"}
        
        movie_data = details_response.json()
        
        # Get reviews
        reviews_url = f"{TMDB_BASE_URL}/movie/{movie_id}/reviews"
        reviews_params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "page": 1
        }
        
        reviews_response = requests.get(reviews_url, params=reviews_params)
        review_text = "No reviews available"
        
        if reviews_response.status_code == 200:
            reviews_data = reviews_response.json()
            if reviews_data.get("results"):
                # Get the first review
                review_text = reviews_data["results"][0].get("content", "No reviews available")
                # Truncate review if too long
                if len(review_text) > 200:
                    review_text = review_text[:200] + "..."
        
        result = {
            "rating": movie_data.get("vote_average", "N/A"),
            "review": review_text
        }
        
        # Cache the result
        tmdb_cache[movie_title] = result
        cache_time[movie_title] = current_time
        
        return result
        
    except Exception as e:
        print(f"Error fetching TMDb data for {movie_title}: {e}")
        return {"rating": "N/A", "review": "Error fetching data from TMDb"}

emotion_genre_map = {
    "happy": "Comedy",
    "sad": "Romance",
    "angry": "Action",
    "fear": "Horror",
    "surprise": "Animation",
    "neutral": "Comedy",
    "disgust": "Horror"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json["image"]
    encoded = data.split(",")[1]
    img_bytes = base64.b64decode(encoded)

    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result = DeepFace.analyze(
        frame,
        actions=['emotion'],
        enforce_detection=False,
        detector_backend='opencv'
    )
    emotion = result[0]['dominant_emotion']

    genre = emotion_genre_map.get(emotion, "Comedy")
    rec = movies[movies["genre"] == genre]

    movie = "No movie found"
    rating = "N/A"
    review = "No review available"
    emoji = emotion_emoji_map.get(emotion, "😐")

    if not rec.empty:
        movie = random.choice(rec["title"].values)
        # Fetch data from TMDb API instead of hardcoded data
        tmdb_data = get_tmdb_movie_data(movie)
        rating = tmdb_data["rating"]
        review = tmdb_data["review"]

    return jsonify({
        "emotion": emotion,
        "emoji": emoji,
        "genre": genre,
        "movie": movie,
        "rating": rating,
        "review": review
    })

if __name__ == "__main__":
    app.run(debug=True)
