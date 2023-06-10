# MADARCHOD BANAYA HAI

import streamlit as st
import requests
import json
import fitz
import base64
import os
from PIL import Image
from streamlit_chat import message
from dotenv import load_dotenv

with st.sidebar:    
    st.write("Follow me on Instagram [@adarsh.py](https://www.instagram.com/adarsh.py/)!")
    st.warning("This app is still in development. Please report any bugs or issues.")

conversation_history = ""
load_dotenv()
api_key = os.getenv('API_KEY')
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
        conversation_history += f'\n\n{response_json["completion"]}'

        # Return the entire conversation history
        return conversation_history
    else:
        return f'Error: {response.status_code}'
    
# Create the app interface
#st.title("Murph")
col1,col2=st.columns([1,6])
with col1:
    st.image("logo.png")
with col2:
    st.markdown("<h1 style = 'margin-bottom:-5%;'>Mur<span style= 'color:  #7327d6;'>ph</span>📄</h1>", unsafe_allow_html=True)
    st.markdown("<p style = 'padding-bottom: 10%'>~LOL</p>",unsafe_allow_html=True)
with st.sidebar:
    st.title("Bhagwaan Bharose :sunglasses:") 
    st.sidebar.image("logo.png", use_column_width=True)

try:
    uploaded_file = st.file_uploader("Choose a file", type=['pdf'])
    if uploaded_file is not None:
        text = '' # initialize text buffer
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc: # open the pdf document
            for page in doc: # iterate through the pages
                text += page.get_text() # append the text of each page to the buffer


    with open('output.txt', 'w', encoding='utf-8') as f: # open a file for writing
        f.write(text)
    # initialize text 
except:
    pass

box = st.container()
box.title("Chat Box")

user_question1 = box.text_input(label="Enter your question here")
if box.button("Chat"):
    message(user_question1, is_user=True)
    response = chat_with_ai(text + user_question1, api_key, model)
    message(response, is_user=False)
