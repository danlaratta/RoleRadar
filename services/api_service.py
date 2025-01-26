import os
import urllib
from typing import List, Dict, Any
from urllib.parse import urlencode
from dotenv import load_dotenv
import requests
import pandas as pd


class ApiService:
    # Load environment variables
    def __init__(self):
        load_dotenv()
        self.api_key: str = os.getenv('API_KEY')
        self.host: str = os.getenv('HOST')
        self.base_url: str = os.getenv('BASE_URL')
        self.headers: Dict[str, str] = {'x-rapidapi-key': self.api_key, 'x-rapidapi-host':self.host}
        self.params: Dict[str, str] = { 'title_filter': 'Software Engineer', 'location_filter': 'United States'}

        if not self.api_key or not self.host or not self.base_url or not self.headers or not self.params:
            raise ValueError('One of the required values are missing for Api request.')


    # Get job listing json data
    def get_job_listings(self) -> List[Dict[str, Any]]:
        try:
            # Replaces + which gets added for white space to %20
            encoded_params = urlencode(self.params, quote_via=urllib.parse.quote)

            # Make request and return parsed json
            response = requests.get(self.base_url, headers=self.headers, params=encoded_params)
            response.raise_for_status() # Raise an HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return []


    # Convert Json into dataframe
    def create_job_dataframe(self):
        # Get json job listing data
        job_listings = self.get_job_listings()

        if not job_listings:
            raise ValueError('No json job data available.')

        # Create dataframe of jobs
        df = pd.DataFrame([
            {
                # Extract these fields from json and use as columns with None fallback for missing values
                'date_posted': job.get('date_posted', None),
                'title': job.get('title', None),
                'company': job.get('organization', None),
                'salary_type': job['salary_raw']['value']['unitText'] if job.get('salary_raw') else None, # tenary for certain rows where salary is null
                'salary_min': job['salary_raw']['value']['minValue'] if job.get('salary_raw') else None,  # tenary for certain rows where salary is null
                'salary_max': job['salary_raw']['value']['maxValue'] if job.get('salary_raw') else None,  # tenary for certain rows where salary is null
                'location': job.get('locations_derived', None),
                'is_remote': job.get('remote_derived', None),
                'experience_level': job.get('seniority', None),
                'employment_type': job.get('employment_type', None),
            }
            for job in job_listings # list comprehension goes through all jobs and adds them to dataframe
        ])

        return df
