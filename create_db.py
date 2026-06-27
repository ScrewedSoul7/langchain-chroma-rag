from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import os, shutil
from dotenv import load_dotenv

DATA_PATH = "Data"
CHROMA_PATH = "chroma"

load_dotenv()

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_db(chunks)

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md", loader_cls=TextLoader)
    documents = loader.load()
    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=350, 
        chunk_overlap=50,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[7]
    print(document.page_content)
    print(document.metadata)

    return chunks

def save_db(chunks):
    
    #clear the database
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    gemini_embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    db = Chroma.from_documents(chunks,embedding= gemini_embedding , persist_directory=CHROMA_PATH)
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

    model = ChatGoogleGenerativeAI()
if __name__ == "__main__":
    main() 