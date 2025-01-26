from crewai import Agent
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch  # Import inch from reportlab.lib.units
from reportlab.pdfgen import canvas

class InterviewPreparerAgent:
    def __init__(self):
        self.agent = Agent(
            role="Interview Preparer",
            goal="Generate a list of targeted interview questions based on job description and resume.",
            tools=["nlp", "question_generation"],
            verbose=True
        )

    def generate_questions(self, job_details, resume_data):
        """
        Generate a list of targeted interview questions.
        """
        try:
            # Extract keywords from job description and resume
            keywords = set(job_details["requirements"].split() + resume_data["skills"])

            # Generate questions based on keywords
            questions = [
                f"Can you explain your experience with {keyword}?"
                for keyword in keywords
            ]

            return questions
        except Exception as e:
            raise Exception(f"Failed to generate interview questions: {e}")

    def generate_questions_pdf(self, questions, filename="interview_questions.pdf"):
        """
        Generate a PDF file for the interview questions.
        """
        try:
            # Create a PDF canvas
            c = canvas.Canvas(filename, pagesize=letter)

            # Start writing text at the top of the page
            y_position = 10 * inch  # Start 10 inches from the bottom (top of the page)

            # Add a title
            c.drawString(1 * inch, y_position, "Interview Questions:")
            y_position -= 0.5 * inch  # Move down by 0.5 inches

            # Add each question to the PDF
            for question in questions:
                if y_position <= 1 * inch:  # If we're near the bottom of the page, start a new page
                    c.showPage()
                    y_position = 10 * inch  # Reset y_position for the new page
                c.drawString(1 * inch, y_position, question)
                y_position -= 0.25 * inch  # Move down by 0.25 inches after each question

            # Save the PDF
            c.save()
            return filename
        except Exception as e:
            raise Exception(f"Failed to generate interview questions PDF: {e}")

# Example usage
if __name__ == "__main__":
    preparer = InterviewPreparerAgent()
    job_details = {"requirements": "Python, Machine Learning, Data Analysis"}
    resume_data = {"skills": ["Python", "Data Analysis"]}
    questions = preparer.generate_questions(job_details, resume_data)
    pdf_path = preparer.generate_questions_pdf(questions)
    print(f"Interview questions PDF generated at: {pdf_path}")