import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

# Function to fetch and parse HTML content from a URL
def fetch_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Function to save HTML content to a file
def save_html_content(html_content, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)

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
            
            # Save the HTML content to a file
            html_content = str(soup)
            filename = "webpage_content.html"
            save_html_content(html_content, filename)
            
            # Provide a link to the user to access the saved HTML file
            st.markdown(f"[Download Webpage Content]({filename})")
            
        except Exception as e:
            st.error(f"Error loading URL: {e}")
    else:
        st.warning("Please enter a URL")
