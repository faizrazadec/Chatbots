# Free GPT+ Chatbot and PDF Processor

**Free GPT+** is a chatbot application built using Google Generative AI (Gemini) API and Streamlit. The chatbot allows users to interact with AI-driven responses while also processing PDF documents for text extraction. It supports uploading multiple PDF files and querying the extracted text.

## Features
- **Chat Interface**: A conversational interface where users can input queries and receive responses from the chatbot.
- **PDF Text Extraction**: Upload multiple PDFs, extract the content, and use it to ask document-based questions.
- **Real-time Typing Effect**: Simulates a real-time text generation effect for the chatbot's responses.
- **Chat History**: Displays previous user inputs and chatbot responses in an organized manner.
- **Interactive UI**: Built using Streamlit, with custom HTML/CSS for a user-friendly experience.

## How It Works
1. Users can upload PDF files to extract the text content.
2. Type any query or ask questions based on the uploaded PDF.
3. The chatbot generates a response using Google Generative AI (Gemini) and provides document-based answers if needed.

## Installation
To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/free-gpt-plus.git
   cd free-gpt-plus
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
3. Add your Google Generative AI API key to a .env file:
   ```bash
   GOOGLE_API_KEY=your_api_key
4. Run the application:
   ```bash
   streamlit run app.py
5. Create venv.

   ## Technologies Used
- Google Generative AI (Gemini)
- Streamlit for UI development
- PyPDF2 for PDF text extraction
- Python for backend logic

## Future Enhancements
- Add support for different file types beyond PDF.
- Improve the chatbot’s ability to process more complex documents.
- Enable multi-language support for global users.

Developed by Faiz Raza | faiz.raza.dec@gmail.com
