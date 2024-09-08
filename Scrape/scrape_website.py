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

class ScrapedData(BaseModel):
    headings: List[Heading]
    paragraphs: List[str]
    links: List[Link]


class Website:

    def __init__(self, username):
        self.username = username
    

    def read_data(self):
        with open(f'{self.username}.json', 'r') as f:
            data = json.load(f)
            return data['blog']

    def parse_website(self, url):
        # URL of the website to scrape
        # url = "https://machoharsh-tech.vercel.app/"

        # Send a GET request
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting data
        headings = []
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                headings.append({"text": heading.text.strip()})

        paragraphs = [para.text.strip() for para in soup.find_all('p')]

        links = []
        for link in soup.find_all('a'):
            links.append({
                "text": link.text.strip(),
                "url": link.get('href')
            })

        # Combine into the structure for Pydantic validation
        data = {
            "headings": headings,
            "paragraphs": paragraphs,
            "links": links,
        }

        # Validate with Pydantic
        try:
            scraped_data = ScrapedData(**data)
            with open(f'{self.username}-website.json', 'w') as f:
                json.dump(scraped_data.model_dump(), f, indent=4)
            print(f"Data successfully saved to {self.username}-website.json .")
        except Exception as e:
            print(f"Error: {e}")

# if __name__ == "__main__":
#     username = 'harshkasat'
    