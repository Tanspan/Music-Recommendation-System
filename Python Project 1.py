import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = 'eb10f689c74146b9a8e215e688cce191'
CLIENT_SECRET = '7fcfde395f0e46bca0e377856ef1194b'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

st.title("🎧 Simple Spotify Recommender (Artist Top Tracks)")

song_url = st.text_input("Paste a Spotify Song Link:")

if song_url and st.button("Get Recommendations"):
    try:
        track_id = song_url.split("/")[-1].split("?")[0]
        track = sp.track(track_id)
        artist_id = track['artists'][0]['id']
        top_tracks = sp.artist_top_tracks(artist_id)

        st.success(f"Selected Song: {track['name']} by {', '.join(a['name'] for a in track['artists'])}")
        st.subheader("Recommended (Top Tracks by Same Artist):")

        for item in top_tracks['tracks']:
            st.write(f"🎶 {item['name']} - [Listen on Spotify]({item['external_urls']['spotify']})")

    except Exception as e:
        st.error(f"Error: {e}")
