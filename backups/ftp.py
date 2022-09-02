import settings
import logging
import datetime
from ftplib import FTP


class Ftp():

    def __init__(self, filename: str = "", uploadpath: str = "", org_path: str = "") -> None:
        self.filename = filename
        self.uploadpath = uploadpath
        self.org_path = org_path
        self.time = datetime.datetime.now()
        logging.basicConfig(filename='logs.log', filemode='a+',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO, datefmt='%d-%m-%Y %H:%M:%S')
        try:
            self.connection = FTP(host=settings.FTP_URL + settings.FTP_PORT)
            self.connection.login(user=settings.FTP_USER, passwd=settings.FTP_PASSWPORD)
            self.connection.cwd(settings.FTP_FOLDER)
            logging.info('FTP backer started')
        except Exception as e:
            logging.error(f'Error trying to connect with FTP: {e}')
        print(self.connection.pwd())

    def upload_basic(self):
        """
        Insert a new file
        """

        try:
            with open(self.filename, 'rb') as file:
                self.connection.storbinary(f'STOR {self.filename.split("/")[1]}', file)
                logging.warning(f'File {self.filename.split("/")[1]} from: {self.org_path} \
                                uploaded to FTP')

        except Exception as e:
            logging.error(F'An error occurred: {e}')

        return

    def create_dir(self, dirname):
        """create new directory if not existant"""
        try:
            if dirname not in self.get_directories():
                self.connection.mkd(dirname)
                logging.warning(f'{dirname} folder created on FTP')
            else:
                logging.error(f'{dirname} already exists')

        except Exception as e:
            logging.error(F'An error occurred: {e}')

        return

    def get_directories(self):
        """get a list of all directories on the ftp"""
        dir_list = list()
        self.connection.dir(dir_list.append)
        directories = [dir.split(" ")[-1] for dir in dir_list if dir.split(" ")[0] == "drwxr-xr-x"]
        return directories


if __name__ == "__main__":
    ftpcon = Ftp()
    # ftpcon.basic_upload()
    print(ftpcon)
    # ftpcon.create_dir()
