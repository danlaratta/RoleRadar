from services import ApiService, ResumeParser

class Main:
    @staticmethod
    def run():
        # service = ApiService()
        # print(service.create_job_dataframe().to_string())

        parser = ResumeParser()
        # print(parser.parse_resume())
        print(parser.get_resume_data().to_string())

if __name__ == '__main__':
    print('Project is starting to run.')
    Main.run()