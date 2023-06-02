import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_chat import message
import langchain

st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

st.sidebar.title("Media Chat")
st.title("Media Chat")
st.write("Welcome to Media Chat! This is a place where you can chat with other people about your favorite media. You can also see what other people are saying about your favorite media. To get started, select a media from the sidebar.")


# A chatbot that uses streamlit for the UI. takes in a pdf from upload or a link and then passes the contents to langchain to get the summary. Users cna then chat with the chatbot about the contents in the pdf.

