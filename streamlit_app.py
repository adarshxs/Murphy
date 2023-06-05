import streamlit as st
from streamlit_chat import message


st.set_page_config(page_title="Murph", page_icon="logo.png")
col1,col2=st.columns([1,6])
with col1:
    st.image("logo.png")
with col2:
    st.markdown("<h1 style = 'margin-bottom:-5%;'>Mur<span style= 'color:  #7327d6;'>ph</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style = 'padding-bottom: 10%'>~LOL</p>",unsafe_allow_html=True)

st.write("Ever had long complicated documents, complicated and boring YouTube videos that you have to go through? Well, we have a solution for you. Murph is a tool that helps you talk to you documents, videos, and even E-Commerce products, all at one place!")
st.write("![Your Awsome GIF](https://media.giphy.com/media/3ohzdIuqJoo8QdKlnW/giphy.gif)")
         

def PDF():
    st.write("PDF SHIT")

def VIDEO():
    st.write("VIDEO SHIT")

def LINKS():
    st.write("LINKS SHIT")

st.markdown("""
<style>
    /* Reset some default browser styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* Apply a nice background color and font styles */
body {
  background-color: #f8f8f8;
  font-family: Arial, sans-serif;
  color: #333;
}

/* Center the content horizontally */
.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 20px;
}

/* Add a nice heading style */
h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

/* Style links */
a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

/* Add a subtle box shadow to elements on hover */
button,
a,
input[type="submit"] {
  transition: box-shadow 0.3s ease;
}

button:hover,
a:hover,
input[type="submit"]:hover {
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* Style buttons */
button,
input[type="submit"] {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* Add spacing between elements */
.space-bottom {
  margin-bottom: 20px;
}

.space-top {
  margin-top: 20px;
}

/* Create a responsive layout for smaller screens */
@media (max-width: 768px) {
  .container {
    padding: 10px;
  }
}

/* Add some CSS designs */

/* Create a beautiful card design */
.card {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

/* Style form inputs */
input[type="text"],
input[type="email"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f8f8f8;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus,
input[type="email"]:focus,
textarea:focus {
  border-color: #007bff;
}

/* Add a beautiful image hover effect */
.image-container {
  position: relative;
  display: inline-block;
  overflow: hidden;
}

.image-container img {
  transition: transform 0.3s ease;
}

.image-container:hover img {
  transform: scale(1.1);
}

.image-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-container:hover::before {
  opacity: 1;
}

.image-container span {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  font-size: 20px;
  font-weight: bold;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-container:hover span {
  opacity: 1;
}

</style>
""", unsafe_allow_html=True)
