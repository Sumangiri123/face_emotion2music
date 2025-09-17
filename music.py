import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
class SpotifyEmotionPlaylistRecommender:
    def __init__(self, client_id, client_secret, redirect_uri):
        """
        Initialize the Spotify playlist recommender
        """
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="playlist-read-private,user-read-private"
            ))
        except Exception as e:
            print(f"Error initializing Spotify client: {e}")
            self.sp = None

        # ✅ Match your 7 corrected labels
        self.emotion_to_playlist = {
            'happy': {
                'name': 'Feel Good Vibes',
                'description': 'Upbeat songs to match your joyful mood',
                'energy': 0.8,
                'valence': 0.9
            },
            'neutral': {
                'name': 'Focus & Flow',
                'description': 'Balanced tracks for any activity',
                'energy': 0.5,
                'valence': 0.5
            },
            'surprise': {
                'name': 'Curiosity & Wonder',
                'description': 'Intriguing tracks for unexpected moments',
                'energy': 0.7,
                'valence': 0.8
            },
            'rock': {
                'name': 'Rock On!',
                'description': 'High-energy rock music to boost your mood',
                'energy': 0.9,
                'valence': 0.7
            },
            'angry': {
                'name': 'Calm Down & Relax',
                'description': 'Soothing tracks to ease frustration',
                'energy': 0.3,
                'valence': 0.4
            },
            'sad': {
                'name': 'Gentle Comfort',
                'description': 'Understanding songs for difficult moments',
                'energy': 0.2,
                'valence': 0.3
            }
        }

        # ✅ Queries for Spotify search
        self.emotion_search_terms = {
            'happy': 'happy upbeat feel good',
            'neutral': 'focus concentration',
            'surprise': 'eclectic surprising',
            'rock': 'classic rock hard rock',
            'angry': 'calm relaxing',
            'sad': 'sad melancholic'
        }

    def search_spotify_playlists(self, query, limit=5):
        if not self.sp:
            print("Spotify client not initialized")
            return []

        try:
            results = self.sp.search(q=query, type='playlist', limit=limit)
            playlists = []

            if not results or 'playlists' not in results or 'items' not in results['playlists']:
                return playlists

            for item in results['playlists']['items']:
                if item is None:
                    continue
                playlist = {
                    'name': item.get('name', 'Unknown Playlist'),
                    'description': item.get('description', 'No description available'),
                    'uri': item.get('uri', ''),
                    'external_url': item.get('external_urls', {}).get('spotify', ''),
                    'owner': item.get('owner', {}).get('display_name', 'Unknown'),
                    'total_tracks': item.get('tracks', {}).get('total', 0)
                }
                playlists.append(playlist)
            return playlists
        except Exception as e:
            print(f"Error searching Spotify playlists: {e}")
            return []

    def recommend_spotify_playlist(self, emotion):
        emotion = emotion.lower()
        if emotion not in self.emotion_to_playlist:
            emotion = 'neutral'

        playlist_info = self.emotion_to_playlist[emotion].copy()
        search_query = self.emotion_search_terms.get(emotion, 'focus')
        spotify_playlists = self.search_spotify_playlists(search_query)

        playlist_info['spotify_playlists'] = spotify_playlists
        return playlist_info


if __name__ == "__main__":
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    try:
        spotify_recommender = SpotifyEmotionPlaylistRecommender(client_id, client_secret, redirect_uri)

        # ✅ Your corrected labels
        emotions = ["happy", "neutral", "surprise", "rock", "angry", "sad"]

        for emotion in emotions:
            print(f"\n=== Recommendation for {emotion} ===")
            recommendation = spotify_recommender.recommend_spotify_playlist(emotion)

            print(f"Playlist Name: {recommendation['name']}")
            print(f"Description: {recommendation['description']}")

            if recommendation['spotify_playlists']:
                print("Spotify Playlists:")
                for i, playlist in enumerate(recommendation['spotify_playlists'], 1):
                    print(f"{i}. {playlist['name']} by {playlist['owner']}")
                    print(f"   Tracks: {playlist['total_tracks']}")
                    print(f"   URL: {playlist['external_url']}\n")
            else:
                print("No Spotify playlists found for this emotion")

    except Exception as e:
        print(f"Error in main execution: {e}")
