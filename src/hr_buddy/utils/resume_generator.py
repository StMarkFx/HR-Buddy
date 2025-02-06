import os
import re
import nltk
from nltk.corpus import stopwords
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from jinja2 import Template
from crewai.tools import BaseTool

nltk.download("stopwords")

class ResumeGeneratorTool(BaseTool):
    name: str = "ResumeGenerator"
    description: str = "Generates a tailored, ATS-optimized resume."
    llm: str = os.getenv("OPENAI_API_KEY")  # Placeholder for LLM integration (optional)

    def _run(self, data: dict, job_description: str = None, filename: str = "tailored_resume.pdf") -> str:
        """
        Generates an ATS-optimized resume based on user data and job description.

        Parameters:
        - data (dict): User profile data (name, work experience, skills, etc.).
        - job_description (str): Job description for keyword extraction (optional).
        - filename (str): Name of the output PDF file.

        Returns:
        - str: Path to the generated PDF file.
        """
        try:
            # Extract Job-Specific Keywords
            keywords = self._extract_keywords(job_description) if job_description else []

            # Resume Template
            resume_template = """
                <b>{{ name }}</b><br/>
                {{ email }} | {{ phone }} | 
                {% if linkedin %} <a href="{{ linkedin }}">LinkedIn</a> {% endif %}
                {% if github %} | <a href="{{ github }}">GitHub</a> {% endif %}
                <br/><br/>

                <b>Summary</b><br/>
                {{ summary }}<br/><br/>

                <b>Skills</b><br/>
                {{ skills|join(', ') }}<br/><br/>

                <b>Work Experience</b><br/>
                {% for experience in work_experience %}
                <b>{{ experience['title'] }}</b> - {{ experience['company'] }}<br/>
                {{ experience['start_date'] }} - {{ experience['end_date'] }}<br/>
                {{ experience['description'] }}<br/><br/>
                {% endfor %}

                <b>Education</b><br/>
                {% for education in education %}
                <b>{{ education['degree'] }}</b> in {{ education['field'] }}<br/>
                {{ education['institution'] }} | Graduated: {{ education['year'] }}<br/><br/>
                {% endfor %}

                <b>Certifications</b><br/>
                {% for certification in certifications %}
                - {{ certification }}<br/>
                {% endfor %}
            """

            # Render Template with User Data
            template = Template(resume_template)
            resume_text = template.render(
                name=data.get("name", "Name Not Provided"),
                email=data.get("email", "Email Not Provided"),
                phone=data.get("phone", "Phone Not Provided"),
                linkedin=data.get("linkedin"),
                github=data.get("github"),
                summary=data.get("summary", "Dynamic professional with proven expertise."),
                skills=data.get("skills", []),
                work_experience=data.get("work_experience", []),
                education=data.get("education", []),
                certifications=data.get("certifications", []),
            )

            # Optimize for ATS
            ats_optimized_text = self._optimize_for_ats(resume_text, keywords)

            # Generate PDF
            file_path = self._generate_pdf(ats_optimized_text, filename)

            return file_path
        except Exception as e:
            return f"Error generating resume: {str(e)}"

    def _extract_keywords(self, job_description: str) -> list:
        """
        Extracts important keywords from a job description.

        Parameters:
        - job_description (str): The job description text.

        Returns:
        - list: Extracted job-relevant keywords.
        """
        stop_words = set(stopwords.words("english"))
        words = re.findall(r'\b\w+\b', job_description.lower())
        return [word for word in words if word not in stop_words and len(word) > 2]

    def _optimize_for_ats(self, text: str, keywords: list) -> str:
        """
        Enhances the resume with ATS-friendly keyword optimization.

        Parameters:
        - text (str): Original resume text.
        - keywords (list): Extracted keywords from job description.

        Returns:
        - str: Enhanced resume text with ATS optimization.
        """
        missing_keywords = [kw.capitalize() for kw in keywords if kw not in text.lower()]
        if missing_keywords:
            text += f"\n\n<b>ATS Keywords:</b> {', '.join(missing_keywords)}"
        return text

    def _generate_pdf(self, text: str, filename: str) -> str:
        """
        Generates a formatted PDF from resume text.

        Parameters:
        - text (str): Resume text formatted using HTML-like tags.
        - filename (str): Output PDF file name.

        Returns:
        - str: Path to the generated PDF.
        """
        file_path = os.path.join(os.getcwd(), filename)
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []

        for section in text.split("\n\n"):
            content.append(Paragraph(section.strip(), styles["Normal"]))
            content.append(Spacer(1, 12))

        doc.build(content)
        return file_path
