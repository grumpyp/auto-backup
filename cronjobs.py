from crontab import CronTab
import logging
import getpass
import os


class Croncontroller():

    def __init__(self) -> None:
        self.username = getpass.getuser()
        self.filepath = os.path.dirname(os.path.abspath(__file__))
        self.cron = CronTab(user=f'{self.username}')
        logging.basicConfig(filename='logs.log', filemode='a+',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO,
                            datefmt='%d-%m-%Y %H:%M:%S')

    def add_daily(self, task) -> CronTab:
        '''
        this will activate the cronjob and execute it every day at 12
        '''
        try:
            init_file = self.filepath + "/main.py"
            job = self.cron.new(command=f'/opt/homebrew/bin/python3.9 {init_file} {task}')
            job.setall('* 12 * * *')
            self.cron.write()
            logging.warning(f'Cronjob added daily 12 pm: {task}')
            return job
        except Exception as e:
            logging.error(f'Cronjob adding error {e}')

    def disable(self) -> CronTab:
        for job in self.cron:
            job.enable(False)
        return self.cron

    @staticmethod
    def modify(job) -> CronTab:
        return job

    @staticmethod
    def show_jobs(self) -> list[CronTab]:
        return [job for job in self.cron]


if __name__ == "__main__":
    cronjobs = Croncontroller()
    cronjobs.add_daily('--upload "/Users/grumpyp/Documents/GitHub/auto-backup/logs.log" -ftp')
    cronjobs.disable()
    print(cronjobs.show_jobs(cronjobs))
