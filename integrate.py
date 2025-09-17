import cv2
import numpy as np
import mediapipe as mp
import time
from keras.models import load_model
from music import SpotifyEmotionPlaylistRecommender   # import your class from music.py

# Load trained model and corrected labels
model = load_model("model.h5")
labels = ["happy", "neutral", "surprise", "rock", "angry", "sad"]

# Mediapipe setup
holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)
print("🎥 Starting camera... Capturing emotions for 5 seconds...")

# Store predictions
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

        # Show prediction live
        cv2.putText(frame, f"Prediction: {pred_label}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Emotion Detection", frame)

    # Stop after 5 seconds
    if time.time() - start_time > 5:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# --- Process Captured Emotions ---
if captured_predictions:
    dominant_emotion = max(set(captured_predictions), key=captured_predictions.count)
    print(f"\n✅ Dominant Emotion Detected: {dominant_emotion}")
else:
    dominant_emotion = "neutral"
    print("\n⚠️ No emotion detected, defaulting to neutral.")

# --- Spotify Recommendation ---
client_id = "112c1e4119734226aa7a46691dd18604"
client_secret = "6bf8845b9dea432181a2b11a5deae0a9"
redirect_uri = "http://127.0.0.1:8000/callback"

spotify_recommender = SpotifyEmotionPlaylistRecommender(client_id, client_secret, redirect_uri)
recommendation = spotify_recommender.recommend_spotify_playlist(dominant_emotion)

print(f"\n🎵 Recommended Playlist for {dominant_emotion.capitalize()} 🎵")
print(f"Playlist Name: {recommendation['name']}")
print(f"Description: {recommendation['description']}")

if recommendation['spotify_playlists']:
    print("\nSpotify Playlists:")
    for i, playlist in enumerate(recommendation['spotify_playlists'], 1):
        print(f"{i}. {playlist['name']} by {playlist['owner']}")
        print(f"   Tracks: {playlist['total_tracks']}")
        print(f"   URL: {playlist['external_url']}\n")
else:
    print("No Spotify playlists found for this emotion.")
