from crewai import Agent
from crewai_tools import GithubSearchTool
from crewai_tools.tools.website_search.website_search_tool import WebsiteSearchTool
from embedchain.embedder.ollama import OllamaEmbedder


class SocialMediaProfilerAgent:
    def __init__(self):
        self.linkedin_tool = WebsiteSearchTool(embedding_model=OllamaEmbedder(model_name="deepseek-r1:1.5b"))
        self.github_tool = GithubSearchTool()
        self.agent = Agent(
            role="Social Media Profiler",
            goal=(
                "Analyze LinkedIn and GitHub profiles to extract relevant work experience, skills, and contributions. "
                "Identify alignment with job requirements based on extracted data."
            ),
            backstory=(
                "You are an expert in professional networking analysis. You analyze LinkedIn profiles to extract "
                "job history, education, and skills. You also scan GitHub profiles to assess coding contributions and technical proficiency."
            ),
            tools=[self.linkedin_tool, self.github_tool],
            verbose=True
        )
    
    def extract_profiles(self, linkedin_url, github_url):
        data = {}
        if linkedin_url:
            data["linkedin"] = self.linkedin_tool.run(linkedin_url)
        if github_url:
            data["github"] = self.github_tool.run(github_url)
        return data
