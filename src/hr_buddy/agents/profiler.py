import requests
from crewai import Agent

class SocialMediaProfilerAgent:
    def __init__(self):
        self.agent = Agent(
            role="Social Media Profiler",
            goal="Gather professional information from linked social media profiles",
            tools=["social_media_api"],
            verbose=True
        )

    def fetch_linkedin_profile(self, linkedin_url):
        """
        Fetch LinkedIn profile data using the LinkedIn API.
        """
        try:
            # Replace with actual LinkedIn API call
            response = requests.get(linkedin_url)
            response.raise_for_status()
            return response.json()  # Assuming the API returns JSON
        except Exception as e:
            raise Exception(f"Failed to fetch LinkedIn profile: {e}")

    def fetch_github_profile(self, github_url):
        """
        Fetch GitHub profile data using the GitHub API.
        """
        try:
            # Replace with actual GitHub API call
            response = requests.get(github_url)
            response.raise_for_status()
            return response.json()  # Assuming the API returns JSON
        except Exception as e:
            raise Exception(f"Failed to fetch GitHub profile: {e}")

# Example usage
if __name__ == "__main__":
    profiler = SocialMediaProfilerAgent()
    linkedin_data = profiler.fetch_linkedin_profile("https://linkedin.com/in/username")
    github_data = profiler.fetch_github_profile("https://github.com/username")
    print(linkedin_data, github_data)