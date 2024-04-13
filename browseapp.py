import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Function to fetch and parse HTML content from a URL using a proxy
def fetch_url_with_proxy(url, proxy):
    proxies = {"http": proxy, "https": proxy}
    response = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Streamlit app layout
st.title("Gamma Web Browser")

# Input field for entering URL
url = st.text_input("Enter URL")

# Input field for entering proxy server (if required)
proxy = st.text_input("Enter Proxy Server (Optional)")

if st.button("Load"):
    if url:
        # Check if the URL includes a scheme (e.g., http:// or https://)
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            # If no scheme is provided, prepend https://
            url = "https://" + url

        try:
            # Fetch and parse HTML content from the entered URL
            if proxy:
                soup = fetch_url_with_proxy(url, proxy)
            else:
                soup = fetch_url(url)
            
            # Display the parsed HTML content
            st.write(soup.prettify())
            
            # Display the HTML content in a new tab
            html_content = str(soup)
            st.components.v1.html(
                html_content,
                width=1000, height=600, scrolling=True
            )
            
        except Exception as e:
            st.error(f"Error loading URL: {e}")
    else:
        st.warning("Please enter a URL")
