from crewai import Agent, Crew, Process, Task
from hr_buddy.utils.web_scraper import WebScraperTool # Replace with your actual tool class
from hr_buddy.utils.resume_parser import ResumeParserTool # Replace with your actual tool class
# ... other imports ...


class HRBuddyCrew(Crew):
    def __init__(self, agents_config):
        super().__init__(agents_config)

    @Process
    def job_posting_analysis(self, job_url):
        # 1. Job Posting Input
        researcher_agent = self.researcher()
        research_results = researcher_agent.run(job_url=job_url, tool=WebScraperTool())
        return research_results

    @Process
    def social_media_profile(self, social_media_links):
        # 2. Social Media Integration (Optional)
        social_media_profiler_agent = self.social_media_profiler()
        social_profile = social_media_profiler_agent.run(social_media_links=social_media_links, tool=WebScraperTool())
        return social_profile

    @Process
    def resume_processing(self, resume_text):
        # 3. Resume Upload and Processing
        resume_parser = self.resume_parser()
        parsed_resume = resume_parser.run(resume_text=resume_text, tool=ResumeParserTool())
        return parsed_resume

    @Process
    def resume_generation(self, job_data, social_profile, resume_data):
        # 4. Resume Generation
        resume_strategist_agent = self.resume_strategist()
        generated_resume = resume_strategist_agent.run(job_data=job_data, social_profile=social_profile, resume_data=resume_data)
        return generated_resume

    @Process
    def interview_preparation(self, job_data, resume_data):
        # 5. Interview Preparation
        interview_preparer_agent = self.interview_preparer()
        interview_questions = interview_preparer_agent.run(job_data=job_data, resume_data=resume_data)
        return interview_questions

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )

    @agent
    def social_media_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_profiler'],
            verbose=True
        )

    @agent
    def resume_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_strategist'],
            verbose=True
        )

    @agent
    def interview_preparer(self) -> Agent:
        return Agent(
            config=self.agents_config['interview_preparer'],
            verbose=True
        )

    @agent
    def resume_parser(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_parser'],
            verbose=True
        )
