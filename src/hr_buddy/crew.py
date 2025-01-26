from crewai import Crew, Task
from hr_buddy.agents.researcher import ResearcherAgent
from hr_buddy.agents.profiler import SocialMediaProfilerAgent
from hr_buddy.agents.strategist import ResumeStrategistAgent
from hr_buddy.agents.preparer import InterviewPreparerAgent
from hr_buddy.utils.resume_generator import ResumeGeneratorTool

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
            resume_data = self.strategist.agent.tools["resume_parsing"].parse_resume(resume_file) if resume_file else None

            # Step 4: Generate a tailored resume using the Strategist Agent
            resume_pdf_path = self.strategist.generate_resume(job_details, resume_data, filename="tailored_resume.pdf")

            # Step 5: Generate interview questions using the Preparer Agent
            interview_questions = self.preparer.generate_questions(job_details, resume_data)

            # Step 6: Generate interview questions PDF
            interview_pdf_path = self._generate_interview_pdf(interview_questions, filename="interview_questions.pdf")

            # Return the results
            return {
                "resume_pdf_path": resume_pdf_path,
                "interview_pdf_path": interview_pdf_path
            }
        except Exception as e:
            raise Exception(f"An error occurred during crew execution: {e}")

    def _generate_interview_pdf(self, questions, filename="interview_questions.pdf"):
        """
        Generate a PDF file for the interview questions.
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas

            c = canvas.Canvas(filename, pagesize=letter)
            y_position = 11 * inch

            c.drawString(1 * inch, y_position, "Interview Questions:")
            y_position -= 0.5 * inch

            for question in questions:
                if y_position <= 1 * inch:  # Prevent text from going outside the page
                    c.showPage()
                    y_position = 11 * inch
                c.drawString(1 * inch, y_position, question)
                y_position -= 0.25 * inch

            c.save()
            return filename
        except Exception as e:
            raise Exception(f"Failed to generate interview questions PDF: {e}")

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