import requests
from bs4 import BeautifulSoup
import json
from pydantic import BaseModel
from typing import List

# Define Pydantic models for validation
class Heading(BaseModel):
    text: str

class Link(BaseModel):
    text: str
    url: str


class Website:

    def __init__(self, url):
        self.url = url
    

    def parse_website(self):

        # Send a GET request
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()  # This will raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch the website: {e}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting data
        headings = ""
        paragraphs = ""
        links = ""
        
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                headings += heading.text.strip() + '\n'

        for para in soup.find_all('p'):
            paragraphs += para.text.strip() + '\n'

        for link in soup.find_all('a'):
            links += f"text: {link.text.strip()}, url: {link.get('href')} \n" 

        # Combine into the structure for Pydantic validation
        scraped_data = f""" headings: {headings}, paragraphs: {paragraphs}, links: {links}"""

        # Validate with Pydantic
        try:
            print(f"Website successfully parsed.")
            return scraped_data
        except Exception as e:
            print(f"Error: {e}")

# if __name__ == '__main__':
#     # Example usage
#     url  = 'https://machoharsh-tech.vercel.app/'
#     website = Website(url)
#     scraped_data = website.parse_website()
#     print(scraped_data)
    