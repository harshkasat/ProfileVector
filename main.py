from Scrape.Github.repo import GithubFetcher
from Scrape.Github.user_info import User
from Scrape.Github.helper import Helper
from Scrape.scrape_website import Website
from Scrape.scrape_resume import parse_resume


from Llm.config import configure_embedding
from Llm.VectorStore.config import PineconeConfig
from Llm.VectorStore.pinecone import load_document
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

    # # Scrape Website information
    website = Website(username)
    website_link = website.read_data()
    parsed_website = website.parse_website(website_link)

    # Fetch Resume information from PDF
    raw_text = parse_resume(pdf_path)

    # Create Langchain documents
    documents = create_document(user_data=extracted_data, repo_data=repo_info, 
        website_content=parsed_website, resume_content=raw_text)
    

    # Configure the embedding model
    embedd_model =  configure_embedding()

    # Configure the Pinecone index_name
    p = PineconeConfig(username)
    index_name = p.configure_pinecone()

    load_document(embeddings=embedd_model, index=index_name, chunks=documents)