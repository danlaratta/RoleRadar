
class SearchFilter:
    def __init__(self, desired_salary: int, is_remote: bool, employment_type: str, experience_level: str):
        self.desired_salary = desired_salary
        self.is_remote = is_remote
        self.employment_type = employment_type
        self.experience_level = experience_level