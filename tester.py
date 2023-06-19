import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from colour_randomisation import color_randomisation
from random import randint
import gc

UP_AREA = np.array([[160, 0], [1120, 0], [800, 360], [480, 360]])
DOWN_AREA = np.array([[160, 720], [1120, 720], [800, 360], [480, 360]])
LEFT_AREA = np.array([[0, 0], [160, 0], [480, 360], [160, 720], [0, 720]])
RIGHT_AREA = np.array([[1120, 0], [1280, 0], [1280, 720], [1120, 720], [800, 360]])

FONT = cv2.FONT_HERSHEY_PLAIN
FONT_THICKNESS = 20
FONT_SCALE = 10
# x1, y1 = 0, 0

# canvas = None

bg_color = color_randomisation()
dot_color = color_randomisation()
while dot_color == bg_color:
    dot_color = color_randomisation()

font_color = bg_color
max_dots = 150

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    # Initiate canvas
    # if canvas is None:
    #     canvas = np.zeros_like(img)

    up_sec = cv2.polylines(img, [UP_AREA], True, (255, 255, 255))
    down_sec = cv2.polylines(img, [DOWN_AREA], True, (255, 255, 255))
    left_sec = cv2.polylines(img, [LEFT_AREA], True, (255, 255, 255))
    right_sec = cv2.polylines(img, [RIGHT_AREA], True, (255, 255, 255))

    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        print(lmList)
        cursor = lmList[9]
        up = cv2.pointPolygonTest(UP_AREA, cursor, False)
        down = cv2.pointPolygonTest(DOWN_AREA, cursor, False)
        left = cv2.pointPolygonTest(LEFT_AREA, cursor, False)
        right = cv2.pointPolygonTest(RIGHT_AREA, cursor, False)

        # Drawing function
        # x2, y2 = lmList[9]
        #
        bg_color[randint(0, 2)] += randint(1, 5)
        dot_color[randint(0, 2)] += randint(1, 5)
        for i in bg_color:
            if i >= 255:
                bg_index = bg_color.index(i)
                bg_color[bg_index] -= 200

        for i in dot_color:
            if i >= 200:
                dot_index = dot_color.index(i)
                dot_color[dot_index] -= 200

        font_color = dot_color

    #     color = (img[y1 - 5, x1 + 5])
    #     color = color.tolist()
    #
    #     if x1 == 0 and y1 == 0:
    #         x1, y1 = x2, y2
    #     else:
    #         canvas = cv2.line(canvas, (x1, y1), (x2, y2), color, 4)
    #     x1, y1 = x2, y2
    # else:
    #     x1, y1 = 0, 0

    # try:
    #     img = cv2.add(img, canvas)
    # except:
    #     IndexError
    #
    #     # Stack frame and show it
    # stacked = np.hstack((canvas, img))

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    downsized_img = cv2.resize(img, (max_dots, int(h * (max_dots / w))))

    dh, dw = downsized_img.shape

    multiplier = 8

    blank_img_h = dh * multiplier
    blank_img_w = dw * multiplier

    padding = int(multiplier / 2)

    bg_blank = np.full((blank_img_h, blank_img_w, 3), bg_color, dtype=np.uint8)

    for y in range(0, dh):
        for x in range(0, dw):
            cv2.circle(bg_blank, (((x * multiplier) + padding), ((y * multiplier) + padding)),
                       int((0.9 * multiplier) * ((255 - downsized_img[y][x]) / 255)), dot_color, -1)

    try:
        if up == 1.0:
            cv2.putText(bg_blank, "UP", (490, 200), FONT, FONT_SCALE, font_color, FONT_THICKNESS, cv2.LINE_AA, )
        if down == 1.0:
            cv2.putText(bg_blank, "DOWN", (360, 600), FONT, FONT_SCALE, font_color, FONT_THICKNESS, cv2.LINE_AA, )
        if left == 1.0:
            cv2.putText(bg_blank, "LEFT", (50, 400), FONT, FONT_SCALE, font_color, FONT_THICKNESS, cv2.LINE_AA, )
        if right == 1.0:
            cv2.putText(bg_blank, "RIGHT", (760, 400), FONT, FONT_SCALE, font_color, FONT_THICKNESS, cv2.LINE_AA, )
    except:
        NameError

    gc.collect()
    # print('1')

    cv2.imshow("im", bg_blank)
    # cv2.imshow('canvas',canvas)

    cv2.waitKey(1)
