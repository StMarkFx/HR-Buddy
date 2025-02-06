import requests
from bs4 import BeautifulSoup

class SocialProfiler:
    """Extracts key details from LinkedIn and GitHub profiles."""

    @staticmethod
    def scrape_github_profile(url: str) -> dict:
        """Fetches basic profile info from a public GitHub profile."""
        if not url.endswith("/"):
            url += "/"

        response = requests.get(url)
        if response.status_code != 200:
            return {"error": "GitHub profile not accessible"}

        soup = BeautifulSoup(response.text, "html.parser")
        name = soup.find("span", class_="p-name").text.strip() if soup.find("span", class_="p-name") else None
        bio = soup.find("div", class_="p-note").text.strip() if soup.find("div", class_="p-note") else None

        return {"name": name, "bio": bio, "profile_url": url}

    @staticmethod
    def scrape_linkedin_profile(url: str) -> dict:
        """Fetches basic profile info from a public LinkedIn profile."""
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return {"error": "LinkedIn profile not accessible"}

        soup = BeautifulSoup(response.text, "html.parser")
        name = soup.find("title").text.strip() if soup.find("title") else None

        return {"name": name, "profile_url": url}
