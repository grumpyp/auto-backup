
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


## Usage

You can do backups with the following commands
make sure you're in the directory of the `main.py`.

to upload the whole directory: `python3 main.py --upload /Users/foo/Documents/Skydive -google -dir`

to upload a single file `python3 main.py --upload "/Users/foo/Documents/Skydive/Me.jpeg" -google`

to see the last 20 logs (only successful uploads and errors) in console `python3 main.py -logs`

to compress a file or directory `python3 main.py --upload "/Users/foo/Documents/Skydive/Me.jpeg" -compress`

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


## Feature Dev and Contributions
Please use the two functions in `main.py` to either upload a single file or dir and connect it to the files in `/backups` to keep the structure. Use the `settings.py` for CONSTANTS like API tokens and filepaths to secrets.

Fork it and create a PR.

### Idea's to build

- [x]  create bash script to compress directories or files
- [ ]  command to create and edit a cronjob (auto-backup)
- [ ]  different backups like dropbox, Applecloud, Onedrive,..
- [ ]  You have a good future idea? -> Create an issue!