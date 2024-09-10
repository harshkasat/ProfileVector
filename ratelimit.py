import requests
import os
from dotenv import load_dotenv

load_dotenv()


url = "https://api.github.com/rate_limit"
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

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
