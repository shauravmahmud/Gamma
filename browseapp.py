import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import webbrowser

# Function to fetch and parse HTML content from a URL
def fetch_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Streamlit app layout
st.title("Gamma Web Browser")

# Input field for entering URL
url = st.text_input("Enter URL")

# Checkbox to choose display option
display_in_browser = st.checkbox("Display in Browser")

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
            
            # Check if the user selected to display in the browser
            if display_in_browser:
                # Open the web page in the default browser
                webbrowser.open(url)
            
        except Exception as e:
            st.error(f"Error loading URL: {e}")
    else:
        st.warning("Please enter a URL")
