import requests
import base64
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import time

# Step 1: Get the Access Token with retry mechanism
def get_access_token(client_id, client_secret, retries=3):
    client_credentials = f"{client_id}:{client_secret}"
    client_credentials_base64 = base64.b64encode(client_credentials.encode()).decode()
CLIENT_ID = 'eb10f689c74146b9a8e215e688cce191'
CLIENT_SECRET = '7fcfde395f0e46bca0e377856ef1194b'

    token_url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': f'Basic {client_credentials_base64}', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials'}
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

    for attempt in range(retries):
        try:
            response = requests.post(token_url, headers=headers, data=data, timeout=10)
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                return access_token
        except requests.exceptions.ConnectionError:
            time.sleep(5)
    return None
st.title("🎧 Simple Spotify Recommender (Artist Top Tracks)")

# Step 2: Calculate Weighted Popularity
def calculate_weighted_popularity(release_date):
    try:
        release_year = int(release_date[:4])
        current_year = datetime.now().year
        age = current_year - release_year
    except (TypeError, ValueError):
        return 0
    return max(0, 100 - age * 10)

# Step 3: Fetch playlist data
def get_trending_playlist_data(playlist_id, client_id, client_secret):
    access_token = get_access_token(client_id, client_secret)
    if not access_token:
        print("Failed to obtain access token.")
        return pd.DataFrame()

    sp = spotipy.Spotify(auth=access_token)
    tracks = []
song_url = st.text_input("Paste a Spotify Song Link:")

if song_url and st.button("Get Recommendations"):
    try:
        results = sp.playlist_tracks(playlist_id, fields='items(track(id, name, artists, album(id, name, release_date), popularity)), next', limit=100)
        tracks.extend(results['items'])

        while results.get('next'):
            results = sp.next(results)
            tracks.extend(results['items'])

    except Exception as e:
        print(f"Error fetching playlist data: {e}")
        return pd.DataFrame()

    music_data = []
    for track_info in tracks:
        track = track_info['track']
        if not track:
            continue

        # Extract track details
        track_name = track['name']
        artists = ', '.join([artist['name'] for artist in track['artists']])
        album_name = track['album']['name']
        album_id = track['album']['id']
        track_id = track['id']
        release_date = track['album'].get('release_date', None)
        popularity = track.get('popularity', 0)

        # Calculate weighted popularity
        weighted_popularity = calculate_weighted_popularity(release_date)

        # Get audio features
        audio_features = sp.audio_features(track_id)[0] if track_id else None

        # Store track information
        track_data = {
            'Track Name': track_name,
            'Artists': artists,
            'Album Name': album_name,
            'Album ID': album_id,
            'Track ID': track_id,
            'Release Date': release_date,
            'Popularity': popularity,
            'Weighted Popularity': weighted_popularity,
            'Danceability': audio_features['danceability'] if audio_features else None,
            'Energy': audio_features['energy'] if audio_features else None,
            'Loudness': audio_features['loudness'] if audio_features else None,
            'Speechiness': audio_features['speechiness'] if audio_features else None,
            'Acousticness': audio_features['acousticness'] if audio_features else None,
            'Instrumentalness': audio_features['instrumentalness'] if audio_features else None,
            'Liveness': audio_features['liveness'] if audio_features else None,
            'Valence': audio_features['valence'] if audio_features else None,
            'Tempo': audio_features['tempo'] if audio_features else None,
            'Duration_ms': audio_features['duration_ms'] if audio_features else None,
        }
        music_data.append(track_data)

    return pd.DataFrame(music_data)
        track_id = song_url.split("/")[-1].split("?")[0]
        track = sp.track(track_id)
        artist_id = track['artists'][0]['id']
        top_tracks = sp.artist_top_tracks(artist_id)

# Normalize features
def normalize_features(df):
    scaler = MinMaxScaler()
    return pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
        st.success(f"Selected Song: {track['name']} by {', '.join(a['name'] for a in track['artists'])}")
        st.subheader("Recommended (Top Tracks by Same Artist):")

# Calculate similarity and get recommendations
def get_hybrid_recommendations(playlist_data, selected_track_name, top_n=10):
    if selected_track_name not in playlist_data['Track Name'].values:
        print(f"Track '{selected_track_name}' not found in the playlist.")
        return pd.DataFrame()
        for item in top_tracks['tracks']:
            st.write(f"🎶 {item['name']} - [Listen on Spotify]({item['external_urls']['spotify']})")

    selected_index = playlist_data[playlist_data['Track Name'] == selected_track_name].index[0]

    audio_features = playlist_data.drop(
        ['Track Name', 'Artists', 'Album Name', 'Album ID', 'Track ID', 'Release Date', 'Popularity', 'Weighted Popularity'], axis=1
    ).fillna(0)

    normalized_features = normalize_features(audio_features)
    similarity_matrix = cosine_similarity(normalized_features)
    similarity_scores = similarity_matrix[selected_index]

    recommendations = pd.DataFrame({
        'Track Name': playlist_data['Track Name'],
        'Content Similarity': similarity_scores
    })

    recommendations = recommendations[recommendations['Track Name'] != selected_track_name]
    return recommendations.sort_values(by='Content Similarity', ascending=False).head(top_n)

def plot_recommendations(recommendations):
    if recommendations.empty:
        return

    plt.figure(figsize=(12, 6))
    plt.bar(recommendations['Track Name'], recommendations['Content Similarity'], color='orange')
    plt.xlabel('Track Name')
    plt.ylabel('Similarity Score')
    plt.title('Recommended Songs')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def main(client_id, client_secret, playlist_id, selected_track_name, top_n=10):
    playlist_data = get_trending_playlist_data(playlist_id, client_id, client_secret)
    if playlist_data.empty:
        return

    recommendations = get_hybrid_recommendations(playlist_data, selected_track_name, top_n)
    plot_recommendations(recommendations)

# Input Parameters
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_secret_key'
PLAYLIST_ID = '7bczOWUTWDDVRX09GCQakM'
SELECTED_TRACK_NAME = 'Lucid Dreams'
TOP_N_RECOMMENDATIONS = 10

if __name__ == "__main__":
    main(CLIENT_ID, CLIENT_SECRET, PLAYLIST_ID, SELECTED_TRACK_NAME, TOP_N_RECOMMENDATIONS)
    except Exception as e:
        st.error(f"Error: {e}")
