#Добавлена обработка всех возможных ошибок в тексте текстового файла
#Добавлена проверка на наличие текстового файла
#Добавлена обработка пустых строк
#Добавлено создание папки с названием файла скетча
#Добавлена переменная общего пути


import os
import shutil
import re
import time
import serial
import sys
import subprocess
import configparser
from win32com.shell import shell, shellcon

from SOF_TO_FPGA_4 import FPGA_flash
from Find_arduino_v2 import Find_Arduino



def Launch(User_path_to_file):

    # Открываем файл настроек
    # config = configparser.ConfigParser()
    # with open('Config.ini') as configfile:
    #     config.read(configfile)
    #
    #     #Actualised a directory with a script.
    #     # abspath = os.path.abspath(__file__)
    #     # dname = os.path.dirname(abspath)
    #     # os.chdir(dname)
    #
    #     # Задаем директорию проекта
    #     #root_path = config['Path']['root_path']
    root_path ="C:/PROJECT_930/Prototype_new_3"

    #Поиск файла прошивки

    # zip_dir = User_path_to_file.split("/",1)[0]
    # main_dir = root_path + "/" + zip_dir
    # print("ZIP DIR PATH = " + zip_dir,'/n')
    # if os.path.exists(zip_dir):
    #     for dirs in os.listdir(zip_dir):
    #         shutil.rmtree(zip_dir + "/" + dirs)




    # scetch_name = "scetch"
    errs_f = "errors.txt"

    #errs_name = os.path.join(root_path,User_path_to_file)
    #errs_name = os.path.join(root_path, User_path_to_file)
    errs_name = root_path + "/" + User_path_to_file
    #errs_path = os.path.join(errs_name,errs_f)
    errs_path = errs_name + '/' + errs_f
    errors_file = open(errs_path, "w")

    script_file_path = "%"
    sof_path = "%"

    for root, dirs, files in os.walk(User_path_to_file):
        for file in files:
            if file.endswith(".txt") \
                    and not file.endswith(".sof") \
                    and not(file.endswith("JTAG_config.txt")) \
                    and not(file.endswith("Compil_result.txt")) \
                    and not(file.endswith("errors.txt"))\
                    and not(file.endswith("video_timing.txt"))\
                    and not(root == "db"):


                script_file_path = root + '/' + file
                result_dir = os.path.join(root_path,root)
                script_file_name = file
                script_file_path = root_path + "/" + script_file_path
                # result_dir = os.path.join(root_path,result_dir)
                print(script_file_path)



    #file_path = os.path.join(root_path,file_path)




    if not os.path.exists(script_file_path):

        errors_file.write("Отсутствует файл сценария\n")
    else:



        # Выведем все строки включая пустые






        if os.path.exists(script_file_path):
            Arduino_port = Find_Arduino()
            print(Arduino_port, '\n')
            print(Arduino_port[0:3], '\n')
            if Arduino_port[0:3] != 'COM':
                errors_file.write("Проблема при передаче управляющих сигналов, свяжитесь с преподавателем\n")

            # print(FPGA_flash(User_path=User_path_to_file))
            if FPGA_flash(User_path=User_path_to_file) != 'OK':
                errors_file.write("Проблема с компиляцией проекта, или прошивкой платы, изучите файлы логов\n")



            for root, dirs, files in os.walk(User_path_to_file):
                for file in files:
                    if file.endswith(".sof"):
                        sof_path = os.path.join(root, file)
                        print(sof_path)
                        sof_path = root_path + "/" + sof_path
                        sof_file_name = file
                        print(sof_path)

            if os.path.exists(sof_path):
                Video_chek = subprocess.Popen([sys.executable, 'Video.py'], stdout=subprocess.PIPE)


                input_file = open(script_file_path)
                print(result_dir)


                print(len(re.findall(r"[\n']+?", open(script_file_path).read())))
                all_strings = len(re.findall(r"[\n']+?", open(script_file_path).read()))

                # выведем количество без пустых строк
                print(len(re.findall(r"[\n']+", open(script_file_path).read())))
                strings = len(re.findall(r"[\n']+", open(script_file_path).read()))

                video_file = open("video_timing.txt", "w")
                video_file.write(str(strings * 3))
                video_file.close()
                #subprocess.Popen([sys.executable, 'Video.py'])

                time.sleep(3)
                vid_chek = str(Video_chek.stdout)
                # Запускаем процесс прошивки платы ПЛИС в подпроцессе

                #software = subprocess.call("C:\\intelFPGA_lite\\17.0\\quartus\\bin64\\quartus_pgm.exe -c \"USB-Blaster [USB-0]\" -m JTAG -o p;C:/PROJECT_930/PROTOTYPE/golden.sof")
                #time.sleep(1)

                #FPGA_flashing = subprocess.Popen([sys.executable, 'SOF_TO_FPGA_4.py'], )

                #os.system("@echo off")
                #os.system("cd C:\\intelFPGA_lite\\17.1\\quartus\\bin64\ rem")# quartus_pgm.exe -m JTAG -o p; sof_path Jtag_info.txt)
                #os .system("quartus_pgm.exe -m JTAG -o p;{0}> Jtag_info.txt".format(str(sof_path)))
                #os.system("quartus_pgm.exe -m JTAG -o p; golden.sof > Jtag_info.txt")

                # В подпроцессе запускаем запись видео
                #subprocess.call("Video.py", shell = True)
                #exec(open("Video.py").read())
                #subprocess.call("Video.py", shell=True)
                #print(sys.executable)

                # Arduino_port = subprocess.Popen([sys.executable, 'Find_arduino_v2'],
                #                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                #                                 text=True)


                time.sleep(1)




                errors_file = open(errs_path, "w")

                lines = input_file.readlines()



                curent_pin = 0
                but = ["button"]
                sw = ["switch"]
                end = ["end"]
                numbers = ["09"]
                delay = ["delay"]
                start = ["ardok"]
                switches = dict([(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)])
                current_commands = 0


                arduino = serial.Serial(port=Arduino_port, baudrate=9600, timeout=.1)
                y = 0

                # waiting for device
                time.sleep(3)

                while y != 1:
                    poslanie = "Hellohel\n"
                    print("prohodka")
                    # st = str(poslanie)
                    arduino.write(bytearray(poslanie, 'utf-8'))
                    # data = arduino.readline()
                    # data = arduino.read(arduino.inWaiting())
                    data = str(arduino.readline().decode().strip('\r\n'))
                    if str(data).count(start[0]):
                        print("Poluchenorazhreshenie")
                        # data = ""
                        # poslanie = "1H"
                        # arduino.write(bytes(poslanie, 'utf-8'))
                        y += 1
                # data = arduino.read(arduino.inWaiting())
                print("Начало передачи сигналов")
                for i in range(strings):

                    # if (lines[i] == "\n"):
                    #     i = i + 1
                    #     print("Empty string")
                    # print(lines[i][-2])
                    num = re.findall(r'\d+', str(lines[i]))
                    false_pin = False
                    # #if (i != all_strings):
                    #     #if (int(lines[i][-2]) > 8) or (int(lines[i][-2]) < 1):
                    # print(num)
                    for item in num:
                        numbers = int(item)
                    if (lines[i] != "\n"):
                        print(numbers)
                        if (int(numbers) > 8) or (int(numbers) < 1):
                            i += 1
                            false_pin = True
                            errors_file.write("Количество активных пинов равно 9 (строка " + str(i) + ")\n")
                            print("not write pin\n")
                    if (lines[i] == "\n"):
                        i += 1
                    #    print("Empty string")

                    # if (i):
                    #     i = i + 1
                    #     errors_file.write("Количество активных пинов равно 9\n")
                    #     print("Количество активных пинов равно 9\n")

                    elif (false_pin == False):
                        if (lines[i].count(but[0])):  # Кнопки
                            curent_pin = num[0]
                            comand_but1 = str(curent_pin) + "H\n"
                            y = 0
                            data = ""
                            # while y != 1:
                            arduino.write(bytearray(comand_but1, 'utf-8'))
                            # arduino.write(bytes("", 'utf-8'))
                            time.sleep(1)
                            # if data.count(h1[0]):
                            # y += 1
                            print("EST")
                            # arduino.write(bytes("Hoy", 'utf-8'))
                            print(comand_but1)
                            time.sleep(0.1)
                            print(data)
                            data = ""
                            time.sleep(0.1)
                            comand_but2 = str(curent_pin) + "L\n"
                            arduino.write(bytearray(comand_but2, 'utf-8'))
                            print(comand_but2)
                            time.sleep(0.1)
                            print(data)
                            current_commands += 1
                            # print("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100)\n digitalWrite(pin"+str(curent_pin)+", LOW);\n")
                            #
                            # output_file.write("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100);\n digitalWrite(pin"+str(curent_pin)+", LOW);\n")
                        # elif (lines[i].count(sw[0])):
                        #     if switches[i-1] == 0:
                        #         print("digitalWrite(pin" + str(lines[i][-2]) + ", HIGH);\n sleep(500)\n")  # digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                        #         output_file.write("digitalWrite(pin" + str(lines[i][-2]) + ", HIGH);\n sleep(500)\n") #digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                        #         switches[i-1] = 1

                        elif (lines[i].count(sw[0])) and (switches[int(num[0])] == 0) and (false_pin != True):  # Свитч 0
                            curent_pin = num[0]
                            # print("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100);\n")  # digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                            # output_file.write("digitalWrite(pin" + str(curent_pin) + ", HIGH);\n delay(100);\n") #digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                            # switches[int(curent_pin)] = 1
                            comand_sw1 = str(curent_pin) + "H\n"
                            arduino.write(bytearray(comand_sw1, 'utf-8'))
                            print(comand_sw1)
                            time.sleep(1)
                            print(data)
                            time.sleep(0.1)
                            switches[int(curent_pin)] = 1
                            current_commands += 1

                        elif (lines[i].count(sw[0])) and switches[int(num[0])] == 1 and false_pin != True:  # Свитч 1
                            curent_pin = num[0]
                            # print("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(100);\n")  # digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                            # output_file.write("digitalWrite(pin" + str(curent_pin) + ", LOW);\n delay(100);\n") #digitalWrite(pin"+str(lines[i][-2])+", LOW);\n")
                            # switches[int(curent_pin)] = 0
                            # switches.insert(int(lines[i][-2]),1)
                            comand_sw2 = str(curent_pin) + "L\n"
                            arduino.write(bytearray(comand_sw2, 'utf-8'))
                            print(comand_sw2)
                            time.sleep(1)
                            print(data)
                            time.sleep(0.1)
                            switches[int(curent_pin)] = 0
                            current_commands += 1

                        elif (lines[i].count(end[0])):
                            print(switches)
                            input_file.close()
                            print(current_commands)
                            break
                # output_file.close()
                input_file.close()
            else:
                errors_file.write("Отсутствует файл прошивки или проект на ПЛИС\n")
        else:
            errors_file.write("Отправте данные повторно, включая файл сценария\n")
            #errors_file.close()

    #users_dir = os.path.join(root_path,User_path_to_file)
    users_dir = root_path + '/' + User_path_to_file
    #    os.remove(files)
    #shutil.copy(r"C:\PROJECT_930\Prototype_new_2\result.zip", "" + User_path_to_file)
    #for files in os.listdir(users_dir):
        #if not files.endswith("output.mp4"):
        #    errors_file.write("Отсутствует файл видеозаписи работы платы, перезалейте свои файлы\n")
    errors_file.close()

    #serial.Serial.close(arduino)
    if os.path.exists(User_path_to_file + "/filename.zip"):
        os.remove(User_path_to_file + "/filename.zip")

    chek = 1

    os.chdir(users_dir)
    print(users_dir,'\n')

    chek1 = ""
    chek2 = ""
    log_name = "@"
    er_name = "$"
    config_file = "!"
    for files in os.listdir(users_dir):
        if files.find("errors.txt") != -1:
            check_er = open(files)
            chek1 = check_er.read(2)
            er_name = files
            check_er.close()
            #print(chek1, '\n')

        print('\n')

        if files.find("Proj_compil_result.txt") != -1:
            check_comp = open(files)
            chek2 = check_comp.read(2)
            log_name = files
            check_comp.close()
            #print(chek2, '\n')

        time.sleep(2)

        config_name = "JTAG_config.txt"
        if config_name in files:
            config_file = files
            #print(chek2, '\n')

    errs_file_path = users_dir + "/" + er_name
    compil_path = users_dir + "/" + log_name
    config_path = users_dir + "/" + config_file

    if chek1 == "" and os.path.exists(errs_file_path):
        os.remove(users_dir + "/" + er_name)

    if chek2 == "" and os.path.exists(compil_path):
        os.remove(users_dir + "/" + log_name)

    # Перемещение файлов в конечную папку пользователя
    if not os.path.exists(users_dir + "/" + "Report"):
        os.mkdir(users_dir + "/" + "Report")


    print("File with errors = " + er_name,'\n')
    if os.path.exists(errs_file_path):
        print("Перенос файла ошибок\n")
        shutil.copy(errs_file_path, users_dir + "/" + "Report" + "/" + er_name)
        time.sleep(1)
        os.remove(errs_file_path)


    print("File_compil = " + log_name,'\n')
    if os.path.exists(compil_path):
        print("Перенос файла отчета компиляции\n")
        shutil.copy(compil_path, users_dir + "/" + "Report" + "/" + log_name)
        time.sleep(1)
        os.remove(compil_path)



    print("Config file = " + config_file)
    if os.path.exists(config_path):
        print("Перенос файла отчета прошивки\n")
        shutil.copy(config_path, users_dir + "/" + "Report" + "/" + config_file)
        time.sleep(1)
        os.remove(config_path)



    print("TXT_script_file = ", script_file_path)
    print(script_file_path,'\n')
    if os.path.exists(script_file_path):
        print("Перенос файла сценария\n")
        shutil.copy(script_file_path, users_dir + "/" + "Report" + "/" + script_file_name)
        time.sleep(1)
        os.remove(script_file_path)

    print("SOF_FILE = ", sof_path)
    print(sof_path, '\n')
    if os.path.exists(sof_path):
        print("Перенос файла прошивки\n")
        shutil.copy(sof_path, users_dir + "/" + "Report" + "/" + sof_file_name)
        time.sleep(1)
        os.remove(sof_path)


    vid_exists = True
    marker = ["done"]
    video_fragment = "subprocess.Popen object at"

    # Проверка на окончание записи видео
    video_end_chek = "<_io.BufferedReader"
    # video_found = True
    # while video_found:
    #     try:
    #         vid_chek = str(Video_chek.stdout)
    #         if vid_chek.find(video_end_chek) != -1:

    vid_chek = "video_none"
    print(vid_chek,'\n')
    i = 0
    while vid_exists or i == 1:
        #if os.path.exists(prot_dir + "video_done.txt"):
            # vid_chek= open("video_done.txt")
            #video_chek = vid_chek.readline()
            #print("File_read,'\n")
        #if os.path.exists("output.mp4") and (video_chek.count(marker)):
        #print(Video_chek)
        video_path = root_path + "/output.mp4"
        if os.path.exists(video_path) and os.path.exists(root_path + "/video_done.txt")\
                and vid_chek.find(video_end_chek) != -1:#Video_chek.stdout != "b''":
            print("File_est",'\n')
            time.sleep(15)
            shutil.copy(video_path,  root_path + '/' + User_path_to_file + "/Report/output.mp4")
            time.sleep(15)
            os.remove(video_path)
            vid_exists = False
        else:
            i += 1
            vid_exists = False

    if os.path.exists(root_path + "/video_done.txt")\
            and os.path.isfile(root_path + "/video_done.txt"):
        print("Удаление файла video_done.txt\n")
        os.remove(root_path + "/video_done.txt")

    if os.path.exists(root_path + "/video_timing.txt")\
            and os.path.isfile(root_path + "/video_timing.txt"):
        print("Удаление файла video_timing.txt\n")
        os.remove(root_path + "/video_timing.txt")
    # shutil.make_archive("Your_archive", 'zip', User_path_to_file + "//Your_archive.zip")
    #archive = zipfile.ZipFile('result.zip', 'w')
    #for file in os.listdir(users_dir):
        # archive.write(file, compress_type=zipfile.ZIP_DEFLATED)
    new_users_dir = root_path + "/Archived"
    archive_dir = root_path + "/Archive"
    os.chdir(new_users_dir)

    result_directory = User_path_to_file.split('/', 2)[1]
    if os.path.exists(new_users_dir + "/" + result_directory):
        shutil.rmtree(new_users_dir + "/" + result_directory)
        os.mkdir(result_directory)
        os.chdir(os.path.join(new_users_dir, result_directory))
        #os.rmdir(new_users_dir + "/" + result_directory)
        print("Создание архива на отправку/n")
        shutil.make_archive("result", 'zip', users_dir)
        #     time.sleep(2)
        print("Архив на отправку создан/n")
    else:
        os.mkdir(result_directory)
        os.chdir(os.path.join(new_users_dir, result_directory))
        print("Создание архива на отправку")
        shutil.make_archive("result", 'zip', users_dir)
        #     time.sleep(2)
        print("Архив на отправку создан")
    if os.path.exists(archive_dir):
        users_directory = archive_dir + "/" + result_directory
        if os.path.exists(users_directory):
            shutil.rmtree(users_directory)
            os.mkdir(users_directory)
            os.chdir(users_directory)
            print("Создание архива в хранилище/n")
            shutil.make_archive("result", 'zip', users_dir)
            #     time.sleep(2)
            print("Архив в хранилище создан/n")
        else:
            os.mkdir(users_directory)
            os.chdir(users_directory)
            print("Создание архива в хранилище/n")
            shutil.make_archive("result", 'zip', users_dir)
            #     time.sleep(2)
            print("Архив в хранилище создан/n")
    else:
        os.chdir(root_path)
        os.mkdir(archive_dir)
        users_directory = archive_dir + "/" + result_directory
        if os.path.exists(users_directory):
            shutil.rmtree(users_directory)
            os.mkdir(users_directory)
            os.chdir(users_directory)
            print("Создание архива в хранилище/n")
            shutil.make_archive("result", 'zip', users_dir)
            #     time.sleep(2)
            print("Архив в хранилище создан/n")
        else:
            os.mkdir(users_directory)
            os.chdir(users_directory)
            print("Создание архива в хранилище/n")
            shutil.make_archive("result", 'zip', users_dir)
            #     time.sleep(2)
            print("Архив в хранилище создан/n")



    #     # archive.close()
    # for files in User_path_to_file:

    # for files in os.listdir(User_path_to_
    #shutil.copy(users_dir + r"/result/result.zip", r"C:\PROJECT_930\Prototype_new_2\Archived")

    # def empty(confirm, show_progress, sound):
    #     flags = 0
    #     if not confirm:
    #         flags |= shellcon.SHERB_NOCONFIRMATION
    #     if not show_progress:
    #         flags |= shellcon.SHERB_NOPROGRESSUI
    #     if not sound:
    #         flags |= shellcon.SHERB_NOSOUND
    #     shell.SHEmptyRecycleBin(None, None, flags)
    # empty(confirm=False, show_progress=True, sound=False)
    # print("Корзина очищена")
    #config.close()

    return("OK")


#if __name__ == '__main__':
#Launch(User_path_to_file="C:\PROJECT_930\Prototype_new\student_zip\sasha.lorens@yandex.ru")
#Launch(User_path_to_file="C:\intelFPGA_lite\Otladka")
Launch(User_path_to_file="student_zip/Desorder2881488")
#Launch(User_path_to_file="C:\PROJECT_930\Prototype_new_2\student_zip\proverka@mail.ru")