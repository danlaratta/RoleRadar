from services import ApiService

class Main:
    @staticmethod
    def run():
        service = ApiService()
        print(service.create_job_dataframe().to_string())

if __name__ == '__main__':
    print('Project is starting to run.')
    Main.run()