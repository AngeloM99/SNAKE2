import cv2
import numpy as np
from cvzone.FaceDetectionModule import FaceDetector
import random

UP_AREA = np.array([[160, 0], [1120, 0], [800, 360], [480, 360]])
DOWN_AREA = np.array([[160, 720], [1120, 720], [800, 360], [480, 360]])
LEFT_AREA = np.array([[0, 0], [160, 0], [480, 360], [160, 720], [0, 720]])
RIGHT_AREA = np.array([[1120, 0], [1280, 0], [1280, 720], [1120, 720], [800, 360]])

message_up = "CYBORG!"
message_down = "SEES"
message_left = "COMPUTER"
message_right = "HUMAN"

# Constant
MULTIPLIER_VALUE = 8
PADDING_VALUE = 2

FONT = cv2.FONT_HERSHEY_TRIPLEX
FONT_THICKNESS = 1
FONT_SCALE = 0.3

MESSAGE_FONT = cv2.FONT_HERSHEY_PLAIN

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = FaceDetector()

bg_color = (225, 225, 225)
txt_color = (0, 0, 0)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    bbox, img = detector.findFaces(img)
    randomValue = random.randint(0, 100)
    MESSAGE_FONT_THICKNESS = random.randint(15, 30)
    MESSAGE_FONT_SCALE = random.randint(10, 15)

    if bbox:
        bbox_dimension = bbox[0]['lmList']
        bbox = hands[0]['bbox']
        cursor = lmList[8]
        up = cv2.pointPolygonTest(UP_AREA, cursor, False)
        down = cv2.pointPolygonTest(DOWN_AREA, cursor, False)
        left = cv2.pointPolygonTest(LEFT_AREA, cursor, False)
        right = cv2.pointPolygonTest(RIGHT_AREA, cursor, False)

        print(bbox)

        try:
            if up == 1.0:
                cv2.putText(img, message_up, (cursor[0] - 500 + randomValue, (cursor[1] - randomValue)), MESSAGE_FONT,
                            MESSAGE_FONT_SCALE, (255, 255, 255),
                            MESSAGE_FONT_THICKNESS, cv2.LINE_AA, )
            if down == 1.0:
                cv2.putText(img, message_down, (cursor[0] - 250 + randomValue, (cursor[1] - randomValue)), MESSAGE_FONT,
                            MESSAGE_FONT_SCALE, (255, 255, 255),
                            MESSAGE_FONT_THICKNESS, cv2.LINE_AA, )
            if left == 1.0:
                cv2.putText(img, message_left, (cursor[0] - 250 + randomValue, (cursor[1] - randomValue)), MESSAGE_FONT,
                            MESSAGE_FONT_SCALE,
                            (255, 255, 255),
                            MESSAGE_FONT_THICKNESS, cv2.LINE_AA, )
            if right == 1.0:
                cv2.putText(img, message_right, (cursor[0] - 500 + randomValue, (cursor[1] - randomValue)),
                            MESSAGE_FONT, MESSAGE_FONT_SCALE, (255, 255, 255),
                            MESSAGE_FONT_THICKNESS, cv2.LINE_AA, )
        except:
            NameError

    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # pixelated size
    pw, ph = (64, 36)

    temp = cv2.resize(img, (pw, ph), interpolation=cv2.INTER_LINEAR)

    out = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

    # blank = np.full((h, w, 3), bg_color, dtype=np.uint8)

    for y in range(0, ph):
        for x in range(0, pw):
            cv2.putText(out,
                        str(temp[y, x]),
                        (int(x * 20), int(y * 20 + 10)),
                        FONT,
                        FONT_SCALE,
                        (255 - int(temp[y, x])),
                        FONT_THICKNESS,
                        cv2.LINE_AA)

    cv2.imshow("out", out)
    cv2.waitKey(1)
