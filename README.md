# AI Movie Recommender

An emotion-based movie recommendation system that uses facial recognition to analyze your mood and suggest movies accordingly.

## Features

- **Emotion Detection**: Uses your webcam to detect facial emotions
- **Smart Recommendations**: Suggests movies based on detected emotions
- **TMDb Integration**: Fetches real movie ratings and reviews from TMDb API
- **Emoji Display**: Shows corresponding emoji for detected emotions
- **Real-time Analysis**: Instant movie recommendations

## Emotion to Genre Mapping

- 😊 **Happy** → Comedy
- 😢 **Sad** → Romance  
- 😠 **Angry** → Action
- 😨 **Fear** → Horror
- 😮 **Surprise** → Animation
- 😐 **Neutral** → Comedy
- 🤢 **Disgust** → Horror

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get TMDb API Key

1. Go to [TMDb API](https://www.themoviedb.org/documentation/api)
2. Create an account if you don't have one
3. Navigate to Settings → API
4. Generate a new API key

### 3. Configure API Key

Replace `YOUR_TMDB_API_KEY` in `app.py` with your actual TMDb API key:

```python
TMDB_API_KEY = "your_actual_tmdb_api_key_here"
```

### 4. Run the Application

```bash
python app.py
```

### 5. Access the Application

Open your browser and navigate to `http://localhost:5000`

## How It Works

1. **Camera Access**: The application requests access to your webcam
2. **Emotion Analysis**: Takes a snapshot and analyzes your facial expression
3. **Movie Selection**: Based on your emotion, selects a movie from the corresponding genre
4. **TMDb Integration**: Fetches real ratings and reviews from TMDb API
5. **Display Results**: Shows the movie recommendation with emoji, rating, and review

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Emotion Detection**: DeepFace library
- **Movie Data**: TMDb API
- **Caching**: 5-minute cache to avoid rate limiting

## Notes

- The application caches TMDb API responses for 5 minutes to avoid hitting rate limits
- Reviews are truncated to 200 characters for better display
- **TMDb API Required**: This application strictly uses TMDb API for movie data. No fallback data is provided.
- The application now includes 25+ movies across 5 different genres for better recommendations
- **Important**: You must configure a valid TMDb API key for the application to work properly

## Troubleshooting

- **Camera Access**: Ensure your browser has permission to access the camera
- **API Errors**: Check your TMDb API key and internet connection
- **Dependencies**: Make sure all required packages are installed