import fitz
import re
import pandas as pd

class ResumeParser:
    @staticmethod
    def parse_resume():
        # Open the resume PDF file
        doc = fitz.open('asset/resume.pdf')

        # Extract data from resume in blocks/sections
        page = doc.load_page(0)  # resume is only 1 page so gets that page
        blocks = page.get_text('blocks')  # extract the text blocks
        text = '\n'.join(block[4].strip() for block in blocks if block[4].strip())
        return text


    def get_resume_data(self):
        # Get resume text
        text = self.parse_resume()

        # Define job title, company keywords, and regex for date ranges
        job_keywords = ['software engineer', 'software developer']
        company_keywords = ['Future Skies, Inc.', 'South Fulton Recording Studio', 'Cognixia']
        date_pattern = r'\b([A-Za-z]{3,}\.\s\d{4})\s*–\s*([A-Za-z]{3,}\.\s\d{4})\b'

        # Split the full text into lines
        lines = text.split('\n')

        # Extract job titles and company names
        job_matches = [
            line for line in lines
            if any(keyword.lower() in line.lower() for keyword in job_keywords)
        ]
        company_matches = [
            line for line in lines
            if any(company.lower() in line.lower() for company in company_keywords)
        ]

        # Extract start and end dates from date ranges
        date_matches = re.findall(date_pattern, text)
        start_dates = [start for start, end in date_matches]
        end_dates = [end for start, end in date_matches]

        # Normalize the data to ensure all lists are the same length
        max_length = max(len(job_matches), len(company_matches), len(start_dates), len(end_dates))
        job_matches += [None] * (max_length - len(job_matches))
        company_matches += [None] * (max_length - len(company_matches))
        start_dates += [None] * (max_length - len(start_dates))
        end_dates += [None] * (max_length - len(end_dates))
        data = {
            'Job Titles': job_matches,
            'Companies': company_matches,
            'Start Date': start_dates,
            'End Date': end_dates,
        }

        # Create df and remove last row in df because it's a project description that contains 'software engineer' not a job
        df = pd.DataFrame(data)
        df = df.iloc[:-1]
        return df

