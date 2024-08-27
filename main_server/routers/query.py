from fastapi import APIRouter,Depends,HTTPException
from utils.auth import get_current_user
from utils.query_utils import llm,get_message_history,context_retriever
from constants.prompts import user_message,human_message_template
from models.schems import RequestModel 
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


router = APIRouter(
    tags=['query']
)




prompt = ChatPromptTemplate.from_messages(
    [
        ("system", user_message),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

@router.post("/query")
async def answer_query(req: RequestModel,user: dict = Depends(get_current_user) ):
    try:
        collection_name = 'companyinit'
        namespace_name = user["company_id"]
        rag_chain = prompt | llm | StrOutputParser()
        with_message_history = RunnableWithMessageHistory(
            rag_chain,
            get_message_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        final_response = await with_message_history.ainvoke(
            {"context": context_retriever(req.query, collection_name, namespace_name), "input": req.query,"chatbot_name":user["chatbot_name"],"base_url":user["metadata"]["base_link"]},
            config={"configurable": {"session_id": req.session_id}},
        )
        return final_response

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))