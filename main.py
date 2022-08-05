import argparse
import subprocess
import os
from backups import googledrive, ftp


def upload_single(working_dir: str, path: str, storage: str):
    """move file to upload, upload and delete"""
    print("cp " + path, working_dir)
    subprocess.call(f'cp "{path}" {working_dir}/temp_storage', shell=True)
    file = path.split('/')[-1]
    if storage == "google":
        drive = googledrive.Googledrive("temp_storage/" + file)
        drive.upload_basic()
    if storage == "ftp":
        ftpstorage = ftp.Ftp("temp_storage/" + file)
        ftpstorage.upload_basic()
    subprocess.call(f'rm "{working_dir}/temp_storage/{file}"', shell=True)
    print("Uploaded " + path + " to " + storage)
    return


def upload_dir(working_dir: str, path: str, storage: str):
    for file in os.listdir(path):
        subprocess.call(f'cp "{path}/{file}" {working_dir}/temp_storage', shell=True)
        if storage == "google":
            drive = googledrive.Googledrive("temp_storage/" + file)
            drive.upload_basic()
        elif storage == "ftp":
            ftpstorage = ftp.Ftp("temp_storage/" + file)
            ftpstorage.upload_basic()
        subprocess.call(f'rm "{working_dir}/temp_storage/{file}"', shell=True)
        print("Uploaded " + file + " to " + storage)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', help="path to file/dir")

    parser.add_argument('-google', help="Upload to Googledrive",
                        required=False, action='store_true')

    parser.add_argument('-ftp', help="Upload to FTP",
                        required=False, action='store_true')

    parser.add_argument('-dir', help="Uploads the whole directory",
                        required=False, action='store_true')

    args = parser.parse_args()
    working_dir = os.path.abspath(os.getcwd())
    if not os.path.exists(working_dir + "/temp_storage"):
        subprocess.run('mkdir temp_storage', shell=True)

    if args.upload and args.google and args.dir:
        path = args.upload
        upload_dir(working_dir, path, 'google')

    elif args.upload and args.ftp and args.dir:
        path = args.upload
        upload_dir(working_dir, path, 'ftp')

    elif args.upload and args.google:
        path = args.upload
        upload_single(working_dir, path, 'google')

    elif args.upload and args.ftp:
        path = args.upload
        upload_single(working_dir, path, 'ftp')

