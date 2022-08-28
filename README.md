
# auto-backup 

Python project to safe/backup files and whole directories on remote storages

## Available backups
- [x]  Googledrive
- [ ]  SSH
- [x]  FTP

## Setup

Use the `settings_template.py` file, fill the path to your secrets and rename the file to `settings.py`.
You also have to get the folder ID from your Googledrive Folder.
You'll get this f.e. from the URL of the folder which could look like:

`https://drive.google.com/drive/folders/1CXyv3332kkkKKeD9lZFQlMhzdvdZZo` which results in `1CXyv3332kkkKKeD9lZFQlMhzdvdZZo`


### Ngrok

We are implementing a server to share files and make the backup-management which uses a `flask` server globally accessible.
Right now we are trying to work with `ngrok`.

#### Setup

1. Install `ngrok`: https://ngrok.com/download
2. Add your auth-token by executing in the terminal `ngrok config add-authtoken <your-token>`

You can also just commend out line 138 in main.py `expose = Thread(target=ngrok).start()`

## Usage

You can do backups with the following commands
make sure you're in the directory of the `main.py`.

to upload the whole directory: `python3 main.py --upload /Users/foo/Documents/Skydive -google -dir`

to upload a single file `python3 main.py --upload "/Users/foo/Documents/Skydive/Me.jpeg" -google`

to see the last 20 logs (only successful uploads and errors) in console `python3 main.py -logs`

to compress a file or directory `python3 main.py --upload "/Users/foo/Documents/Skydive/Me.jpeg" -compress`

to setup a cronjob `python3 main.py --upload "/Users/foo/Documents/Skydive/Me.jpeg" -ftp --cron add`

to view all running cronjobs `python3 main.py --upload "/Users/foo/Documents/Skydive/Me.jpeg" -ftp --cron show`

> You can delete all cronjobs with the following command in your terminal `crontab -r`

## Terminal usage

As there is no official pypi package yet, you can add an alias to your `shell`.

Steps in the Mac console:

1. `vim ~/.zshrc`
2. add 
`# auto-backup`
`alias autobackup="<yourpythonexecution> /Users/path/to/file/auto-backup/main.py"`

f.e. like this `alias autobackup="python3 /Users/px/Documents/GitHub/auto-backup/main.py"`

from there on you can execute everything like this: f.e. 
`autobackup --upload "/Users/foo/Documents/Skydive/Me.jpeg" -ftp`

### Googledrive Setup

To use the Googledrive API you have to follow these steps:

https://developers.google.com/drive/api/guides/enable-drive-api

after activating the drive API, you must add the e-mail from your service to a Googledrive folder in which you'll also backup all the stuff.

### Cronjob Setup

To use the cronjob feature you'd need to specifiy your Python path and change it in the line 25 of `cronjobs.py`

`/opt/homebrew/bin/python3.9` is the sample path. 

For my `macOS` to be precice `Big Sur`, I had to give `cron` some rights. The following tutorial made it work.

https://www.bejarano.io/fixing-cron-jobs-in-mojave/


## Feature Dev and Contributions
Please use the two functions in `main.py` to either upload a single file or dir and connect it to the files in `/backups` to keep the structure. Use the `settings.py` for CONSTANTS like API tokens and filepaths to secrets.

Fork it and create a PR.

### Idea's to build

- [x]  create bash script to compress directories or files
- [ ]  ~command to create~, edit a cronjob (auto-backup)
- [ ]  different backups like dropbox, Applecloud, Onedrive,..
- [ ]  Return a link to send the link to other people to easily download the file / dir which got uploaded
- [ ]  Create whole management tool for all backups f.e. with Flask (WIP)
- [ ]  You have a good future idea? -> Create an issue!