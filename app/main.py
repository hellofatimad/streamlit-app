import streamlit as st
from login import add_user, authenticate_user, login_user
from breast_cancer import show_bc
from patient_experience import pt_exp
from form import display_dashboard
from laboratory import notebook
from settings import show_settings
from home import checklist

st.set_page_config(
        layout = "wide",
        initial_sidebar_state= "expanded"
    )

def login_menu():
    menu = st.sidebar.selectbox('Menu', ['Login', 'Register'])
    if menu == 'Register':
        st.subheader('Register')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        
        if st.button('Register'):
            add_user(username, password)

    elif menu == 'Login':
        
        st.subheader('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        
        if st.button('Login'):
            if authenticate_user(username, password):
                login_user(username, password)
                st.rerun() 
            else:
                st.error('Invalid username or password')

def app():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None

    if not st.session_state.logged_in:
        login_menu()
    else:
        # Display navigation menu if logged in
        menu = st.sidebar.selectbox('Menu', ['Checklist','Breast Cancer', 'Patient Experience', 'Playground', 'Laboratory', 'Settings'])
        if menu == 'Checklist':
            checklist()
        if menu == 'Breast Cancer':
            show_bc()
        if menu == 'Patient Experience':
            pt_exp()
        if menu == 'Playground':
            display_dashboard()
        if menu == 'Laboratory':
            notebook()
        if menu == 'Settings':
            show_settings()

    

if __name__ == "__main__":
    app()