import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import webbrowser
import os

# Function to fetch and parse HTML content from a URL
@st.cache
def fetch_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup, response.content

# Function to save HTML content to a file
def save_html_to_file(html_content, filename):
    # Decode the bytes content to a string
    html_string = html_content.decode('utf-8')
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_string)

# Streamlit app layout
st.title("Simple Web Browser")

# Input field for entering URL
url = st.text_input("Enter URL")

if st.button("Load"):
    if url:
        # Check if the URL includes a scheme
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            # If no scheme is provided, prepend https://
            url = "https://" + url

        try:
            # Fetch and parse HTML content
            soup, html_content = fetch_url(url)

            # Display Parsed HTML (Text-Based View)
            st.write(f"Here's the parsed HTML content of {url}:")
            st.code(soup.prettify())

            # Save HTML content to a temporary file
            temp_file_path = "temp.html"
            save_html_to_file(html_content, temp_file_path)

            # Open HTML file in Browser (Interactive)
            if st.button("Open in Browser"):
                # Open the HTML file in browser
                with open(temp_file_path, "r", encoding="utf-8") as file:
                    html_code = file.read()
                    st.components.v1.html(html_code, height=600)

        except Exception as e:
            st.error(f"Error loading URL: {e}")
    else:
        st.warning("Please enter a URL")
