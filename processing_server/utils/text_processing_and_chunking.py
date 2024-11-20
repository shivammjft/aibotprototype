from langchain.text_splitter import RecursiveCharacterTextSplitter
import re


def chunk_text(text, chunk_size=400, chunk_overlap=60):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(text)
    return chunks


def chunk_text_docs(text, chunk_size=600, chunk_overlap=60):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents([text])
    return chunks

def preprocess_text(text):
 
    text = re.sub(r'\n+', '\n', text)
    text = '\n'.join(line.strip() for line in text.split('\n'))
    text = re.sub(r'\n\s*\n+', '\n\n', text)    
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text
