# pages/5_RAG.py
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import tempfile
import os

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please login first!")
    st.stop()

def process_document(file_path):
    """Process document and create RAG chain"""
    try:
        # Load and split document
        loader = PyPDFLoader(file_path)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = text_splitter.split_documents(loader.load())
        
        # Create vectorstore
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(docs, embeddings)
        
        # Create QA chain
        prompt_template = """Answer the question based only on the following context:
        {context}
        
        Question: {question}
        Answer: """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(temperature=0),
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": prompt}
        )
        
        return chain, vectorstore.as_retriever(), prompt
        
    except Exception as e:
        st.error(f"Error processing document: {str(e)}")
        return None, None, None

def main():
    st.title("RAG Chatbot")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chain" not in st.session_state:
        st.session_state.chain = None
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # File upload
        uploaded_file = st.file_uploader("Upload Document", type=['pdf'])
        
        # API Keys
        openai_key = st.text_input("OpenAI API Key", type="password")
        
        # Activation button
        openai_active = st.button("Activate OpenAI")
        
        # Process API activation
        if openai_active and openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
            st.success("OpenAI API activated!")

    # Main content area
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # Process document if not already processed
        if st.session_state.chain is None:
            with st.spinner("Processing document..."):
                chain, retriever, prompt = process_document(tmp_file_path)
                if chain:
                    st.session_state.chain = chain
                    st.success("Document processed! You can now ask questions.")

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("What would you like to know about the document?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            try:
                # Get response from RAG chain
                with st.spinner("Thinking..."):
                    response = st.session_state.chain.invoke(prompt)
                
                # Add assistant message to chat history
                st.session_state.messages.append({"role": "assistant", "content": response['result']})
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(response['result'])
                    
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
        
        # Cleanup temporary file
        os.unlink(tmp_file_path)
    else:
        st.write("Please upload a document to start chatting!")

if __name__ == "__main__":
    main()