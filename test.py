import os
import fitz  # PyMuPDF for PDF handling
import spacy
import re

# Load the spaCy NLP model
nlp = spacy.load('en_core_web_sm')

# Function to extract text from PDF using fitz (PyMuPDF)
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text("text")  # Extracting text from each page
    return text

# Helper function to extract contact information
def extract_contact_info(text):
    contact_info = {}

    # Extract email
    email_match = re.findall(r'\S+@\S+', text)
    if email_match:
        contact_info['Email'] = email_match[0]

    # Extract phone number (basic regex for phone numbers)
    phone_match = re.findall(r'(\+?\d{1,2}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}', text)
    if phone_match:
        contact_info['Phone'] = ''.join(phone_match[0])

    # Extract LinkedIn profile
    linkedin_match = re.findall(r'(https?://www\.linkedin\.com/in/[^\s]+)', text)
    if linkedin_match:
        contact_info['LinkedIn'] = linkedin_match[0]
    
    return contact_info

# Helper function to extract education information
def extract_education(text):
    education = []
    education_keywords = ["education", "university", "college", "degree", "bachelor", "master", "phd"]
    lines = text.lower().split("\n")
    
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in education_keywords):
            education.append(lines[i:i + 2])  # Grabbing the next line for context
    return education

# Helper function to extract work experience
def extract_experience(text):
    experience = []
    experience_keywords = ["experience", "employment", "work history", "professional experience"]
    lines = text.lower().split("\n")
    
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in experience_keywords):
            experience.append(lines[i:i + 4])  # Grabbing the next 4 lines for context
    return experience

# Helper function to extract skills
def extract_skills(text):
    skills = []
    skills_keywords = ["skills", "technologies", "technical skills", "expertise"]
    lines = text.lower().split("\n")
    
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in skills_keywords):
            skills.append(lines[i])
    return skills

# Helper function to extract remaining text as "Other Info"
def extract_other_info(text, parsed_sections):
    other_info = []
    lines = text.split("\n")

    # Remove already parsed sections from the text
    for section in parsed_sections:
        for item in section:
            if isinstance(item, list):
                for sub_item in item:
                    text = text.replace(sub_item, "")
            else:
                text = text.replace(item, "")

    # Split into lines and return the rest as "Other Info"
    other_info = [line.strip() for line in text.split("\n") if line.strip()]
    return other_info

# Function to parse resume details from a PDF
def parse_resume(file_path):
    if not file_path.endswith(".pdf"):
        raise ValueError("Unsupported file format! Only PDF files are supported.")

    # Extract text from PDF
    text = extract_text_from_pdf(file_path)

    # Extracting various sections
    contact_info = extract_contact_info(text)
    education = extract_education(text)
    experience = extract_experience(text)
    skills = extract_skills(text)

    # Combine parsed sections for easier removal from the original text
    parsed_sections = [list(contact_info.values()), education, experience, skills]

    # Extract any remaining text as "Other Info"
    other_info = extract_other_info(text, parsed_sections)

    return {
        "Contact Info": contact_info,
        "Education": education,
        "Experience": experience,
        "Skills": skills,
        "Other Info": other_info
    }

# Example usage
if __name__ == "__main__":
    file_path = "C:/Users/Zedmat/Downloads/Harsh Resume.pdf"  # Replace with the path to your PDF resume
    parsed_resume = parse_resume(file_path)
    print(parsed_resume)
