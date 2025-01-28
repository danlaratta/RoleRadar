from services import ResumeParser
from dateutil.relativedelta import relativedelta
import re
import pandas as pd

class ResumeService:
    #TODO: go through and refactor comments
    # Extract data from parsed resume and store in dataframe
    def get_resume_data(self):
        # Get resume text
        text = ResumeParser.parse_resume()

        # Define job title, company keywords, and regex for date ranges
        job_keywords = ['software engineer', 'software developer']
        company_keywords = ['Future Skies, Inc.', 'South Fulton Recording Studio', 'Cognixia']
        date_pattern = r'\b([A-Za-z]{3,}\s\d{4})\s*[-–]\s*([A-Za-z]{3,}\s\d{4})\b'

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

        # Skip the first two date matches (assumed to be education dates)
        job_date_matches = date_matches[2:]  # Skip the first two

        # Separate the start and end dates and convert string dates to datetime objects
        start_dates = [start for start, end in job_date_matches]
        end_dates = [end for start, end in job_date_matches]

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

        # Create DataFrame and clean up unnecessary rows
        df = pd.DataFrame(data)
        # Optionally remove the last row if it's not a valid job entry
        df = df.iloc[:-1] if not df.iloc[-1].notnull().all() else df

        return df


    # Calculate total years of experience from all jobs worked
    def get_years_of_experience(self):
        # Get the resume dataframe
        df = self.get_resume_data()

        # Convert string date to datetime store in temporary vars to keep original columns
        start_date_temp = pd.to_datetime(df['Start Date'], format='%b %Y')
        end_date_temp = pd.to_datetime(df['End Date'], format='%b %Y')

        # Calculate number of days worked at each job and add column to dataframe
        time_at_job = end_date_temp - start_date_temp
        df['Time at Job'] = time_at_job

        # Get total number of days worked for all jobs and calculate number of years worked
        total_time = df['Time at Job'].sum()
        years = round(total_time.days / 365, 1)
        return years


    # Return the experience level based on my years of experience
    def get_experience_level(self):
        pass