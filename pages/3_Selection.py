import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Select Chat Type", page_icon="🤖")

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please login first!")
    st.stop()

st.title("Select Chat Type")

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

col1, col2 = st.columns(2)

with col1:
    if st.button("ChatBot", use_container_width=True):
        nav_page("Chatbot")

with col2:
    if st.button("RAG Chatbot", use_container_width=True):
        nav_page("RAG")

st.markdown("---")
st.write("Choose your preferred chat interface:")
st.write("- **ChatBot**: General conversation using OpenAI")
st.write("- **RAG**: Chat with your documents using AI")