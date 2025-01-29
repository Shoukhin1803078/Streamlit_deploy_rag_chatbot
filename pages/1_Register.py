import streamlit as st
import pandas as pd
from datetime import datetime
from config import EXCEL_FILE

st.set_page_config(page_title="Register", page_icon="📝")
st.title("User Registration")

def save_credentials(username, password):
    df = pd.read_excel(EXCEL_FILE)
    if username in df['username'].values:
        return False
    new_user = pd.DataFrame({'username': [username], 'password': [password]})
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)
    return True

with st.form("register_form", clear_on_submit=True):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Register")
    
    if submit:
        if username and password:
            if save_credentials(username, password):
                st.success("Registration successful! Please proceed to login.")
            else:
                st.error("Username already exists!")
        else:
            st.error("Please fill all fields!")