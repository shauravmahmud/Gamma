import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import webbrowser
import tempfile

# Function to fetch and parse HTML content from a URL
@st.cache
def fetch_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup, response.content

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

            # Open HTML content in Browser (Interactive)
            if st.button("Open in Browser"):
                with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp_file:
                    tmp_file.write(html_content)
                    webbrowser.open_new_tab(tmp_file.name)

        except Exception as e:
            st.error(f"Error loading URL: {e}")
    else:
        st.warning("Please enter a URL")
