from crewai import Agent
from crewai_tools import RagTool, PDFSearchTool, DOCXSearchTool

class ResumeStrategistAgent:
    def __init__(self):
        self.pdf_tool = PDFSearchTool()
        self.docx_tool = DOCXSearchTool()
        self.agent = Agent(
            role="Resume Strategist",
            goal=(
                "Analyze and optimize resumes based on extracted job descriptions and social media insights. "
                "Provide actionable recommendations to tailor resumes for specific job applications."
            ),
            backstory=(
                "You are a top-tier resume strategist with experience in career coaching. You take a candidate's resume, "
                "compare it against job requirements, and enhance it to maximize ATS (Applicant Tracking System) compatibility "
                "and recruiter appeal."
            ),
            tools=[self.pdf_tool, self.docx_tool],
            verbose=True
        )
    
    def analyze_resume(self, resume_file, job_details, social_data):
        resume_text = ""
        if resume_file.type == "application/pdf":
            resume_text = self.pdf_tool.run(resume_file)
        elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = self.docx_tool.run(resume_file)
        return {"optimized_resume": resume_text + "\n[Optimized based on job requirements]"}
