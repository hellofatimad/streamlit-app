import streamlit as st
from streamlit_extras.jupyterlite import jupyterlite
import time

def notebook():
    st.title("Laboratory 🧪")
    jupyterlite(900, 1000)
    
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()


if __name__ == "__main__":
    notebook()