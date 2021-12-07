#Cory Mavis

import cv2
import numpy
import sys
import subprocess
import os
import statistics
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
    global hsv
    global hide
    
    if(event == 4):
        cv2.setTrackbarPos("Calibrate","LiveFeed",0)
    print(params)
    if(params[0] == 1 and flags == 1 and event == 1):
        print("working")
        if(params[1] == 0):
            blueMark = hsv[y,x]
            maxblue = numpy.array([blueMark[0] + 8, 255, 255])
            minblue = numpy.array([blueMark[0] - 8, blueMark[1] - 50, blueMark[2] - 20])
            
        elif(params[1] == 1):
            greenMark = hsv[y,x]
            maxgreen = numpy.array([greenMark[0] + 10, 255, 255])
            if(greenMark[2] - 100 < 20):
                greenMark[2] = 120
            mingreen = numpy.array([greenMark[0] - 5, greenMark[1] - 100, greenMark[2] - 100])
            print(greenMark)
        elif(params[1] == 2):
            redMark = hsv[y,x]
            maxred = numpy.array([redMark[0] + 3, 255, 255])
            if(redMark[2] - 100 < 55):
                redMark[2] = 155
            minred = numpy.array([redMark[0] - 3, redMark[1] - 100, redMark[2] - 100])
            print(redMark)
            
        state[1] = params[1] + 1
        if(state[1] == 3):
            state = numpy.array([0,0])
            params[1] = 0
            params[0] = 0
            print("complete")
            hide = True
            print(state)
    gx = x
    gy = y
    
state = numpy.array([0,0])

cv2.setMouseCallback("LiveFeed",callback,state)

vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_AUTO_EXPOSURE,0.25)
vid.set(cv2.CAP_PROP_EXPOSURE, -5.0)
 
hide = True

def recalibrate(value):
    global state
    global hide
    global angle
    if(value == 1):
        try:
            params[0] = 1
            print(params)
        except:
            print("error")
        hide = False
        angle = [None] * 20
        state[0] = 1
        state[1] = 0
        cv2.setMouseCallback("LiveFeed",callback,state)
        print("Choose New Points for color calibration in this order:")
        print("Blue, Green, Red")
        

cv2.createTrackbar("Calibrate","LiveFeed",0,1,recalibrate)

angle = [None] * 50

print(angle)

maxred = (8,255,255)
minred = (2,130,55)
maxgreen = (90,255,255)
mingreen = (50,100,20)
maxblue = (120,255,255)
minblue = (100,50,0)
while(cv2.waitKey(1) != 27):
    ret,frame = vid.read()
    if(not ret):
        print("Broke")
        break
    ogFrame = frame.copy()
    frame = cv2.blur(frame, (20,20),cv2.BORDER_DEFAULT)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cv2.imshow("blur",frame)
    
    redParts = cv2.inRange(hsv,minred,maxred)
    greenParts = cv2.inRange(hsv,mingreen,maxgreen)
    blueParts = cv2.inRange(hsv,minblue,maxblue)
    
    kernel = numpy.ones((15,15),numpy.uint8)
    
    redParts = cv2.morphologyEx(redParts, cv2.MORPH_OPEN, kernel)
    redParts = cv2.morphologyEx(redParts, cv2.MORPH_CLOSE, kernel)
    
    greenParts = cv2.morphologyEx(greenParts, cv2.MORPH_OPEN, kernel)
    greenParts = cv2.morphologyEx(greenParts, cv2.MORPH_CLOSE, kernel)
    
    blueParts = cv2.morphologyEx(blueParts, cv2.MORPH_OPEN, kernel)
    blueParts = cv2.morphologyEx(blueParts, cv2.MORPH_CLOSE, kernel)
    
    cv2.imshow("Angles Feed",redParts)
    cv2.imshow("Green Parts",greenParts)
    cv2.imshow("Blue Parts",blueParts)
    
    M = cv2.moments(redParts)
    cXR = None
    if(M["m00"] != 0):
        cXR = int(M["m10"] / M["m00"])
        cYR = int(M["m01"] / M["m00"])
        cv2.circle(ogFrame,(cXR, cYR),15,(0,0,255),-1)
        middle = hsv[cYR,cXR][1] + 30
        if(middle > 255):
            middle = 255
        #minred = [hsv[cYR,cXR][0] - 2,middle - 125,0]
        #maxred = [hsv[cYR,cXR][0] + 2,middle,255]
        
            
    M = cv2.moments(greenParts)
    cXG = None
    if(M["m00"] != 0):
        cXG = int(M["m10"] / M["m00"])
        cYG = int(M["m01"] / M["m00"])
        cv2.circle(ogFrame,(cXG, cYG),15,(0,255,0),-1)
    
    M = cv2.moments(blueParts)
    cXB = None
    if(M["m00"] != 0):
        cXB = int(M["m10"] / M["m00"])
        cYB = int(M["m01"] / M["m00"])
        cv2.circle(ogFrame,(cXB, cYB),15,(255,0,0),-1)
    complete = 0
    
    if(cXG != None and cXR != None and hide):    
        cv2.line(ogFrame,(cXG,cYG),(cXR,cYR),(255,255,255),10)
        complete = complete + 1
        
    if(cXG != None and cXB != None and hide):    
        cv2.line(ogFrame,(cXG,cYG),(cXB,cYB),(255,255,255),10)
        complete = complete + 1
        
    if(complete == 2 and hide):
        
        points = numpy.array([[cXR,cYR], [cXG,cYG], [cXB,cYB]])
       
        A = points[2] - points[0]
        B = points[1] - points[0]
        C = points[2] - points[1]

        angles = []
        
        for e1, e2 in ((A, B), (A, C), (B, -C)):
            num = numpy.dot(e1, e2)
            denom = numpy.linalg.norm(e1) * numpy.linalg.norm(e2)
            angles.append(numpy.arccos(num/denom) * 180 / numpy.pi)
        

        angle.append(int(str(round(angles[2],0))[:-2]))
   
        del angle[0]
    
        if(angle[0] != None):
            outangle = int(statistics.mean(angle))
            cv2.putText(ogFrame,str(outangle) + " degrees",(int(statistics.mean([cXR,cXG,cXB])),int(statistics.mean([cYR,cYG,cYB]))),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3)

    cv2.imshow("LiveFeed",ogFrame)
    
cv2.destroyAllWindows()
vid.release()