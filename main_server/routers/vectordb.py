from fastapi import APIRouter, HTTPException
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
import uuid
from langchain_qdrant import QdrantVectorStore
from models.schemas import AddDataRequest
from langchain_core.documents import Document

router = APIRouter(prefix='/admin', tags=['Admin'])


qdrant_client = QdrantClient(url="http://64.227.160.209:6333", timeout=300) 


 

@router.post("/add-to-collection/")
async def add_to_collection(data: AddDataRequest):
    try:
        document_id = str(uuid.uuid4())
        embeddings = OpenAIEmbeddings()
        
        document = Document(
            page_content=data.text,
            metadata={"source": data.source, "title": data.title, "description": data.description},
        )
        vector_store = QdrantVectorStore.from_existing_collection(embedding=embeddings, collection_name=data.collection_name, url="http://64.227.160.209:6333")
        vector_store.add_documents(
            documents=[document],
            ids=[document_id],
        )

        return {"status": "success", "id": document_id, "message": "Data added to Qdrant collection successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

