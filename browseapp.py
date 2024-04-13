import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Function to fetch and parse HTML content from a URL
def fetch_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Function to make links clickable in HTML content
def make_links_clickable(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for a_tag in soup.find_all('a', href=True):
        a_tag['target'] = '_blank'
    return str(soup)

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
            
            # Display the HTML content in a new tab
            html_content = str(soup)
            clickable_html_content = make_links_clickable(html_content)
            st.components.v1.html(
                clickable_html_content,
                width=1000, height=600, scrolling=True
            )
            
        except Exception as e:
            st.error(f"Error loading URL: {e}")
    else:
        st.warning("Please enter a URL")
