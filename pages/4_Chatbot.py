import streamlit as st
import openai

st.set_page_config(page_title="ChatBot", page_icon="🤖")
st.title("ChatBot")

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please login first!")
    st.stop()

# Initialize OpenAI key
if 'OPENAI_API_KEY' not in st.session_state:
    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    if api_key:
        st.session_state['OPENAI_API_KEY'] = api_key
        openai.api_key = api_key

if 'OPENAI_API_KEY' in st.session_state:
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What's your question?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate OpenAI response
        with st.chat_message("assistant"):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            response_text = response.choices[0].message.content
            st.markdown(response_text)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_text})