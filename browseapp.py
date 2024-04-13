import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Function to fetch and parse HTML content from a URL
def fetch_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Streamlit app layout
st.title("Gamma Web Browser")

# Input field for entering URL
url = st.text_input("Enter URL")

if st.button("Load"):
    if url:
        # Check if the URL includes a scheme (e.g., http:// or https://)
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            # If no scheme is provided, prepend https://
            url = "https://" + url

        try:
            # Fetch and parse HTML content from the entered URL
            soup = fetch_url(url)
            
            # Display the parsed HTML content
            st.write(soup.prettify())
            
            # Embed the web page using an iframe
            st.write(
                f'<iframe src="{url}" width="100%" height="600px" scrolling="yes"></iframe>',
                unsafe_allow_html=True,
            )
            
            # Add a link to open the URL in a new tab
            st.markdown(f"[Open in new tab]({url})", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error loading URL: {e}")
    else:
        st.warning("Please enter a URL")
