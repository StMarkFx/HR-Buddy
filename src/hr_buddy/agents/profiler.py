import requests
from crewai import Agent

class SocialMediaProfilerAgent:
    def __init__(self):
        self.agent = Agent(
            role="Social Media Profiler",
            goal="Gather professional information from LinkedIn and GitHub profiles",
            tools=["social_media_api"],
            verbose=True
        )

    def fetch_linkedin_profile(self, linkedin_url):
        """
        Fetch LinkedIn profile data using the LinkedIn API.
        """
        try:
            # Example LinkedIn API endpoint (replace with actual API logic)
            linkedin_api_url = f"https://api.linkedin.com/v2/me?url={linkedin_url}"
            headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}  # Add proper authentication
            response = requests.get(linkedin_api_url, headers=headers)
            response.raise_for_status()
            return response.json()  # Assuming the API returns JSON
        except Exception as e:
            raise Exception(f"Failed to fetch LinkedIn profile: {e}")

    def fetch_github_profile(self, github_url):
        """
        Fetch GitHub profile data using the GitHub API.
        """
        try:
            # GitHub API URL format (replace with actual API logic)
            github_api_url = f"https://api.github.com/users/{github_url.split('/')[-1]}"
            response = requests.get(github_api_url)
            response.raise_for_status()
            return response.json()  # Assuming the API returns JSON
        except Exception as e:
            raise Exception(f"Failed to fetch GitHub profile: {e}")

# Example usage
if __name__ == "__main__":
    profiler = SocialMediaProfilerAgent()
    linkedin_url = "https://linkedin.com/in/username"
    github_url = "https://github.com/username"
    
    try:
        linkedin_data = profiler.fetch_linkedin_profile(linkedin_url)
        github_data = profiler.fetch_github_profile(github_url)
        print("LinkedIn Profile Data:", linkedin_data)
        print("GitHub Profile Data:", github_data)
    except Exception as e:
        print(f"Error: {e}")
