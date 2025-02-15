# Spotify Playlist Song Recommendation System

## Overview
This project retrieves trending songs from a Spotify playlist, derives their audio features, and gives recommendations on similar content using cosine similarity. Both popularity and musical features are used by the recommendation system to recommend similar songs for a provided song.

## Features
- Retrieves song information from a Spotify playlist with the help of the Spotify API.
- Derives audio features such as danceability, energy, loudness, valence, and tempo.
- Computed content similarity through cosine similarity.
- MinMaxScaled the data to have higher accuracy.
- Outputs a ranked list of songs as recommendations by similarity.
- Presents the recommendations via bar chart.

## Dependencies
Make sure to install the following Python packages:
pip install requests pandas numpy spotipy scikit-learn matplotlib

## Usage
### 1. Set Up Your Spotify Credentials
Get yourself a Spotify API client ID and client secret via the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

### 2. Run the Script
Modify the following parameters in the script:
- `CLIENT_ID`: Your Spotify API Client ID
- `CLIENT_SECRET`: Your Spotify API Client Secret
- `PLAYLIST_ID`: The ID of the playlist you want to fetch songs from
- `SELECTED_TRACK_NAME`: The name of the song for which you want recommendations
- `TOP_N_RECOMMENDATIONS`: Number of recommendations to generate

### 3. Then Execute

## Functions Explained
### `get_access_token(client_id, client_secret, retries=3)`
Retrieves an access token from Spotify using client credentials.
### `calculate_weighted_popularity(release_date)`
Computes popularity of songs based on release date and scales older songs' popularity.
### `get_trending_playlist_data(playlist_id, client_id, client_secret)`
Retrieves playlist information, track metadata, and audio features.
### `normalize_features(df)`
Scales numerical features with MinMaxScaler for similarity comparison.
### `get_hybrid_recommendations(playlist_data, selected_track_name, top_n=10)`
Calculates cosine similarity among tracks and returns similar songs.
### `plot_recommendations(recommendations)`
Plots the recommended songs in a bar chart.
### `main(client_id, client_secret, playlist_id, selected_track_name, top_n=10)'
Runs the process of data retrieval, recommendation calculation, and visualization.

### Output:
![Screenshot 2025-02-15 115334](https://github.com/user-attachments/assets/90005251-b2f8-4594-9c53-d754c78a13e9)

