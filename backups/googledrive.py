from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials
import settings
import logging
import datetime


class Googledrive():

    def __init__(self, filename: str = "", uploadpath: str = "") -> None:
        self.filename = filename
        self.uploadpath = uploadpath
        self.parent_folder = settings.GOOGLEDRIVE_FOLDER
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(settings.GOOGLEDRIVE_API)
        self.time = datetime.datetime.now()
        logging.basicConfig(filename='logs.log', filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO,
                            datefmt='%d-%m-%Y %H:%M:%S')
        logging.info('Googledrive backer started')

    def upload_basic(self):
        """Insert new file.
        Returns : Id's of the file uploaded

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """

        try:
            # create drive api client
            service = build('drive', 'v3', credentials=self.creds)

            file_metadata = {'name': f'{self.filename.split("/")[1]}',
                             'parents': [f'{self.parent_folder}']}

            media = MediaFileUpload(self.filename)
            file = service.files().create(body=file_metadata, media_body=media,
                                          fields='id').execute()
            logging.warning(F'File {self.filename.split("/")[1]} uploaded to Googledrive with ID: {file.get("id")}')

        except HttpError as error:
            logging.error(F'An error occurred: {error}')
            file = None

        return file.get('id')


if __name__ == '__main__':
    drive = Googledrive("test")
    drive.upload_basic()
