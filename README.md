# HR Buddy: Your AI-Powered HR Assistant

HR Buddy is an AI-powered application designed to streamline the job application process.  It leverages CrewAI to orchestrate multiple agents, each specializing in a specific task, to help users create compelling resumes and prepare for interviews.

## Features

**Main Application:**

* **Job Posting Input:** Enter a job posting URL to automatically extract key details like job title, description, and requirements.
* **Social Media Integration (Optional):** Connect your LinkedIn, GitHub, X (formerly Twitter), and Medium profiles to enrich your application.
* **Resume Upload:** Upload your existing resume for analysis and refinement.  Missing information will be dynamically requested.
* **Premium Resume Generation:** Receive a tailored, high-quality resume optimized for the target job posting.
* **Profile/Resume Management:** Save completed profiles and resumes to your account for future use (requires account signup).
* **Dynamic Information Collection:**  If critical information is missing from your uploaded resume, HR Buddy will prompt you to fill in the gaps using dynamic forms.


**AI-Powered Agents:**

* **Researcher Agent:** Extracts job title, description, and requirements from the job posting URL.
* **Social Media Profiler Agent:** Gathers information from your linked social media profiles to build a comprehensive professional profile.
* **Resume Strategist Agent (Expert Agent):**  Crafts a highly tailored resume optimized for the specific job posting, using data from the Researcher and Social Media Profiler agents.
* **Interview Preparer Agent:** Generates a list of targeted interview questions based on the job description and your resume.


## User Workflow

1. **Job Posting Input:** Provide the job URL.  The Researcher Agent extracts key information.
2. **Social Media Integration (Optional):** Add links to your professional profiles. The Social Media Profiler Agent builds a detailed profile.
3. **Resume Upload:** Upload your resume.  Missing information is flagged, and you'll be prompted to complete it.
4. **Resume Generation:** The Resume Strategist Agent creates a polished, job-specific resume.
5. **Interview Preparation:** The Interview Preparer Agent generates tailored interview questions.
6. **Profile Saving (Optional):** Save your profile and generated resumes for future use (requires account signup).

## Project Structure
    hr-buddy/
    ├── src/
    │   └── hr_buddy/
    │       ├── crew.py             # Main CrewAI code
    │       ├── config/
    │       │   ├── agents.yaml      # Agent configurations
    │       │   └── tasks.yaml       # Task configurations
    │       └── utils/              # Helper functions (optional)
    │           └── ...
    ├── tests/                       # Unit tests (optional)
    │   └── ...
    ├── .env                         # Environment variables
    ├── .gitignore
    ├── README.md
    └── requirements.txt           # Project dependencies


## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   ```

2. **Create a virtual environment:**
   ```
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:** Create a `.env` file and add your API keys (e.g., OpenAI API key) and any other necessary environment variables.  **Do not commit this file to version control.**  Example:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Run the Streamlit app:**
   ```bash
   streamlit run src/hr_buddy/app.py
   ```

## Usage

1. Open the Streamlit app in your web browser.
2. Enter the job URL and optionally provide your LinkedIn, GitHub profiles, and upload your resume.
3. Click "Generate Resume & Prepare Interview".
4. The app will display the generated resume and interview questions.

## Agents

* **Researcher:** Extracts job title, requirements, and other relevant information from the job posting URL.
* **Resume Strategist:** Tailors the resume to match the job requirements, using the information gathered by the Researcher and the user-provided resume.
* **Interview Preparer:** Generates interview questions based on the job description and resume.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

[Specify your license here]


## Contact

[Your contact information]