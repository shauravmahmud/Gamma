import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Function to fetch and parse HTML content from a URL
def fetch_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Function to extract all links from HTML content
def extract_links(soup):
    links = soup.find_all('a', href=True)
    return links

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
            st.subheader("Parsed HTML Content")
            st.code(soup.prettify(), language='html')
            
            # Extract all links from the HTML content
            links = extract_links(soup)
            
            # Display the links
            st.subheader("Links")
            if links:
                for link in links:
                    st.markdown(f"- [{link.text.strip()}]({link['href']})")
            else:
                st.write("No links found in the HTML content.")
            
            # Display the HTML content in a new tab
            st.subheader("HTML Content")
            html_content = str(soup)
            st.code(html_content, language='html')
            
        except Exception as e:
            st.error(f"Error loading URL: {e}")
    else:
        st.warning("Please enter a URL")
