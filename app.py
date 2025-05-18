from flask import Flask, request, jsonify  # Import Flask for web framework, request for handling client requests, jsonify for returning JSON responses
from flask_cors import CORS  # Import CORS for handling Cross-Origin Resource Sharing to enable communication between frontend and backend
import pickle  # For loading the saved tokenizer from a pickle file
import random  # For selecting random fallback responses
import re  # For using regular expressions to preprocess the text
import tensorflow as tf  # For working with TensorFlow to load and use the trained model
from tensorflow.keras.models import load_model  # Import Keras model loading function
from tensorflow.keras.preprocessing.sequence import pad_sequences  # For padding sequences to a fixed length

# إعداد Flask
app = Flask(__name__)  # Creates an instance of the Flask application
CORS(app)  # Enables Cross-Origin Resource Sharing to allow the frontend to connect to this backend

# تحميل الموديل والتوكنيزر
model = load_model('chatbot_response.keras', compile=False)  # Loads the pre-trained model (chatbot) from the saved file

with open('tokenizer.pkl', 'rb') as f:  # Loads the tokenizer from the saved pickle file
    tokenizer = pickle.load(f)

# ثابتات
MAX_LEN = 100  # Maximum length for padding the input sequences to ensure consistent input size for the model

# ردود احتياطية
fallbacks = [  # List of fallback responses in case the model fails to generate a proper reply
    "I'm here for you. Please tell me more.",
    "That sounds really tough. Want to share more about it?",
    "You're not alone. Would you like to talk more?",
    "I’m listening. Go on when you're ready."
]

# دوال الموديل
def preprocess_sentence(sentence):  # Function to clean and preprocess the input sentence
    sentence = sentence.lower().strip()  # Convert to lowercase and strip any extra spaces
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)  # Add spaces around punctuation
    sentence = re.sub(r"[^a-zA-Z?.!,]+", " ", sentence)  # Remove non-alphabetic characters
    sentence = sentence.replace("Customer :", "").replace("Agent :", "")  # Remove speaker labels
    sentence = re.sub(r"\s+", " ", sentence).strip()  # Remove extra spaces between words
    return sentence

def postprocess_response(response):  # Function to format and clean the model's output
    response = response.replace("i ", "I ")  # Capitalize "i" to "I"
    response = response.replace("i'm", "I'm").replace("i m", "I'm")  # Fix lowercase "i" to "I'm"
    response = re.sub(r"\s([?.!,])", r"\1", response)  # Remove extra spaces before punctuation
    return response.capitalize()  # Capitalize the first letter of the response

def decode_sequence(input_text, tokenizer, model, max_len=MAX_LEN):  # Function to generate the bot's reply using the model
    input_text = preprocess_sentence(input_text)  # Preprocess the user input sentence
    input_seq = tokenizer.texts_to_sequences([f"<start> {input_text} <end>"])  # Tokenize the input with start and end tokens
    input_seq = pad_sequences(input_seq, maxlen=max_len, padding='post')  # Pad the sequence to the fixed length

    decoder_input = tokenizer.texts_to_sequences(["<start>"])[0]  # Get the start token for the decoder
    decoder_input = tf.expand_dims(decoder_input, 0)  # Expand dimensions to match the model's input shape

    result = []  # Initialize an empty list to store the generated words

    for _ in range(max_len):  # Loop through the maximum sequence length
        predictions = model.predict([input_seq, decoder_input], verbose=0)  # Get predictions from the model
        predicted_id = tf.argmax(predictions[0, -1, :]).numpy()  # Get the most probable word ID
        predicted_word = tokenizer.index_word.get(predicted_id)  # Get the word from the token ID

        if predicted_word == "<end>" or predicted_word is None:  # Stop when the end token is generated
            break

        result.append(predicted_word)  # Append the predicted word to the result
        decoder_input = tf.concat([decoder_input, [[predicted_id]]], axis=-1)  # Update the decoder input with the predicted word

    if not result:  # If no result is generated, return a fallback response
        return random.choice(fallbacks)

    response = postprocess_response(' '.join(result))  # Join the result words and process the response
    return response

# API endpoint
@app.route('/chat', methods=['POST'])  # Define the route for the chat API with POST method
def chat_api():
    data = request.get_json()  # Get the JSON data from the request
    user_message = data.get('message', '')  # Extract the user's message from the request data

    if not user_message:  # If no message is provided, return an error
        return jsonify({'error': 'No message provided'}), 400

    response = decode_sequence(user_message, tokenizer, model)  # Get the bot's response using the model
    return jsonify({'reply': response})  # Return the response in JSON format

if __name__ == '__main__':  # If this script is run directly, start the Flask app
    app.run(host='0.0.0.0', port=5000)  # Run the Flask app on all network interfaces (0.0.0.0) on port 5000
