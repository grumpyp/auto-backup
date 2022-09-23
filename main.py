import argparse
import subprocess
import os
from threading import Thread

import cronjobs
from backups import googledrive, ftp


def upload_single(working_dir: str, path: str, storage: str):
    """move file to upload, upload and delete"""
    print(['cp',f'{path} ', f'{working_dir}/temp_storage'])
    subprocess.call(['cp',f'{path}', f'{working_dir}/temp_storage'])
    file = path.split('/')[-1]
    if storage == "google":
        drive = googledrive.Googledrive("temp_storage/" + file, org_path=f"{path}")
        drive.upload_basic()
    if storage == "ftp":
        ftpstorage = ftp.Ftp("temp_storage/" + file, org_path=f"{path}")
        ftpstorage.upload_basic()
    subprocess.call(['rm', f'{working_dir}/temp_storage/{file}'])
    print("Uploaded " + path + " to " + storage)
    return


def upload_dir(working_dir: str, path: str, storage: str):
    for file in os.listdir(path):
        subprocess.call(['cp', f'{path}/{file}', f'{working_dir}/temp_storage'])
        if storage == "google":
            drive = googledrive.Googledrive("temp_storage/" + file, org_path=f"{path}")
            drive.upload_basic()
        elif storage == "ftp":
            ftpstorage = ftp.Ftp("temp_storage/" + file, org_path=f"{path}")
            ftpstorage.upload_basic()
        subprocess.call(['rm', f'{working_dir}/temp_storage/{file}'])
        print("Uploaded " + file + " to " + storage)
    return


def compress(working_dir: str, path: str):
    try:
        commands = f"""
                    cd {working_dir}/temp_storage
                    bash create_compressed.sh {path}
        """
        print(path)
        compress_file = subprocess.run(commands, shell=True, capture_output=True)
        compressed_file_name = compress_file.stdout.decode('utf-8').split(" ")[0]
        return compressed_file_name

    except Exception as e:
        print(e)


def _server(c):
    from server import main
    main.start()


def ngrok():
    subprocess.call('ngrok http 5000', shell=True)


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

    parser.add_argument('--cron', help='Cronjob commands', required=False)

    args = parser.parse_args()
    cronjob = args.cron

    path = args.upload
    working_dir = os.path.abspath(os.getcwd())
    if not os.path.exists(working_dir + "/temp_storage"):
        subprocess.run('mkdir temp_storage', shell=True)

    uploadfunc = upload_dir if args.dir else upload_single

    if cronjob:
        cron = cronjobs.Croncontroller()
        if cronjob == "add":
            cron.add_daily('--upload "/Users/grumpyp/Documents/GitHub/auto-backup/logs.log" -ftp')
        if cronjob == "show":
            print("Running Cronjobs: ")
            print(cron.show_jobs(cron))

    if args.compress:
        compressed_filename = compress(working_dir, path)
        if args.google:
            upload_single(working_dir, compressed_filename, 'google')
        elif args.ftp:
            upload_single(working_dir, compressed_filename, 'ftp')

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
    # current problem: when uploading another file, another Thread of expose will be started
    # free version is limited to 1
    # it keeps working but Exceptions show up
    serv = Thread(target=_server, args=[5]).start()
    expose = Thread(target=ngrok).start()
