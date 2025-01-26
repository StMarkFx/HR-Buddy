import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from jinja2 import Template
from crewai.tools import BaseTool

class ResumeGeneratorTool(BaseTool):
    name: str = "ResumeGenerator"
    description: str = "Generates a tailored, ATS-optimized resume."
    llm: str = os.getenv("OPENAI_API_KEY")  # OpenAI API key for additional data enhancement (optional)

    def _run(self, data: dict, job_description: str = None, filename: str = "premium_resume.pdf") -> str:
        """
        Generates an ATS-optimized resume based on provided data and job description.

        Parameters:
        - data (dict): User profile data (name, work experience, skills, etc.).
        - job_description (str): The job description for tailoring the resume (optional).
        - filename (str): The name of the output PDF file.

        Returns:
        - str: Path to the generated PDF file.
        """
        try:
            # Step 1: Extract Keywords from Job Description
            keywords = self._extract_keywords(job_description) if job_description else []

            # Step 2: Prepare Resume Template
            resume_template = """
                {{ name }}
                {{ email }} | {{ phone }} | {{ linkedin if linkedin else '' }} {{ github if github else '' }}

                Summary
                -------
                {{ summary }}

                Skills
                ------
                {% for skill in skills %}
                - {{ skill }}
                {% endfor %}

                Work Experience
                ---------------
                {% for experience in work_experience %}
                {{ experience['title'] }} - {{ experience['company'] }}
                {{ experience['start_date'] }} - {{ experience['end_date'] }}
                {{ experience['description'] }}
                {% endfor %}

                Education
                ---------
                {% for education in education %}
                {{ education['degree'] }} in {{ education['field'] }}
                {{ education['institution'] }} | Graduated: {{ education['year'] }}
                {% endfor %}

                Certifications
                --------------
                {% for certification in certifications %}
                - {{ certification }}
                {% endfor %}
            """

            # Step 3: Render Template with Data
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

            # Step 4: Optimize for ATS
            ats_optimized_text = self._optimize_for_ats(resume_text, keywords)

            # Step 5: Generate PDF
            self._generate_pdf(ats_optimized_text, filename)

            return filename
        except Exception as e:
            return f"Error generating resume: {str(e)}"

    def _extract_keywords(self, job_description: str) -> list:
        """
        Extracts relevant keywords from the job description using simple regex.

        Parameters:
        - job_description (str): The job description text.

        Returns:
        - list: Extracted keywords.
        """
        return re.findall(r'\b\w+\b', job_description.lower())

    def _optimize_for_ats(self, text: str, keywords: list) -> str:
        """
        Optimizes resume text for ATS by including relevant keywords.

        Parameters:
        - text (str): The original resume text.
        - keywords (list): List of relevant keywords.

        Returns:
        - str: ATS-optimized resume text.
        """
        for keyword in keywords:
            if keyword not in text.lower():
                text += f"\nKeyword: {keyword.capitalize()}"
        return text

    def _generate_pdf(self, text: str, filename: str) -> None:
        """
        Generates a PDF file from the provided text.

        Parameters:
        - text (str): The resume text to be added to the PDF.
        - filename (str): The name of the output PDF file.
        """
        c = canvas.Canvas(filename, pagesize=letter)
        text_lines = text.splitlines()
        y_position = 11 * inch

        for line in text_lines:
            if y_position <= 1 * inch:  # Prevent text from going outside the page
                c.showPage()
                y_position = 11 * inch
            c.drawString(1 * inch, y_position, line)
            y_position -= 0.25 * inch

        c.save()