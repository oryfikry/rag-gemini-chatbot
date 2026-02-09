# Bizzy Wifi Product RAG Chatbot

A simple yet powerful Retrieval-Augmented Generation (RAG) chatbot for **Bizzy Wifi Product**. This application uses Google's Gemini LLM and FAISS vector database to provide accurate, context-aware information about internet packages and services.

## Features

- **RAG Architecture**: Retrieves relevant product information from a local JSON database before generating responses.
- **Premium UI**: Modern, clean, and responsive chat interface with a bubble-chat design.
- **Context-Aware**: Specifically tailored for Bizzy Wifi products with additional context about 1:1 speed and service areas (Jabodetabek).
- **HTML Formatting**: Bot responses are beautifully formatted with bold text, lists, and clear spacing.
- **Fast retrieval**: Uses FAISS for efficient similarity search across product data.

## Tech Stack

- **Backend**: Python, Flask
- **LLM**: Google Gemini (Flash/Pro)
- **Framework**: LangChain
- **Vector DB**: FAISS
- **Database**: JSON
- **Frontend**: Vanilla HTML/CSS/JS (embedded in Flask)

## Prerequisites

- Python 3.9+
- A Google API Key (for Gemini and Google Embeddings)

## Installation

1. Clone or download the repository:
   ```bash
   cd rag-chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Create a `.env` file in the root directory and add your Google API key:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Start chatting with the Bizzy Assistant!

## Core Files

- `app.py`: Flask web server and frontend interface.
- `rag_engine.py`: Core RAG logic, vector store management, and Gemini integration.
- `products.json`: The "knowledge base" containing all internet package details.
- `requirements.txt`: Python package dependencies.
