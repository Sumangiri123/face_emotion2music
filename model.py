# model.py

import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model

# Load trained model and labels
model = load_model("model.h5")
# Corrected labels (order must match the original model's training order)
labels = ["happy", "neutral", "surprise", "rock", "angry", "sad"]


# Mediapipe setup
holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

print("🎥 Starting camera... Press 'q' to quit.")

while True:
    lst = []

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    res = holis.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if res.face_landmarks:
        # Collect face landmark relative positions
        for i in res.face_landmarks.landmark:
            lst.append(i.x - res.face_landmarks.landmark[1].x)
            lst.append(i.y - res.face_landmarks.landmark[1].y)

        # Left hand
        if res.left_hand_landmarks:
            for i in res.left_hand_landmarks.landmark:
                lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
        else:
            lst.extend([0.0] * 42)

        # Right hand
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

        # Display prediction
        cv2.putText(frame, f"Prediction: {pred_label}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Draw landmarks
    # drawing.draw_landmarks(frame, res.face_landmarks, holistic.FACEMESH_CONTOURS)
    # drawing.draw_landmarks(frame, res.left_hand_landmarks, hands.HAND_CONNECTIONS)
    # drawing.draw_landmarks(frame, res.right_hand_landmarks, hands.HAND_CONNECTIONS)

    # Show window
    cv2.imshow("Emotion Detection", frame)

    # Quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
