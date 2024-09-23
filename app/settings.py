# In settings.py or wherever the show_settings function is defined
import streamlit as st
from login import logout  # Import the logout function

def show_settings():
    st.title("Settings")

    # Other settings options...

    # Add a logout button
    if st.button('Logout'):
        logout()
        st.rerun()  # Refresh the app to show the login screen
