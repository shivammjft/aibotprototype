from fastapi import FastAPI
from consumer import consumer,run
from config.db import collection
from dotenv import load_dotenv
from models.schemas import LinkRequest
from utils.scraper_links import get_links
import asyncio

load_dotenv()
app = FastAPI()


# run(consumer, collection)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run(consumer, collection))


@app.get("/")
def read_root():
    return {"message": "FastAPI server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)


