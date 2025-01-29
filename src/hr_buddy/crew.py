import sys
from pathlib import Path
import logging
from typing import Optional, Dict, Any
from crewai import Crew, Task

# Add the src/ directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

# Import agents
from hr_buddy.agents.researcher import ResearcherAgent
from hr_buddy.agents.profiler import SocialMediaProfilerAgent
from hr_buddy.agents.strategist import ResumeStrategistAgent
from hr_buddy.agents.preparer import InterviewPreparerAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class HRBuddyCrew:
    def __init__(self):
        """
        Initialize all agents required for the HR Buddy crew.
        """
        self.researcher = ResearcherAgent()
        self.profiler = SocialMediaProfilerAgent()
        self.strategist = ResumeStrategistAgent()
        self.preparer = InterviewPreparerAgent()

    def run_crew(
        self,
        job_url: str,
        linkedin_url: Optional[str] = None,
        github_url: Optional[str] = None,
        resume_file: Optional[str] = None,
        missing_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, str]:
        """
        Orchestrate the multi-agent system to generate a tailored resume and interview questions.

        Args:
            job_url (str): URL of the job posting.
            linkedin_url (Optional[str]): LinkedIn profile URL (optional).
            github_url (Optional[str]): GitHub profile URL (optional).
            resume_file (Optional[str]): Path to the uploaded resume file (optional).
            missing_info (Optional[Dict[str, Any]]): Missing information to update in the resume data.

        Returns:
            Dict[str, str]: Paths to the generated resume and interview questions PDFs.

        Raises:
            Exception: If any step in the process fails.
        """
        try:
            logger.info("Starting HR Buddy Crew execution...")

            # Step 1: Extract job details using the Researcher Agent
            logger.info("Extracting job details...")
            job_details = self.researcher.extract_job_details(job_url)
            if not job_details:
                raise ValueError("Failed to extract job details from the provided URL.")

            # Step 2: Gather social media profile data using the Profiler Agent
            logger.info("Fetching social media profiles...")
            linkedin_data = (
                self.profiler.fetch_linkedin_profile(linkedin_url) if linkedin_url else None
            )
            github_data = (
                self.profiler.fetch_github_profile(github_url) if github_url else None
            )

            # Step 3: Parse the uploaded resume (if provided)
            resume_data = {}
            if resume_file:
                logger.info("Parsing resume...")
                resume_data = self.strategist.agent.tools["resume_parsing"].parse_resume(resume_file)
                if missing_info:
                    logger.info("Updating resume data with missing information...")
                    resume_data.update(missing_info)

            # Step 4: Generate a tailored resume using the Strategist Agent
            logger.info("Generating tailored resume...")
            resume_pdf_path = self.strategist.generate_resume(
                job_details, resume_data, filename="tailored_resume.pdf"
            )

            # Step 5: Generate interview questions using the Preparer Agent
            logger.info("Generating interview questions...")
            interview_questions = self.preparer.generate_questions(job_details, resume_data)

            # Step 6: Generate interview questions PDF
            logger.info("Creating interview questions PDF...")
            interview_pdf_path = self.preparer.generate_questions_pdf(
                interview_questions, filename="interview_questions.pdf"
            )

            logger.info("HR Buddy Crew execution completed successfully.")
            return {
                "resume_pdf_path": resume_pdf_path,
                "interview_pdf_path": interview_pdf_path,
            }

        except Exception as e:
            logger.error(f"An error occurred during crew execution: {e}")
            raise Exception(f"Crew execution failed: {e}")


# Example usage
if __name__ == "__main__":
    try:
        # Initialize the crew
        hr_buddy_crew = HRBuddyCrew()

        # Run the crew with sample inputs
        results = hr_buddy_crew.run_crew(
            job_url="https://example.com/job-posting",
            linkedin_url="https://linkedin.com/in/username",
            github_url="https://github.com/username",
            resume_file="path/to/resume.pdf",
            missing_info={"skills": "Python, Machine Learning", "education": "BSc in Computer Science"},
        )

        # Display the results
        print("Resume PDF Path:", results["resume_pdf_path"])
        print("Interview Questions PDF Path:", results["interview_pdf_path"])

    except Exception as e:
        print(f"An error occurred: {e}")