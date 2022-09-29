import sys
import os
import shutil
import configparser
# if os.path.exists('C:/PROJECT_930/Prototype_with_mail_bot/ul_cad_1.json'):
#     print("kek")
# print(sys.argv[0])
# path = sys.argv[0]
# path_len = len(path.split('/')) - 1
# new_path = path.split('/')[:-1]
# new_str_path = "/".join(new_path)
# print(new_str_path)
#
# print(new_path)
# folder_send = 'C:/PROJECT_930/Prototype_with_mail_bot/Archived/grisha.petuxov'
# for file in os.listdir(folder_send):
#     if file.endswith("zip"):
#         file_path = folder_send + "/" + file
# print(file_path)
# config = configparser.ConfigParser()
# # # with open('Config.ini') as configfile:
# # config.read(configfile)
# config.read("Config.ini")
#
# # Задаем директорию исполняемых файлов quartus
# # Задаем изначальную директорию исполняемых файлов Quartus
# keys = config.keys()
# for key in keys:
#     print(config[key])
# print(config.sections())
# root_directory = config['Direc']['Path']
# Quartus_pgm_path = config['Quartus']['Quartus_pgm_path']
# Quartus_sh_path = config['Quartus']['Quartus_sh_path']
# default = config['DEFAULT']['path']
# print(default)
# #
# # #root_directory = config['Path']['root_path']
# # root_directory = "C:/PROJECT_930/Prototype_new_3"
#
# # Quartus_pgm_path = "C:/intelFPGA_lite/17.0/quartus/bin64/quartus_pgm.exe"
# # Quartus_jtag_path = "C:/intelFPGA_lite/17.0/quartus/bin64/jtagconfig.exe"
# # Quartus_sh_path = "C:/intelFPGA_lite/17.0/quartus/bin64/quartus_sh.exe"
# # root_directory = "C:/PROJECT_930/Prototype_new_3"
#
# print(Quartus_pgm_path)
# print(Quartus_sh_path)
# print(root_directory)
# config['Quartus']['Quartus_pgm_path'] = "Kekser"
# with open('kek.ini', 'w') as configfile:
#     config.write(configfile)

def Files_to_archive(path_to_dir, user_name, for_delivery, users_dir):
    new_path = path_to_dir + '/' + user_name
    # В случае если папка копирования существует, создаем в ней архив с файлами
    if os.path.exists(new_path):
        shutil.rmtree(new_path)
        os.mkdir(new_path)
        os.chdir(new_path)
        shutil.make_archive("result", 'zip', users_dir)
        if for_delivery:
            folder_send = "" + new_path
            return folder_send
    # В случае, если папка пользователя не существует, создаем ее и архив файлов
    else:
        os.mkdir(new_path)
        os.chdir(new_path)
        shutil.make_archive("result", 'zip', new_path)

User_path_to_file="student_zip/grisha.petuxov"
root_path="C:/Project_930/Prototype_with_mail_bot_TO_EXE(2)"
new_users_dir = root_path + "/Archived"
users_dir = root_path + '/' + User_path_to_file
result_directory = User_path_to_file.split('/', 2)[1]

folder_send = Files_to_archive(new_users_dir, result_directory, 1, users_dir)





# path = sys.argv[0]
# path_len = len(path.split('/')) - 1
# new_path = path.split('/')[:-1]
# new_str_path = "/".join(new_path)
# print(new_str_path)
# config = configparser.ConfigParser()
# config.read(new_str_path + "/Config.ini")
# root_path = config['Project']['Path']
# if root_path != new_str_path:
#     config['Project']['Path'] = new_str_path
#     with open(new_str_path + '/Config.ini', 'w') as configfile:
#         config.write(configfile)