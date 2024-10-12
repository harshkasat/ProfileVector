from langchain.schema import Document



documents = []
class CreateDocument(object):
    
    
    def user_documents(user_data):
        # User Information
        documents.append(Document(
            page_content=user_data,
            metadata={"source": "user_info"}
        ))
    
    def repo_documents(repo_data):
        # Repository Information
        documents.append(Document(
            page_content=repo_data,
            metadata={"source": "repository name, repository url, language, topics, README information"}))
    
    def website_documents(website_content):
        # Website Content

        # Ensure website_content is a string
        if not isinstance(website_content, str) or len(website_content) == 0:
            print("Error: Website content is not a valid string or is empty.")
            return  # Skip document creation

        documents.append(Document(
            page_content=website_content,  # Truncate to 1000 chars
            metadata={"source": "Personal Portfolio website information"}
        ))
    
    def resume_documents(resume_content):
        # Resume Content
        documents.append(Document(
            page_content=resume_content, 
            metadata={"source": "Resume information"}
        ))
    

def create_document(user_data, repo_data, website_content, resume_content):
        """
        Create a list of Document objects from the user's data.
        """

        CreateDocument.user_documents(user_data)
        CreateDocument.repo_documents(repo_data)
        CreateDocument.website_documents(website_content)
        CreateDocument.resume_documents(resume_content)

        return documents
