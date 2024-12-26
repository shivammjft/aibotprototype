from fastapi import APIRouter, HTTPException
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_openai import OpenAIEmbeddings
import uuid
from langchain_qdrant import QdrantVectorStore
from models.schemas import AddDataRequest, DeleteDataRequest, SearchDataByMetaDataRequest, DocumentResponse
from langchain_core.documents import Document
from typing import List



router = APIRouter(prefix='/dbmanipulation', tags=['VectorDB'])


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
    
@router.post("/search-by-metadata/", response_model=List[DocumentResponse])
async def search_by_metadata(request: SearchDataByMetaDataRequest):
    try:
        filter_condition = models.Filter(
            must=[
                models.FieldCondition(
                    key=f"metadata.{request.key}",
                    match=models.MatchValue(value=request.value)
                )
            ]
        )

        search_results, _ = qdrant_client.scroll(
            collection_name=request.collection_name,
            scroll_filter=filter_condition,
            limit=request.to_retrive,  
            with_payload=True  
        )

        documents = [
            DocumentResponse(
                id=point.id,
                content=point.payload.get("page_content", ""),
                metadata=point.payload.get("metadata", {})
            )
            for point in search_results
        ]

        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-from-collection/")
async def delete_from_collection(request: DeleteDataRequest):
    try:
        response = qdrant_client.delete(
            collection_name=request.collection_name,
            points_selector=models.PointIdsList(
                points=request.document_ids  
            )
        )
        return {
            "status": "success",
            "message": f"Documents with IDs {request.document_ids} deleted successfully.",
            "response": response.dict()  
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

