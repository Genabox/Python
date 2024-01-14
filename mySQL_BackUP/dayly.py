# by Genabox (28/12/2023)
# if you want, say thanks ~ btc: 14CZG7Tp9vyHLxJoCi1FYKzgyjeG3BuPMe
import subprocess
import datetime
import os
import datetime
import re

# Replace this data with your MySQL database connection information

db_config = {
    'user': 'root',
    'password': 'dapass',
    'host': 'localhost',
    'database': 'dbname',
}

# Replace this path with the location where the SQL backup file will be saved
backup_folder = 'H:\server\domains\localhost\BackUp'

files = os.listdir(backup_folder)

def create_mysql_backup(db_config, backup_folder):
    # Path to mysqldump.exe
    mysqldump_path = "H:\\server\\modules\\database\\MariaDB-10.8-Win10\\bin\\mysqldump.exe"

    # Get the current date
    today = datetime.datetime.now().date()

    # Function to determine the file's creation date
    def get_creation_date(file_name):
        # Extract the date from the file name (search for the pattern 'yyyy-mm-dd')
        date_pattern = re.search(r'\d{4}-\d{2}-\d{2}', file_name)
        if date_pattern:
            date_str = date_pattern.group()
            return datetime.datetime.strptime(date_str, '%Y-%m-%d')
        else:
            return datetime.datetime.min  # Return the minimum date if date is not found

    # Get the list of files in the backup folder
    files = os.listdir(backup_folder)

    # Find the most recently created file and its creation date
    latest_backup = max(files, key=get_creation_date, default=None)
    latest_backup_date = get_creation_date(latest_backup) if latest_backup else None

    # Check if the latest backup was created today
    if latest_backup_date and latest_backup_date.date() == today:
        result = "A backup has already been created today. Doing nothing."
    else:
        # Generate a new name for the backup
        new_backup_date_str = today.strftime('%Y-%m-%d')
        new_backup_name = f"embrezzaphpbb_{new_backup_date_str}.sql"

        # Command to create the backup
        backup_command = f"{mysqldump_path} -u{db_config['user']} -p{db_config['password']} " \
                        f"-h {db_config['host']} {db_config['database']} > " \
                        f"{os.path.join(backup_folder, new_backup_name)}"

        try:
            # Execute the command to create the backup
            subprocess.run(backup_command, shell=True, check=True)
            result = f"A new backup has been created with the name: {new_backup_name}"
        except subprocess.CalledProcessError as e:
            result = f"An error occurred while executing mysqldump: {e}"

    print(result)
    return result

# Call the function to create a backup
create_mysql_backup(db_config, backup_folder)
