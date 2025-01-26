import streamlit as st
from hr_buddy.crew import HRBuddyCrew

# Streamlit App
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
        if not job_url:
            st.error("Please enter a job posting URL.")
        else:
            st.write("Processing...")

            # Initialize the HRBuddyCrew
            hr_buddy_crew = HRBuddyCrew()

            # Run the crew
            try:
                results = hr_buddy_crew.run_crew(job_url, linkedin_url, github_url, resume_file)

                # Display Results
                st.success("Resume and interview questions generated successfully!")

                # Download Links
                st.write("### Download Your Tailored Resume")
                with open(results["resume_pdf_path"], "rb") as file:
                    st.download_button(
                        label="Download Resume",
                        data=file,
                        file_name="tailored_resume.pdf",
                        mime="application/pdf"
                    )

                st.write("### Download Interview Questions")
                with open(results["interview_pdf_path"], "rb") as file:
                    st.download_button(
                        label="Download Interview Questions",
                        data=file,
                        file_name="interview_questions.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()