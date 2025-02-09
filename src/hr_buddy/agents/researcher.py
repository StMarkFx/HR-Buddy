from crewai import Agent
from crewai_tools import ScrapeWebsiteTool

class ResearcherAgent:
    def __init__(self):
        self.tool = ScrapeWebsiteTool()
        self.agent = Agent(
            role="Job Researcher",
            goal=(
                "Extract detailed job requirements, qualifications, and expectations from a given job posting URL. "
                "Ensure all responsibilities, preferred skills, and necessary experience are captured accurately."
            ),
            backstory=(
                "You are a highly skilled job researcher with deep expertise in web scraping. "
                "Your job is to gather critical details from job postings and structure them in a way that helps candidates "
                "optimize their resumes and prepare for interviews."
            ),
            tools=[self.tool],
            verbose=True
        )
    
    def extract_job_details(self, url):
        return self.tool.run(url)
