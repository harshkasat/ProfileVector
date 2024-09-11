from langchain_community.chat_message_histories import ChatMessageHistory

from fastapi import FastAPI
from pydantic import BaseModel
from question_rag import chain_with_history
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



session_id = "bcd"
config = {"configurable": {"session_id": session_id}}


class Questions(BaseModel):
    question: str


@app.get("/")
async def hello():
    return {"message": "Hello, World!"}

@app.post("/questions")
async def process_question(question: Questions):
    response = chain_with_history.invoke(question.question)
    return {"response": response}
