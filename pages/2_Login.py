import streamlit as st
import pandas as pd
from config import EXCEL_FILE
import streamlit.components.v1 as components

st.set_page_config(page_title="Login", page_icon="🔐")
st.title("User Login")

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elapsed = new Date().getTime() - start_time;
                if (elapsed < timeout_secs * 1000) {
                    setTimeout(function() {
                        attempt_nav_page(page_name, start_time, timeout_secs);
                    }, 100);
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date().getTime(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    components.html(nav_script)

def verify_credentials(username, password):
    try:
        df = pd.read_excel(EXCEL_FILE)
        # Strip whitespace and convert to string
        df['username'] = df['username'].astype(str).str.strip()
        df['password'] = df['password'].astype(str).str.strip()
        
        # Clean input credentials
        username = str(username).strip()
        password = str(password).strip()
        
        # Get user row
        user_row = df[df['username'] == username]
        
        if user_row.empty:
            return False
            
        stored_password = user_row['password'].iloc[0]
        stored_username = user_row['username'].iloc[0]
        
        # Debug prints
        print(f"Input username: '{username}', stored username: '{stored_username}'")
        print(f"Input password: '{password}', stored password: '{stored_password}'")
        print(f"Username match: {username == stored_username}")
        print(f"Password match: {password == stored_password}")
        
        # Simple equality check after cleaning
        return username == stored_username and password == stored_password
        
    except Exception as e:
        print(f"Error in verification: {str(e)}")
        return False

with st.form("login_form", clear_on_submit=True):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")
    
    if submit:
        if username and password:
            if verify_credentials(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Login successful! Redirecting to selection page...")
                nav_page("Selection")
            else:
                st.error("Invalid credentials!")
        else:
            st.error("Please fill all fields!")