import cv2
import time
import numpy as np
import json

video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

# Создайте окно для просмотра видео
cv2.namedWindow('Video')

# Инициализируйте переменные для управления воспроизведением
paused = False

# Задайте координаты квадратов массивом
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

    # cv2.imshow('Video', frame)

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