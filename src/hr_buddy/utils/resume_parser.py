import pdfplumber
import docx
import re

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF resume."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX resume."""
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_resume(file_path):
    """Parses resume and extracts structured information."""
    ext = file_path.split(".")[-1].lower()
    text = ""
    
    if ext == "pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == "docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Upload a PDF or DOCX file.")
    
    # Extract key details
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    experience = extract_experience(text)
    education = extract_education(text)
    
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "work_experience": experience,
        "education": education
    }

def extract_name(text):
    """Extracts name from resume (basic heuristic)."""
    lines = text.split("\n")
    if len(lines) > 0:
        return lines[0]  # Assume first line is the name (improve logic as needed)
    return "Unknown"

def extract_email(text):
    """Extracts email from resume."""
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group(0) if match else "Not Found"

def extract_phone(text):
    """Extracts phone number from resume."""
    match = re.search(r'\b\d{10,15}\b', text)
    return match.group(0) if match else "Not Found"

def extract_skills(text):
    """Extracts skills from resume."""
    keywords = ["Python", "Machine Learning", "Data Science", "SQL", "Java", "AI", "Deep Learning", "Excel", "TensorFlow"]
    found_skills = [skill for skill in keywords if skill.lower() in text.lower()]
    return ", ".join(found_skills) if found_skills else "Not Found"

def extract_experience(text):
    """Extracts work experience (basic logic)."""
    experiences = re.findall(r'([A-Za-z]+ .*\d{4})', text)  # Looks for patterns like "Software Engineer at XYZ 2021"
    return experiences if experiences else "Not Found"

def extract_education(text):
    """Extracts education details (basic logic)."""
    education_patterns = ["BSc", "MSc", "PhD", "Bachelor", "Master", "Doctorate"]
    for pattern in education_patterns:
        match = re.search(pattern + r'.*\d{4}', text, re.IGNORECASE)
        if match:
            return match.group(0)
    return "Not Found"

# Example Usage
if __name__ == "__main__":
    sample_resume = "path/to/sample_resume.pdf"  # Replace with actual file path
    parsed_data = parse_resume(sample_resume)
    print(parsed_data)
