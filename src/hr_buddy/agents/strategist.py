from crewai import Agent
from hr_buddy.utils.resume_generator import ResumeGeneratorTool
import subprocess
import json

class ResumeStrategistAgent:
    def __init__(self):
        self.agent = Agent(
            role="Resume Strategist",
            goal="Generate a tailored, ATS-optimized resume based on job details and user profile.",
            tools=["resume_parsing", "nlp", "template_engine"],
            verbose=True
        )
        self.resume_generator = ResumeGeneratorTool()

    def generate_resume(self, job_details, resume_data, filename="tailored_resume.pdf"):
        """
        Generate a tailored, ATS-optimized resume in PDF format.
        """
        try:
            # Prepare data for resume generation
            resume_data["job_description"] = job_details.get("description", "")

            # Use DeepSeek model via ollama for processing and providing tailored suggestions if necessary
            # You can pass resume data and job details to the model for additional optimization.
            deepseek_input = {
                "job_description": job_details.get("description", ""),
                "resume_data": resume_data
            }

            # Call DeepSeek via subprocess
            result = subprocess.run(
                ["ollama", "run", "deepseek-r1:1.5b"],
                input=json.dumps(deepseek_input), text=True, capture_output=True
            )

            # Process the model's response
            model_output = result.stdout
            print("DeepSeek output:", model_output)

            # Generate the resume PDF using the original resume generator logic
            pdf_path = self.resume_generator._run(
                data=resume_data,
                job_description=job_details.get("description", ""),
                filename=filename
            )

            return pdf_path
        except Exception as e:
            raise Exception(f"Failed to generate tailored resume: {e}")

# Example usage
if __name__ == "__main__":
    strategist = ResumeStrategistAgent()
    job_details = {"description": "We are looking for a Data Scientist with experience in Python and Machine Learning."}
    resume_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "linkedin": "https://linkedin.com/in/johndoe",
        "github": "https://github.com/johndoe",
        "summary": "Dynamic professional with proven expertise in Python and Machine Learning.",
        "skills": ["Python", "Machine Learning", "Data Analysis"],
        "work_experience": [
            {
                "title": "Data Scientist",
                "company": "XYZ Corp",
                "start_date": "Jan 2020",
                "end_date": "Present",
                "description": "Developed machine learning models for predictive analytics."
            }
        ],
        "education": [
            {
                "degree": "MS in Computer Science",
                "field": "Data Science",
                "institution": "ABC University",
                "year": "2019"
            }
        ],
        "certifications": ["Certified Data Scientist", "AWS Machine Learning Specialty"]
    }
    pdf_path = strategist.generate_resume(job_details, resume_data)
    print(f"Resume generated at: {pdf_path}")
