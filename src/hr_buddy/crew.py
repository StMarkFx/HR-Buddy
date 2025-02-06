import sys
import traceback
from pathlib import Path
import logging
from typing import Optional, Dict, Any
from crewai import Crew, Task

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
        """Initialize HR Buddy Crew class (lazy agent instantiation)."""
        pass  # Instantiate agents only when needed

    def extract_job_details(self, job_url: str) -> Dict[str, Any]:
        """Extract job details using the ResearcherAgent."""
        try:
            researcher = ResearcherAgent()
            job_details = researcher.extract_job_details(job_url)
            if not job_details:
                raise ValueError("Job details extraction failed.")
            return job_details
        except Exception as e:
            logger.error(f"Error extracting job details: {e}")
            logger.debug(traceback.format_exc())
            raise

    def fetch_social_profiles(self, linkedin_url: Optional[str], github_url: Optional[str]) -> Dict[str, Any]:
        """Fetch LinkedIn and GitHub profile data."""
        profiler = SocialMediaProfilerAgent()
        return {
            "linkedin": profiler.fetch_linkedin_profile(linkedin_url) if linkedin_url else None,
            "github": profiler.fetch_github_profile(github_url) if github_url else None
        }

    def parse_resume(self, resume_file: str, missing_info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Parse and update resume data."""
        try:
            strategist = ResumeStrategistAgent()
            resume_data = strategist.agent.tools["resume_parsing"].parse_resume(resume_file)

            # Ensure missing_info is merged correctly
            if missing_info:
                for key, value in missing_info.items():
                    if key not in resume_data or not resume_data[key]:  # Fill only missing fields
                        resume_data[key] = value

            return resume_data
        except Exception as e:
            logger.error(f"Error parsing resume: {e}")
            logger.debug(traceback.format_exc())
            raise

    def generate_resume(self, job_details: Dict[str, Any], resume_data: Dict[str, Any]) -> str:
        """Generate a tailored resume."""
        strategist = ResumeStrategistAgent()
        resume_pdf_path = strategist.generate_resume(job_details, resume_data, filename="tailored_resume.pdf")
        return resume_pdf_path

    def generate_interview_questions(self, job_details: Dict[str, Any], resume_data: Dict[str, Any]) -> str:
        """Generate interview questions and save as a PDF."""
        preparer = InterviewPreparerAgent()
        interview_questions = preparer.generate_questions(job_details, resume_data)
        interview_pdf_path = preparer.generate_questions_pdf(interview_questions, filename="interview_questions.pdf")
        return interview_pdf_path

    def run_crew(self, job_url: str, linkedin_url: Optional[str] = None, github_url: Optional[str] = None,
                 resume_file: Optional[str] = None, missing_info: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Orchestrate the multi-agent process to generate a tailored resume and interview questions.
        """
        try:
            logger.info("🔍 Extracting job details...")
            job_details = self.extract_job_details(job_url)

            logger.info("📢 Fetching social media profiles...")
            social_profiles = self.fetch_social_profiles(linkedin_url, github_url)

            resume_data = {}
            if resume_file:
                logger.info("📄 Parsing resume...")
                resume_data = self.parse_resume(resume_file, missing_info)

            logger.info("✍️ Generating tailored resume...")
            resume_pdf_path = self.generate_resume(job_details, resume_data)

            logger.info("🎤 Generating interview questions...")
            interview_pdf_path = self.generate_interview_questions(job_details, resume_data)

            logger.info("✅ HR Buddy Crew execution completed successfully.")
            return {"resume_pdf_path": resume_pdf_path, "interview_pdf_path": interview_pdf_path}

        except Exception as e:
            logger.error(f"🚨 Crew execution failed: {e}")
            logger.debug(traceback.format_exc())
            raise


# Example usage
if __name__ == "__main__":
    try:
        hr_buddy_crew = HRBuddyCrew()

        results = hr_buddy_crew.run_crew(
            job_url="https://example.com/job-posting",
            linkedin_url="https://linkedin.com/in/username",
            github_url="https://github.com/username",
            resume_file="path/to/resume.pdf",
            missing_info={"skills": "Python, Machine Learning", "education": "BSc in Computer Science"},
        )

        print("Resume PDF Path:", results["resume_pdf_path"])
        print("Interview Questions PDF Path:", results["interview_pdf_path"])

    except Exception as e:
        print(f"An error occurred: {e}")
