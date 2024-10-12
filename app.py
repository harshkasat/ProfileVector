
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from question_rag import RetrievalChain
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
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
    rag_chain = RetrievalChain(username='harshkasat')._history_retrieval_chain()
    response = rag_chain.invoke({"input": question.question, "chat_history": chat_history})
    return {'response': response}

@app.websocket("/ws/questions")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    rag_chain = RetrievalChain(username='harshkasat')
    
    while True:
        try:
            data = await websocket.receive_text()  # Receive the question from the client
            question = data.strip()
            # Call your RAG chain
            # response = rag_chain.invoke({"input": question, "chat_history": chat_history})
            response = rag_chain._retrieve_and_answer(question)
            # Send the response back to the client
            await websocket.send_text(response)

        except Exception as e:
            print(f"Error: {e}")
            break

    await websocket.close()