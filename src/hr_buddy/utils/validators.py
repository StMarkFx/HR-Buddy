import re

def is_valid_url(url: str) -> bool:
    """Validates if a given string is a properly formatted URL."""
    regex = re.compile(
        r'^(https?:\/\/)?'  # Optional HTTP/HTTPS
        r'([\da-z\.-]+)\.([a-z\.]{2,6})'  # Domain
        r'([\/\w \.-]*)*\/?$'  # Path
    )
    return bool(re.match(regex, url))

def is_valid_linkedin_url(url: str) -> bool:
    """Validates a LinkedIn profile URL."""
    regex = re.compile(r"^https:\/\/(www\.)?linkedin\.com\/in\/[a-zA-Z0-9-_%]+\/?$")
    return bool(re.match(regex, url))

def is_valid_github_url(url: str) -> bool:
    """Validates a GitHub profile URL."""
    regex = re.compile(r"^https:\/\/(www\.)?github\.com\/[a-zA-Z0-9-]+\/?$")
    return bool(re.match(regex, url))
