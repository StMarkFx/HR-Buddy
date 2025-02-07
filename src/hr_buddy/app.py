import os
import streamlit as st
from utils.resume_generator import ResumeGeneratorTool

# Initialize Resume Generator
resume_tool = ResumeGeneratorTool()

def main():
    st.set_page_config(page_title="ATS Resume Generator", layout="centered")
    st.title("📄 AI-Powered ATS Resume Generator")
    st.write("Generate a customized, ATS-optimized resume tailored to a job description.")

    # Personal Information
    st.header("📝 Personal Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn URL")
    github = st.text_input("GitHub URL (Optional)")
    summary = st.text_area("Professional Summary", "Experienced professional with expertise in...")

    # Skills
    skills_list = [skill.strip() for skill in st.text_area("Skills (comma-separated)", "Python, Data Science, Machine Learning").split(",")]

    # Work Experience
    st.header("💼 Work Experience")
    work_experience = [
        {"title": st.text_input(f"Job Title {i+1}"),
         "company": st.text_input(f"Company {i+1}"),
         "start_date": st.text_input(f"Start Date {i+1}"),
         "end_date": st.text_input(f"End Date {i+1}"),
         "description": st.text_area(f"Job Description {i+1}")}
        for i in range(st.number_input("How many jobs do you want to add?", min_value=0, max_value=5, step=1))
    ]

    # Education
    st.header("🎓 Education")
    education = [
        {"degree": st.text_input(f"Degree {i+1}"),
         "field": st.text_input(f"Field of Study {i+1}"),
         "institution": st.text_input(f"Institution {i+1}"),
         "year": st.text_input(f"Graduation Year {i+1}")}
        for i in range(st.number_input("How many degrees do you want to add?", min_value=0, max_value=3, step=1))
    ]

    # Certifications
    st.header("🏅 Certifications")
    certifications_list = [cert.strip() for cert in st.text_area("List your certifications (comma-separated)").split(",")]

    # Job Description Upload
    st.header("📄 Upload Job Description (Optional)")
    uploaded_file = st.file_uploader("Upload a job description text file", type=["txt"])
    job_description = uploaded_file.read().decode("utf-8") if uploaded_file else ""
    if job_description:
        st.text_area("Job Description Content", job_description, height=150)

    # Generate Resume
    if st.button("Generate Resume"):
        user_data = {
            "name": name, "email": email, "phone": phone,
            "linkedin": linkedin, "github": github, "summary": summary,
            "skills": skills_list, "work_experience": work_experience,
            "education": education, "certifications": certifications_list
        }
        output_file = "generated_resume.pdf"
        file_path = resume_tool._run(user_data, job_description, output_file)

        if os.path.exists(file_path):
            st.success("🎉 Resume generated successfully!")
            with open(file_path, "rb") as pdf_file:
                st.download_button(label="📥 Download Resume", data=pdf_file, file_name=output_file, mime="application/pdf")
        else:
            st.error("Something went wrong while generating the resume.")

if __name__ == "__main__":
    main()
