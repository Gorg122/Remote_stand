import os

import time
import cv2
import numpy as np
import json


def Video():
    #cap = cv2.VideoCapture(0)

    # HIGH_VALUE = 10000
    # WIDTH = HIGH_VALUE
    # HEIGHT = HIGH_VALUE



    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #focus = int(capture.get(cv2.CAP_PROP_AUTOFOCUS))
    # capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    # #capture.set(cv2.CAP_PROP_FOCUS, 200)
    # capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    # frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))


    # Get the Default resolutions
    #frame_width = int(capture.get(4))
    #frame_height = int(capture.get(4))
    cur_dir = os.getcwd()
    #os.chdir(cur_dir)
    print(cur_dir)
    # print(width)
    # print(height)
    # print(frame_width)
    # print(frame_height)
    files = "video_timing.txt"
    timing = open(files)
    time_rest = timing.readline()
    print(time_rest)
    timing.close()


    # Define the codec and filename.
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #out = cv2.VideoWriter('output.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    # out = cv2.VideoWriter('video/video.mp4', fourcc, 30.0, (frame_width, frame_height))

    cnt = 0

    # Some characteristics from the original video
    w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # Here you can define your croping values
    # x, y, h, w = 80, 250, 150, 400
    x, y, h, w = 80, 150, 300, 450
    # start = 0
    # cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter('video/video.mp4', fourcc, fps, (w, h))
    tik = time.time()
    print(tik)
    tok = 0.0
    print("tok = ", tok)
    print("tok-tik = ", tok - tik)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while(cap.isOpened() and (tok-tik<=int(time_rest))): #or (start == 1))):
        ret, frame = cap.read()
        crop_frame = frame[y:y + h, x:x + w]

        # Percentage

        # frame_re = frame[60:500, 200:400]
        # ret, image = cap.read()
        # frame = cv2.resize(frame, (500, 500))
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # To grayscale
        color = (255, 0, 0)
        # this is the part to add to your code
        # cv2.rectangle(frame, (0, 0), (500, 200), color, -1)
        #print("tok-tik = ", tok - tik)
        if ret==True :

            #print("tok-tik = ", tok - tik)
            # write the  frame
            tok = time.time()
            # cnt += 1  # Counting frames
            # xx = cnt * 100 / frames
            # print(int(xx), '%')
            out.write(crop_frame)
            # cv2.imshow('frame', frame)
            #if cv2.waitKey(1) & 0xFF == ord('q') & int(tok - tik) >= 30:
            if int(tok - tik) >= int(time_rest):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    time.sleep(4)
    files_2 = "video_done.txt"
    done_chek = open(files_2, "w")
    done_chek.write("done")
    done_chek.close()
    # quit()
def get_data_from_video():
    video_path = 'output.mp4'
    cap = cv2.VideoCapture(video_path)

    # Создайте окно для просмотра видео
    cv2.namedWindow('Video')
    print("I am working")
    # Инициализируйте переменные для управления воспроизведением
    paused = False

    # Задайте координаты квадратов массивом
    # rectangles = [
    #     [(261, 360), (267, 365)],
    #     [(284, 360), (290, 365)],
    #     [(306, 359), (312, 364)],
    #     [(332, 359), (338, 364)],
    #     [(355, 358), (361, 363)],
    #     [(381, 358), (387, 363)],
    #     [(403, 357), (410, 362)],
    #     [(427, 356), (434, 361)],
    #     [(453, 356), (459, 361)],
    #     [(476, 355), (482, 360)],
    #     # First number
    #     [(32, 390), (37, 395)],
    #     [(12, 390), (17, 395)],
    #     [(22, 383), (27, 388)],
    #     [(22, 402), (27, 407)],
    #     [(18, 422), (23, 427)],
    #     [(8, 412), (13, 417)],
    #     [(28, 412), (33, 417)],
    #     # Second number
    #     [(72, 390), (77, 395)],
    #     [(52, 390), (57, 395)],
    #     [(62, 383), (67, 388)],
    #     [(62, 402), (67, 407)],
    #     [(58, 422), (63, 427)],
    #     [(48, 412), (53, 417)],
    #     [(68, 412), (73, 417)],
    #     # Third number
    #     [(117, 387), (122, 392)],
    #     [(98, 387), (103, 392)],
    #     [(107, 380), (112, 385)],
    #     [(107, 399), (112, 404)],
    #     [(103, 419), (108, 424)],
    #     [(93, 409), (98, 414)],
    #     [(113, 409), (118, 414)],
    #     # Fourth number
    #     [(155, 387), (160, 392)],
    #     [(138, 387), (143, 392)],
    #     [(148, 380), (153, 385)],
    #     [(145, 399), (150, 404)],
    #     [(146, 419), (151, 424)],
    #     [(136, 409), (141, 414)],
    #     [(153, 409), (158, 414)],
    #     # Fifth number
    #     [(198, 387), (203, 392)],
    #     [(178, 387), (183, 392)],
    #     [(188, 380), (193, 385)],
    #     [(188, 399), (193, 404)],
    #     [(186, 419), (191, 424)],
    #     [(176, 409), (181, 414)],
    #     [(196, 409), (201, 414)],
    #     # Sixth number
    #     [(240, 385), (245, 390)],
    #     [(220, 385), (225, 390)],
    #     [(230, 378), (235, 383)],
    #     [(228, 397), (233, 402)],
    #     [(228, 417), (233, 422)],
    #     [(218, 407), (223, 412)],
    #     [(238, 407), (243, 412)],
    # ]
    rectangles = [
        [(333, 155), (340, 150)],
        [(317, 155), (324, 150)],
        [(301, 155), (308, 150)],
        [(285, 156), (292, 151)],
        [(270, 156), (277, 151)],
        [(254, 157), (261, 152)],
        [(238, 157), (245, 152)],
        [(222, 157), (229, 152)],
        [(207, 159), (214, 154)],
        [(191, 159), (198, 154)],
        # First number
        [(49, 187), (53, 191)],
        [(51, 172), (55, 176)],
        [(44, 167), (48, 171)],
        [(44, 177), (48, 181)],
        [(38, 172), (42, 176)],
        [(36, 187), (40, 191)],
        [(42, 192), (46, 196)],
        # Second number
        [(74, 187), (78, 191)],
        [(76, 172), (80, 176)],
        [(69, 167), (73, 171)],
        [(69, 177), (73, 181)],
        [(63, 172), (67, 176)],
        [(61, 187), (65, 191)],
        [(67, 192), (71, 196)],
        # Third number
        [(99, 187), (103, 191)],
        [(101, 172), (105, 176)],
        [(94, 167), (98, 171)],
        [(94, 177), (98, 181)],
        [(88, 172), (92, 176)],
        [(86, 187), (90, 191)],
        [(92, 192), (96, 196)],
        # Fourth number
        [(124, 187), (128, 191)],
        [(126, 172), (130, 176)],
        [(119, 167), (123, 171)],
        [(119, 177), (123, 181)],
        [(113, 172), (117, 176)],
        [(111, 187), (115, 191)],
        [(117, 192), (121, 196)],
        # Fifth number
        [(149, 187), (153, 191)],
        [(151, 172), (155, 176)],
        [(144, 167), (148, 171)],
        [(144, 177), (148, 181)],
        [(138, 172), (142, 176)],
        [(136, 187), (140, 191)],
        [(142, 190), (146, 194)],
        # Sixth number
        [(174, 187), (178, 191)],
        [(176, 172), (180, 176)],
        [(169, 167), (173, 171)],
        [(169, 177), (173, 181)],
        [(163, 172), (167, 176)],
        [(161, 187), (165, 191)],
        [(167, 190), (171, 194)],
    ]


    # Rectangles for numbers
    diode_mask_old = [False] * len(rectangles)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # To grayscale

        color = (205, 92, 92)
        diode_mask_new = [False] * len(rectangles)
        flag_mask_changed = False

        for idx, rect in enumerate(rectangles):
            cv2.rectangle(frame, rect[0], rect[1], color, 2)  # Draw rectangle

            # Извлечь область квадрата из кадра
            x1, y1 = rect[0]
            x2, y2 = rect[1]
            roi = frame[y1:y2, x1:x2]  # Truncated frame for one diode

            diode_mask_new[idx] = bool(roi.mean(axis=(0, 1)) > 230)  # Switched on condition

        if diode_mask_new != diode_mask_old:
            diode_mask_old = diode_mask_new
            flag_mask_changed = True

        cv2.imshow('Video', frame)

        key = cv2.waitKey(30)

        if flag_mask_changed:   # Print only if diode mask changed
            json_data = json.dumps(diode_mask_new)
            print(json_data)

        # Обработка клавиш:
        if key == ord('q'):
            break
        elif key == ord('r'):
            # Сброс в начало видео (нажмите 'r')
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Освободите видеопоток и закройте окно
    cap.release()
    cv2.destroyAllWindows()
    return diode_mask_new

if __name__ == '__main__':
    # Video()
    kek = get_data_from_video()
    print(kek)
