# pages/6_Show_Credentials.py
import streamlit as st
import pandas as pd
from config import EXCEL_FILE

# Set page config
st.set_page_config(page_title="User Credentials", page_icon="📊")

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please login first!")
    st.stop()

# Page title
st.title("User Credentials")
st.write("Here are all registered users:")

try:
    # Read the Excel file
    df = pd.read_excel(EXCEL_FILE)
    
    # Display total number of users
    st.write(f"Total number of registered users: {len(df)}")
    
    # Add a search box
    search = st.text_input("Search by username:")
    if search:
        df = df[df['username'].str.contains(search, case=False)]
    
    # Display the dataframe with styling
    st.dataframe(
        df,
        column_config={
            "username": "Username",
            "password": "Password"
        },
        hide_index=True,
        width=800
    )

except Exception as e:
    st.error(f"Error reading credentials file: {str(e)}")