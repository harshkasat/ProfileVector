from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser


from uuid import uuid4
from Scrape.Github.repo import GithubFetcher
from Scrape.Github.user_info import User
from Scrape.Github.helper import Helper
from Scrape.scrape_website import Website
from Scrape.scrape_resume import extract_text_from_pdf, parse_resume
from Llm.Rag.text_splitter import recursive_text_splitter
from Llm.config import configure_embedding, configure_llm, configure_prompt_template
from Llm.VectorStore.config import PineconeConfig
from Llm.VectorStore.pinecone import load_document, load_vector_store
from Llm.VectorStore.langchain_document import create_document



if __name__ == "__main__":
    username='harshkasat'
    pdf_path = "C:/Users/Zedmat/Downloads/Harsh Resume.pdf"

    # Fetch User information from Github
    user_info = User(username)
    data = user_info.fetch_data()
    extracted_data = Helper()._extract(data=data)

    # Fetch repositories from Github
    fetcher = GithubFetcher(username)
    repo_info = fetcher.fetch_repo_info()

    # Scrape Website information
    website = Website(username)
    website_link = website.read_data()
    parsed_website = website.parse_website(website_link)

    # Fetch Resume information from PDF
    raw_text = extract_text_from_pdf(pdf_path)
    parsed_resume = parse_resume(raw_text)


    combined_data = {
        "User Information": extracted_data,
        "Repository Information": repo_info,
        "Website Content": parsed_website,
        "Resume": parsed_resume
    }
    # Splitting the combined text into smaller chunks
    chunks = recursive_text_splitter(''.join(combined_data))
    
    # Create Langchain documents
    documents = create_document(user_data=extracted_data, repo_data=repo_info, 
        website_content=parsed_website, resume_content=parsed_resume)
    

    # Configure the embedding model
    embedd_model =  configure_embedding()

    # Configure the Pinecone index_name
    p = PineconeConfig(username)
    index_name = p.configure_pinecone()


    load_document(embeddings=embedd_model, index=index_name, chunks=documents)
    vstore = load_vector_store(embeddings=embedd_model, index_name=username)
    
    retriever = vstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'score_threshold': 0.8}
    )
    

    llm_prompt = configure_prompt_template()
    llm = configure_llm()
    
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

    question = input(str("What questions do you want to ask ? "))
    print(rag_chain.invoke(question))
