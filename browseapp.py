import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time


# Function to hide the Streamlit main menu
def hide_streamlit_menu():
    """Hides the Streamlit main menu including the GitHub icon."""
    st.markdown("""<style>
        #MainMenu {visibility: hidden;}
    </style>""", unsafe_allow_html=True)

# Hide the Streamlit main menu
hide_streamlit_menu()


# Hide the GitHub icon and the "Fork this app" option
st.set_page_config(page_title="Gamma Web Browser", page_icon=None, layout='wide')

# Function to fetch and parse HTML content from a URL
def fetch_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Function to modify the href attributes of all links to connect to the source link
def modify_links(soup, url):
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    
    links = soup.find_all('a', href=True)
    for link in links:
        href = link.get('href')
        if href.startswith('#'):
            # Skip internal links
            continue
        if not href.startswith('http'):
            # If the href attribute does not start with http, it's a relative link, so prepend base_url
            href = base_url + href
        link['href'] = href
    return soup

# Streamlit app layout
st.title("Gamma Web Browser")

# Input field for entering URL
url = st.text_input("Enter URL")

# Placeholder for the message
placeholder = st.empty()

if st.button("Load"):
    if url:
        # Display the message about the short delay
        placeholder.text("There will be a short delay after clicking load.")
        time.sleep(0.5)  # Add a short delay
        
        # Check if the URL includes a scheme (e.g., http:// or https://)
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            # If no scheme is provided, prepend https://
            url = "https://" + url

        try:
            # Fetch and parse HTML content from the entered URL
            soup = fetch_url(url)
            
            # Modify the href attributes of links to connect to the source link
            soup = modify_links(soup, url)
            
            # Display the subheader for the HTML content
            st.subheader("Content Window")
            
            # Display the HTML content in a new tab
            html_content = str(soup)
            st.components.v1.html(
                html_content,
                width=1000, height=600, scrolling=True
            )
            
            # Display the clickable links below the HTML content
            st.subheader("Clickable Links:")
            for link in soup.find_all('a'):
                st.markdown(f"[{link.text.strip()}]({link['href']})", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error loading URL: {e}")
    else:
        st.warning("Please enter a URL")
