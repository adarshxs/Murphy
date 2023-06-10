
import streamlit as st
import requests
import json
import os
from gradio_client import Client
from streamlit_chat import message
from dotenv import load_dotenv

session_state = st.session_state

with st.sidebar:    
    st.write("Follow me on Instagram [@adarsh.py](https://www.instagram.com/adarsh.py/)!")
    st.warning("This app is still in development. Please report any bugs or issues.")
conversation_history = ""
load_dotenv()
api_key = os.getenv('API_KEY')
model = "claude-v1.3-100k"

@st.cache_data # Cache the API call
def chat_with_ai(user_question, api_key, model):
    global conversation_history

    # Instantiate the endpoint URL
    url = 'https://api.anthropic.com/v1/complete'

    # Define the headers for the HTTP request
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key,
    }

    # Define the parameters for the request
    params = {
        'prompt': f'{conversation_history}\n\nHuman: {user_question}\n\nAssistant:',
        'model': model,
        'max_tokens_to_sample': 4000,
        'stop_sequences': ['\n\nHuman:'],
        'temperature': 0.8,
        'top_p': -1,
        'metadata': {}
    }

    # Convert the params dict to a JSON string
    params_json = json.dumps(params)

    # Send the HTTP request to the API
    response = requests.post(url, headers=headers, data=params_json)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_json = response.json()
        conversation_history += f'\n\n{response_json["completion"]}'

        # Return the entire conversation history
        return conversation_history
    else:
        return f'Error: {response.status_code}'

#st.title("Murph") 
col1,col2=st.columns([1,6])
with col1:
    st.image("logo.png")
with col2:
    st.markdown("<h1 style = 'margin-bottom:-5%;'>Mur<span style= 'color:  #7327d6;'>ph</span>🎥</h1>", unsafe_allow_html=True)
    st.markdown("<p style = 'padding-bottom: 10%'>~LOL</p>",unsafe_allow_html=True)
with st.sidebar:
    st.title("Bhagwaan Bharose :sunglasses:") 
    st.sidebar.image("logo.png", use_column_width=True)

url = st.text_input(label="Enter a video link and wait for some time until the video preview loads!")
url = str(url)

API_URL = "https://sanchit-gandhi-whisper-jax.hf.space/"

client = Client(API_URL)

def transcribe_audio(audio_path, task="translate", return_timestamps=False):
    """Function to transcribe an audio file using the Whisper JAX endpoint."""
    text = client.predict(
        audio_path,
        task,
        return_timestamps,
        api_name="/predict_2",
    )
    return text

if url:
    if "transcription" not in session_state:
        session_state.transcription = transcribe_audio(url)

    if session_state.transcription:
        output_with_timestamps = session_state.transcription
        text = '' # Initialize text buffer
        for i in output_with_timestamps:
            text += i
    else:
        text = ''
    st.video(url)

box = st.container()
box.title("Chat Box")

user_question1 = box.text_input(label="Enter your question here")
if box.button("Chat"):
    message(user_question1, is_user=True)
    response = chat_with_ai(text + user_question1, api_key, model)
    message(response, is_user=False)




