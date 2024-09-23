import snowflake.connector
#import streamlit_authenticator as stauth
import streamlit as st
import bcrypt


# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = None

conn = st.connection("snowflake")

def add_user(username, password):
   
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO USERDB (username, password) VALUES (?, ?)",
                         (username, password))
            conn._instance.commit()
            st.success('User registered successfully! Please head to the login menu option')
    except Exception as e:
        st.error(f"An error occurred: {e}")

def authenticate_user(username, password):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT password FROM USERDB WHERE username = ?
            """, (username,))
            result = cur.fetchone()
            if result:
                stored = result[0]
                if stored == password:
                    return True
                
            return False
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False
    
def login_user(username, password):
    if authenticate_user(username, password):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success('Login successful!')
        return True
    else:
        st.error('Invalid username or password')
        return False

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.success('Logged out successfully!')


# Streamlit app code
#st.title('User Authentication with Snowflake')




#login_menu()



