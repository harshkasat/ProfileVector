import json
from typing import List, Optional
from pydantic import BaseModel, Field
import fitz  # PyMuPDF

class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class Education(BaseModel):
    institution: str
    degree: str
    graduation_date: Optional[str] = None

class Experience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None

class Resume(BaseModel):
    contact_info: ContactInfo
    education: List[Education] = []
    experience: List[Experience] = []
    skills: List[str] = []
    other: Optional[str] = None

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    extracted_text = ""
    for page in doc:
        extracted_text += page.get_text() + "\n\n"
    doc.close()
    return extracted_text

def parse_resume(text: str) -> Resume:
    # This is a basic parser. You'll need to expand this based on your specific needs.
    sections = {
        "contact_info": "",
        "education": "",
        "experience": "",
        "skills": "",
        "other": ""
    }
    
    current_section = "other"
    
    for line in text.split('\n'):
        line = line.strip()
        if line.lower() in ["contact information", "personal details"]:
            current_section = "contact_info"
        elif line.lower() in ["education", "academic background"]:
            current_section = "education"
        elif line.lower() in ["experience", "work experience", "professional experience"]:
            current_section = "experience"
        elif line.lower() in ["skills", "technical skills"]:
            current_section = "skills"
        else:
            sections[current_section] += line + "\n"
    
    # Basic parsing logic (you'll need to improve this based on your resume format)
    contact_info = ContactInfo(
        name=sections["contact_info"].split('\n')[0],
        email=next((line for line in sections["contact_info"].split('\n') if '@' in line), None),
        phone=next((line for line in sections["contact_info"].split('\n') if any(char.isdigit() for char in line)), None),
    )
    
    education = [Education(institution=line.split(',')[0], degree=line.split(',')[1]) 
                 for line in sections["education"].split('\n') if ',' in line]
    
    experience = [Experience(company=line.split('-')[0].strip(), 
                             position=line.split('-')[1].strip(), 
                             start_date="Unknown")  # You'll need to extract actual dates
                  for line in sections["experience"].split('\n') if '-' in line]
    
    skills = [skill.strip() for skill in sections["skills"].split(',') if skill.strip()]
    
    return Resume(
        contact_info=contact_info,
        education=education,
        experience=experience,
        skills=skills,
        other=sections["other"] if sections["other"].strip() else None
    ).model_dump_json()



# if __name__ == "__main__":
#     # Usage
#     username = 'harshkasat'
#     pdf_path = "C:/Users/Zedmat/Downloads/Harsh Resume.pdf"

#     raw_text = extract_text_from_pdf(pdf_path)
#     parsed_resume = parse_resume(raw_text)