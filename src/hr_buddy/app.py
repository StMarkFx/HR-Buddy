import streamlit as st
from hr_buddy.crew import HRBuddyCrew  # Adjust import path as needed

st.title("HR Buddy")

# Input fields for user data
job_url = st.text_input("Job URL:")
linkedin_url = st.text_input("LinkedIn Profile URL (Optional):")
github_url = st.text_input("GitHub Profile URL (Optional):")
resume = st.file_uploader("Upload Resume (Optional):", type=["pdf", "docx"])

if st.button("Generate Resume & Prepare Interview"):
    inputs = {
        "job_url": job_url,
        "linkedin_url": linkedin_url,
        "github_url": github_url,
        "resume": resume,  # Handle resume upload appropriately
    }

    try:
        crew = HRBuddyCrew()
        results = crew.run(inputs)

        # Display results (customize this section based on your agent outputs)
        st.subheader("Generated Resume:")
        st.text(results.get("resume", "Resume generation failed.")) # Access resume from results

        st.subheader("Interview Questions:")
        interview_questions = results.get("interview_questions", [])
        if interview_questions:
            for question in interview_questions:
                st.write(f"- {question}")
        else:
            st.write("Interview question generation failed.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
