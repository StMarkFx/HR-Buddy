import os
import streamlit as st
from agents.researcher import ResearcherAgent
from agents.profiler import SocialMediaProfilerAgent
from agents.strategist import ResumeStrategistAgent
from agents.preparer import InterviewPreparerAgent

# Initialize Agents
researcher = ResearcherAgent()
social_profiler = SocialMediaProfilerAgent()
resume_strategist = ResumeStrategistAgent()
interview_preparer = InterviewPreparerAgent()

def main():
    st.set_page_config(page_title="AI Resume & Interview Prep", layout="centered")
    st.title("📄 AI-Powered Resume Enhancement & Interview Prep")
    st.write("Optimize your resume based on a job posting and get interview questions tailored to the role.")
    
    # User Inputs
    st.header("🔗 Job & Profile Links")
    job_url = st.text_input("Job Posting URL")
    linkedin_url = st.text_input("LinkedIn Profile URL (Optional)")
    github_url = st.text_input("GitHub Profile URL (Optional)")
    
    # Resume Upload
    st.header("📄 Upload Your Resume")
    uploaded_resume = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    
    if st.button("Analyze & Optimize"):
        if not job_url or not uploaded_resume:
            st.error("Please provide a job posting URL and upload your resume.")
            return
        
        with st.spinner("Extracting job details..."):
            job_details = researcher.extract_job_details(job_url)
        
        social_data = {}
        if linkedin_url or github_url:
            with st.spinner("Extracting social media insights..."):
                social_data = social_profiler.extract_profiles(linkedin_url, github_url)
        
        with st.spinner("Analyzing your resume..."):
            resume_analysis = resume_strategist.analyze_resume(uploaded_resume, job_details, social_data)
        
        with st.spinner("Generating interview questions..."):
            interview_questions = interview_preparer.generate_questions(job_details)
        
        # Display Results
        st.success("✅ Analysis Complete! Download your optimized resume and review interview questions.")
        
        if resume_analysis.get("optimized_resume"):
            st.download_button(
                label="📥 Download Optimized Resume",
                data=resume_analysis["optimized_resume"],
                file_name="optimized_resume.pdf",
                mime="application/pdf"
            )
        
        st.header("🎤 Suggested Interview Questions")
        for idx, question in enumerate(interview_questions, 1):
            st.write(f"{idx}. {question}")
    
if __name__ == "__main__":
    main()
