'''
Author: Moiz Lakdawala
'''

from datetime import datetime, date, timedelta
import os
import shutil
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import configparser

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Get credentials and paths from config
credentials_dict = {
    'type': config.get('Credentials', 'type'),
    'project_id': config.get('Credentials', 'project_id'),
    'private_key_id': config.get('Credentials', 'private_key_id'),
    'private_key': config.get('Credentials', 'private_key'),
    'client_email': config.get('Credentials', 'client_email'),
    'client_id': config.get('Credentials', 'client_id'),
}
destination_files = config.get('Paths', 'destination_files')
ziparchivefile = config.get('Paths', 'ziparchivefile')

# Initialize client
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict)
client = storage.Client(credentials=credentials, project=credentials_dict['project_id'])
bucket = client.get_bucket("wazuh_log_archive1")


def log_file_path_generator():
    # get today's datetime
    now = datetime.now()
    year = now.year
    month = now.strftime('%b')
    day = now.day
    day = day - 1
    #day = 9
    if 0 <= day <= 9:
        day = f'0{day}'
    else:
        day = day

    log_location_path = f'/var/ossec/logs/archives/{year}/{month}/ossec-archive-{day}*'
    return log_location_path


def copy_logs(source_files, destination_files):
    # copy only files
    if os.path.isfile(source_files):
        shutil.copy(source_files, destination_files)
        print('copied')

def archive_files(dir_name):
    today = date.today()
    log_day = today - timedelta(days = 1)
    output_filename=f'/<outputfile_location>/{log_day}-archive'
    shutil.make_archive(output_filename, 'zip', dir_name)
    filename = f'{log_day}-archive.zip'
    blob = bucket.blob(filename)
    blob.upload_from_filename(f'/{destination_files}/{log_day}-archive.zip')
def cleanup(cplogfiles,ziparchive):
    os.system(f'rm -rf {cplogfiles}/*')
    os.system(f'rm -rf {ziparchive}/*')

def main():
    source_file = log_file_path_generator()
    os.system(f'cp {source_file} {destination_files}')
    archive_files(destination_files)
    cleanup(destination_files,ziparchivefile)

if __name__ == "__main__":
    main()
