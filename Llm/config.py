import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()


genai_api_key = os.getenv('GEMINI_API_KEY')
os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')
if genai_api_key is None:
    raise ValueError("Missing GEMINI_API_KEY environment variable")


# Initialize the API client
def configure_llm():
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
            temperature=0.7, top_p=0.85)
        if llm is None:
            raise ValueError("LLM component is None")
        return llm
    except Exception as e:
        print(f"Failed to configure LLM: {e}")
        return None

def configure_embedding():
    task_type = ['retrieval_query',
                #  'retrieval_document',
                #  'question_answering',
    ]

    try:

        model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        return model
    except Exception as e:
        print(f"Failed to configure embedding: {e}")
        return None

def configure_prompt_template():
    llm_prompt  = """You are an assistant for question-answering tasks.
Use the following context to answer the question.
If you don't know the answer, just say that you don't know.
Use five sentences maximum and keep the answer concise.\n
Question: {question} \nContext: {context} \nAnswer:"""
    return PromptTemplate.from_template(llm_prompt)

# if __name__ == "__main__":
#     # Replace this with the text you want to analyze
#     username= 'harshkasat'
#     result = configure_embedding(username)
#     print(result)