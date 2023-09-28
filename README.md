# Automated Wazuh log Archival Script for GCP buckets.

This Script is to automate the task of archiving the Logs of Wazuh Siem from the on prem server/instace to an arvhival class GCP storage bucket.

For details of generatting Service account token or Configuring access to GCP bucket please follow all the instructions on : Cyberviewpoint.com

## How to:

### 1) the script executes by setting a cron job on the Wazuh Server.
#### Open Cron Tab
```sh
    crontab -e
```
#### set the follwoing command
```sh
    00 5 * * * /usr/bin/python3 /root/scripts/archivemodule/main.py
```
##### note: I have set the task to run every day at 1:00 AM ETC , you can set that as per your time zone

### 2)Configure the internal variables of the Script in the config.ini file:
```sh
[Credentials]
type = service_account
project_id = <project_id> would be in the jwt token file generated for the service account
private_key_id = <project_key> would be in the jwt token file generated for the service account
private_key = <private_key> would be in the jwt token file generated for the service account
client_email = <client_name> would be in the jwt token file generated for the service account
client_id = <client_id> would be in the jwt token file generated for the service account

[Paths]
destination_files = <outputfile_location> file where you want to copy all the archive files of that day
ziparchivefile = <archivefile_location> directory path where you want to save the arched file path
```
