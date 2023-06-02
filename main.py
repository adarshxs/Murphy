import streamlit as st
import requests
import json

# Define a global variable for the conversation history
conversation_history = ""
api_key = "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"
model = "claude-v1.3-100k"
# Define a function to chat with AI
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
        conversation_history += f'\n\nHuman: {user_question}\n\nAssistant: {response_json["completion"]}'

        # Return the entire conversation history
        return conversation_history
    else:
        return f'Error: {response.status_code}'

# Create the app interface
st.title("Chat with AI")
user_question = st.text_input("Enter your question")
if st.button("Chat"):
    st.write(chat_with_ai(user_question, api_key, model))
