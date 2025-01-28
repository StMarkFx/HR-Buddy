import streamlit as st
#from crew import HRBuddyCrew

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

    # Dynamic Form Handling for Missing Resume Information
    missing_info = {}  # Store missing information from resume parsing
    if resume_data and missing_info:
        st.subheader("Please complete the following information:")
        for field, value in missing_info.items():
            if field == "skills":
                missing_info[field] = st.text_input(f"Enter your {field} (comma-separated):", value)
            elif field == "work_experience":
                # Add more complex form for work experience
                missing_info[field] = []
                num_experiences = st.number_input("Number of work experiences to add:", min_value=0)
                for i in range(num_experiences):
                    experience = {}
                    experience["title"] = st.text_input(f"Experience {i+1} - Title:")
                    experience["company"] = st.text_input(f"Experience {i+1} - Company:")
                    experience["start_date"] = st.date_input(f"Experience {i+1} - Start Date:")
                    experience["end_date"] = st.date_input(f"Experience {i+1} - End Date:")
                    experience["description"] = st.text_area(f"Experience {i+1} - Description:")
                    missing_info[field].append(experience)
            else:
                missing_info[field] = st.text_input(f"Enter your {field}:", value)



    # Generate Button
    if st.button("Generate Resume & Prepare Interview"):
        if not job_url:
            st.error("Please enter a job posting URL.")
        else:
            st.write("Processing...")

            # Initialize the HRBuddyCrew
            #hr_buddy_crew = HRBuddyCrew()

            # Run the crew
            try:
                #results = hr_buddy_crew.run_crew(job_url, linkedin_url, github_url, resume_file)

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