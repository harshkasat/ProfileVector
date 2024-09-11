import os
import requests
import base64
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# Fetch the GitHub API token from the environment variables
github = os.getenv("GITHUB_ACCESS_TOKEN")

if not github:
    print("Error: GITHUB_PAT environment variable not set.")
    exit(1)

payload = {}
headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {github}',
    'X-GitHub-Api-Version': '2022-11-28'
}


class GithubFetcher:

    def __init__(self, username) -> None:
        self.username: str = username
        self.repo_url: str = f"https://api.github.com/users/{username}/repos"
        self.readme_url: str = f"https://api.github.com/repos/{username}/"

    def fetch_repo_info(self, limit: Optional[int] = 10) -> list:
        """
        Fetches and returns the top repositories of a given user.
        """
        try:
            response = requests.get(self.repo_url, headers=headers, data=payload)
            repos = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {e}")
            return []

        # Save the top repositories to a list
        try:
            top_repos = repos[:limit]
            simplified_repos = []

            for repo in top_repos:
                if isinstance(repo, dict):
                    simplified = (
                        f"Repository: {repo.get('name', 'N/A')}\n"
                        f"URL: {repo.get('html_url', 'N/A')}\n"
                        f"Language: {repo.get('language', 'N/A')}\n"
                        f"Topics: {', '.join(repo.get('topics', [])) if repo.get('topics') else 'None'}\n"
                    )
                    # Fetch README separately
                    readme_content = self.fetch_readme(repo.get('name', ''))
                    simplified += f"README: {readme_content}" if readme_content else "README: Not available"
                    simplified_repos.append(simplified)
                else:
                    print(f"Unexpected data format: {repo}")

            if simplified_repos:
                print("Fetched info and README from repositories successfully")
                return simplified_repos
            else:
                print("No repositories found.")
                return []

        except Exception as e:
            print(f"Error processing repository data: {e}")
            return []

    def fetch_readme(self, repo_name: str) -> Optional[str]:
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
            return None


# Example usage
# if __name__ == '__main__':
#     username = 'harshkasat'
#     fetcher = GithubFetcher(username)
#     repo_info = fetcher.fetch_repo_info()
#     for info in repo_info:
#         print(info)
