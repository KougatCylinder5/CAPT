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
    global maxred
    global minred
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

maxred = (255,255,255)
minred = (150,50,50)
maxgreen = (200,255,200)
mingreen = (100,0,100)
maxblue = (255,255,255)
minblue = (150,150,0)

recalibrate(1)

while(cv2.waitKey(1) != 27):
    ret,frame = vid.read()
    if(not ret):
        break
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hsv = cv2.blur(hsv, (20,20))
    redParts = cv2.inRange(hsv,minred,maxred)
    greenParts = cv2.inRange(hsv,mingreen,maxgreen)
    cv2.imshow("Angles Feed",redParts)
    cv2.imshow("Green Parts",greenParts)
    M = cv2.moments(redParts)
    if(M["m00"] != 0):
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame,(cX, cY),5,(0,0,255),-1)
    M = cv2.moments(greenParts)
    if(M["m00"] != 0):
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(frame,(cX, cY),5,(0,255,0),-1)
    cv2.imshow("camFeed",frame)
cv2.destroyAllWindows()
vid.release()
