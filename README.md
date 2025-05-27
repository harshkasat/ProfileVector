## ProfileVector: README Generation based on Provided Code

Based on the provided code, ProfileVector is a question-answering system that leverages a user's GitHub profile, website content, and resume to answer questions.  It uses Langchain for building the retrieval chain, Pinecone for vector storage, and a large language model (LLM) for question answering.

**a. Purpose/Features:**

ProfileVector aims to create a comprehensive knowledge base from a user's online presence. This knowledge base is then used to answer questions about the user's skills, experience, projects, and other relevant information.  The system supports both single-shot question answering and streaming responses via a websocket.

**b. Functions/Code Details:**

The system is comprised of several key components:

* **Data Scraping (Scrape directory):**
    * `user_info.py`: Fetches user information (profile details, social links) from GitHub.
    * `repo.py`: Fetches repository information from GitHub.
    * `scrape_website.py`: Scrapes content from a given website URL.
    * `scrape_resume.py`: Parses a resume PDF (presumably using PyMuPDF).
    * `helper.py`:  Contains helper functions for data extraction and processing.

* **Vector Store Creation (Llm/VectorStore directory):**
    * `config.py`: Configuration settings for embedding models and Pinecone.
    * `langchain_document.py`: Creates Langchain Documents from the scraped data.
    * `pinecone.py`:  Handles interaction with the Pinecone vector database, loading and querying documents.

* **LLM Interaction (Llm directory and `question_rag.py`):**
    * `config.py`: Configuration for the LLM (likely OpenAI or Google AI).
    * `question_rag.py`:  The core question-answering logic.  Uses `RetrievalChain` to:
        * `_retrieve_vstore()`:  Retrieves relevant documents from the Pinecone vector store using MMR (Maximal Marginal Relevance) search.
        * `_history_retrieval_chain()`: Creates a chain that contextualizes the question based on chat history before retrieving and answering. This uses a `ChatPromptTemplate` to structure the prompts for the LLM.
        * `_retrieve_and_answer()`:  The main function to retrieve and answer a question, updating chat history.


* **API (app.py):**
    * A FastAPI application providing two endpoints:
        * `/questions` (POST): Accepts a question and returns a single answer.
        * `/ws/questions/stream` (WebSocket):  Allows for streaming answers, managing chat history.  Uses `HumanMessage` and `AIMessage` from `langchain_core.messages` to maintain conversation context.

* **main.py:** Orchestrates the data scraping and vector store loading process.  The `parsed_documents` function fetches and processes data, and `vector_document` loads the data into Pinecone.


**Example Code Snippet (from `question_rag.py`):**

```python
def _retrieve_and_answer(self, user_question):
    result = self._history_retrieval_chain.rag_chain.invoke({"input": user_question, "chat_history": self.chat_history})
    self.chat_history.append(HumanMessage(content=user_question))
    self.chat_history.append(AIMessage(content=result["answer"]))
    return result["answer"]
```

This shows the core logic of receiving a question, invoking the retrieval chain, updating chat history, and returning the answer.


**c. Setup/Usage:**

1. **Install Dependencies:**  Use `pip install -r requirements.txt`.
2. **Set up Pinecone:** Create a Pinecone account and index.  Update the Pinecone configuration in `Llm/VectorStore/config.py` with your API key and index name.
3. **Set up LLM:** Configure the LLM in `Llm/config.py` with your API key (OpenAI, Google AI, etc.).
4. **Run `main.py`:** This will scrape data and load it into Pinecone.  **Note:**  The provided `main.py` is commented out, you'll need to uncomment and adjust paths to your resume and website URL.  Also, ensure you have a `.env` file with your GitHub access token (`GITHUB_ACCESS_TOKEN`).
5. **Run `app.py`:** This starts the FastAPI server. You can then send POST requests to `/questions` or connect to `/ws/questions/stream` using a WebSocket client.


**Missing Information:**

The provided code lacks a comprehensive README.  The prompt requests a full README, but the code only provides the building blocks.  A complete README would need to be written based on this code structure, incorporating all the sections requested in the prompt.  I cannot generate a full README.md file without additional information about the project's goals, licensing, and other details not present in the code.
