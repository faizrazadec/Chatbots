# Streamlit Chatbot with Google Generative AI API 🤖

Welcome to the **Streamlit Chatbot** application! This project integrates the **Google Generative AI API (Gemini)** into a user-friendly interface built with **Streamlit**. The chatbot leverages the capabilities of the AI to provide conversational responses in real-time, complete with a smooth typing effect to enhance user experience.

---

## 🚀 Project Overview

This project creates a conversational AI that allows users to interact with a chatbot through a clean, easy-to-use **Streamlit** web interface. Powered by Google's **Generative AI (Gemini)** model, the chatbot is capable of generating dynamic and context-aware responses. The model checks for safety concerns before delivering responses, ensuring appropriate interaction.

### Key Features:
- **Streamlit Interface**: The app uses Streamlit's sleek and minimalist layout for displaying chat history and generating new responses.
- **Google Generative AI (Gemini)**: A robust language model generates responses to user input, utilizing the API to provide accurate, safe content.
- **Real-Time Text Generation**: As the chatbot types its response, it displays a character-by-character typing effect, simulating human interaction.
- **Safety Filtering**: Each AI-generated response undergoes a safety check, filtering out content deemed inappropriate or unsafe.

---

## 🧠 How the AI Works

The AI model behind this chatbot is **Gemini-1.5 Flash**, provided by **Google Generative AI**. This model generates conversational responses based on the input text while ensuring content appropriateness through built-in safety ratings.

- **User Input**: The user provides a text prompt.
- **Content Generation**: The model generates a response based on the user's input.
- **Safety Ratings**: The response is evaluated using safety ratings to ensure it meets safety standards.
- **Typing Effect**: The response is displayed with a typing effect, enhancing the user experience.

---

## 💻 Technologies Used

- **Streamlit**: A Python-based web application framework for the interactive UI.
- **Google Generative AI API (Gemini)**: The core AI model providing natural language responses.
- **Python**: For building the backend and integrating the AI API.
- **Session State**: Used to store and update chat history.

---

## 🛠️ How to Run the Project

### Prerequisites:
- A valid **Google API key** for accessing the Generative AI (Gemini) API.
- Python 3.x installed on your system.
- Required Python libraries: `streamlit`, `google-generativeai`.

### Installation:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/streamlit-chatbot.git
   cd streamlit-chatbot
