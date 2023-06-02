import os
import re
import shutil
import urllib.request
from pathlib import Path
from tempfile import NamedTemporaryFile

import fitz
import numpy as np
import claude
import tensorflow_hub as hub
from fastapi import UploadFile
from lcserve import serving
from sklearn.neighbors import NearestNeighbors
import toml

# Load the config file
config = toml.load("config.toml")


claude_key = config["claude"]["api_key"]


recommender = None


def download_pdf(url, output_path):
    urllib.request.urlretrieve(url, output_path)


def preprocess(text):
    text = text.replace('\n', ' ')
    text = re.sub('\s+', ' ', text)
    return text


def pdf_to_text(path, start_page=1, end_page=None):
    doc = fitz.open(path)
    total_pages = doc.page_count

    if end_page is None:
        end_page = total_pages

    text_list = (preprocess(doc.load_page(i).get_text("text")) for i in range(start_page - 1, end_page))
    doc.close()
    return text_list


def text_to_chunks(texts, word_length=150, start_page=1):
    chunks = []
    for idx, text in enumerate(texts, start=start_page):
        words = text.split()
        for i in range(0, len(words), word_length):
            chunk = ' '.join(words[i: i + word_length]).strip()
            if i + word_length > len(words) and idx < len(texts):
                texts[idx] = chunk + ' ' + ' '.join(texts[idx].split()[word_length:])
                break
            chunk = f'[Page no. {idx}] "{chunk}"'
            chunks.append(chunk)
    return chunks


class SemanticSearch:
    def __init__(self):
        self.use = hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')
        self.fitted = False

    def fit(self, data, batch=1000, n_neighbors=5):
        self.data = data
        self.embeddings = self.get_text_embedding(data, batch=batch)
        n_neighbors = min(n_neighbors, len(self.embeddings))
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        self.nn.fit(self.embeddings)
        self.fitted = True

    def __call__(self, text, return_data=True):
        inp_emb = self.use([text])
        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]

        if return_data:
            return [self.data[i] for i in neighbors]
        else:
            return neighbors

    def get_text_embedding(self, texts, batch=1000):
        embeddings = []
        for i in range(0, len(texts), batch):
            text_batch = texts[i : (i + batch)]
            emb_batch = self.use(text_batch)
            embeddings.append(emb_batch)
        embeddings = np.vstack(embeddings)
        return embeddings


def load_recommender(path, start_page=1):
    global recommender
    if recommender is None:
        recommender = SemanticSearch()

    texts = pdf_to_text(path, start_page=start_page)
    chunks = text_to_chunks(texts, start_page=start_page)
    recommender.fit(chunks)
    return 'Corpus Loaded.'




def create_text(prompt, engine="text-claude-001"):
    # Use the global variable claude_key
    global claude_key
    # Set the API key
    claude.api_key = claude_key
    # Create the text response
    responses = claude.Text.create(
        engine=engine,
        prompt=prompt,
        max_tokens=512,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = responses.data[0].text
    return message


def create_answer(question):
    # Use the global variable claude_key
    global claude_key
    # Get the top chunks from the recommender function
    topn_chunks = recommender(question)
    # Initialize the prompt string
    prompt = ""
    prompt += 'search results:\n\n'
    # Add each chunk to the prompt string
    for c in topn_chunks:
        prompt += c + '\n\n'

    prompt += (
        "Instructions: Compose a comprehensive reply to the query using the search results given. "
        "Cite each reference using [ Page Number] notation (every result has this number at the beginning). "
        "Citation should be done at the end of each sentence. If the search results mention multiple subjects "
        "with the same name, create separate answers for each. Only include information found in the results and "
        "don't add any additional information. Make sure the answer is correct and don't output false content. "
        "If the text does not relate to the query, simply state 'Text Not Found in PDF'. Ignore outlier "
        "search results which has nothing to do with the question. Only answer what is asked. The "
        "answer should be short and concise. Answer step-by-step. \n\nQuery: {question}\nAnswer: "
    )

    # Add the question to the prompt string
    prompt += f"Query: {question}\nAnswer:"
    # Create the answer using the create_text function
    answer = create_text(prompt, "text-claude-001")
    return answer


def load_claude_key() -> str:
    # Check if the key is valid
    if claude_key is None or not claude_key.startswith("sk-"):
        raise ValueError(
            "[ERROR]: Please pass a valid CLAUDE_API_KEY. Get your key here : https://console.anthropic.com/account/api-keys"
        )
    return claude_key


@serving
def ask_url(url: str, question: str):
    download_pdf(url, 'corpus.pdf')
    load_recommender('corpus.pdf')
    claude_key = load_claude_key()
    return create_answer(question, claude_key)


@serving
async def ask_file(file: UploadFile, question: str) -> str:
    suffix = Path(file.filename).suffix
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    load_recommender(str(tmp_path))
    claude_key = load_claude_key()
    return create_answer(question, claude_key)


