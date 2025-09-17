# 🎭 Emotion Detection & 🎵 Music Recommendation

## Project Overview

This project fuses Deep Learning, Computer Vision, and the Spotify API to deliver a real-time Emotion-to-Music Recommender System. It captures facial expressions from webcam, detects emotions using a trained neural network, and recommends Spotify playlists tailored to the user’s mood.

---

## 🚀 Features

- Real-time facial emotion recognition
- Multi-modal landmark processing: face + left hand + right hand
- Interactive video UI powered by Streamlit
- Emotion-based Spotify playlist recommendations
- Automatic fallback to neutral emotion

---

## ⚙️ Tech Stack

| Component           | Technology           |
|---------------------|---------------------|
| Deep Learning       | Keras, TensorFlow   |
| Computer Vision     | OpenCV, Mediapipe   |
| API Integration     | Spotify Web API     |
| Frontend            | Streamlit           |
| Programming Language| Python              |

---

## 🧠 Deep Learning Model

- **Input:** Normalized coordinates of face & hand landmarks
- **Output:** Predicted emotion (`happy`, `neutral`, `surprise`, `rock`, `angry`, `sad`)
- **Architecture:** Dense layers trained on a custom dataset
- **Model File:** `model.h5`

---

## 📺 Workflow

1. Capture real-time webcam frames via OpenCV
2. Extract face and hand landmarks using Mediapipe Holistic
3. Feed features to the trained DL model to classify emotion
4. Aggregate predictions over ~5 seconds to determine dominant emotion
5. Fetch Spotify playlists for the detected emotion
6. Display recommended playlists with clickable links in Streamlit

---

## 📝 Installation & Usage

### 1️⃣ Install Dependencies

```
pip install -r requirements.txt
```


### 2️⃣ Run the Streamlit App

```
streamlit run app.py
```


### 3️⃣ Interact

- Allow webcam access  
- The app captures your expressions for ~5 seconds  
- The dominant emotion is displayed  
- Recommended Spotify playlists for your mood are shown

---

## 📊 Example Output

Detected Emotion: Happy

Recommended Playlists:

1. appy Vibes (Spotify Official)

2. Bollywood Happy Hits

3. Global Pop Mix


---

## 📂 Project Files

| File             | Purpose                                  |
|------------------|------------------------------------------|
| app.py           | Streamlit main app (UI and workflow)     |
| model.h5         | Trained Deep Learning model              |
| music.py         | Spotify playlist recommender class       |
| requirements.txt | Dependencies                             |
| README.md        | Documentation                            |

---

## 💡 Future Improvements

- Add multi-language support for playlist search
- Integrate speech-based emotion detection
- Use transformers for (text + audio) emotion detection
- Deploy on Render or HuggingFace Spaces

---

## 📖 License

Released under MIT License.

---

## 🙏 Acknowledgements

- Mediapipe for landmark extraction
- Spotify Web API
- Streamlit for interactive UI
- TensorFlow and Keras for deep learning framework

