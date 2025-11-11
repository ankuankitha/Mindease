import json, spotipy
from spotipy.oauth2 import SpotifyOAuth

with open("spotify_creds.json") as f:
    creds = json.load(f)

def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        redirect_uri=creds["redirect_uri"],
        scope="playlist-read-private playlist-read-collaborative"
    ))

def embed_spotify_playlist(playlist_id):
    return f"https://open.spotify.com/embed/playlist/{playlist_id}"

def recommend_music(emotion):
    playlists = {
        "happy": "1rpHTgLGdo1WCl8fjAbe9j",
        "sad": "6irxS2m3XrDjWPZFkE5qgo",
        "angry": "5tPKfHMEdpRFUtcJNXtILi",
        "neutral": "4nl8KfqGINaA1w9DYmSGfY",
        "stressed": "6YKW0eikQJwXnm9DCwBNG8"
    }
    return embed_spotify_playlist(playlists.get(emotion.lower(), "4nl8KfqGINaA1w9DYmSGfY"))
