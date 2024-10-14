from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage


from Llm.VectorStore.pinecone import load_vector_store
from Llm.config import configure_embedding, configure_llm, configure_prompt_template



class RetrievalChain:
    def __init__(self, username) -> None: 
        self.embedd_model = configure_embedding()
        self.llm_prompt = configure_prompt_template()
        self.llm = configure_llm()
        self.vstore = load_vector_store(embeddings=self.embedd_model, index_name=username)
        self.chat_history = []
    
    def _retrieve_vstore(self):
        retriever = self.vstore.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 6, 'lambda_mult': 0.4}
        )

        # retriever = vstore.as_retriever(
        # search_type="similarity_score_threshold",
        # search_kwargs={'score_threshold': 0.1}
        # )

        # retriever = vstore.as_retriever(search_kwargs={'k': 5})

        if retriever is None or self.llm_prompt is None or self.llm is None:
            raise ValueError("One or more components (retriever, llm_prompt, llm) are None")
        return retriever

    def _history_retrieval_chain(self):
        ### Contextualize question ###
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            self.llm, self._retrieve_vstore(), contextualize_q_prompt
        )

        ### Answer question ###
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)

        chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        print("Chain created successfully")

        return chain

    def _retrieve_and_answer(self, user_question):
        result = self._history_retrieval_chain.rag_chain.invoke({"input": user_question, "chat_history": self.chat_history})
        self.chat_history.append(HumanMessage(content=user_question))
        self.chat_history.append(AIMessage(content=result["answer"]))

        return result["answer"]
