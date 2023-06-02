import json
import requests
import streamlit as st
config = toml.load("config.toml")



def ask_api(
 lcserve_host: str,
 url: str,
 file: _TemporaryFileWrapper,
 question: str,
 claude_key: str,
) -> str:
 if not lcserve_host.startswith('http'):
 return '[ERROR]: Invalid API Host'

 if url.strip() == '' and file == None:
 return '[ERROR]: Both URL and PDF is empty. Provide atleast one.'

 if url.strip() != '' and file != None:
 return '[ERROR]: Both URL and PDF is provided. Please provide only one (eiter URL or PDF).'

 if question.strip() == '':
 return '[ERROR]: Question field is empty'

 _data = {
 'question': question,
 'envs': {
 'CLAUD_API_KEY': claude_key,
 },
 }

 if url.strip() != '':
 r = requests.post(
 f'{lcserve_host}/ask_url',
 json={'url': url, **_data},
 )

 else:
 with open(file.name, 'rb') as f:
 r = requests.post(
 f'{lcserve_host}/ask_file',
 params={'input_data': json.dumps(_data)},
 files={'file': f},
 )

 if r.status_code != 200:
 raise ValueError(f'[ERROR]: {r.text}')

 return r.json()['result']

title = 'PDF Claude'
description = """ PDF Claude allows you to chat with your PDF file using Universal Sentence Encoder and Claude. It gives hallucination free response than other tools as the embeddings are better than OpenAI. The returned response can even cite the page number in square brackets([]) where the information is located, adding credibility to the responses and helping to locate pertinent information quickly."""

st.title(title)
st.markdown(description)

lcserve_host = st.text_input(
 label='Enter your API Host here',
 value='http://localhost:8080',
)
st.markdown(
 f'<p style="text-align:center">Get your Claude API key <a href="https://console.anthropic.com/account/api-keys">here</a></p>', unsafe_allow_html=True
)
claude_key = config["claude"]["api_key"]
pdf_url = st.text_input(label='Enter PDF URL here')
st.markdown("<center><h4>OR<h4></center>", unsafe_allow_html=True)
file = st.file_uploader(
 label='Upload your PDF/ Research Paper / Book here', type=['pdf']
)
question = st.text_input(label='Enter your question here')
btn = st.button(value='Submit')

if btn:
 answer = ask_api(lcserve_host, pdf_url, file, question, claude_key)
 st.text_area(label='The answer to your question is :', value=answer)
