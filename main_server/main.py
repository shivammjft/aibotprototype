from fastapi import FastAPI
import os
from routers import auth,query,prepare,admin
from dotenv import load_dotenv
from config.db import Base,engine
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

Base.metadata.create_all(bind = engine)


load_dotenv()

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



# creating prompt

# declaring llm
# llm = ChatGroq(
#     temperature=0.0,
#     groq_api_key=os.getenv("GROQ_API_KEY"),
#     model_name="llama3-70b-8192",
# )

# llm_4o = ChatOpenAI(model="gpt-4o-mini")




@app.get("/")
def read_root():
    return {"message": "Welcome to the Jellyfish Technologies AI!"}

app.include_router(prepare.router)
app.include_router(query.router)
app.include_router(auth.router)
app.include_router(admin.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)