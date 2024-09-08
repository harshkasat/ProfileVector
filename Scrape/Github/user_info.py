import json
import requests
from Scrape.Github.helper import Helper


class User:

    def __init__(self, username) -> None:
        self.username = username

    
    def fetch_data(self) -> json:
        """
        Fetches data from the GitHub API and returns it as a JSON object.
        Raises an exception if the request fails.
        """
        url = f"https://api.github.com/users/{self.username}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data from {url}: {response.status_code}")
    


# if __name__ == "__main__":
#     username = 'harshkasat'
