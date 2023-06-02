# MADARCHOD BANAYA HAI

import streamlit as st
import requests
import json
import fitz
import base64
import os
from PIL import Image


conversation_history = ""
api_key = "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"
model = "claude-v1.3-100k"
# chat ke liye function
@st.cache_data # Cache the API call
def chat_with_ai(user_question, api_key, model):
    global conversation_history

    # claude ka endpoint url
    url = 'https://api.anthropic.com/v1/complete'

    # API request ke liye headers
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key,
    }

    # request ke params
    params = {
        'prompt': f'{conversation_history}\n\nHuman: {user_question}\n\nAssistant:',
        'model': model,
        'max_tokens_to_sample': 4000,
        'stop_sequences': ['\n\nHuman:'],
        'temperature': 0.8,
        'top_p': -1,
        'metadata': {}
    }

    # param dict ko json karke
    params_json = json.dumps(params)

    # request bhejna
    response = requests.post(url, headers=headers, data=params_json)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_json = response.json()
        conversation_history += f'\n\nHuman: {user_question1}\n\nAssistant: {response_json["completion"]}'

        # Return the entire conversation history
        return conversation_history
    else:
        return f'Error: {response.status_code}'

# Create the app interface
st.title("PB & J")
with st.sidebar:
    st.title("Bhagwaan Bharose")	
    st.header('Bhagwaan Bharose nhi! PB & J Bharose! :sunglasses:')
    st.sidebar.image("logo.jpg", use_column_width=True)
uploaded_file = st.file_uploader("Choose a file", type=['pdf']) 


user_question1 = st.text_input(label="Enter your question here")
if st.button("Chat"):
    st.write(chat_with_ai(text+user_question1, api_key, model))