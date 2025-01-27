from typing import List


class Resume:
    def __init__(self, name: str, title: str, job_titles: List[str], date_ranges: List[str]):
        self.name = name
        self.title = title
        self.job_titles = job_titles
        self.date_ranges = date_ranges