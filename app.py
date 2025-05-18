from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import random
import re
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)
CORS(app)

model = load_model('chatbot_response.keras', compile=False)

with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

MAX_LEN = 100

fallbacks = [
    "I'm here for you. Please tell me more.",
    "That sounds really tough. Want to share more about it?",
    "You're not alone. Would you like to talk more?",
    "I’m listening. Go on when you're ready."
]

def preprocess_sentence(sentence):
    sentence = sentence.lower().strip()
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    sentence = re.sub(r"[^a-zA-Z?.!,]+", " ", sentence)
    sentence = sentence.replace("Customer :", "").replace("Agent :", "")
    sentence = re.sub(r"\s+", " ", sentence).strip()
    return sentence

def postprocess_response(response):
    response = response.replace("i ", "I ")
    response = response.replace("i'm", "I'm").replace("i m", "I'm")
    response = re.sub(r"\s([?.!,])", r"\1", response)
    return response.capitalize()

def decode_sequence(input_text, tokenizer, model, max_len=MAX_LEN):
    input_text = preprocess_sentence(input_text)
    input_seq = tokenizer.texts_to_sequences([f"<start> {input_text} <end>"])
    input_seq = pad_sequences(input_seq, maxlen=max_len, padding='post')

    decoder_input = tokenizer.texts_to_sequences(["<start>"])[0]
    decoder_input = tf.expand_dims(decoder_input, 0)

    result = []

    for _ in range(max_len):
        predictions = model.predict([input_seq, decoder_input], verbose=0)
        predicted_id = tf.argmax(predictions[0, -1, :]).numpy()
        predicted_word = tokenizer.index_word.get(predicted_id)

        if predicted_word == "<end>" or predicted_word is None:
            break

        result.append(predicted_word)
        decoder_input = tf.concat([decoder_input, [[predicted_id]]], axis=-1)

    if not result:
        return random.choice(fallbacks)

    response = postprocess_response(' '.join(result))
    return response

# ✅ Route to render the chatbot interface
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    response = decode_sequence(user_message, tokenizer, model)
    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
