#Cory Mavis


import pandas
import cv2
import numpy
import sys
import subprocess
import os
import statistics
import math
from time import time
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()



cv2.namedWindow("LiveFeed")

def callback (event,x,y,flags,params):
    global markThree #update the position of the blue point
    global markTwo #update the position of the green point
    global markOne #update the position of the red point
    global state #update global value
    global maxColorOne
    global minColorOne
    global maxColorTwo
    global minColorTwo
    global maxColorThree
    global minColorThree
    global maxColorFour
    global minColorFour
    global gx,gy
    global hsv
    global hide
    
    if(event == 4):
        cv2.setTrackbarPos("Calibrate","LiveFeed",0)
    if(params[0] == 1 and flags == 1 and event == 1):
        if(params[1] == 0):
            markThree = hsv[y,x]
            maxColorThree = numpy.array([markThree[0] + 8, 255, 255])
            minColorThree = numpy.array([markThree[0] - 8, markThree[1] - 50, markThree[2] - 20])
            
        elif(params[1] == 1):
            markTwo = hsv[y,x]
            maxColorTwo = numpy.array([markTwo[0] + 10, 255, 255])
            if(markTwo[2] - 100 < 20):
                markTwo[2] = 120
            minColorTwo = numpy.array([markTwo[0] - 5, markTwo[1] - 50, markTwo[2] - 100])

        elif(params[1] == 2):
            markOne = hsv[y,x]
            maxColorOne = numpy.array([markOne[0] + 3, 255, 255])
            if(markOne[2] - 100 < 55):
                markOne[2] = 155
            minColorOne = numpy.array([markOne[0] - 3, markOne[1] - 100, markOne[2] - 100])
        elif(params[1] == 3):
            markFour = hsv[y,x]
            maxColorFour = numpy.array([markFour[0] + 8, 255, 255])
            minColorFour = numpy.array([markFour[0] - 8, markFour[1] - 50, markFour[2] - 20])
            
        state[1] = params[1] + 1
        if(state[1] == 4):
            state = numpy.array([0,0])
            params[1] = 0
            params[0] = 0
            print("complete")
            hide = True
    gx = x
    gy = y
    
state = numpy.array([0,0])
cv2.setMouseCallback("LiveFeed",callback,state)
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_AUTO_EXPOSURE,0.25)
vid.set(cv2.CAP_PROP_EXPOSURE, -5.0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)



hide = True
def recalibrate(value):
    global state
    global hide
    global angle
    if(value == 1):
        hide = False
        angle = [None] * 20
        state[0] = 1
        state[1] = 0
        cv2.setMouseCallback("LiveFeed",callback,state)
        print("Choose New Points for color calibration in this order:")
        print("Blue, Green, Red")
        
def record(value):
    global record
    if(value == 1):
        record = True
    else:
        record = False

i = 0
file = None
def rewatch(value):
    global file
    if(value == 1):
        file_path = filedialog.askopenfilename()
        #cv2.setTrackbarPos("ReWatch?","LiveFeed",0)
        print(file_path)
        if(len(file_path) > 0):
            file = pandas.read_csv(file_path)
        else:
            cv2.setTrackbarPos("ReWatch?","LiveFeed",0)

        
cv2.createTrackbar("Calibrate","LiveFeed",0,1,recalibrate)
cv2.createTrackbar("Record","LiveFeed",0,1,record)
cv2.createTrackbar("Save?","LiveFeed",0,1,lambda x: None)
cv2.createTrackbar("ReWatch?","LiveFeed",0,1,rewatch)

record = False

dtime = []

dX1 = []
dY1 = []
dX2 = []
dY2 = []
dX3 = []
dY3 = []
dX4 = []
dY4 = []

angle = [None] * 10

maxColorOne = (8,255,255)
minColorOne = (2,130,55)
maxColorTwo = (90,255,255)
minColorTwo = (50,100,20)
maxColorThree = (120,255,255)
minColorThree = (100,50,0)
maxColorFour = (29,255,255)
minColorFour = (13,205,182)   

while(cv2.waitKey(1) != 27):
    ret,frame = vid.read()
    if(not ret):
        print("Broke")
        break
    ogFrame = frame.copy()
    frame = cv2.blur(frame, (20,20),cv2.BORDER_DEFAULT)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cv2.imshow("blur",frame)
    
    colorOne = cv2.inRange(hsv,minColorOne,maxColorOne)
    colorTwo = cv2.inRange(hsv,minColorTwo,maxColorTwo)
    colorThree = cv2.inRange(hsv,minColorThree,maxColorThree)
    colorFour = cv2.inRange(hsv,minColorFour,maxColorFour)
    
    kernel = numpy.ones((15,15),numpy.uint8)
    
    colorOne = cv2.morphologyEx(colorOne, cv2.MORPH_OPEN, kernel)
    colorOne = cv2.morphologyEx(colorOne, cv2.MORPH_CLOSE, kernel)
    
    colorTwo = cv2.morphologyEx(colorTwo, cv2.MORPH_OPEN, kernel)
    colorTwo = cv2.morphologyEx(colorTwo, cv2.MORPH_CLOSE, kernel)
    
    colorThree = cv2.morphologyEx(colorThree, cv2.MORPH_OPEN, kernel)
    colorThree = cv2.morphologyEx(colorThree, cv2.MORPH_CLOSE, kernel)
    
    colorFour = cv2.morphologyEx(colorFour, cv2.MORPH_OPEN, kernel)
    colorFour = cv2.morphologyEx(colorFour, cv2.MORPH_CLOSE, kernel)

    cv2.imshow("Angles Feed",colorOne)
    cv2.imshow("Green Parts",colorTwo)
    cv2.imshow("Blue Parts",colorThree)
    cv2.imshow("Yellow Parts",colorFour)

    M = cv2.moments(colorOne)
    cX1 = None
    if(M["m00"] != 0):
        cX1 = int(M["m10"] / M["m00"])
        cY1 = int(M["m01"] / M["m00"])
        cv2.circle(ogFrame,(cX1, cY1),15,(0,0,255),-1)
        
    M = cv2.moments(colorTwo)
    cX2 = None
    if(M["m00"] != 0):
        cX2 = int(M["m10"] / M["m00"])
        cY2 = int(M["m01"] / M["m00"])
        cv2.circle(ogFrame,(cX2, cY2),15,(0,255,0),-1)
    
    M = cv2.moments(colorThree)
    cX3 = None
    if(M["m00"] != 0):
        cX3 = int(M["m10"] / M["m00"])
        cY3 = int(M["m01"] / M["m00"])
        cv2.circle(ogFrame,(cX3, cY3),15,(255,0,0),-1)
        
    M = cv2.moments(colorFour)
    cX4 = None
    if(M["m00"] != 0):
        cX4 = int(M["m10"] / M["m00"])
        cY4 = int(M["m01"] / M["m00"])
        cv2.circle(ogFrame,(cX4, cY4),15,(78,255,237),-1)
    complete = 0
    
       
    if(cv2.getTrackbarPos("ReWatch?","LiveFeed") == 1):
        length = len(file["Unnamed: 0"])
        if(i > length - 3):
            i = 0
            cv2.setTrackbarPos("ReWatch?","LiveFeed",0)
            continue
        else:
            i = i + 1
            
        cX1 = file["cX1"][i]
        cY1 = file["cY1"][i]
        cX2 = file["cX2"][i]
        cY2 = file["cY2"][i]
        cX3 = file["cX3"][i]
        cY3 = file["cY3"][i]
        cX4 = file["cX4"][i]
        cY4 = file["cY4"][i]
        ogFrame = numpy.zeros((len(ogFrame),len(ogFrame[0]),3))
        cv2.circle(ogFrame,(cX1, cY1),15,(0,0,255),-1)
        cv2.circle(ogFrame,(cX2, cY2),15,(0,255,0),-1)
        cv2.circle(ogFrame,(cX3, cY3),15,(255,0,0),-1)
        cv2.circle(ogFrame,(cX4, cY4),15,(78,255,237),-1)
        cv2.waitKey(file["time"][i + 1] - file["time"][i])
        #print(file["time"][i + 1] - file["time"][i])
        
    
    if(cX2 != None and cX1 != None and hide):    
        cv2.line(ogFrame,(cX2,cY2),(cX1,cY1),(255,255,255),10)
        complete = complete + 1
        
    if(cX3 != None and cX4 != None and hide):    
        cv2.line(ogFrame,(cX3,cY3),(cX4,cY4),(255,255,255),10)
        complete = complete + 1
    
    
    
    if(complete == 2 and hide and cX1 != cX2 and cX3 != cX4):
        
        if(record):
            
            dtime.append(math.floor(time()*1000))
        
            dX1.append(cX1)
            dY1.append(cY1)
            dX2.append(cX2)
            dY2.append(cY2)
            dX3.append(cX3)
            dY3.append(cY3)
            dX4.append(cX4)
            dY4.append(cY4)
            
                
        m1 = (cY1-cY2)/(cX1-cX2)
        m2 = (cY3-cY4)/(cX3-cX4)
        b1 = cY1 - m1 * cX1
        b2 = cY3 - m2 * cX3
        if(m1 != m2):
            xi = (b1 - b2) / (m2 - m1)
            yi = m1 * xi + b1
            cv2.circle(ogFrame,(int(xi),int(yi)),15,(150,150,150),-1)
      
        points = numpy.array([[cX1,cY1], [xi,yi], [cX4,cY4]])
        
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
            cv2.putText(ogFrame,str(outangle) + " degrees",(int(statistics.mean([cX1,cX2,cX3])),int(statistics.mean([cY1,cY2,cY3]))),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)
    else:
        cv2.setTrackbarPos("Record", "LiveFeed",0)
        
    cv2.imshow("LiveFeed",ogFrame)
    
    if(cv2.getTrackbarPos("Save?","LiveFeed") == 1):
        db = {"time" : dtime, "cX1" : dX1, "cY1" : dY1, "cX2" : dX2, "cY2" : dY2, "cX3" : dX3, "cY3" : dY3, "cX4" : dX4, "cY4" : dY4}
        columns = ("time", "cX1","cY1","cX2","cY2","cX3","cY3","cX4","cY4")
        df = pandas.DataFrame(data = db)
        if(not os.path.exists(path.join("C:","Users",os.path.expanduser("~"),"Documents","MOCAP")):
           os.makedirs(os.path.join("C:","Users",os.path.expanduser("~"),"Documents","MOCAP")
        saveLocation = askopen.asksaveasfile(filetype = [("CSV Files":"*.csv")], defaultdir = os.path.join("C:","Users",os.path.expanduser("~"),"Documents","MOCAP"))
        df.to_csv("MoCap.csv")

cv2.destroyAllWindows()
vid.release()
