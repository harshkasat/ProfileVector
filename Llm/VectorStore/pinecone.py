from langchain_pinecone import PineconeVectorStore
from langchain_community.vectorstores import Pinecone
from uuid import uuid4

def load_document(embeddings, index, chunks):
    try:
        # Generate UUIDs for each document
        uuids = [str(uuid4()) for _ in range(len(chunks))]
        vector_store = PineconeVectorStore(index=index, embedding=embeddings)
        vector_store.add_documents(documents=chunks, ids=uuids)
        print(f"Documents loaded successfully into Pinecone index {index}")

    except Exception as e:
        print(f"An error occurred while loading documents into Pinecone: {e}")

def load_vector_store(index_name, embeddings):
    vstore = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)
    print(f"Successfully loaded document from vectors store into memory at index {index_name}")
    return vstore