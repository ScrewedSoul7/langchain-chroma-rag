Local RAG AI Agent

📖 High-Level Overview

This project is a custom-built AI assistant that can read, understand, and answer questions about specific, private documents. Instead of relying on an AI's general knowledge (which can often lead to making things up or "hallucinating"), this tool uses a technique called Retrieval-Augmented Generation (RAG).

It first searches through a local folder of your personal documents to find the exact paragraphs relevant to your question. It then feeds only that verified, factual information to the AI to generate a precise and accurate answer.

💡 Motivation

My main motivation behind this project was to deep dive into the topic of Artificial Intelligence beyond just basic API calling. I wanted to understand the underlying architecture of modern machine learning pipelines—specifically how vector embeddings work, how semantic search operates under the hood using a local vector database (ChromaDB), and how to programmatically control a Large Language Model's context window.

📸 Visuals & Action

This is a command-line interface (CLI) application. Here is an example of what the pipeline looks like in action:

1. Ingesting Data into the Vector Database:

$ python create_db.py
Split 1 documents into 32 chunks.
Saved 32 chunks to chroma.


2. Querying the Agent:

$ python query_data.py "Which devil fruit does Law have?"
Based on the provided context, Law (Trafalgar D. Water Law) has the Ope Ope no Mi devil fruit.


⚙️ Detailed Setup & Execution Instructions

Prerequisites

Python 3.8 or higher installed on your machine.

A Google Gemini API Key.

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME


2. Set Up a Virtual Environment

Using a virtual environment ensures these dependencies are isolated and don't conflict with your global system.

# Create the virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt


4. Environment Variables

Create a file named .env in the root directory of the project. Add your API key as follows:

GOOGLE_API_KEY="your_actual_api_key_here"


(Note: The .env file is included in the .gitignore so your key remains safe and private locally).

5. Run the Application

Build the Database: Place any Markdown (.md) files you want the AI to read into the Data/ folder. Then run:

python create_db.py


Ask a Question:
Run the query script followed by your question wrapped in quotes:

python query_data.py "Type your question here inside quotes?"


🧪 Running Tests

To verify the data ingestion and relevance threshold logic are working correctly:

Add a test text file to the Data/ folder and run python create_db.py. Verify the chunk count updates.

Run a query for a topic explicitly not in your documents (e.g., python query_data.py "What is the capital of France?").

You should see the automated relevance threshold guardrail successfully trigger:
Unable to find the information

🐛 Known Issues

Known Issues:

Relevance Thresholding: The current relevance score threshold is strictly set to < 0.6. Depending on the density of the documents added, this might occasionally filter out vaguely related but correct chunks. This requires manual tuning per dataset.
