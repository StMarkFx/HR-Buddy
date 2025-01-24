import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from pydantic import Field
from langchain_community.utilities import GoogleSerperAPIWrapper
from bs4 import BeautifulSoup
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from pyresparser import ResumeParser


load_dotenv() # Load environment variables from .env file (if you have API keys there)

class WebSearchTool(BaseTool):
    name: str = "WebSearch"
    description: str = "Useful for web search queries.  Use this to find information on the web."
    search: GoogleSerperAPIWrapper = Field(default_factory=GoogleSerperAPIWrapper) #Requires langchain_community

    def _run(self, query: str) -> str:
        try:
            results = self.search.run(query) #Use langchain's GoogleSerperAPIWrapper
            return results
        except Exception as e:
            return f"Error performing web search: {str(e)}"

class ResumeGeneratorTool(BaseTool):
    name: str = "ResumeGenerator"
    description: str = "Generates a resume based on provided data.  Input should be a dictionary."
    llm: str = os.getenv("OPENAI_API_KEY") #Requires OpenAI API key

    def _run(self, data: dict) -> str:
        #This is a placeholder.  You'll need to implement a robust resume generation function here.
        #This function should use an LLM (like OpenAI's API) to generate the resume text based on the input data.
        #Consider using templates or examples of well-formatted resumes to guide the LLM.
        #Handle missing data gracefully.
        #Example (replace with your actual LLM integration):
        #import openai
        #response = openai.Completion.create(engine="text-davinci-003", prompt=f"Generate a resume based on this data: {data}", max_tokens=500)
        #resume_text = response.choices[0].text
        #return resume_text
        return "This is a placeholder resume.  Implement your LLM-based resume generation here."

class ResumeParserTool(BaseTool):
    name: str = "ResumeParser"
    description: str = "Parses a resume and extracts key information."

    def _run(self, resume_text: str) -> dict:
        try:
            data = ResumeParser(resume_text).get_extracted_data()
            return data
        except Exception as e:
            return {"error": f"Resume parsing failed: {str(e)}"}

class PDFGeneratorTool(BaseTool):
    name: str = "PDFGenerator"
    description: str = "Generates a PDF document from text."

    def _run(self, text: str, filename: str = "resume.pdf") -> str:
        try:
            c = canvas.Canvas(filename, pagesize=letter)
            text_lines = text.splitlines()
            y_position = 11 * inch
            for line in text_lines:
                c.drawString(1 * inch, y_position, line)
                y_position -= 0.2 * inch
            c.save()
            return filename
        except Exception as e:
            return f"Error generating PDF: {str(e)}"
