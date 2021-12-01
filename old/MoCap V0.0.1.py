#Cory Mavis

import cv2
import numpy
import sys
import subprocess
import os

cv2.namedWindow("LiveFeed")

def callback (event,x,y,flags,params):
    global blueMark #update the position of the blue point
    global greenMark #update the position of the green point
    global redMark #update the position of the red point
    global state #update global value
    global maxred1
    global minred1
    global maxred2
    global minred2
    global maxblue
    global minblue
    global maxgreen
    global mingreen
    if(params[0] == 1 and flags == 1):
        if(params[1] == 0):
            blueMark = (x,y)
        elif(params[1] == 1):
            greenMark = (x,y)
        elif(params[1] == 2):
            redMark = (x,y)
        state[1] = params[1] + 1
        if(state[1] == 3):
            state = numpy.array([0,0])
state = numpy.array([0,0])
cv2.setMouseCallback("LiveFeed",callback,state)

vid = cv2.VideoCapture(0)

def recalibrate(value):
    global state
    if(value == 1):
        state[0] = 1
        print("Choose New Points for color calibration in this order:")
        print("Blue, Green, Red")
        state = numpy.array([0,0])
        cv2.setTrackbarPos("Recalibrate","LiveFeed",0)

cv2.createTrackbar("Recalibrate","LiveFeed",0,1,recalibrate)

maxred1 = (255,150,150)
minred1 = (150,150,150)
minred2 = (0,100,100)
maxred2 = (0,100,100)

recalibrate(1)

while(cv2.waitKey(1) != 27):
    ret,frame = vid.read()
    if(not ret):
        break
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    redParts1 = cv2.inRange(hsv,minred1,maxred1)
    #redParts2 = cv2.inRange(hsv,minred2,maxred2)
    cv2.imshow("LiveFeed",redParts1)
    M = cv2.moments(redParts1)
    if(M["m00"] != 0):
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame,(cX, cY),5,(255,255,255),-1)
    cv2.imshow("camFeed",frame)
cv2.destroyAllWindows()
vid.release()
