import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse


st.set_page_config(
    page_title="Gamma",
    page_icon="./image/Greek_lc_gamma.svg.png",
    layout="wide"
)

hide_st_style = """
      <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      header {visibility: hidden;}
      </style>
      """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Function to fetch and parse HTML content from a URL
def fetch_and_parse_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def modify_links(soup, url):
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    
    if not base_url.startswith('http'):
        # If base_url does not start with http, assume it's a relative link and add https:// as default
        base_url = "https://" + base_url
    
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
st.markdown("<h1 style='text-align: center;'>Gamma</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'> Pierce through anything</h3>", unsafe_allow_html=True)

# Input field for entering URL
url = st.text_input("Enter URL")

# Placeholder for the message
placeholder = st.empty()

if st.button("Load"):
    if url:
        # Display the message about the short delay
        placeholder.text("There will be a short delay after clicking load.")
      
        
        try:
            # Fetch and parse HTML content from the entered URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                # Prepend "https://" if no scheme is provided
                url = "https://" + url
            soup = fetch_and_parse_html(url)
            
            # Modify the href attributes of links to connect to the source link
            soup = modify_links(soup, url)
            
            # Display the subheader for the HTML content
            st.subheader("Content Window")
            
            # Display the HTML content in a new tab
            html_content = str(soup)
            st.components.v1.html(
                html_content,
                width=1100, height=600, scrolling=True
            )
            
            # Display the clickable links below the HTML content
            st.subheader("Clickable Links:")
            for link in soup.find_all('a'):
                st.markdown(f"[{link.text.strip()}]({link['href']})", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error loading URL: {e}")
    else:
        st.warning("Please enter a URL")
