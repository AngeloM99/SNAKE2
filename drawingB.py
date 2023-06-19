import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from statistics import mean
import colour_randomisation

CAMERA_ID = 0

x1, y1 = 0, 0

canvas = None
cap = cv2.VideoCapture(CAMERA_ID)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

xlist = []
ylist = []

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    cursor_color = colour_randomisation.color_randomisation()

    # Initiate canvas
    if canvas is None:
         canvas = np.zeros_like(img)

    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]

        xlist.append(cursor[0])
        ylist.append(cursor[1])

        if len(xlist) > 3:
            xlist.pop(0)

        if len(ylist) > 3:
            ylist.pop(0)

        smoothX = round(mean(xlist))
        smoothY = round(mean(ylist))

        x2, y2 = smoothX, smoothY
        try:
            color = (img[y1 - 10, x1 + 10])
            color = color.tolist()
        except:
            IndexError

        canvas = cv2.circle(canvas, cursor, 5, cursor_color, -1)

        if x1 == 0 and y1 == 0:
            x1, y1 = x2, y2
        else:
            canvas = cv2.line(canvas, (x1, y1), (x2, y2), color, 10)
        x1, y1 = x2, y2
    else:
        x1, y1 = 0, 0

    try:
        img = cv2.addWeighted(img, 0.2, canvas, 0.9, 0.5)
    except:
        IndexError

    canvas = cv2.putText(canvas,
                "Raise your hand in front of camera to draw whatever you want",
                (100,100),
                cv2.FONT_HERSHEY_DUPLEX,
                1,
                (255,255,255),
                1,
                cv2.LINE_AA)
    
    cv2.imshow('canvas',img)
    cv2.waitKey(1)
