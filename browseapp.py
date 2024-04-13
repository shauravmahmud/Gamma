import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Function to fetch and parse HTML content from a URL
def fetch_url(url, proxy=None):
    if proxy:
        proxies = {"http": proxy, "https": proxy}
        response = requests.get(url, proxies=proxies)
    else:
        response = requests.get(url)
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
            soup = fetch_url(url, proxy)
            
            # Display the webpage title
            title = soup.title.string if soup.title else "No Title Found"
            st.header(title)
            
            # Display specific HTML elements
            st.subheader("HTML Elements:")
            selected_tags = st.multiselect("Select HTML elements to display:", ["h1", "p", "a"])
            for tag in selected_tags:
                elements = soup.find_all(tag)
                if elements:
                    for element in elements:
                        st.write(element)
                else:
                    st.write(f"No <{tag}> found on the page.")
            
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
