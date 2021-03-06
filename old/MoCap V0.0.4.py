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
    global gx,gy
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
    gx = x
    gy = y
state = numpy.array([0,0])
cv2.setMouseCallback("LiveFeed",callback,state)

vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def recalibrate(value):
    global state
    if(value == 1):
        state[0] = 1
        print("Choose New Points for color calibration in this order:")
        print("Blue, Green, Red")
        state = numpy.array([0,0])
        cv2.setTrackbarPos("Recalibrate","LiveFeed",0)

cv2.createTrackbar("Recalibrate","LiveFeed",0,1,recalibrate)

maxred1 = (10,255,255)
minred1 = (0,90,0)
maxred2 = (255,255,255)
minred2 = (255,255,255)
maxgreen = (100,255,255)
mingreen = (50,75,0)
maxblue = (130,255,255)
minblue = (70,150,0)

recalibrate(1)

while(cv2.waitKey(1) != 27):
    ret,frame = vid.read()
    if(not ret):
        print("Broke")
        break
    frame = cv2.blur(frame, (15,15),cv2.BORDER_DEFAULT)
    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    print(hsv[0,0])
    
    cv2.imshow("blur",frame)
    redParts1 = cv2.inRange(hsv,minred1,maxred1)
    redParts2 = cv2.inRange(hsv,minred2,maxred2)
    redParts = cv2.bitwise_or(redParts1,redParts2)
    greenParts = cv2.inRange(hsv,mingreen,maxgreen)
    blueParts = cv2.inRange(hsv,minblue,maxblue)
    cv2.imshow("Angles Feed",redParts)
    cv2.imshow("Green Parts",greenParts)
    cv2.imshow("Blue Parts",blueParts)
    M = cv2.moments(redParts)
    cXR = None
    if(M["m00"] != 0):
        cXR = int(M["m10"] / M["m00"])
        cYR = int(M["m01"] / M["m00"])
        cv2.circle(frame,(cXR, cYR),15,(0,0,255),-1)
    M = cv2.moments(greenParts)
    cXG = None
    if(M["m00"] != 0):
        cXG = int(M["m10"] / M["m00"])
        cYG = int(M["m01"] / M["m00"])
        cv2.circle(frame,(cXG, cYG),15,(0,255,0),-1)
    
    if(cXG != None and cXR != None):    
        cv2.line(frame,(cXG,cYG),(cXR,cYR),(255,255,255),10)
    M = cv2.moments(blueParts)
    if(M["m00"] != 0):
        cXB = int(M["m10"] / M["m00"])
        cYB = int(M["m01"] / M["m00"])
        cv2.circle(frame,(cXB, cYB),5,(255,0,0),-1)
    cv2.imshow("LiveFeed",frame)
cv2.destroyAllWindows()
vid.release()
