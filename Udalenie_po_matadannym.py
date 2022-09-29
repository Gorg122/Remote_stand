import os
import shutil

import win32com.client
from datetime import date
from dateutil import parser
import pythoncom


def get_file_metadata(path, filename, metadata):
    # Path shouldn't end with backslash, i.e. "E:\Images\Paris"
    # filename must include extension, i.e. "PID manual.pdf"
    # Returns dictionary containing all file metadata.
    sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
    # xl = win32com.client.Dispatch("Excel.Application", pythoncom.CoInitialize())
    ns = sh.NameSpace(path)

    # Enumeration is necessary because ns.GetDetailsOf only accepts an integer as 2nd argument
    file_metadata = dict()
    item = ns.ParseName(str(filename))
    for ind, attribute in enumerate(metadata):
        attr_value = ns.GetDetailsOf(item, ind)
        if attr_value:
            file_metadata[attribute] = attr_value

    return file_metadata


# *Note: you must know the total path to the file.*
# Example usage:

def File_deleting(folder):
    deleting = True
    while deleting:
        delete = 0
        print("Пробегаю")
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".zip"):
                    file_name = file
                    file_path = root + "/" + file_name
                    print(file_path)
                    filename = file_name
                    metadata = ['Name', 'Size', 'Item type', 'Date modified', 'Date created']
                    file_metadata = get_file_metadata(root, filename, metadata)
                    # print(file_metadata)
                    date_modify = file_metadata['Date modified']
                    print(date_modify)
                    today = date.today()
                    file_date_str = str(date_modify)
                    file_date = file_date_str.split(" ", 1)[0]
                    print(file_date)
                    today = str(today)
                    old_date = parser.parse(file_date)
                    cur_date = parser.parse(today)
                    print("Old_date = ", old_date)
                    print("Current_date = ", cur_date)
                    print("Difference = ", cur_date - old_date)
                    old_file = cur_date - old_date
                    old_file = str(old_file)
                    print(old_file)
                    old_file = old_file.split(" ", 1)[0]
                    print(old_file)
                    old_file = old_file.split(':', 1)[0]
                    old_file = int(old_file)
                    if old_file > 2:
                        new_path = file_path.split('/')[:-1]
                        new_path = ''.join(new_path)
                        print(new_path)
                        shutil.rmtree(new_path, ignore_errors=True)
                        delete = 1

        deleting = False
        print("Удалять нечего")
        return "Все файлы удалены"

        # if delete == 0:
        #     print("Больше не удаляю")
        #     return "Удалять нечего"
        #     deleting = False


File_deleting(folder="C:\Project_930\Prototype_with_mail_bot\Archived")
