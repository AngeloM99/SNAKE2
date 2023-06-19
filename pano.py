import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import random

cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture()

while True:
    success, img1 = cap1.read()
    success, img2 = cap2.read()
    img1 = cv2.flip(img1, 1)
    img2 = cv2.flip(img2, 1)

    cv2.imshow("im", img1)
    cv2.imshow('im2', img2)
    # cv2.imshow('canvas',canvas)

    cv2.waitKey(1)