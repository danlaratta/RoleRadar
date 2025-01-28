from services import ApiService, ResumeParser, ResumeService


class Main:
    @staticmethod
    def run():
        # service = ApiService()
        # print(service.create_job_dataframe().to_string())

        r = ResumeService()
        print(r.get_resume_data().to_string())
        # print(r.get_years_of_experience())

if __name__ == '__main__':
    print('Project is starting to run.')
    Main.run()