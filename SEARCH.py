import subprocess
import os

# quickstart_path = subprocess.run("where /r c:\ quickstart.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
# print(quickstart_path.stdout, '\n')
# data = str(quickstart_path.stdout.decode().strip('\r\n'))
# print(data, '\n')
# data.replace("c", "C", 1)
# if os.path.exists(data):
#     root_path = data

def Find_files_by_ext(dir_path, file_ext):
    for root, dirs, files in os.walk(dir_path):  # В цикле проходим все папки и файлы в корневой папке
        print(files)
        for file in files:
            print(file)
            if file.endswith(file_ext):     # Производим поиск по расширению файла
                filepath = root + '/' + file  # Добавляем в путь папки и необходимый файл
                return filepath
            else:
                print("ytn")
    else:
        return 0


print(Find_files_by_ext(dir_path="C:/Project_930/Prototype_with_mail_bot_TO_EXE", file_ext='ini'))