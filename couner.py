import paramiko
import os
import datetime

# define the SSH credentials
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('194.186.150.221', username='user', password='1qaz!QAZ')

# define the remote directory to check
remote_dir = '/srv/filehosting/images/spot-test/'

# define the date to check against
date_cutoff = datetime.datetime(2023, 2, 10) # replace with your desired date

# execute the command to list all files in the remote directory and its subdirectories, with timestamps
command = "find {} -type f -newermt '{}' -printf '1\n' | wc -l".format(remote_dir, date_cutoff.strftime('%Y-%m-%d %H:%M:%S'))
stdin, stdout, stderr = ssh.exec_command(command)

# read the output and print the number of files found
num_files = int(stdout.read().decode('utf-8').strip())
print("Number of files modified after {}: {}".format(date_cutoff, num_files))

# close the SSH connection
ssh.close()