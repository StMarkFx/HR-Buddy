import streamlit as st
from hr_buddy.crew import run_crew  # Import CrewAI orchestration

# Streamlit UI
def main():
    st.title("HR Buddy: AI-Powered HR Assistant")

    # Job Posting Input
    job_url = st.text_input("Enter Job Posting URL")

    # Social Media Integration
    linkedin_url = st.text_input("Enter LinkedIn Profile URL (Optional)")
    github_url = st.text_input("Enter GitHub Profile URL (Optional)")

    # Resume Upload
    resume_file = st.file_uploader("Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])

    # Generate Button
    if st.button("Generate Resume & Prepare Interview"):
        st.write("Processing...")
        
        # Call CrewAI backend
        results = run_crew(job_url, linkedin_url, github_url, resume_file)
        
        # Display Results
        st.write("Generated Resume:")
        st.write(results["resume"])
        
        st.write("Interview Questions:")
        st.write(results["interview_questions"])

if __name__ == "__main__":
    main()