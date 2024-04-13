import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import urlparse

# Streamlit app layout
st.title("Simple Web Browser")

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
            # Embed the web page using an iframe
            st.write(f"Here's the web page at {url}:")
            st.components.v1.iframe(url, height=600, scrolling=True)

        except Exception as e:
            st.error(f"Error loading URL: {e}")
    else:
        st.warning("Please enter a URL")
