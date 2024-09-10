import os
import time
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

pinecone_api_key = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=pinecone_api_key)


class PineconeConfig(object):
    def __init__(self, username):
        self.username = username

    def configure_pinecone(self):

        index_name = self.username
        if index_name in pc.list_indexes().names():
            print("Pinecone index already exists")
            return pc.Index(index_name)

        pc.create_index(
            name=index_name,
            dimension=768, # Replace with your model dimensions
            metric="cosine", # Replace with your model metric
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ) 
        )
        
        return pc.Index(index_name)

    def delete_pinecone(self):
        try:
            pc.delete_index(self.username)
            print("Pinecone indexes is deleted of index_name: %s" % self.username)
        except Exception as e:
            print(f"Error deleting index: {e}")


# if __name__ == '__main__':
#     username = 'harshkasat'
#     p = Pinecone(username)
#     # p.configure_pinecone()
#     p.delete_pinecone()