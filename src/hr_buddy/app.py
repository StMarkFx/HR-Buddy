import streamlit as st
from datetime import datetime
import os
import tempfile
import requests
from crew import HRBuddyCrew  # Ensure this is properly implemented
from resume_parser import parse_resume  # Implement resume parsing logic
from validators import validate_url  # Helper function to validate URLs
from social_profiler import fetch_social_data  # Extract LinkedIn & GitHub details

# Initialize HRBuddy Crew
hr_buddy_crew = HRBuddyCrew()

# Streamlit App
def main():
    st.title("HR Buddy: AI-Powered HR Assistant")
    st.write("An intelligent tool to generate tailored resumes & interview questions.")

    # Job Posting Input
    job_url = st.text_input("Enter Job Posting URL")
    
    # Validate Job URL
    if job_url and not validate_url(job_url):
        st.error("Invalid job URL. Please enter a valid link.")
        return

    # Social Media Integration
    linkedin_url = st.text_input("Enter LinkedIn Profile URL (Optional)")
    github_url = st.text_input("Enter GitHub Profile URL (Optional)")

    # Resume Upload
    resume_file = st.file_uploader("Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])
    resume_data = {}

    # Resume Parsing & Dynamic Input Handling
    if resume_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.name)[1]) as temp_file:
            temp_file.write(resume_file.read())
            temp_file_path = temp_file.name

        resume_data = parse_resume(temp_file_path)  # Extract structured resume data
        os.remove(temp_file_path)  # Clean up temp file

    # Handle Missing Resume Information
    missing_info = {
        "skills": resume_data.get("skills", ""),
        "work_experience": resume_data.get("work_experience", []),
        "education": resume_data.get("education", "")
    }

    st.subheader("Complete Your Profile")

    # Skills
    missing_info["skills"] = st.text_input("Skills (comma-separated):", missing_info["skills"])

    # Work Experience
    num_experiences = max(len(missing_info["work_experience"]), st.number_input("Number of work experiences:", min_value=0, value=0))
    work_experience_list = []
    for i in range(num_experiences):
        st.write(f"### Experience {i+1}")
        work_experience_list.append({
            "title": st.text_input(f"Title:", key=f"exp_title_{i}"),
            "company": st.text_input(f"Company:", key=f"exp_company_{i}"),
            "start_date": st.date_input(f"Start Date:", key=f"exp_start_{i}"),
            "end_date": st.date_input(f"End Date:", key=f"exp_end_{i}"),
            "description": st.text_area(f"Description:", key=f"exp_desc_{i}")
        })
    missing_info["work_experience"] = work_experience_list

    # Education
    missing_info["education"] = st.text_input("Education:", missing_info["education"])

    # Generate Button
    if st.button("Generate Resume & Prepare Interview"):
        if not job_url:
            st.error("Please enter a job posting URL.")
        else:
            with st.spinner("Processing..."):
                try:
                    # Fetch Job Details
                    job_data = hr_buddy_crew.extract_job_details(job_url)

                    # Fetch Social Profile Data
                    social_profile = fetch_social_data(linkedin_url, github_url)

                    # Generate Tailored Resume
                    tailored_resume = hr_buddy_crew.generate_resume(job_data, social_profile, missing_info)

                    # Prepare Interview Questions
                    interview_questions = hr_buddy_crew.prepare_interview_questions(job_data, tailored_resume)

                    # Save Outputs
                    resume_pdf_path = hr_buddy_crew.save_resume_as_pdf(tailored_resume)
                    interview_pdf_path = hr_buddy_crew.save_interview_as_pdf(interview_questions)

                    # Display Success Message
                    st.success("Resume and interview questions generated successfully!")

                    # Download Buttons
                    st.write("### Download Your Tailored Resume")
                    with open(resume_pdf_path, "rb") as file:
                        st.download_button("Download Resume", file, "tailored_resume.pdf", "application/pdf")

                    st.write("### Download Interview Questions")
                    with open(interview_pdf_path, "rb") as file:
                        st.download_button("Download Questions", file, "interview_questions.pdf", "application/pdf")

                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
