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

    def __init__(self, username):
        self.username = username
    

    def read_data(self):
        with open(f'{self.username}.json', 'r') as f:
            data = json.load(f)
            return data['blog']

    def parse_website(self, url):

        # Send a GET request
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # This will raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch the website: {e}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting data
        headings = []
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                headings.append(f"text: {heading.text.strip()}")

        paragraphs = [para.text.strip() for para in soup.find_all('p')]

        links = []
        for link in soup.find_all('a'):
            links.append(f"text: {link.text.strip()}, url: {link.get('href')}")

        # Combine into the structure for Pydantic validation
        data = f""" headings: {headings}, paragraphs: {paragraphs}, links: {links}"""

        # Validate with Pydantic
        try:
            scraped_data = data
            print(f"Website successfully parsed.")
            return scraped_data
        except Exception as e:
            print(f"Error: {e}")

# if __name__ == "__main__":
#     username = 'harshkasat'
    