
# MentAssist-Chatbot

An AI-powered chatbot for mental health support using NLP and a custom-trained deep learning model.

---

## 🧠 Project Overview

MentAssist is a web-based chatbot designed to support users emotionally through text-based conversations. It uses a trained seq2seq model (with TensorFlow) and a tokenizer to generate responses based on user input.

---

## 🚀 Features

- Natural language understanding using a custom-trained model
- Real-time chatbot interface (HTML + JS + Flask backend)
- Background video animation with a modern UI
- Fallback replies for unknown inputs
- Fully responsive design

---

## 🛠️ Technologies Used

- Python (Flask, TensorFlow, Keras)
- JavaScript (Fetch API)
- HTML5, CSS3, Bootstrap
- Git LFS for managing large model files
- Trained model (`chatbot_response.keras`)
- Pre-trained tokenizer (`tokenizer.pkl`)

---

## 📁 Project Structure

```
MentAssist-Chatbot/
├── app.py
├── requirements.txt
├── chatbot_response.keras
├── tokenizer.pkl
├── emotion-emotion_69k.csv
├── test_request.py
├── templates/
│   └── index.html
├── static/
│   ├── js/
│   │   └── main.js
│   ├── CSS/
│   │   └── style.css
│   └── video/
│       └── Floating-Island.mp4
```

---

## ▶️ Getting Started

### 1. Clone the repository:

```bash
git clone https://github.com/mohab-yasser/MentAssist-Chatbot.git
cd MentAssist-Chatbot
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

> Make sure you have Git LFS installed to download the `.keras` model file properly.

### 3. Run the backend:

```bash
python app.py
```

This will launch the Flask server at `http://localhost:5000`

---

## 💬 Testing the API

You can use `test_request.py` to test the backend manually:

```bash
python test_request.py
```

Or test it via Postman:

- POST to: `http://localhost:5000/chat`
- Body (JSON): `{ "message": "your message" }`

---

## 📸 Screenshot (optional)

_Add a screenshot here showing the chatbot interface in action._

---

## 📌 Notes

- The model and tokenizer were pre-trained and saved in the repo.
- This project is meant for educational and prototyping purposes only.

---
