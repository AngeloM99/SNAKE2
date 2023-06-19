import time
from turtle import Screen

import gc

import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

from food import Food
from score import Score
from snake import Snake

# Constant values for the four areas to check
UP_AREA = np.array([[160, 0], [1120, 0], [800, 360], [480, 360]])
DOWN_AREA = np.array([[160, 720], [1120, 720], [800, 360], [480, 360]])
LEFT_AREA = np.array([[0, 0], [160, 0], [480, 360], [160, 720], [0, 720]])
RIGHT_AREA = np.array([[1120, 0], [1280, 0], [1280, 720], [1120, 720], [800, 360]])

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor('black')
screen.title("SNAKE!")
screen.colormode(255)

# Turn on Webcam and setup hand detection with CVzone and MediaPipe
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)
# Turn off the image tracer and replace it with update() method, that snake won't move funny
screen.tracer(0)

scoreboard = Score()
snake = Snake()
food = Food()
ai_on = True



# screen.listen()
# screen.onkey(snake.up, 'Up')
# screen.onkey(snake.down, 'Down')
# screen.onkey(snake.left, 'Left')
# screen.onkey(snake.right, 'Right')
game_is_on = True
ai_on = True

while game_is_on:
    # update all three segment at once if we put the update() outside for loop
    scoreboard.draw_boundaries()
    screen.update()
    time.sleep(0.1)
    snake.move()

    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    # Configure four areas to check.
    cv2.polylines(img, [UP_AREA], True, (255, 255, 255))
    cv2.polylines(img, [DOWN_AREA], True, (255, 255, 255))
    cv2.polylines(img, [LEFT_AREA], True, (255, 255, 255))
    cv2.polylines(img, [RIGHT_AREA], True, (255, 255, 255))

    # Set up hand detector
    hands, img = detector.findHands(img, flipType=False)

    # If hand was detected, track the index finger value in index 8.
    if hands:
        ai_on = False
        lmList = hands[0]['lmList']
        cursor = lmList[8]

        # Set up polygon test of areas to check, returns a float 1.0 if hand found within the polygon
        up = cv2.pointPolygonTest(UP_AREA, cursor, False)
        down = cv2.pointPolygonTest(DOWN_AREA, cursor, False)
        left = cv2.pointPolygonTest(LEFT_AREA, cursor, False)
        right = cv2.pointPolygonTest(RIGHT_AREA, cursor, False)

        # If returns 1.0, snake move accordingly
        if up == 1.0:
            snake.up()
        if down == 1.0:
            snake.down()
        if left == 1.0:
            snake.left()
        if right == 1.0:
            snake.right()

    # detect collision with food
    if snake.head.distance(food) < 20:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()
        gc.collect()

    # detect collision with wall
    if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 290 or snake.head.ycor() < -290:
        print(scoreboard.score)
        if scoreboard.score != 0:
            scoreboard.record_scores()
        # Store current score in dictionary
        #     current_record_scores[game_start_time] = scoreboard.score
        #     crs = pd.DataFrame.from_dict(current_record_scores, orient='index')
        #     crs.to_csv("record.csv", mode='a', header=False)
        scoreboard.gameover_countdown()
        scoreboard.reset_scoreboard()
        snake.reset_snake()
        gc.collect()

    # detect collision with tail
    # if head collides with any segment in tail:
    # trigger games over
    for segment in snake.segments:
        if segment == snake.head:
            pass
        elif snake.head.distance(segment) < 10:
            if scoreboard.score != 0:
                scoreboard.record_scores()
            scoreboard.gameover_countdown()
            scoreboard.reset_scoreboard()
            snake.reset_snake()
            gc.collect()

screen.exitonclick()
