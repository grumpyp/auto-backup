import argparse
import subprocess
import os
from backups import googledrive


def upload_single(working_dir: str, path: str):
    """move file to upload, upload and delete"""
    print("cp " + path, working_dir)
    subprocess.call(f'cp "{path}" {working_dir}', shell=True)
    file = path.split('/')[-1]
    drive = googledrive.googledrive(file)
    drive.upload_basic()
    subprocess.call(f'rm {working_dir}/{file}', shell=True)
    print("Uploaded " + path + " to googledrive")
    return


def upload_dir(working_dir: str, path: str):
    for file in os.listdir(path):
        print(f'{path}/{file}')
        subprocess.call(f'cp "{path}/{file}" "{working_dir}"', shell=True)
        drive = googledrive.googledrive(file)
        drive.upload_basic()
        subprocess.call(f'rm "{working_dir}/{file}"', shell=True)

        print("Uploaded " + file + " to googledrive")
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', help="path to file/dir")

    parser.add_argument('-google', help="Upload to Googledrive",
                        required=False, action='store_true')

    parser.add_argument('-dir', help="Uploads the whole directory",
                        required=False, action='store_true')

    args = parser.parse_args()
    working_dir = os.path.abspath(os.getcwd())

    if args.upload and args.google and args.dir:
        path = args.upload
        upload_dir(working_dir, path)

    elif args.upload and args.google:
        path = args.upload
        upload_single(working_dir, path)
