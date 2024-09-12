import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import tempfile
import time

# Load environment variables from .env file
load_dotenv()

# Streamlit app title and layout configuration
st.set_page_config(page_title="RAG Model Q&A", page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUK1yEobsuxFek46BWgBlu7qw4sGuXTBqmpw&s", layout="wide")

# Add custom CSS for vertical text
st.markdown("""
    <style>
    .vertical-text {
        position: fixed;
        right: 70px;
        top: 90%;
        transform: rotate(90deg);
        transform-origin: right bottom;
        font-size: 20px;
        color: #333;
        font-family: Arial, sans-serif;
        font-weight: bold;
        z-index: 100;
        background-color: #f1f1f1;
        padding: 10px;
    }
    </style>
    <div class="vertical-text">RAG Model by Faiz Raza | faiz.raza.dec@gmail.com</div>
    """, unsafe_allow_html=True)

st.title("RAG Model Q&A with Gemini")

# Initialize session state for chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Layout for chat history and chatbot interface
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Chat History")
    for chat in st.session_state.history:
        if chat['role'] == 'user':
            st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #00bfff; color: black; border: 1px solid #ddd; margin-bottom: 5px;'><strong>You:</strong> {chat['message']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #1e1e1e; color: white; border: 1px solid #ddd; margin-bottom: 5px;'><strong>Chatbot:</strong> {chat['message']}</div>", unsafe_allow_html=True)

with col2:
    st.subheader("Chatbot")

    # File upload interface for multiple PDFs
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    # If files are uploaded, extract text
    docs = None
    if uploaded_files:
        pdf_text = ""
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name

            # Load PDF and extract text
            try:
                loader = PyPDFLoader(temp_file_path)
                data = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
                docs = text_splitter.split_documents(data)
                pdf_text += "\n".join([doc.page_content for doc in docs])
                st.success("PDFs uploaded and text extracted successfully.")
            except Exception as e:
                st.error(f"Failed to extract text from PDFs: {e}")
                docs = None

    # Create a form for user input
    with st.form(key='chat_form', clear_on_submit=True):
        user_question = st.text_input("Type your question here...", key="user_input", label_visibility="hidden")
        submit_button = st.form_submit_button("Send")

    # Set up RAG model if there is user input and documents are available
    if user_question:
        st.session_state.history.append({"role": "user", "message": user_question})

        if docs:
            # Display loading spinner
            with st.spinner("Generating response..."):
                # Embedding model for vector store
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

                # Create vectorstore using Chroma
                vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)

                # Create retriever from the vectorstore
                retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

                # Set up the LLM model (Gemini)
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, max_tokens=500)

                # System prompt for the model
                system_prompt = (
                    "You are an expert assistant for question-answering tasks. "
                    "You'll answer the questin based on the pdf provided by user "
                    "and you'll also look online and you'll response like a pro "
                    "Use the following pieces of retrieved context to answer "
                    "the question. If you don't know the answer, say that you "
                    "don't know. Use three sentences maximum and keep the "
                    "response simple and clear.\n\n"
                    "{context}"
                )

                # Create the prompt template for conversation
                prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", system_prompt),
                        ("human", "{input}"),
                    ]
                )

                # Create the question-answering chain with LLM and prompt
                question_answer_chain = create_stuff_documents_chain(llm, prompt)
                rag_chain = create_retrieval_chain(retriever, question_answer_chain)

                # Generate response using RAG model
                response = rag_chain.invoke({"input": user_question})
                response_text = response["answer"]

                # Simulate real-time text generation
                display_text = ""
                chat_placeholder = st.empty()
                for char in response_text:
                    display_text += char
                    time.sleep(0.005)  # Typing effect delay
                    chat_placeholder.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: black; color: white; border: 1px solid #ddd; margin-bottom: 5px;'> {display_text}</div>", unsafe_allow_html=True)

                st.session_state.history.append({"role": "chatbot", "message": display_text})
        else:
            st.error("No documents uploaded or processed. Please upload PDF files for context.")