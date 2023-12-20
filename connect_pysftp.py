import pysftp
from decouple import config, AutoConfig
import os
# Loading Credentials
# set the environment variables in the server from the .env file. Run this command in the folder in gitbash
# set -o allexport && source .env && set +o allexport
config = AutoConfig(search_path='.env')
USERNAME = config("USER_NAME")
PASSWORD = config("PASSWORD")
PORT=config("PORT")
IP_ADDRESS=config("IP_ADDRESS")

# print(IP_ADDRESS, PORT, USERNAME, PASSWORD)
sftpHost = IP_ADDRESS
sftpPort = int(PORT)
uname = USERNAME
passw = PASSWORD

cnOpts = pysftp.CnOpts()
cnOpts.hostkeys = None

upload_file_path = os.path.join('data', 'aq_file_upload.txt')
#upload_folder = os.path.join('.', 'aq_upload')
with pysftp.Connection(host=sftpHost,
                       port=sftpPort,
                       username=uname,
                       password=passw, cnopts=cnOpts) as sftp:
    print('Connected to sftp server')

    #print(sftp.pwd)
    #sftp.cwd("./uploads")
    print(sftp.pwd)
    x = sftp.listdir()
    print(x)

    sftp.put(upload_file_path, preserve_mtime=True, remotepath="./uploads/test_new.txt")
    #sftp.put_d(upload_folder, preserve_mtime=True, remotepath="./uploads")

    x = sftp.listdir("./uploads")
    print(x)


