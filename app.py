
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from question_rag import RetrievalChain
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

from langchain_core.messages import HumanMessage, AIMessage


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://profile-vector.vercel.app/", "http://localhost:3000/"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


chat_history = []


class Questions(BaseModel):
    question: str


@app.get("/")
async def hello():
    return {"message": "Hello, World!"}

@app.post("/questions")
async def process_question(question: Questions):
    rag_chain = RetrievalChain(username='harshkasat')
    response = rag_chain._retrieve_and_answer(question.question)
    return {'response': response}


@app.websocket("/ws/questions/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    rag_chain = RetrievalChain(username='harshkasat')
    chat_history = []
    
    while True:
        try:
            data = await websocket.receive_text()  # Receive the question from the client
            question = data.strip()
            full_response = ""
            # Call your RAG chain

            stream_rag_chain = rag_chain._history_retrieval_chain().stream({"input": question, "chat_history":chat_history})
            chat_history.append(HumanMessage(content=question))

            for chunk in stream_rag_chain:
                if response := chunk.get("answer"):
                    # Send the response back to the client
                    full_response += response
            chat_history.append(AIMessage(content=full_response))
            await websocket.send_text(full_response)
        except Exception as e:
            print(f"Error: {e}")
            break

    await websocket.close()
