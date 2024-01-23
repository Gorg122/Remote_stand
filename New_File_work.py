from Video import get_data_from_video
import os
import shutil
import re
import time
import serial
import sys
import subprocess
from fastapi import File, UploadFile, FastAPI
from typing import List
import uvicorn
from Sof_to_FPGA import FPGA_flash
from Find_arduino import Find_Arduino
# import configparser

def Script_file_detect(User_path_to_file, root_path):
    print(root_path)
    # Создание файла с текущими ошибками в файле скрипта
    script_file_path = "%"

    # Поиск файла скрипта, создание переменной пути к данному файлу
    if User_path_to_file != "":
        for root, dirs, files in os.walk(root_path + '/' + User_path_to_file):
            for file in files:
                if file.endswith(".txt") \
                        and not file.endswith(".sof") \
                        and not (file.endswith("JTAG_config.txt")) \
                        and not (file.endswith("Compil_result.txt")) \
                        and not (file.endswith("errors.txt")) \
                        and not (file.endswith("video_timing.txt")) \
                        and not (root == "db"):
                    script_file_name = file
                    script_file_path = root + '/' + script_file_name
                    print(script_file_path)
    return (script_file_path)
# Словарь текущих состояний переключателей
switches = dict([(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)])
# Скрипт передачи управляющих команд на плату Ардуино
def Serial_delivery(arduino, cur_action, curent_pin, sleep, sleep_dur):
    global switches
    # Распознаем текущую команду
    if cur_action:
        # Проверяем текущее состояние переключателя
        print("Curent_pin = ", curent_pin)
        print("Curent_pin_status = ", switches[int(curent_pin)])
        if switches[int(curent_pin)] == 0:
            comand_sw1 = str(curent_pin) + "H"
            arduino.write(bytes(comand_sw1, 'utf-8'))
            print("SW - {} - H".format(curent_pin))
            switches[int(curent_pin)] = 1

        else:# switches[int(curent_pin)] == 1:
            comand_sw2 = str(curent_pin) + "L"
            print("SW - {} - L".format(curent_pin))
            arduino.write(bytes(comand_sw2, 'utf-8'))
            switches[int(curent_pin)] = 0
        #arduino.write(bytes(comand_sw1, 'utf-8'))
        time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        time.sleep(1)
        print(data, '\n')
        GUI.print_log("Номер пина распознанный на плате ", data)
        # Изменяем состояние данного переключателя в словаре на текущее
        if sleep:
            print("sleep for ", sleep_dur)
            GUI.print_log("sleep for ", sleep_dur)
            time.sleep(sleep_dur)
            print("sleep is over")
            GUI.print_log("sleep is over")

    else:
        comand_but1 = str(curent_pin) + "H"
        arduino.write(bytes(comand_but1, 'utf-8'))
        print("BT - {} - H".format(curent_pin))
        time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        time.sleep(1)
        print(data, '\n')
        GUI.print_log("Номер пина распознанный на плате ", data)

        comand_but2 = str(curent_pin) + "L"
        arduino.write(bytes(comand_but2, 'utf-8'))
        print("BT - {} - L".format(curent_pin))
        time.sleep(1)
        # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
        data = str(arduino.readline().decode().strip('\r\n'))
        time.sleep(1)
        print(data, '\n')
        GUI.print_log("Номер пина распознанный на плате ", data)
        # Запускаем процесс ожидания задержки, указанной пользователем
        if sleep:
            print("sleep for ", sleep_dur)
            GUI.print_log("sleep for ", sleep_dur)
            time.sleep(sleep_dur)
            print("sleep is over")
            GUI.print_log("sleep is over")

            # Передаем сигнал о необходимости перевести в неактивное положение необходимую кнопку
            comand_but2 = str(curent_pin) + "L"
            arduino.write(bytes(comand_but2, 'utf-8'))
            print("BT - {} - L".format(curent_pin))
            time.sleep(1)
            # Получаем ответ от платы Ардуино об удачной отправке данного сигнала
            data = str(arduino.readline().decode().strip('\r\n'))
            time.sleep(1)
            print(data, '\n')
            GUI.print_log("Номер пина распознанный на плате ", data)
    return switches

def Arduino_Serial(script_file_path, Arduino_port):
    # Открываем файл сценария
    input_file = open(script_file_path)

    config = configparser.ConfigParser()
    config.read("Config.ini")

    # Выведем общее количество строк в файле
    print(len(re.findall(r"[\n']+?", open(script_file_path).read())))
    all_strings = len(re.findall(r"[\n']+?", open(script_file_path).read()))

    # Выведем количество без пустых строк
    print(len(re.findall(r"[\n']+", open(script_file_path).read())))
    GUI.print_log("Строк в файле сценария ", len(re.findall(r"[\n']+", open(script_file_path).read())))
    strings = len(re.findall(r"[\n']+", open(script_file_path).read()))

    time.sleep(1)

    # Открываем файл текущими ошибками в файле скрипта
    # errors_file = open(errs_path, "w")

    # Построчно читаем файл сценария
    lines = input_file.readlines()

    # Задаем основные переменные для распознавания файла сценария
    but = ["button", "but", "But", "Button"]
    sw = ["switch", "sw", "Switch", "Sw"]
    end = ["end"]
    delay = ["delay"]
    start = ["ardok"]
    current_commands = 0

    # Подключаемся к плату Ардуино через последовательный порт, к заранее определенному COM порту
    arduino = serial.Serial(port=Arduino_port, baudrate=9600, timeout=.1)
    y = 0
    # Ожидаем успешного подключения
    time.sleep(3)

    # Отправляем контрольную последовательность и ожидаем положительного ответа
    while y != 1:
        poslanie = "Hello"
        print("Подключение к плате Ардуино")
        GUI.print_log("Подключение к плате Ардуино")
        arduino.write(bytes(poslanie, 'utf-8'))
        data = str(arduino.readline().decode().strip('\r\n'))
        if str(data).count(start[0]):
            print("Контрольная последовательность получена")
            GUI.print_log("Контрольная последовательность получена")
            y += 1

    # Начало передачи управляющих сигналов на плату Ардуино
    print("Начало передачи сигналов")
    GUI.print_log("Начало передачи сигналов")
    # Выполняем проходку по непустым строкам файла сценария
    for i in range(strings):
        wrong_delay = 0
        end_of_file = 0
        sleep_dur = 0
        # Поиск численного значения в строке
        num = re.findall(r'\d+', str(lines[i]))
        false_pin = False
        cur_action = 2
        sleep = 0

        # Собираем число из списка отдельных чисел в строке
        for item in num:
            numbers = int(item)

        # Определяем текущее действие (нажаите кнопки или нажатие переключателя)
        for j in range(len(but)):
            if (lines[i].count(but[j])):
                cur_action = 0      # Текущей командой является нажатие кнопки
            elif (lines[i].count(sw[j])):
                cur_action = 1      # Текущеу командой является переключение переключателя
        if (lines[i].count(end[0])):
            end_of_file = 1
        # Определяем наличие задержки по времени к данному действию
        if not(end_of_file):
            if (lines[i + 1].count(delay[0])) and (cur_action != 2):
                sleep = 1
                sleep_num = re.findall(r'\d+', str(lines[i + 1]))
                #i = i + 1
                for item in sleep_num:
                    sleep_dur += int(item)

                # Обработка ошибки слишком большой длительности записи видео (с указанием конкретной строки)
                if sleep_dur > 30:
                    delay_string = i + 1
                    wrong_delay = 1
                    # errors_file.write("Длительность задержки не больше 30 секунд (строка: " + str(delay_string) + ")\n")

        # В случае, если строка не пустая, определяем верно ли указаны номера кнопок и переключателей
        if lines[i] != "\n" and lines[i] != "":
            print(numbers)
            GUI.print_log("Номер текущего пина ", numbers)
            if (sleep != 1) and (cur_action != 2):

                # Если номер кнопки или переключателя больше 8 или меньше 1, данная команда не обрабатывается
                if (int(numbers) > 8) or (int(numbers) < 1):
                    i += 1
                    false_pin = True

                    # Запись ошибки невверно указанного номера пина (с указанием конкретной строки)
                    # errors_file.write("Количество активных пинов равно 9 (строка " + str(i) + ")\n")
                    print("Неверно указан номер пина\n")
        # Если строка пустая, пропускаем её
        if (lines[i] == "\n"):
            i += 1

        # В случае, если номер пина введен верно, и строка не является пустой, начинаем обработку команды
        elif (false_pin == False):

            # Обработка команд управления
            # Обработка нажатия переключателя
            if (cur_action == 1):
                # Проверяем данную команду на предмет установленных задержек
                if (sleep) and (not(wrong_delay)):
                    # Запускаем функцию передачи управляющего сигнала на плату Arduino
                    switches=Serial_delivery(arduino, 1, num[0], 1, sleep_dur)
                    current_commands += 1
                    i += 1
                    num[0] = 0
                if not(lines[i].count(delay[0])):
                    switches=Serial_delivery(arduino, 1, num[0], 0, 0)
                    current_commands += 1

            # Обработка нажатия кнопки
            elif (cur_action == 0):
                # Проверяем данную команду на предмет установленных задержек
                if sleep and (not(wrong_delay)):
                    switches=Serial_delivery(arduino, 0, num[0], 1, sleep_dur)
                    current_commands += 1
                else:
                    switches=Serial_delivery(arduino, 0, num[0], 0, 0)
                    current_commands += 1

            # Определяем ключ окончания обработки файла сценария
            if (lines[i].count(end[0])):
                print(switches)
                # Закрываем файл сценария пользователя
                input_file.close()
                # Выводим итоговое количество команд в файле сценария
                break
    # Закрываем файл ошибок, и ещё раз закрываем файл сценария
    input_file.close()
    # errors_file.close()
    print("Total_commands = ", current_commands)
    # = current_commands
    return ("Ok", current_commands)

 # Если файл сценария существует
def main(root_path, User_path_to_file, script_file_path):
    if os.path.exists(script_file_path):
        # Запускаем процесс обработки пользовательской прошивки
        sof_path = "#"
        # Запускаем функцию взаимодействия с платой Ардуино, выводим порт подключения
        Arduino_port = Find_Arduino(root_path=root_path)
        print(Arduino_port, '\n')
        print(Arduino_port[0:3], '\n')

        # Обрабатываем ошибку поиска порта подключения платы Ардуино
        if Arduino_port[0:3] != 'COM':
            # errors_file.write("Проблема при передаче управляющих сигналов, свяжитесь с преподавателем\n")
            print("Неверный порт подключения Arduino")
        # Запускаем функцию взаимодействия с платой ПЛИС
        FPGA_chek, pr_type = FPGA_flash(User_path=User_path_to_file, FPGA_num=1, root_path=root_path)
        # Производим обработку ошибок компиляции проекта или прошивки платы
        if FPGA_chek != "OK":
            returncode = 1
            # errors_ = 1
            # errors_file.write("Проблема с компиляцией проекта, или прошивкой платы, изучите файлы логов\n")

        # Производим поиск файла прошивки после окончания прошивки платы ПЛИС или компиляции проекта
        for root, dirs, files in os.walk(root_path + '/' + User_path_to_file):
            for file in files:
                if file.endswith(".sof"):
                    sof_file_name = file
                    sof_path = root + '/' + sof_file_name

                    print(sof_path)
                    GUI.print_log("Путь к файлу прошивки ", sof_path)

        # Маркер существования видеофайла
        vid_chek = "video_none"

        # Если файл прошивки существует, и работа с платой ПЛИС успешна, запускаем обработку прошивки пользователя
        if os.path.exists(sof_path) and FPGA_chek == "OK":

            # Открываем файл сценария
            input_file = open(script_file_path)

            # print(len(re.findall(r"[\n']+", open(script_file_path).read())))
            # Построчно читаем файл сценария
            lines = input_file.readlines()
            # Найдем количество не пустых строк в файле сценария
            strings = len(re.findall(r"[\n']+", open(script_file_path).read()))
            print("ВСЕГО НЕ ПУСТЫХ СТРОК = ", strings)
            sleep_timing = 0
            for i in range(strings):
                # Поиск указания временных задержек
                if lines[i].count(delay[0]):
                    # Поиск чисел в конкретной строке файла сценария
                    sleep_num = re.findall(r'\d+', str(lines[i]))
                    for item in sleep_num:
                        sleep_dur = int(item)
                    # Длительность единократной задержки не более 30 секунд
                    if sleep_dur > 30:
                        sleep_dur = 30
                    print("Очередной слип на", sleep_dur)
                    sleep_timing = sleep_timing + sleep_dur
            strings = strings

            # Выводим суммарные тайминг
            # Длительностт видео не может быть больше 2 минут
            if strings > 120:
                strings = 120
            # Выводим суммарное время записи видео

            # Создаем файл временных параметров записи видео
            video_file = open("video_timing.txt", "w")
            # Записываем в данный файо необходимую длительность видео
            video_file.write(str(strings))
            video_file.close()
            input_file.close()
            time.sleep(1)

            # Запускаем функцию записи видео
            video_script_path = root_path + '/' + "Video.py"
            python_path = "C:/Users/UL_CAD_REMOTE/AppData/Local/Programs/Python/Python38/python.exe"
            print("---------------------------------------------------------------------------------------------------")
            print("PYTHON _PATH = ", python_path)
            print("VIDEO_SCRIPT_PATH = ", video_script_path)
            print("---------------------------------------------------------------------------------------------------")
            Video_chek = subprocess.Popen([python_path, video_script_path])

            # Запускаем функцию последовательной передачи управляющих команд на плату Ардуино
            serial, command_num = Arduino_Serial(script_file_path=script_file_path,
                                                 Arduino_port=Arduino_port)

            # Возвращаем флаг удачного завершения процесса передачи данных
            if serial == "OK":
                print("Передача данных окончена")

            # Ожидаем окончания процесса записи видео
            Video_chek.wait()
            # Перепроверяем завершился ли процесс записи видео
            while Video_chek.poll() is None:
                time.sleep(0.5)
            # Выводим код возврата процесса записи видео
            print("Запись видео возвращает:", Video_chek.returncode)
    return 'OK'
# def Delete_files(root_path, User_path_to_file):
#     users_dir = root_path + '/' + User_path_to_file
#     # Производим поиск файла окончания процесса записи видео
#     if os.path.exists(root_path + "/video_done.txt") \
#             and os.path.isfile(root_path + "/video_done.txt"):
#         print("Удаление файла video_done.txt\n")
#         # Удаляем данный файл
#         os.remove(root_path + "/video_done.txt")
#
#     # Производим поиск файла, содержащего длительность записи видео
#     if os.path.exists(root_path + "/video_timing.txt") \
#             and os.path.isfile(root_path + "/video_timing.txt"):
#         print("Удаление файла video_timing.txt\n")
#         # Удаляем данный файл
#         os.remove(root_path + "/video_timing.txt")

app = FastAPI()
@app.post("/upload")
def upload(files: List[UploadFile] = File(...)):
    # path = sys.argv[0]
    # new_path = path.split('/')[:-1]
    # new_str_path = "/".join(new_path)
    # print(new_str_path)
    # root_path = new_str_path
    # User_path_to_file = 'Input_files'
    # script_file_path = Script_file_detect(User_path_to_file, root_path)
    # print(script_file_path)
    # check = main(root_path, User_path_to_file, script_file_path)
    # print(check)
    # if (check == 'OK'):
    #     kekich = get_data_from_video()
    #     print(kekich)
    for file in files:
        try:
            try:
                os.mkdir("Input_files")
                print(os.getcwd())
            except Exception as e:
                print(e)
            file_name = os.getcwd() + "/files/" + file.filename.replace(" ", "-")
            with open(file_name, 'wb+') as f:
                f.write(file.file.read())
                f.close()
            contents = file.file.read()
            with open(file.filename, 'wb') as f:
                f.write(contents)
        # except Exception:
        #     return {"message": "There was an error uploading the file(s)"}
        finally:
            file.file.close()
    User_path_to_file = 'Input_files'
    script_file_path = Script_file_detect(User_path_to_file, root_path)
    print(script_file_path)
    check = main(root_path, User_path_to_file, script_file_path)
    print(check)
    if (check == 'OK'):
        kekich = get_data_from_video()
        print(kekich)

    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}

if __name__ == "__main__":
    # path = sys.argv[0]
    # new_path = path.split('/')[:-1]
    # new_str_path = "/".join(new_path)
    # print(new_str_path)
    # root_path = new_str_path
    # User_path_to_file = 'Input_files'
    # script_file_path = Script_file_detect(User_path_to_file, root_path)
    # main(root_path, User_path_to_file, script_file_path)
    uvicorn.run(app, host="0.0.0.0", port=8001)