import cv2
import numpy as np
import mediapipe as mp
import time
import streamlit as st
from keras.models import load_model
from music import SpotifyEmotionPlaylistRecommender   # your class from music.py
import os

# ------------------------------
# Load trained model and corrected labels
# ------------------------------
model = load_model("model.h5")
labels = ["happy", "neutral", "surprise", "rock", "angry", "sad"]

# Mediapipe setup
holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🎭 Emotion Detection & 🎵 Music Recommendation")
st.markdown("This app captures your facial expression and recommends a Spotify playlist based on your emotion.")

# Button to start camera
if st.button("Start Emotion Detection"):
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    captured_predictions = []
    start_time = time.time()

    while True:
        lst = []
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        res = holis.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if res.face_landmarks:
            for i in res.face_landmarks.landmark:
                lst.append(i.x - res.face_landmarks.landmark[1].x)
                lst.append(i.y - res.face_landmarks.landmark[1].y)

            if res.left_hand_landmarks:
                for i in res.left_hand_landmarks.landmark:
                    lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                    lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
            else:
                lst.extend([0.0] * 42)

            if res.right_hand_landmarks:
                for i in res.right_hand_landmarks.landmark:
                    lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
                    lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
            else:
                lst.extend([0.0] * 42)

            # Predict
            lst = np.array(lst).reshape(1, -1)
            prediction = model.predict(lst, verbose=0)
            pred_label = labels[np.argmax(prediction)]
            captured_predictions.append(pred_label)

            # Display live prediction
            cv2.putText(frame, f"Prediction: {pred_label}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Show webcam in Streamlit
        stframe.image(frame, channels="BGR")

        # Stop after 5 seconds
        if time.time() - start_time > 5:
            break

    cap.release()

    # --- Process Captured Emotions ---
    if captured_predictions:
        dominant_emotion = max(set(captured_predictions), key=captured_predictions.count)
        st.success(f"✅ Dominant Emotion Detected: **{dominant_emotion}**")
    else:
        dominant_emotion = "neutral"
        st.warning("⚠️ No emotion detected, defaulting to **neutral**.")

    # --- Spotify Recommendation ---
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    spotify_recommender = SpotifyEmotionPlaylistRecommender(client_id, client_secret, redirect_uri)
    recommendation = spotify_recommender.recommend_spotify_playlist(dominant_emotion)

    st.subheader(f"🎵 Recommended Playlist for {dominant_emotion.capitalize()}")
    st.write(f"**{recommendation['name']}** - {recommendation['description']}")

    if recommendation['spotify_playlists']:
        for i, playlist in enumerate(recommendation['spotify_playlists'], 1):
            st.markdown(f"**{i}. {playlist['name']}** by *{playlist['owner']}*  \n"
                        f"Tracks: {playlist['total_tracks']}  \n"
                        f"[🔗 Open Playlist]({playlist['external_url']})")
    else:
        st.error("No Spotify playlists found for this emotion.")
