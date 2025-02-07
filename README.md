import os
import streamlit as st
from resume_generator import ResumeGeneratorTool
from job_scraper import JobScraper
from profile_scraper import ProfileScraper
from resume_analyzer import ResumeAnalyzer

# Initialize tools
resume_tool = ResumeGeneratorTool()
job_scraper = JobScraper()
profile_scraper = ProfileScraper()
resume_analyzer = ResumeAnalyzer()

def main():
    st.set_page_config(page_title="ATS Resume Generator", layout="centered")
    st.title("📄 AI-Powered ATS Resume Generator")
    st.write("Generate a customized, ATS-optimized resume tailored to a job description.")

    # User Inputs
    st.header("🔗 Input Details")
    job_url = st.text_input("Job Posting URL")
    linkedin = st.text_input("LinkedIn Profile URL (Optional)")
    github = st.text_input("GitHub Profile URL (Optional)")
    resume_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

    if st.button("Analyze & Generate Resume"):
        if not job_url or not resume_file:
            st.error("Please provide a job posting URL and upload your resume.")
            return

        st.info("🔍 Extracting job details...")
        job_details = job_scraper.extract(job_url)
        
        st.info("🔍 Extracting profile insights...")
        profile_data = profile_scraper.extract(linkedin, github)
        
        st.info("📄 Analyzing resume...")
        resume_text = resume_analyzer.parse_resume(resume_file)
        resume_feedback = resume_analyzer.analyze(resume_text, job_details, profile_data)
        
        st.info("📝 Generating optimized resume and interview questions...")
        output_file = "generated_resume.pdf"
        resume_path, interview_questions = resume_tool.generate(resume_feedback, job_details, output_file)

        if os.path.exists(resume_path):
            st.success("🎉 Resume generated successfully!")
            with open(resume_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download Resume", data=pdf_file,
                    file_name=output_file, mime="application/pdf"
                )
            
            st.header("🎤 Interview Preparation")
            for i, question in enumerate(interview_questions, 1):
                st.write(f"{i}. {question}")
        else:
            st.error("Something went wrong while generating the resume.")

if __name__ == "__main__":
    main()
