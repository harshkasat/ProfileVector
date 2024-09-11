from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from Llm.VectorStore.pinecone import load_vector_store
from Llm.config import configure_embedding, configure_llm, configure_prompt_template


store ={}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

session_id = "bcd"

# Configure the embedding model
embedd_model =  configure_embedding()

# Configure the prompt template
llm_prompt = configure_prompt_template()

# Configure the llm model
llm = configure_llm()

username = 'harshkasat'
vstore = load_vector_store(embeddings=embedd_model, index_name=username)

# retriever = vstore.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={'score_threshold': 0.1}
# )

# retriever = vstore.as_retriever(
#         search_type="mmr",
#         search_kwargs={'k': 5, 'lambda_mult': 0.3}
#     )
retriever = vstore.as_retriever(search_kwargs={'k': 1})

# Check if all components are properly defined
if retriever is None or llm_prompt is None or llm is None:
    raise ValueError("One or more components (retriever, llm_prompt, llm) are None")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | llm_prompt
    | llm
    | StrOutputParser()
)

chain_with_history = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="query",
        history_messages_key="history"
    )



# if __name__ == '__main__':

#     while True:
#         question = input(str("What questions do you want to ask (To quit use 'exit' or 'q')? "))
#         if question.lower() == "exit" or question.lower() == 'q':
#             break
#         print(chain_with_history.invoke(question))