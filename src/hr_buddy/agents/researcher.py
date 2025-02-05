from bs4 import BeautifulSoup
import requests
from crewai import Agent
import subprocess
import json

class ResearcherAgent:
    def __init__(self):
        self.agent = Agent(
            role="Researcher",
            goal="Extract job details from the job posting URL",
            tools=["web_scraping"],
            verbose=True
        )

    def extract_job_details(self, job_url):
        """
        Extract job details from the given job posting URL and process it using DeepSeek.
        """
        try:
            # Fetch the job posting page
            response = requests.get(job_url)
            response.raise_for_status()  # Raise an error for bad status codes

            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract job details (customize selectors based on the job board)
            title = soup.find("h1").text.strip()
            description = soup.find("div", class_="job-description").text.strip()
            requirements = soup.find("div", class_="job-requirements").text.strip()

            # Use DeepSeek to refine the job description if needed (or for additional NLP tasks)
            deepseek_input = {
                "title": title,
                "description": description,
                "requirements": requirements
            }

            # Call DeepSeek via subprocess
            result = subprocess.run(
                ["ollama", "run", "deepseek-r1:1.5b"],
                input=json.dumps(deepseek_input), text=True, capture_output=True
            )

            # Process the model's response
            model_output = result.stdout
            print("DeepSeek output:", model_output)

            # Return the extracted job details
            return {
                "title": title,
                "description": description,
                "requirements": requirements,
                "processed_details": model_output  # You can process the model's output as needed
            }

        except Exception as e:
            raise Exception(f"Failed to extract job details: {e}")

# Example usage
if __name__ == "__main__":
    researcher = ResearcherAgent()
    job_details = researcher.extract_job_details("https://example.com/job-posting")
    print(job_details)
