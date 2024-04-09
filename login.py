import hashlib
import streamlit as st

def hash_password(password):
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    users = st.secrets.get("users", {})
    hashed_input_password = hash_password(password)
    return users.get(username) == hashed_input_password

def authenticate_user():
    with st.form("login_form", clear_on_submit=True):  # Added clear_on_submit for better UX
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        # The check for form submission and authentication is done here to ensure it's processed in the same run
        if submit_button and username and password:
            if check_credentials(username, password):
                st.session_state['logged_in'] = True  # Update session state to reflect successful login
                st.experimental_rerun()  # Rerun the app to reflect the updated session state immediately
            else:
                st.error("Login failed. Please check your username and password.")
