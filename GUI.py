import queue
import tkinter
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import Tk, Frame, Menu
from threading import *
import threading
import subprocess
import time
from tkinter import messagebox
from tkinter.ttk import Progressbar
import queue

import quickstart
from quickstart import *
import Boards_search

# from Boards_search import *

global flag_stop
global thread
global flag_new
global proseed_flag
proseed_flag = False
flag_new = True
thread = Thread(target=quickstart.CAD_LOOP, daemon=True)

# global thread2
# thread2 = Thread(target=Boards_search.Board_search, daemon=True)

############################  Стандартные размеры ################################
common_button_height = 2


###########################  Функции  ################################
def TextWrapper(text, win_num):
    if win_num:
        log_work_fpga.configure(state='normal')
        text_field = log_work_fpga
        text_field.insert(tk.END, text)
        text_field.update()
        log_work_fpga.configure(state='disabled')
    else:
        log_find_fpga.configure(state='normal')
        text_field = log_find_fpga
        text_field.insert(tk.END, text)
        text_field.update()
        log_find_fpga.configure(state='disabled')


def print_log(string, string_add=""):
    string = string + (str(string_add))
    TextWrapper(string + "\n", 1)
    string_new = " "


def print_f_log(string):
    #string = string + (str(string_add))
    TextWrapper(string + "\n", 0)
    string_new = " "

# def print_f_log(string, string_add=""):
#     string = string + (str(string_add))
#     TextWrapper(string + "\n", 0)
#     string_new = " "


def clicked_find():  ## Функция запускающая скрипт поиска плат и выводящая результаты в лог
    # global thread2
    log_find_fpga.configure(state='normal')
    # print_f_log("Начало поиска")
    print_f_log("Search start")
    thread2 = Thread(target=Boards_search.Board_search(), daemon=True)
    thread2.start()
    change_status_log(1)
    change_status_find(1)
    log_work_fpga.configure(state='disabled')


def del_log():
    log_find_fpga.configure(state='normal')
    log_find_fpga.delete(1.0, END)
    log_work_fpga.configure(state='disabled')

def del_log2():
    log_work_fpga.configure(state='normal')
    log_work_fpga.delete(1.0, END)
    log_work_fpga.configure(state='disabled')


def change_frame():
    f_top_log.pack()
    f_bottom_log.pack_forget()


def change_frame_back():
    f_top_log.pack_forget()
    f_bottom_log.pack()


def start_work():
    change_status_log(4)
    global flag_stop
    global thread
    flag_stop = False
    log_work_fpga.configure(state='normal')
    print(thread.is_alive())
    if not thread.is_alive():
        thread.start()
    log_work_fpga.configure(state='disabled')


def check_thread(window, thread):
    if thread.is_alive():
        window.after(100, lambda: window.check_thread(thread))
    else:
        window.start_work_button.config(state=tk.NORMAL)


def pause_work():
    change_status_log(3)
    global flag_stop
    log_work_fpga.configure(state='normal')
    # print_log("Поставили на паузу")
    print_log("Paused")
    flag_stop = True
    log_work_fpga.configure(state='disabled')


def change_status_log(type):
    thread3 = Thread(target=change_status_log_sub(type), daemon=True)
    thread3.start()


def change_status_find(type):
    thread3 = Thread(target=change_status_find_sub(type), daemon=True)
    thread3.start()


def change_status_log_sub(type):
    if type == 1:
        cc.delete("all")
        # cc.create_text(10, 20, anchor=W, font="DejavuSansLight", text="Стенд готов к работе", fill="green")
        cc.create_text(10, 20, anchor=W, font="DejavuSansLight", text="The stand is ready to go", fill="green")
    elif (type == 2):
        cc.delete("all")
        cc.create_text(10, 20, anchor=W, font="DejavuSansLight", text="Требуется поиск плат", fill="brown")
    elif (type == 3):
        cc.delete("all")
        cc.create_text(10, 20, anchor=W, font="DejavuSansLight", text="Стенд на паузе", fill="brown")
    elif (type == 4):
        cc.delete("all")
        # cc.create_text(10, 20, anchor=W, font="DejavuSansLight", text="Стенд работает...", fill="green")
        cc.create_text(10, 20, anchor=W, font="DejavuSansLight", text="The stand works...", fill="green")
    elif (type == 5):
        cc.delete("all")
        cc.create_text(10, 20, anchor=W, font="DejavuSansLight", text="Ошибка", fill="red")


def change_status_find_sub(type):
    if type == 1:
        c.delete("all")
        # c.create_text(10, 20, anchor=W, font="DejavuSansLight", text="Стенд готов к работе", fill="green")
        c.create_text(10, 20, anchor=W, font="DejavuSansLight", text="The stand is ready to go", fill="green")
    elif (type == 2):
        c.delete("all")
        c.create_text(10, 20, anchor=W, font="DejavuSansLight", text="Требуется поиск плат", fill="brown")
    elif (type == 3):
        c.delete("all")
        c.create_text(10, 20, anchor=W, font="DejavuSansLight", text="Стенд на паузе", fill="brown")
    elif (type == 4):
        c.delete("all")
        # c.create_text(10, 20, anchor=W, font="DejavuSansLight", text="Стенд работает...", fill="green")
        c.create_text(10, 20, anchor=W, font="DejavuSansLight", text="The stand works...", fill="green")
    elif (type == 5):
        c.delete("all")
        c.create_text(10, 20, anchor=W, font="DejavuSansLight", text="Ошибка", fill="red")


def on_closing():
    try:
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()
    except:
        print()


def block_button():
    if proseed_flag:
        mainmenu.entryconfigure('Работа лабораторного стенда', state='normal')
    else:
        mainmenu.entryconfigure('Работа лабораторного стенда', state='disabled')


###############################################################

window = Tk()
# window.title('Настройка лабораторного стенда.')
window.title('Setting up the lab')
window.geometry('400x800')
window.resizable(width=False, height=False)
# window.resizable(width=False, height=False)

#########################          Фреймы           ###############################

f_top_log = Frame(window)
f_top_log.pack()
f_left_top_log = Frame(f_top_log)
f_rigth_top_log = Frame(f_top_log)
text_result = Frame(f_top_log)

f_left_top_log.pack()
text_result.pack()
f_rigth_top_log.pack()

f_bottom_log = Frame(window)
f_bottom_log.pack_forget()
f_top_annonse = Frame(f_bottom_log)
f_top_bottom_log = Frame(f_bottom_log)
f_bottom_bottom_log = Frame(f_bottom_log)

f_top_annonse.pack()
f_top_bottom_log.pack()
f_bottom_bottom_log.pack()

############################## Меню и подменю ################################

mainmenu = Menu(window)
window.config(menu=mainmenu)
mainmenu.add_command(label='Поиск плат', command=change_frame)  ####, command=change_frame
mainmenu.add_command(label='Работа лабораторного стенда', command=change_frame_back)  ### , command=change_frame_back

####################### Настройка кнопок и их рассположения #############
# lbl = Label(f_left_top_log, text="Поиск всевозможных \n подключенных плат", font=("Arial Bold", 14), width=100)
lbl = Label(f_left_top_log, text="Search for all possible \n connected boards", font=("Arial Bold", 14), width=100)
lbl.pack(side=TOP, fill=X)

# settings_button = Button(f_left_top_log, text="Начать поиск", width=30, command=clicked_find,
#                          height=common_button_height)
settings_button = Button(f_left_top_log, text="Search", width=30, command=clicked_find,  #####
                         height=common_button_height)
settings_button.pack(side=BOTTOM)

# clearlog_button = Button(f_rigth_top_log, text="Очистить лог", command=del_log, width=30, height=common_button_height)
clearlog_button = Button(f_rigth_top_log, text="Clear log", command=del_log, width=30, height=common_button_height)
clearlog_button.pack(side=BOTTOM)

# clearlog_button = Button(f_bottom_bottom_log, text="Очистить лог", command=del_log2, width=30, height=common_button_height)
clearlog_button = Button(f_bottom_bottom_log, text="Clear log", command=del_log2, width=30, height=common_button_height)
clearlog_button.pack(side=BOTTOM)

c = Canvas(text_result, height=30, bg='white')
c.pack(fill=Y)

# Кнопки второго окна &&&&&&&&&&&&&&&&&&

# start_work_button = Button(f_top_bottom_log, text="Запуск", width=30, command=start_work, height=common_button_height)
start_work_button = Button(f_top_bottom_log, text="Start", width=30, command=start_work, height=common_button_height)
start_work_button.pack(side=LEFT)
# stop_work_button = Button(f_top_bottom_log, text="Стоп", width=30, command=pause_work, height=common_button_height)
stop_work_button = Button(f_top_bottom_log, text="Stop", width=30, command=pause_work, height=common_button_height)
stop_work_button.pack(side=RIGHT)

cc = Canvas(f_top_annonse, height=30, bg='white')
cc.pack(fill=Y)

# clearlog_button.grid(column=1, row=5)
#########################################################################
###########################   Добавление эллементов для вывода консоли   ##################################

log_find_fpga = scrolledtext.ScrolledText(f_rigth_top_log, height=37)
log_find_fpga.configure(state='disabled')
log_find_fpga.pack(side=TOP, fill=X)

log_work_fpga = scrolledtext.ScrolledText(f_bottom_bottom_log, height=40)
log_work_fpga.configure(state='disabled')
log_work_fpga.pack(side=TOP, fill=X)


######################################################################
######################### Окна ошибок  ############################

# messagebox.showwarning('Заголовок', 'Текст')  # показывает предупреждающее сообщение
# messagebox.showerror('Заголовок', 'Текст')  # показывает сообщение об ошибке

##################################################################
def main_start_gui():
    try:
        window.protocol("WM_DELETE_WINDOW", on_closing)
    except:
        print("ff")
    block_button()
    change_status_log(2)
    change_status_find(2)
    window.mainloop()


main_start_gui()
