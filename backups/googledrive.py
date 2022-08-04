import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials
import settings
import logging
import datetime
sys.path.append(".")

# steps
# create a new folder share it with the service e-mail

# start with init to get Folder ID to upload everything in folder ID
# or set folder it yourself

class googledrive():

    def __init__(self, filename: str = "", uploadpath: str = "") -> None:
        self.filename = filename
        self.uploadpath = uploadpath
        self.parent_folder = settings.GOOGLEDRIVE_FOLDER
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(settings.GOOGLEDRIVE_API) #, scopes=SCOPES)
        self.time = datetime.datetime.now()
        print(self.creds)
        logging.basicConfig(filename='logs.log', filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO,
                            datefmt='%d-%m-%Y %H:%M:%S')
        logging.info('Googledrive backer started')

    def create_folder(self):
        """ Create a folder and prints the folder ID
        Returns : Folder Id

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """

        try:
            # create drive api client
            service = build('drive', 'v3', credentials=self.creds)
            file_metadata = {
                'title': 'Rechnungen Backup',
                'mimeType': 'application/vnd.google-apps.folder'
            }

            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, fields='id'
                                        ).execute()
            logging.warning(F'Folder has created with ID: "{file.get("id")}".')
            print("created")

        except HttpError as error:
            logging.error(F'An error occurred: {error}')
            file = None

        return file.get('id')


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

            file_metadata = {'name': f'{self.filename}',
                             'parents': [f'{self.parent_folder}']}

            media = MediaFileUpload(self.filename) # ,mimetype='image/jpeg')
            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, media_body=media,
                                        fields='id').execute()
            logging.warning(F'File uploaded with ID: {file.get("id")}')

        except HttpError as error:
            logging.error(F'An error occurred: {error}')
            file = None

        return file.get('id')


    def search_file(self):
        """Search file in drive location

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """

        try:
            # create drive api client
            service = build('drive', 'v3', credentials=self.creds)
            files = []
            page_token = None
            while True:
                # pylint: disable=maybe-no-member
                response = service.files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                spaces='drive',
                                                fields='nextPageToken, '
                                                    'files(id, name)',
                                                pageToken=page_token).execute()
                for file in response.get('files', []):
                    # Process change
                    logging.warning(F'Found file: {file.get("name")}, {file.get("id")}')
                files.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

        except HttpError as error:
            logging.error(F'An error occurred: {error}')
            files = None

        return files


if __name__ == '__main__':
    # upload_basic()
    drive = googledrive("test")
    # drive.create_folder()
    # drive.search_file()
    drive.upload_basic()