import os
import shutil
import subprocess
from pathlib import Path
# #os.system("rd /s /q %systemdrive%\$Recycle.bin")
# os.system("rd /s %systemdrive%\$Recycle.bin")
# #os.system("Y")
# time.sleep(3)
#input("Y")

from win32com.shell import shell, shellcon   # pip install pywin32

def empty(confirm, show_progress, sound):
    recycle_bin_path = "C:\$RECYCLE.BIN"
    for files in os.listdir(recycle_bin_path):
        print (files)
    try:
        flags = 0
        if not confirm:
            flags |= shellcon.SHERB_NOCONFIRMATION
        if not show_progress:
            flags |= shellcon.SHERB_NOPROGRESSUI
        if not sound:
            flags |= shellcon.SHERB_NOSOUND
        shell.SHEmptyRecycleBin(None, None, flags)
    except:
        print("Корзина пуста")
empty(confirm=False, show_progress=True, sound=True)

# def mycopy(src, dst, follow_symlinks=True):
#     print("video_copying")
#     shutil.copy2(src=src, dst=dst, follow_symlinks=follow_symlinks)
#     return "OK"
# # def robocopy(source, destination, extension=''):
# #     os.system("robocopy {} {} {} /xx /njh".format(source, destination, extension))
# #     return "OK"
# root_path = "C:/PROJECT_930/Prototype_new_3"
# video_path = root_path + "/video/output.mp4"
# User_path_to_file = "student_zip/Desorder2881488"
# copy_dst = root_path + "/" + User_path_to_file + "/Report/output.mp4"
#while vid_exists:
    # if os.path.exists(prot_dir + "video_done.txt"):
    # vid_chek= open("video_done.txt")
    # video_chek = vid_chek.readline()
    # print("File_read,'\n")
    # if os.path.exists("output.mp4") and (video_chek.count(marker)):
    # print(Video_chek)

    # if os.path.exists(video_path) and os.path.exists(root_path + "/video_done.txt") \
    #         and vid_chek.find(video_end_chek) != -1:  # Video_chek.stdout != "b''":
    #     print("File_est", '\n')
    #     time.sleep(5)
# print("video_copy")
# #a = shutil.copytree(video_path, (root_path + '/' + User_path_to_file + "/Report/output.mp4"), copy_function=mycopy, dirs_exist_ok=True)
# #a = mycopy(src=video_path, dst=root_path + '/' + User_path_to_file + "/Report/output.mp4")
# a = subprocess.run("copy " + video_path + " " + copy_dst)
# if a == 0:
#     print("video_copied")
#     os.remove(video_path)