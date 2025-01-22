# HR Buddy: Your AI-Powered HR Assistant

HR Buddy is an AI-powered application designed to streamline the job application process.  It leverages CrewAI to orchestrate multiple agents, each specializing in a specific task, to help users create compelling resumes and prepare for interviews.

## Features

* **Resume Generation:**  Creates a tailored resume based on the job description and user's provided information.
* **Interview Preparation:** Generates insightful interview questions based on the job description and resume.
* **Social Media Integration:**  (Optional) Incorporates information from LinkedIn, GitHub, and other social media profiles to enhance the resume and interview preparation.
* **User-Friendly Interface:**  A Streamlit-based interface provides an intuitive and easy-to-use experience.

## Project Structure
    ```
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
    ```


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