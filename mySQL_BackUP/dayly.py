# by Genabox (28/12/2023)
# if you want, say thanks ~ btc: 14CZG7Tp9vyHLxJoCi1FYKzgyjeG3BuPMe
import subprocess
import datetime
import os
import datetime
import re
# Замените этими данными вашу информацию о подключении к базе данных MySQL
db_config = {
    'user': 'root',
    'password': 'dapass',
    'host': 'localhost',
    'database': 'dbname',
}

# Замените этим путем куда будет сохранен SQL-файл резервной копии
backup_folder = 'H:\server\domains\localhost\embrezza\BackUp'

files = os.listdir(backup_folder)

def create_mysql_backup(db_config, backup_folder):
    # Путь к mysqldump.exe
    mysqldump_path = "H:\\server\\modules\\database\\MariaDB-10.8-Win10\\bin\\mysqldump.exe"


    # Получение текущей даты
    today = datetime.datetime.now().date()

    # Функция для определения даты создания файла
    def get_creation_date(file_name):
        # Извлеките дату из имени файла (поиск по паттерну 'гггг-мм-дд')
        date_pattern = re.search(r'\d{4}-\d{2}-\d{2}', file_name)
        if date_pattern:
            date_str = date_pattern.group()
            return datetime.datetime.strptime(date_str, '%Y-%m-%d')
        else:
            return datetime.datetime.min  # Возвращаем минимальную дату, если дата не найдена

    # Получение списка файлов в папке бэкапов
    files = os.listdir(backup_folder)

    # Найдите последний созданный файл и его дату создания
    latest_backup = max(files, key=get_creation_date, default=None)
    latest_backup_date = get_creation_date(latest_backup) if latest_backup else None

    # Проверьте, был ли последний бэкап создан сегодня
    if latest_backup_date and latest_backup_date.date() == today:
        print("Сегодня уже создан бэкап. Ничего не делаем.")
    else:
        # Генерируйте новое имя для бэкапа
        new_backup_date_str = today.strftime('%Y-%m-%d')
        new_backup_name = f"embrezzaphpbb_{new_backup_date_str}.sql"

        # Команда для создания бэкапа
        backup_command = f"{mysqldump_path} -u{db_config['user']} -p{db_config['password']} " \
                        f"-h {db_config['host']} {db_config['database']} > " \
                        f"{os.path.join(backup_folder, new_backup_name)}"


        try:
            # Выполнение команды для создания бэкапа
            subprocess.run(backup_command, shell=True, check=True)
            print(f"Создан новый бэкап с именем: {new_backup_name}")
        except subprocess.CalledProcessError as e:
            print(f"Произошла ошибка при выполнении mysqldump: {e}")

# Вызов функции для создания бэкапа
create_mysql_backup(db_config, backup_folder)
