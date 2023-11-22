#================= welcome to main bot strartup file ========================#

#============================================================================#
#                (                   (                     )                 #
#                )\ )  *   )   (     )\ )  *   )     (  ( /(   *   )         #
#                (()/(` )  /(   )\   (()/(` )  /(   ( )\ )\())` )  /(        #
#                /(_))( )(_)|(((_)(  /(_))( )(_))  )((_|(_)\  ( )(_))        #
#                (_)) (_(_()) )\ _ )\(_)) (_(_())  ((_)_  ((_)(_(_())        #
#                / __||_   _| (_)_\(_) _ \|_   _|   | _ )/ _ \|_   _|        #
#                \__ \  | |    / _ \ |   /  | |     | _ \ (_) | | |          #
#                |___/  |_|   /_/ \_\|_|_\  |_|     |___/\___/  |_|          #                                            
#============================================================================#
  
import multiprocessing
import subprocess
import os
from colorama import init, Fore, Style
from pydub import AudioSegment
from pydub.playback import play
import threading

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

def play_sound(file_path):
    try:
        sound = AudioSegment.from_file(file_path)
        play(sound)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    mp3_path = r'h:/soft/python/music/bot_ok.wav'  # Замените путь на свой звуковой файл
    sound_thread = threading.Thread(target=play_sound, args=(mp3_path,))
    sound_thread.start()

    # Остальной код вашей программы
    print("....$tarting $y$tem /  ........")

if __name__ == "__main__":
    main()

def run_subscript(script_path):
    subprocess.run(["python", script_path], text=True)

if __name__ == "__main__":
    # Инициализируем colorama
    init()
    print('                                                       ')
    print('                                                       ')
    print('    * _____ __    *   -    __  __    *     __    R     ')
    print('  -  / ___// /_____ ______/ /_/ /_  ____  / /_         ')
    print(' *   \__ \/ __/ __ `/ ___/ __/ __ \/ __ \/ __/   *  -  ')
    print('    ___/ / /_/ /_/ / /  / /_/ /_/ / /_/ / /_   -    *  ')
    print(' * /____/\__/\__,_/_/ * \__/_.___/\____/\__/  *  *     ')
    print('     *        -        *               *           *   ')
    print('                                                       ')
    #==============================================================#
     
    # Цвета для различных частей скрипта
    color_header = Fore.YELLOW
    color_script_name = Fore.CYAN
    color_info = Fore.GREEN

    # Шапка скрипта
    print(color_header + "=== General script ===" + Style.RESET_ALL)

    # Вывод списка подскриптов
    print(color_info + "List of scripts to run:" + Style.RESET_ALL)
    scripts_to_run = [
        "ssh/ssh.py",
        "calculator/calculator.py"
    ]
    script_colors = {script: color for script, color in zip(scripts_to_run, [Fore.MAGENTA, Fore.BLUE, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.RED,  Fore.WHITE, Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTCYAN_EX ])}

    for i, script_name in enumerate(scripts_to_run, 1):
        print(f"{i}. {script_colors[script_name]}{script_name}{Style.RESET_ALL}")

    try:
        # Запуск всех подскриптов в отдельных процессах
        print(color_info + "Running subscripts..." + Style.RESET_ALL)
        with multiprocessing.Pool() as pool:
            pool.map(run_subscript, scripts_to_run)
    except Exception as e:
        print("An error occurred:", e)

    # Завершение
    print(color_header + "=== Script ended ===" + Style.RESET_ALL)

#========================= bot strartup file ============================#
