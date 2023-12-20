import paramiko
from decouple import config, AutoConfig
import os
# Loading Credentials
# set the environment variables in the server from the .env file. Run this command in the folder in gitbash
# set -o allexport && source .env && set +o allexport
config = AutoConfig(search_path='.env')
USERNAME = config("USER_NAME")
PASSWORD = config("PASSWORD")
PORT=int(config("PORT"))
IP_ADDRESS=config("IP_ADDRESS")

print(IP_ADDRESS, PORT, USERNAME, PASSWORD)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=IP_ADDRESS, 
            username=USERNAME,
            password=PASSWORD,
            port=PORT)
sftp_client=ssh.open_sftp()

upload_file_path = os.path.join('data', 'aq_file_upload.txt')
upload_folder = os.path.join('.', 'aq_upload')

# get current working directory
print('Connected to SFTP')
print(sftp_client.getcwd())

# move to the uploads directory
# sftp_client.chdir('./uploads')
sftp_client.chdir(f'/home/{USERNAME}/uploads')
print(sftp_client.getcwd())

# list the files in a directory

# put the file in the uploads directory
sftp_client.put(upload_file_path, './upload3.txt')

# list the files in the uploads directory

# Close the connections
sftp_client.close()
ssh.close()




