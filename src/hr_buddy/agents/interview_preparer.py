from crewai import Agent

class InterviewPreparerAgent:
    def __init__(self):
        self.agent = Agent(
            role="Interview Preparer",
            goal="Generate targeted interview questions based on job description and resume",
            tools=["nlp", "question_generation"],
            verbose=True
        )

    def generate_questions(self, job_details, resume_data):
        """
        Generate interview questions based on job details and resume data.
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

# Example usage
if __name__ == "__main__":
    preparer = InterviewPreparerAgent()
    job_details = {"requirements": "Python, Machine Learning, Data Analysis"}
    resume_data = {"skills": ["Python", "Data Analysis"]}
    questions = preparer.generate_questions(job_details, resume_data)
    print(questions)