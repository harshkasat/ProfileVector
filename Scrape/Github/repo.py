import os
import requests
import json
from dotenv import load_dotenv
from typing import Optional
import base64

load_dotenv()



# Fetch the GitHub API token from the environment variables

github = os.getenv("GITHUB_ACCESS_TOKEN")

if not github:
    print("Error: GITHUB_PAT environment variable not set.")
    exit(1)

payload = {}
headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': github,
    'X-GitHub-Api-Version': '2022-11-28'
}


class GithubFetcher:

    def __init__(self, username) -> None:
        self.username : str = username
        self.repo_url : str = f"https://api.github.com/users/{username}/repos"
        self.readme_url : str = f"https://api.github.com/repos/{username}/"


    def fetch_repo_info(self, limit:Optional[int] = 10) -> None:
        """
        Fetches and returns the top repositories of a given user.
        """
        try:
            response = requests.get(self.repo_url, headers=headers, data=payload)
            repos = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {e}")
            return []
        
        # Save the top repositories to a JSON file
        try:
            top_repos = repos[:limit]
            # Extract only the required information
            simplified_repos = []
            for repo in top_repos:
                simplified_repo = {
                    'name': repo['name'],
                    'html_url': repo['html_url'],
                    'language': repo['language'],
                    'topics': repo['topics'],
                    'readme': self.fetch_readme(repo['name'])
                }
                simplified_repos.append(simplified_repo)
                # Print progress
                print(f"Fetched info and README for: {repo['name']}")

                if simplified_repo:
                    # Save all info in single json file
                    with open(f"{self.username}_repo_info.json", 'w') as f:
                        json.dump(simplified_repo, f, indent=4)
                    
                else:
                    print("No repositories found.")

                print(f"Top repositories info and READMEs saved to {self.username}_repo_info.json")

        except Exception as e:
            print(f"Error saving or printing information: {e}")
            return []


    def fetch_readme(self, repo_name):
        """
        Fetches and returns the readme content of a given repository.
        """
        try:
            response = requests.get(f"{self.readme_url}{repo_name}/readme", headers=headers, data=payload)
            if response.status_code != 200:
                print(f"Error fetching README for {repo_name}: {response.status_code}")
                return None

            readme_data = response.json()
            readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
        
            return readme_content
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching readme: {e}")
            return ""
        

# if __name__ == '__main__':
#     username='harshkasat'
#     fetcher = GithubFetcher(username)

#     print(f"Fetching top repositories info and READMEs for {username}...")

#     repo_info = fetcher.fetch_repo_info()

#     if repo_info:
#         # Save all info in single json file
#         with open(f"{username}_repo_info.json", 'w') as f:
#             json.dump(repo_info, f, indent=4)
        
#         print(f"Top repositories info and READMEs saved to {username}_repo_info.json")
#     else:
#         print("No repositories found.")