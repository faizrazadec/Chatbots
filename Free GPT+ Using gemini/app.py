from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env.

import streamlit as st
import os
import google.generativeai as genai
import PyPDF2
import time

# Configure the Google Generative AI API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_pdfs(uploaded_files):
    all_text = ""
    try:
        for uploaded_file in uploaded_files:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            all_text += text + "\n"  # Add newline between files
        return all_text
    except Exception as e:
        st.error(f"Error while extracting text from PDFs: {e}")
        return None

def get_response(user_input, pdf_text=None):
    try:
        if pdf_text:
            combined_prompt = f"{user_input}\n\nDocument Content:\n{pdf_text}"
        else:
            combined_prompt = user_input
        
        response = model.generate_content(combined_prompt)
        
        candidate = response.candidates[0] if response.candidates else None
        
        if candidate:
            safety_ratings = candidate.safety_ratings
            blocked = False
            for rating in safety_ratings:
                if rating.probability.value > 2:
                    blocked = True
                    break
            
            if blocked:
                return "I apologize, I'm not trained to process this request due to safety concerns."
            else:
                return candidate.content.parts[0].text
        else:
            return "I apologize, I'm not trained to process this request."
    
    except Exception as e:
        return "I apologize, I'm not trained to process this request!"

# Streamlit app layout
st.set_page_config(page_title="Free GPT+", page_icon="🤖", layout="wide")

# Use custom CSS to position the text vertically on the right side
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
    <div class="vertical-text">Free GPT+ built by Faiz Raza. | faiz.raza.dec@gmail.com</div>
    """, unsafe_allow_html=True)

st.title("Free GPT+")

# Initialize session state if not already
if 'history' not in st.session_state:
    st.session_state.history = []

# Layout
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

    # Create a file uploader for multiple PDFs
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    pdf_text = None
    
    if uploaded_files:
        pdf_text = extract_text_from_pdfs(uploaded_files)
        if pdf_text:
            st.success("PDFs uploaded and text extracted successfully.")
        else:
            st.error("Failed to extract text from the PDFs.")
    
    # Create a form to handle Enter key press and button click
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("Type your message here...", "", key="user_input", label_visibility="hidden")
        
        # Form submit button
        submit_button = st.form_submit_button("Send")
    
    # Handle form submission (either button click or pressing Enter)
    if user_input:
        st.session_state.history.append({"role": "user", "message": user_input})
        
        # Display loading spinner
        with st.spinner("Generating response..."):
            response_text = get_response(user_input, pdf_text)
            
            # Simulate real-time text generation
            display_text = ""
            chat_placeholder = st.empty()
            for char in response_text:
                display_text += char
                time.sleep(0.005)  # Adjust delay for desired typing effect
                chat_placeholder.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: black; color: white; border: 1px solid #ddd; margin-bottom: 5px;'> {display_text}</div>", unsafe_allow_html=True)
            
            st.session_state.history.append({"role": "chatbot", "message": display_text})