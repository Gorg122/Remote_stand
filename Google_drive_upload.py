from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
from datetime import date
from dateutil import parser

# Функция получения id главной папки
import GUI


def Get_main_folder_id(service):
    # Производим поиск среди папок по названию
    results = service.files().list(
        pageSize=1,
        fields=" files(id, name, mimeType, parents, createdTime)",
        q="name contains 'Remote_Stand_930' and mimeType='application/vnd.google-apps.folder'").execute()
    #pp.pprint(results['files'])
    file_info = results['files']
    # Получаем id главной папки
    main_folder_id = [item['id'] for item in file_info]
    #print(main_folder_id)
    # Переводим id из списка в строку
    str1 = ''.join(main_folder_id)
    main_folder_id = str1
    return main_folder_id

# Функия по созданию папки пользователя по названию почты
def Folder_create(service, Users_drive, main_folder_id):
    ####### Раскомментировать данный отрезок, если необходимо единоразово создавать только 1 папку пользователя
    # results = service.files().list(
    #     pageSize=1,
    #     fields="files(id, name, mimeType, parents, createdTime)",
    #     q="name contains '" + Users_drive + "' and mimeType='application/vnd.google-apps.folder'").execute()
    # file_info = results['files']
    # folder_id = [item['id'] for item in file_info]
    # #print(folder_id)
    # str1 = ''.join(folder_id)
    # folder_id = str1
    # if folder_id != '':
    #      service.files().delete(fileId='{}'.format(folder_id)).execute()

    # Создание папки пользователя внутри главной папки
    folder_id = main_folder_id
    name = Users_drive
    # Задаем основные данные папки пользователя
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
    }
    # Создание папки с необходимыми метаданными
    r = service.files().create(body=file_metadata,
                               fields='id').execute()
    #pp.pprint(r)
    Folder_id = r['id']
    #print(Folder_id)
    return Folder_id

# Функция загрузки файлов пользователя
def File_upload(service, folder_id, file_path):
    # folder_id = '1PSD7Dutt6TIJqFmlM902oW70mFPy6pPH'
    # Задаем метаданные архива файлов пользователя
    name = 'rezult.zip'
    file_metadata = {
        'name': name,
        'mimeType': 'application/octet-stream',
        'parents': [folder_id]
    }
    # Задаем путь до загружаемых файлов, и необходимый mimetype
    media = MediaFileUpload(file_path, mimetype='application/octet-stream', resumable=True)
    # Загрузка файлов
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    # Тело запроса назначения прав
    file_permission = {"role": "reader", "type": "anyone"}

    # Назначение прав
    service.permissions().create(
        body=file_permission, fileId=r.get("id")
    ).execute()

    #pp.pprint(r)
    # Создаем ссылку на файлы пользователя
    file_id = r['id']
    file_link = r"https://drive.google.com/file/d/" + file_id + r"/view?usp=sharing"
    #print(file_link)
    return file_link

# Функция для удаления устаревших файлов
def Old_files_delete(main_folder_id, service):
    main_folder_id = main_folder_id
    files_deleted = 0
    # Выводим 30 очередных папок в главной папке
    results = service.files().list(
        pageSize=30,
        fields="files(id, name, mimeType, parents, createdTime)",
        q="parents='" + main_folder_id + "' and mimeType='application/vnd.google-apps.folder'").execute()

    #pp.pprint(results['files'])
    # Получаем id данных папок
    file_info = results['files']
    folder_id = [item['id'] for item in file_info]
    #print(folder_id)
    # Получаем текущую дату
    today = date.today()
    # Получаем дату создания данных папок
    createdTime = [item['createdTime'] for item in file_info]
    print(createdTime)
    delete = 0
    # Проходим по списку полученных папок
    for item in range(len(createdTime)):
        # Получаем дату создания данной папки
        create_date = "".join(createdTime[item])
        # Обрезаем дату создания данной папки до дней
        create_date = create_date.split("T", 1)[0]
        print(create_date)
        today = str(today)
        # Производим парсинг текущей даты и даты создания в временной формат
        old_date = parser.parse(create_date)
        cur_date = parser.parse(today)
        # Выводим дату создания папки, текущую дату, разницу в днях
        print("Дата создания = ", old_date)
        #GUI.print_log("Дата создания = ", old_date)
        print("Текущая дата = ", cur_date)
        #GUI.print_log("Текущая дата = ", cur_date)
        print("Разница в днях  = ", cur_date - old_date)
        #GUI.print_log("Разница в днях  = ", cur_date - old_date)
        # Получаем возраст папки
        old_file = str(cur_date - old_date)
        print(old_file)
        #GUI.print_log(old_file)
        if old_file[0] == "0":
            item += 1
        else:
            # Отделяем лишние данные
            old_file = int(old_file.split(" ", 1)[0])
            print(old_file)
            #GUI.print_log(old_file)
            # Производим удаление папки, если возраст данного файла более 3 дней
            if old_file > 3:
                service.files().delete(fileId='{}'.format(folder_id[item])).execute()
                delete = 1
                files_deleted += 1
                return 1
    if files_deleted > 0:
        print("Всего файлов удалено = ", files_deleted)
        GUI.print_log("Всего файлов удалено = ", files_deleted)
    if delete == 0:
        return 0
