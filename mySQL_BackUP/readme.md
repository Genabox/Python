# MySQL Database Backup Script

This Python script is designed to automate the process of creating backups for a MySQL database. It utilizes the `mysqldump` tool to export the database's contents to an SQL file, preserving data integrity. The script checks whether a backup has been created today and, if not, generates a new backup with a timestamped filename.

## Features

- **Automatic Backup:** The script automatically creates backups of a specified MySQL database.

- **Timestamped Backups:** Each backup is named with a timestamp, making it easy to identify when the backup was created.

- **Duplicate Check:** It checks whether a backup for the current day already exists to prevent unnecessary duplications.

## How to Use

1. Update the `db_config` dictionary with your MySQL database connection information, including the username, password, host, and database name.

2. Set the `backup_folder` variable to the path where you want to store the backup files.

3. Ensure that the path to the `mysqldump.exe` tool is correctly specified in the `mysqldump_path` variable.

4. Run the script, and it will automatically create a new backup if one hasn't been created today.

### Example Usage

```python
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'your_database',
}

backup_folder = '/path/to/backup/folder'

create_mysql_backup(db_config, backup_folder)
