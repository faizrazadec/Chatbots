import streamlit as st
import google.generativeai as genai
import os
import time

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

def get_response(user_input):
    try:
        response = model.generate_content(user_input)
        
        # Access the first candidate
        candidate = response.candidates[0] if response.candidates else None
        
        if candidate:
            # Access safety ratings
            safety_ratings = candidate.safety_ratings

            # Check safety ratings
            blocked = False
            for rating in safety_ratings:
                if rating.probability.value > 2:  # Adjust threshold as needed
                    blocked = True
                    break
            
            if blocked:
                return "I apologize, I'm not trained to process this request due to safety concerns."
            else:
                return candidate.content.parts[0].text  # Get the actual response text
        else:
            return "I apologize, I'm not trained to process this request."
    
    except Exception as e:
        return "I apologize, I'm not trained to process this request!"

# Streamlit app layout
st.set_page_config(page_title="Chatbot", page_icon=":speech_balloon:", layout="wide")

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

    # Create a form to handle both button click and Enter key press
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("Type your message here...", "", key="user_input", label_visibility="hidden")
        
        # Form submit button
        submit_button = st.form_submit_button("Send")
    
    # Handle form submission (either button click or pressing Enter)
    if submit_button and user_input:
        st.session_state.history.append({"role": "user", "message": user_input})
        
        # Display loading spinner
        with st.spinner("Generating response..."):
            response_text = get_response(user_input)
            
            # Simulate real-time text generation
            display_text = ""
            chat_placeholder = st.empty()
            for char in response_text:
                display_text += char
                time.sleep(0.005)  # Adjust delay for desired typing effect
                # Clear previous output and show the updated output
                chat_placeholder.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: black; color: white; border: 1px solid #ddd; margin-bottom: 5px;'><strong>Chatbot:</strong> {display_text}</div>", unsafe_allow_html=True)
            
            st.session_state.history.append({"role": "chatbot", "message": display_text})
