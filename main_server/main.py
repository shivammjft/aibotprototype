from fastapi import FastAPI
import os
from routers import auth, query, prepare, admin
from dotenv import load_dotenv
from config.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()


app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.getenv("LANGCHAIN_API_KEY")  
os.environ["LANGCHAIN_PROJECT"] = "Chatbot Doc Mapping"

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Jellyfish Technologies AI!"}

# Include routers
app.include_router(prepare.router)
app.include_router(query.router)
app.include_router(auth.router)
app.include_router(admin.router)

if __name__ == "__main__":
    logger.info("Starting FastAPI application")
    uvicorn.run(app, host="0.0.0.0", port=8000)
