import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
vid = cv2.VideoCapture('1.mp4')
cap.set(3, 1280)
cap.set(4, 720)

if not vid.isOpened():
    print("Failed to open video")

detector = HandDetector(detectionCon=0.65, maxHands=6)

while True:
    ret, frame = vid.read()
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    h1, w1, _ = frame.shape

    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[9]
        cursor_x = cursor[0]
        cursor_y = cursor[1]

    img[cursor_y:cursor_y+w1, cursor_x:cursor_x+h1] = frame

    cv2.imshow("im", img)
    cv2.waitKey(1)
