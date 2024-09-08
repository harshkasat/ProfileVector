import json
from Scrape.Github.repo import GithubFetcher
from Scrape.Github.user_info import User
from Scrape.Github.helper import Helper
from Scrape.scrape_website import Website
from Scrape.scrape_resume import extract_text_from_pdf, parse_resume, save_to_json



if __name__ == "__main__":
    username='harshkasat'

    # Fetch User information from Github
    user_info = User(username)
    data = user_info.fetch_data()
    print("Data fetched successfully.")
    extracted_data = Helper()._extract(data=data)
    Helper()._save(data={"extracted_data":extracted_data, "filename":username})


    # Fetch repositories from Github
    fetcher = GithubFetcher(username)

    print(f"Fetching top repositories info and READMEs for {username}...")

    repo_info = fetcher.fetch_repo_info()


    # Scrape Website information
    website = Website(username)
    website_link = website.read_data()
    website.parse_website(website_link)

    pdf_path = "resume_path.pdf"
    output_json_path = f"{username}-resume.json"

    raw_text = extract_text_from_pdf(pdf_path)
    parsed_resume = parse_resume(raw_text)
    save_to_json(parsed_resume, username)