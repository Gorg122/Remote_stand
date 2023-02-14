from __future__ import print_function

import shutil

import httplib2
import os
import os.path
import io
import zipfile

from googleapiclient.http import MediaIoBaseDownload
from apiclient import discovery
from googleapiclient import discovery
# import googleapiclient.discovery
# from gooleapiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


import GUI
from File_work import Launch
from emailsend import send_email
import pymysql.cursors
import datetime
import time
import sys
from save_def import *
from win32com.shell import shell, shellcon  # Импортируем энкодер
from File_work import *  ## Исспользуются переменные:
from GUI import *

thread = 0
######
###### command_num - колличество команд.
######
from Sof_to_FPGA import *  ## Исспользуются переменные:
######
######pr_type - тип проекта
######
######
import requests

email_name = "Not_email"
stat_3 = 1
stat_4 = 1
stat_5 = 1
#GLOBAL_PC_ID = 2

############################# Функции для работы с яндекс диском #####################################################
# URL = 'https://cloud-api.yandex.net/v1/disk/resources'
# TOKEN = 'AQAAAAAIQKhOAADLW7IIpZ6ywEKymmaczK7ncl0'
# headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}
#
# def upload_file(loadfile, savefile, replace=True):
#     """Загрузка файла.
#     savefile: Путь к файлу на Диске
#     loadfile: Путь к загружаемому файлу
#     replace: true or false Замена файла на Диске"""
#     res = requests.get(f'{URL}/upload?path={savefile}&overwrite={replace}', headers=headers).json()
#     with open(loadfile, 'rb') as f:
#         try:
#             requests.put(res['href'], files={'file':f})
#         except KeyError:
#             print(res)
#
# def disk_file_status(savefile):
#     requests.put(f'{URL}/publish?path={savefile}', headers=headers).json()
#     res = requests.get(f'{URL}?path={savefile}&fields=file', headers=headers).json()
#     print(res)
#     return res
############################## Функции для работы с яндекс диском ###########################################

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
#CLIENT_SECRET_FILE = 'ul_cad_1.json'
CLIENT_SECRET_FILE = 'client_secret_Petukhov.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    #credential_path = os.path.join(credential_dir,
    #                              'drive-python-quickstart2.json')
    credential_path = os.path.join(credential_dir,
                                    'ul_cad_1.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
        GUI.print_log('Storing credentials to ' + credential_path)
    return credentials


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    print("TG")
    service = discovery.build("drive", "v3", http=http, static_discovery=False)
    return service
    # path_firmware = file_downloader(service, id, email)
    # file_delliter(id, service)
    # return service ,path_firmware

    #addr_to = "sasha.lorens@yandex.ru"  # Получатель
    addr_to = "desorder2881488@yandex.ru"  # Получатель
    files = [
        "C:/Users/sasha/PycharmProjects/pythonProject1/sah.lorens@gmail.com/filename.zip"]  # Список файлов, если вложений нет, то files=[]                                      # Если нужно отправить все файлы из заданной папки, нужно указать её
    # send_email(addr_to, "Тема сообщения", "Текст сообщения", files)


def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)
    return 'OK'


def file_download(my_id, email_name):
    con = connect()
    with con:
        cur = con.cursor()
        # try:
        #------------------------ЗАГРУЗКА АРХИВА С ФАЙЛАМИ ПОЛЬЗОВАТЕЛЯ ИЗ БАЗЫ ДАННЫХ НА УПРАВЛЯЮЩЕМ СТЕНДЕ---------------------------------------- 
        sql = ("""SELECT soc_zip
                  FROM status
                  WHERE id = %s""")
        cur.execute(sql, my_id)
        data = cur.fetchone()['soc_zip']
        # con.commit()
        email_short_name = email_name.split('@', 2)[0]
        if not os.path.isdir(
                'student_zip/' + email_short_name):  # Создание дериктории для хранения архива с файлами для прошивки
            os.makedirs('student_zip/' + email_short_name)
        root_path = "C:/Project_930/Project_main"
        os.chdir(root_path + '/student_zip/' + email_short_name)
        write_file(data, root_path + '/student_zip/' + email_short_name + '/filename.zip')
        print("Все нормально")
        GUI.print_log("Все нормально")
        path_firmware = 'student_zip/' + email_short_name
        return path_firmware
        # except:
        #     print("Ничего нет")


def file_delliter(file_id, service):
    try:
        service.files().delete(fileId=file_id).execute()
    except:
        print('Ошибка: файла не существует')
        GUI.print_log("Ошибка: файла не существует")


def file_downloader(service, value_id, email_name, root_path):
    file_id = value_id
    email_short_name = email_name.split('@', 2)[0]
    request = service.files().get_media(fileId=file_id)
    if not os.path.isdir(
            root_path + '/student_zip/' + email_short_name):  # Создание дериктории для хранения архива с файлами для прошивки
        os.makedirs(root_path + '/student_zip/' + email_short_name)
    fh = io.FileIO(root_path + '/student_zip/' + email_short_name + '/filename.zip', 'wb')  # Загрузка
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
        # GUI.print_log("Download %d%%." % int(status.progress() * 100))
    path_firmware = 'student_zip/' + email_short_name + ''
    archive_path = root_path + '/student_zip/' + email_short_name + '/filename.zip'

    # save_response = file_zip_correct(archive_path)
    # GUI.print_log(save_response[1])
    # if save_response[0]:
    #     return ''
    #if not(archive_path.endswith(".7z")):
    zip_file = zipfile.ZipFile(archive_path)  # Разархивирование файла
    zip_file.extractall(root_path + '/student_zip/' + email_short_name)
    return path_firmware

#------------------------------------------------ФУНКЦИЯ ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ НА УПРАВЛЯЮЩЕМ СТЕНДЕ--------------------------
def connect():
    con = pymysql.connect(host='DESKTOP-CG9VKI4',
                          port=3306,
                          user='user_1',
                          password='user_1',
                          database='labstandstatus',
                          cursorclass=pymysql.cursors.DictCursor)
    return con

#---------------------------------------------------ФУНКЦИЯ ИЗМЕНЕНИЯ СТАТУСА КОМПЬЮТЕРА В БАЗЕ ДАННЫХ НА УПРАВЛЯЮЩЕМ СТЕНДЕ------------------
def change_status(my_id, status_change):
    con = connect()
    with con:
        cur = con.cursor()
        sql = ("""UPDATE status
                 SET status = %s
                 WHERE id = %s""")
        print(status_change, my_id)
        GUI.print_log("Смена статуса", status_change)
        GUI.print_log("Текущий статус ", my_id)
        cur.execute(sql, (status_change, my_id))
        con.commit()
    return ('OK', format_time())

#------------------------------------ФУНКЦИЯ ПРОВЕРКИ СТАТУСА ПЕРЕД НАЧАЛОМ ЗАГРУЗКИ ФАЙЛОВ
def check_stat_for_downloading(my_id):
    con = connect()
    with con:
        cur = con.cursor()
        sql = ("SELECT id, status, file_id, email_name, soc_zip FROM status WHERE id = %s")
        cur.execute(sql, (my_id))
        answer = cur.fetchall()
        query_for_my_stand = answer[0]['status']
        if query_for_my_stand == 2:
            if answer[0]['file_id'] != 0:
                id_for_download = answer[0]['file_id']
            else:
                id_for_download = 'BLOB'
            email_for_download = answer[0]['email_name']
            print(id_for_download)
            GUI.print_log("Id файла для загрузки ", id_for_download)
            global stat_3
            #-----------------------ИЗМЕНЕНИЕ СТАТУСА НА "3" - ПРОШИВКА ПРИНЯТА В РАБОТУ(СТЕНД ЗАНЯТ)
            stat_3 = change_status(my_id, 3)[1]
            # change_status_log(4)
            return id_for_download, email_for_download
            print('ok')
            GUI.print_log("ok")
        else:
            return 0, 0
            print('nothing')
            GUI.print_log("nothing")

#--------------------------ФУНКЦИЯ ИЗМЕНЕНИЯ СТАТУСА НА "1" ПОСЛЕ ЗАВЕРШЕНИЯ ПРОЦЕССА ОБРАБОТКИ ФАЙЛОВ ПОЛЬЗОВАТЕЛЯ(СТЕНД СВОБОДЕН)------------
def clear_all(my_id):
    con = connect()
    with con:
        cur = con.cursor()
        sql = ("""UPDATE status
                     SET status = 1, file_id = 0, start_time = 0, email_name = '', soc_zip = '' 
                     WHERE id = %s""")
        cur.execute(sql, (my_id))
        con.commit()
    return ('OK')

def format_time():
    t = datetime.datetime.now()
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    head = s[:-7] # everything up to the '.'
    tail = s[-7:] # the '.' and the 6 digits after it
    # f = float(tail)
    # temp = "{:.03f}".format(f)  # for Python 2.x: temp = "%.3f" % f
    # new_tail = temp[1:] # temp[0] is always '0'; get rid of it
    return head, t# + new_tail


#--------------------------------ФУНКЦИЯ ЗАПИСИ ВРЕМЕНИ НАЧАЛА ОБРАБОТКИ ПРОШИВКИ ПОЛЬЗОВАТЕЛЯ

def write_current_time(id):  ##### Функция записи начала работы прошивки.
    con = connect()
    with con:
        cur = con.cursor()
        #dt_now = datetime.datetime.now()
        #dt_now = datetime.datetime.now().strftime('%y-%m-%d %a %H:%M:%S')[:-6]
        dt_now = format_time()
        #dt_now = dt_now[:-6]
        try:
            sql = ("""UPDATE status
                                           SET start_time = %s
                                           WHERE id = %s""")
            cur.execute(sql, (dt_now, id))
            con.commit()
            print("Все нормально")
            GUI.print_log("Все нормально")
        except:
            print("Не работает")
            GUI.print_log("Не работает")


def empty(confirm, show_progress, sound):
    recycle_bin_path = "C:\$RECYCLE.BIN"
    for files in os.listdir(recycle_bin_path):
        print(files)
    try:
        flags = 0
        if not confirm:
            flags |= shellcon.SHERB_NOCONFIRMATION
        if not show_progress:
            flags |= shellcon.SHERB_NOPROGRESSUI
        if not sound:
            flags |= shellcon.SHERB_NOSOUND
        shell.SHEmptyRecycleBin(None, None, flags)
        print("Корзина очищена")
        GUI.print_log("Корзина очищена")
    except:
        print("Корзина пуста")
        GUI.print_log("Корзина пуста")

#--------------------------------ФУНКЦИЯ ЗАПИСИ СТАТИСТИКИ ПО ОБРАБОТКЕ ФАЙЛОВ ПОЛЬЗОВАТЕЛЯ В БАЗУ ДАННЫХ
def log_upload(stat_work_time, sts_3_time, sts_4_time, sts_5_time, fin_time, type_pr, comm_numm, file_size, email):
    con = connect()
    with con:
        cur = con.cursor()
        try:
            sql = ("""INSERT INTO log_table (start_work_time, status_three_time, status_four_time, status_five_time, finish_time, type_of_project, how_many_commands, file_size, email_name)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""")
            cur.execute(sql, (
            stat_work_time, sts_3_time, sts_4_time, sts_5_time, fin_time, type_pr, comm_numm, file_size, email))
            con.commit()
            print("Лог записан")
            GUI.print_log("Лог записан")

            # sql = ("""SELECT LAST_INSERT_ID()""")
            # cur.execute(sql)
            # last_id = cur.fetchone()
            # print('Данная работа была записана в лог с id ' + last_id[0])
        except:
            print("Лог не записан")
            GUI.print_log("Лог записан")


def sub_main(service, root_path, GLOBAL_PC_ID):
    while True:
        start_time, ttime = format_time()
        start_time_in_sec = time.time()
        # os.chdir(root_path)
        file_id, email = check_stat_for_downloading(GLOBAL_PC_ID)
        if (file_id != 0) and (email != 0):
            if file_id == 'BLOB':
                path_firmware = file_download(GLOBAL_PC_ID, email)
                print(
                    path_firmware + "////////////////////////////////////////////////////////////////////////////////////////////////////////")
                # path_firmware = str(path_firmware)
            else:
                path_firmware = file_downloader(service, file_id, email, root_path)
                file_delliter(file_id, service)
            #------------------------ФУНКЦИЯ ИЗМЕНЕНИЯ СТАТУСА УДАЛЕННОГО СТЕНДА НА "4" (ЗАГРУЗКА ФАЙЛОВ ПРОШЛА УСПЕШНО, НАЧАЛО ОБРАБОТКИ)-----
            stat_4 = change_status(GLOBAL_PC_ID, 4)[1]
            write_current_time(GLOBAL_PC_ID)

            email_name_cur = str(email.split('@')[0])
            print(email_name)
            GUI.print_log(email_name)
            file_p = root_path + "/Archived/" + email_name_cur
            launch_stat, pr_type, command_num, URL, errors_ = Launch(User_path_to_file=path_firmware, root_path=root_path)
            print("LAUNCH_STAT = ", launch_stat)
            GUI.print_log("LAUNCH_STAT = ", launch_stat)
            if launch_stat == "OK":
                # new_users_dir = "C:\PROJECT_930\Prototype_new_2\Archived"
                stat_5 = change_status(GLOBAL_PC_ID, 5)[1]
                print(send_email(addr_to=email,  # "sasha.lorens@yandex.ru",
                                 msg_subj="Ваша прошивка",
                                 msg_text="Ваши файлы",
                                 files='',
                                 URL=URL,
                                 errors_ = errors_))

                #------------------ИЗМЕНЕНИЕ СТЕНДА НА СТАТУС "5" (ОТПРАВКА ОТВЕТНОГО ПИСЬМА ПОЛЬЗОВАТЕЛЮ)-------------
                stat_5 = change_status(GLOBAL_PC_ID, 5)[1]
                if path_firmware == "":
                    main_dir = root_path + '/' + 'student_zip'
                else:
                    main_dir = root_path + '/' + path_firmware.split('/')[0]
            if path_firmware != '':
                file_path = root_path + "/" + path_firmware
                file_size = os.path.getsize(file_path)  ##!!!!!!!!!!!!!!
                log_upload(start_time, stat_3, stat_4, stat_5, format_time(), pr_type, command_num,
                           file_size, email)
            if main_dir != root_path or main_dir != root_path + '/':
                for dirs in os.listdir(main_dir):
                    # os.rmdir(new_path + main_dir + "/" + dirs)
                    shutil.rmtree(main_dir + '/' + dirs)
            else:
                print("SDFKMSJKFZNKLJFSRHFSRZBLHJFSBRGFLBHGRHLG RSG SRHLJG RLHGJD BGHLJDLJHG")
                #GUI.print_log("SDFKMSJKFZNKLJFSRHFSRZBLHJFSBRGFLBHGRHLG RSG SRHLJG RLHGJD BGHLJDLJHG")
            clear_all(GLOBAL_PC_ID)
            empty(confirm=False, show_progress=True, sound=True)
        final_time = datetime.datetime.now()
        dd = final_time - ttime
        #print("DAYS DIFF", dd.days)  # get days
        print("SECONDS DIFF", dd.seconds)  # get seconds
        #print("MILESECIND DIFF", dd.microseconds)  # get microseconds
        #print("MINUTES DIFF", int(round(dd.total_seconds() / 60, 0)))  # get minutes
        GUI.print_log("--- %s seconds ---" % (time.time() - start_time_in_sec))
        while GUI.flag_stop:
            time.sleep(1)
        time.sleep(20)

def Find_files_by_name(dir_path, filename):
    for root, dirs, files in os.walk(dir_path):  # В цикле проходим все папки и файлы в корневой папке
        if filename in files:   # Производим поиск по названию файла
            filepath = os.path.join(root, filename)  # Добавляем в путь папки и необходимый файл
            return filepath
        else:
            return 0

def Find_files_by_ext(dir_path, file_ext):
    for root, dirs, files in os.walk(dir_path):  # В цикле проходим все папки и файлы в корневой папке
        for file in files:
            if file.endswith(file_ext):     # Производим поиск по расширению файла
                filepath = os.path.join(root, file)  # Добавляем в путь папки и необходимый файл
                return filepath
            else:
                return 0
#-----------------------------------------ГЛАВНАЯ ФУНКЦИЯ В КОТОРОЙ ЗАПУСКАЮТСЯ ВСЕ ДОЧЕРНИЕ ФУНКЦИИ
def CAD_LOOP():
    service = main()
    GUI.print_log("Начало работы")

    path = sys.argv[0]
    path_len = len(path.split('/')) - 1
    new_path = path.split('/')[:-1]
    new_str_path = "/".join(new_path)
    print(new_str_path)
    GUI.print_log(new_str_path)
    root_path = new_str_path

    student_zip = root_path+"/student_zip"
    print(student_zip)
    for root, dirs, files in os.walk(student_zip):  # В цикле проходим все папки и файлы в корневой папке
        for dir in dirs:
            dirpath = root + '/' + dir  # Добавляем в путь папки и необходимый файл
            shutil.rmtree(dirpath)
    for dirs in os.walk(root_path):
        if (dirs != "Archived") and (not(os.path.exists(root_path + "/Archived"))):
            os.mkdir(root_path + "/Archived")
        elif (dirs  != "Archive") and (not(os.path.exists(root_path + "/Archive"))):
            os.mkdir(root_path + "/Archive")
        elif (dirs != "video") and (not(os.path.exists(root_path + "/video"))):
            os.mkdir(root_path + "/video")
    # quickstart_path = subprocess.run("WHERE /R C:\ quickstart.exe", stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    # print(quickstart_path.stdout, '\n')
    # # data = str(quickstart_path.stdout.decode().strip('\r\n'))
    # data = quickstart_path.stdout
    # print(data, '\n')
    # data.replace("c", "C", 1)
    # # data.replace('\\', '/', 3)
    # # print(data)
    # # if os.path.exists(data):
    # new_path = data
    # new_path = new_path.split('\\')[:-1]
    # new_str_path = "/".join(new_path)
    # print(new_str_path)
    # root_path = new_str_path


    config = configparser.ConfigParser()
    config_dir = root_path + '/' + "Config.ini"
    config.read(config_dir)
    config_path = config['Direc']['path']
    GLOBAL_PC_ID = config['PC']['id']
    if config_path == root_path:
        print("Путь к папке проекта существует")
    else:
        config['Direc']['path'] = root_path
        with open('Config.ini', 'w') as configfile:
            config.write(configfile)
        print("Путь до текущей директории был изменен")

    print("Root_path = ", root_path)
    sub_main(service, root_path=root_path, GLOBAL_PC_ID=GLOBAL_PC_ID)


if __name__ == '__main__':
    GUI.main_start_gui()

