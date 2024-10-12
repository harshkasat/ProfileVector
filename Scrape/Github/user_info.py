import json
import requests


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
        response.raise_for_status()  # Raises an HTTPError for bad responses
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data from {url}: {response.status_code}")
    
    def fetch_social_account(self):
        """
        Fetches and returns the social media accounts associated with the user.
        """
        url = f"https://api.github.com/users/{self.username}/social_accounts"
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        social = {}
        if response.status_code == 200:
            data = response.json()
            for account in data:
                if account['provider'] == 'linkedin':
                    social['linkedin_url'] = account['url']
                elif account['provider'] == 'twitter':
                    social['twitter_url'] = account['url']

            return social
        else:
            raise Exception(f"Error fetching social media accounts from {url}: {response.status_code}")
    


# if __name__ == "__main__":
#     username = 'harshkasat'
#     user = User(username)
#     print(user.fetch_social_account())
