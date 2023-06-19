import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

UP_AREA = np.array([[160, 0], [1120, 0], [800, 360], [480, 360]])
DOWN_AREA = np.array([[160, 720], [1120, 720], [800, 360], [480, 360]])
LEFT_AREA = np.array([[0, 0], [160, 0], [480, 360], [160, 720], [0, 720]])
RIGHT_AREA = np.array([[1120, 0], [1280, 0], [1280, 720], [1120, 720], [800, 360]])
# x1, y1 = 0, 0

canvas = None
cap = cv2.VideoCapture(2)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.65, maxHands=6)

while True:
    success, img = cap.read()
    # img = cv2.flip(img, 1)
    h, w, _ = img.shape

    # # Initiate canvas
    # if canvas is None:
    #     canvas = np.zeros_like(img)

    up_sec = cv2.polylines(img, [UP_AREA], True, (255, 255, 255))
    down_sec = cv2.polylines(img, [DOWN_AREA], True, (255, 255, 255))
    left_sec = cv2.polylines(img, [LEFT_AREA], True, (255, 255, 255))
    right_sec = cv2.polylines(img, [RIGHT_AREA], True, (255, 255, 255))

    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[9]
        up = cv2.pointPolygonTest(UP_AREA, cursor, False)
        down = cv2.pointPolygonTest(DOWN_AREA, cursor, False)
        left = cv2.pointPolygonTest(LEFT_AREA, cursor, False)
        right = cv2.pointPolygonTest(RIGHT_AREA, cursor, False)

    #     x2, y2 = lmList[9]
    #
    #     color = (img[y1 - 10, x1 + 10])
    #     color = color.tolist()
    #
    #     if x1 == 0 and y1 == 0:
    #         x1, y1 = x2, y2
    #     else:
    #         canvas = cv2.line(canvas, (x1, y1), (x2, y2), color, 4)
    #     x1, y1 = x2, y2
    # else:
    #     x1, y1 = 0, 0
    #
    # try:
    #     img = cv2.add(img, canvas)
    # except:
    #     IndexError
    #
    # # Stack frame and show it
    # stacked = np.hstack((canvas, img))

    try:
        if up == 1.0:
            print('up')
        if down == 1.0:
            print("down")
        if left == 1.0:
            print('left')
        if right == 1.0:
            print('right')
    except:
        NameError

    cv2.imshow("im", img)
    # cv2.imshow('canvas',canvas)
    cv2.waitKey(1)
