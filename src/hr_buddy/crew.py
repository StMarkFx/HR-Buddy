from crewai import Crew, Task
import sys
from pathlib import Path
# Add the src/ directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))
from hr_buddy.agents.researcher import ResearcherAgent
from hr_buddy.agents.profiler import SocialMediaProfilerAgent
from hr_buddy.agents.strategist import ResumeStrategistAgent
from hr_buddy.agents.preparer import InterviewPreparerAgent

class HRBuddyCrew:
    def __init__(self):
        # Initialize all agents
        self.researcher = ResearcherAgent()
        self.profiler = SocialMediaProfilerAgent()
        self.strategist = ResumeStrategistAgent()
        self.preparer = InterviewPreparerAgent()

    def run_crew(self, job_url, linkedin_url=None, github_url=None, resume_file=None):
        """
        Orchestrate the multi-agent system to generate a tailored resume and interview questions.
        """
        try:
            # Step 1: Extract job details using the Researcher Agent
            job_details = self.researcher.extract_job_details(job_url)

            # Step 2: Gather social media profile data using the Profiler Agent
            linkedin_data = self.profiler.fetch_linkedin_profile(linkedin_url) if linkedin_url else None
            github_data = self.profiler.fetch_github_profile(github_url) if github_url else None

            # Step 3: Parse the uploaded resume (if provided)
            resume_data = self.strategist.agent.tools["resume_parsing"].parse_resume(resume_file) if resume_file else {}
            if missing_info:
                resume_data.update(missing_info) # Update resume_data with missing information

            # Step 4: Generate a tailored resume using the Strategist Agent
            resume_pdf_path = self.strategist.generate_resume(job_details, resume_data, filename="tailored_resume.pdf")

            # Step 5: Generate interview questions using the Preparer Agent
            interview_questions = self.preparer.generate_questions(job_details, resume_data)

            # Step 6: Generate interview questions PDF
            interview_pdf_path = self.preparer.generate_questions_pdf(interview_questions, filename="interview_questions.pdf")

            # Return the results
            return {
                "resume_pdf_path": resume_pdf_path,
                "interview_pdf_path": interview_pdf_path
            }
        except Exception as e:
            raise Exception(f"An error occurred during crew execution: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize the crew
    hr_buddy_crew = HRBuddyCrew()

    # Run the crew with sample inputs
    results = hr_buddy_crew.run_crew(
        job_url="https://example.com/job-posting",
        linkedin_url="https://linkedin.com/in/username",
        github_url="https://github.com/username",
        resume_file="path/to/resume.pdf"
    )

    # Display the results
    print("Resume PDF Path:", results["resume_pdf_path"])
    print("Interview Questions PDF Path:", results["interview_pdf_path"])