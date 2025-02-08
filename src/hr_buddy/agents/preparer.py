from crewai import Agent
from crewai_tools import RagTool, PDFSearchTool, DOCXSearchTool

class InterviewPreparerAgent:
    def __init__(self):
        self.rag_tool = RagTool()
        self.agent = Agent(
            role="Interview Preparer",
            goal=(
                "Generate tailored interview questions based on job descriptions, industry trends, and candidate backgrounds. "
                "Ensure that questions are challenging yet relevant to the role."
            ),
            backstory=(
                "You are an expert interview coach with extensive experience in HR and talent acquisition. "
                "You analyze job descriptions and candidate profiles to create highly targeted interview questions."
            ),
            tools=[self.rag_tool],
            verbose=True
        )
    
    def generate_questions(self, job_details):
        return [
            "Tell me about yourself.",
            "What are your strengths?",
            "Why should we hire you for this role?"
        ]
