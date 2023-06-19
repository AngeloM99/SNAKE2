import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
from statistics import mean
import random

CAMERA_ID =0

# Setup Constant
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

bg_color = (225, 225, 225)
txt_color = (0, 0, 0)

# Initiate OpenCV
cap = cv2.VideoCapture(CAMERA_ID)
cap.set(3, 1280)
cap.set(4, 720)

# Initiate Hand Detection
# hand_detector = HandDetector(detectionCon=0.8, maxHands=2)

# Initiate Facial Detection
face_detector = FaceDetector()

# Smoothing List Initiate
xlist = []
ylist = []

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img, bboxs = face_detector.findFaces(img)
    # hands = hand_detector.findHands(img, draw=False, flipType=False)
    h, w, _ = img.shape

    randomValue = random.randint(0, 100)
    MESSAGE_FONT_THICKNESS = random.randint(15, 30)
    MESSAGE_FONT_SCALE = random.randint(10, 15)

    if bboxs:
        # bboxInfo - "id","bbox","score","center"
        center = bboxs[0]["center"]
        top_center = (center[0], round(center[1] + (center[1])))

        xlist.append(top_center[0])
        ylist.append(top_center[1])

        if len(xlist) > 3:
            xlist.pop(0)

        if len(ylist) > 3:
            ylist.pop(0)

        smoothX = round(mean(xlist))
        smoothY = round(mean(ylist))
        smoothCenter = (smoothX, smoothY)

        print(smoothCenter)
        up = cv2.pointPolygonTest(UP_AREA, center, False)
        down = cv2.pointPolygonTest(DOWN_AREA, center, False)
        left = cv2.pointPolygonTest(LEFT_AREA, center, False)
        right = cv2.pointPolygonTest(RIGHT_AREA, center, False)

        try:
            if up == 1.0:
                cv2.putText(img, message_up, (smoothCenter[0] - 500 + randomValue, (smoothCenter[1] - randomValue)),
                            MESSAGE_FONT,
                            MESSAGE_FONT_SCALE, (255, 255, 255),
                            MESSAGE_FONT_THICKNESS, cv2.LINE_AA, )
            if down == 1.0:
                cv2.putText(img, message_down, (smoothCenter[0] - 250 + randomValue, (smoothCenter[1] - randomValue)),
                            MESSAGE_FONT,
                            MESSAGE_FONT_SCALE, (255, 255, 255),
                            MESSAGE_FONT_THICKNESS, cv2.LINE_AA, )
            if left == 1.0:
                cv2.putText(img, message_left, (smoothCenter[0] - 250 + randomValue, (smoothCenter[1] - randomValue)),
                            MESSAGE_FONT,
                            MESSAGE_FONT_SCALE,
                            (255, 255, 255),
                            MESSAGE_FONT_THICKNESS, cv2.LINE_AA, )
            if right == 1.0:
                cv2.putText(img, message_right, (smoothCenter[0] - 500 + randomValue, (smoothCenter[1] - randomValue)),
                            MESSAGE_FONT, MESSAGE_FONT_SCALE, (255, 255, 255),
                            MESSAGE_FONT_THICKNESS, cv2.LINE_AA, )
        except:
            NameError

    black_and_white_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # pixelated size
    pw, ph = (64, 36)

    temp = cv2.resize(black_and_white_img, (pw, ph), interpolation=cv2.INTER_LINEAR)

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
