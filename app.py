import streamlit as st
import pandas as pd
import os
from datetime import datetime
from openpyxl import load_workbook

# Set page configuration
st.set_page_config(
    page_title="User Registration",
    page_icon="📝",
    layout="centered"
)

# Initialize session state for form_submit
if 'form_submit' not in st.session_state:
    st.session_state.form_submit = False

# Add a title and description
st.title("User Registration")
st.write("Please enter your username and password to register.")

def save_to_excel(username, password):
    """
    Save user credentials to an Excel file
    """
    # Create data dictionary
    data = {
        'username': [username],
        'password': [password],
        'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Check if file exists
    file_path = 'user_credentials.xlsx'
    if os.path.exists(file_path):
        # Load existing Excel file
        existing_df = pd.read_excel(file_path)
        # Concatenate with new data
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        # Save updated DataFrame
        updated_df.to_excel(file_path, index=False)
    else:
        # Create new Excel file
        df.to_excel(file_path, index=False)
    
    return True

def clear_form():
    st.session_state.form_submit = True

# Create form
with st.form("registration_form", clear_on_submit=True):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Register", on_click=clear_form)

    if submit:
        if username and password:
            # Save the credentials
            if save_to_excel(username, password):
                st.success("Registration successful! Your information has been saved.")
        else:
            st.error("Please fill in both username and password fields.")

# Add a footer
st.markdown("---")
st.markdown("©️ 2025 User Registration App")