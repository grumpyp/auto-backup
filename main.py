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


def compress(working_dir: str, path: str):
    try:
        commands = f"""
                    cd {working_dir}/temp_storage
                    bash create_compressed.sh {path}
        """
        print(path)
        subprocess.call(commands, shell=True)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', help="path to file/dir")

    parser.add_argument('-google', help="Upload to Googledrive",
                        required=False, action='store_true')

    parser.add_argument('-ftp', help="Upload to FTP",
                        required=False, action='store_true')

    parser.add_argument('-dir', help="Uploads the whole directory",
                        required=False, action='store_true')

    parser.add_argument('-logs', help="Show upload logs",
                        required=False, action='store_true')

    parser.add_argument('-compress', help="Compressed a file/path",
                        required=False, action='store_true')

    args = parser.parse_args()
    path = args.upload
    working_dir = os.path.abspath(os.getcwd())
    if not os.path.exists(working_dir + "/temp_storage"):
        subprocess.run('mkdir temp_storage', shell=True)

    if args.compress:
        compress(working_dir, path)

    elif args.upload and args.google and args.dir:
        upload_dir(working_dir, path, 'google')

    elif args.upload and args.ftp and args.dir:
        upload_dir(working_dir, path, 'ftp')

    elif args.upload and args.google:
        upload_single(working_dir, path, 'google')

    elif args.upload and args.ftp:
        upload_single(working_dir, path, 'ftp')

    elif args.logs:
        try:
            print("\n")
            for n, log in enumerate(reversed(open('logs.log', 'r+').readlines())):
                if "ERROR" in log or "WARNING" in log:
                    print(log)
                    if n > 20:
                        break
            print("To see all logs open logs.log")
        except Exception as e:
            print(f"No logs saved: {e}")
