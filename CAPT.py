#Cory Mavis


import pandas # CSV manipulation library
import numpy
import sys
import subprocess
from os import makedirs
import os.path as path # directory library
import statistics
from math import floor
from time import time
import tkinter as tk # file manipulation/selection library
from tkinter import filedialog
import cv2

root = tk.Tk()
root.withdraw() # deletes empty Tninter box



cv2.namedWindow("LiveFeed",cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("UI")

def callback (event,x,y,flags,params): # mousecall back for clicks
    global state #update global value
    global maxColorOne #fairly obvious variable names
    global minColorOne
    global maxColorTwo
    global minColorTwo
    global maxColorThree
    global minColorThree
    global maxColorFour
    global minColorFour
    global hsv # grabs frame from camera to use in function
    global hide # tells the program to hide the lines connecting the dots while calibrating
    
    if(event == 4):
        cv2.setTrackbarPos("Calibrate","UI",0)
    if(params[0] == 1 and flags == 1 and event == 1):
        if(params[1] == 2):
            markThree = hsv[y,x]
            maxColorThree = numpy.array([markThree[0] + 3, markThree[1] + 20, markThree[2] + 10]) # defines upper and lower limit
            minColorThree = numpy.array([markThree[0] - 3, markThree[1] - 20, markThree[2] - 10])
            
        elif(params[1] == 0):
            markTwo = hsv[y,x]
            maxColorTwo = numpy.array([markTwo[0] + 5, markTwo[1] + 20, markTwo[2] + 20])
            minColorTwo = numpy.array([markTwo[0] - 5, markTwo[1] - 20, markTwo[2] - 20])

        elif(params[1] == 1):
            markOne = hsv[y,x]
            maxColorOne = numpy.array([markOne[0] + 3, 255, 255])
            if(markOne[2] - 100 < 55):
                markOne[2] = 155
            minColorOne = numpy.array([markOne[0] - 3, markOne[1] - 100, markOne[2] - 50])
            
        elif(params[1] == 3):
            markFour = hsv[y,x]
            maxColorFour = numpy.array([markFour[0] + 8, 255, 255])
            minColorFour = numpy.array([markFour[0] - 8, markFour[1] - 50, markFour[2] - 20])
            
        state[1] = params[1] + 1#adds one to the state global so that it sets the next color the next time it is clicked instead of the same one
        if(state[1] == 4): # I don't even know how this works it just works
            state = numpy.array([0,0])
            params[1] = 0
            params[0] = 0
            print("complete")
            hide = True
    
state = numpy.array([0,0]) #settings for callback functions it does a job that regulates thingies
cv2.setMouseCallback("LiveFeed",callback,state)

vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_AUTO_EXPOSURE,0.25)
vid.set(cv2.CAP_PROP_EXPOSURE, -5.0)     # camera default modifications
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)

hide = True
def recalibrate(value): # starts the recalibration sequence to assign points
    global state
    global hide
    global angle
    if(value == 1):
        hide = False
        angle = [None] * 5 # resets the angle array for averaging the angle to prevent irregulaties
        state[0] = 1
        state[1] = 0
        cv2.setMouseCallback("LiveFeed",callback,state)
        print("Choose New Points for color calibration in this order:")
        print("Green, Red, Gold, Blue")
  
record = False

def record(value): # determines if the "Record?" Slider has been altered
    global record
    if(value == 1):
        record = True
    else:
        record = False 


file = None
def rewatch(value): # function to determine if to open a .csv file for playback
    global file
    if(value == 1):
        file_path = filedialog.askopenfilename()
        if(len(file_path) > 0):
            file = pandas.read_csv(file_path)
        else:
            cv2.setTrackbarPos("ReWatch?","UI",0)

        
cv2.createTrackbar("Calibrate","UI",0,1,recalibrate) # creating trackbars for grabbing user input
cv2.createTrackbar("Record","UI",0,1,record)
cv2.createTrackbar("Save?","UI",0,1,lambda x: None)
cv2.createTrackbar("ReWatch?","UI",0,1,rewatch)

dtime = [] # array to store the length of each frame for playback
dX1 = []# blank arrays for recording values for each of the points
dY1 = []
dX2 = []
dY2 = []
dX3 = []
dY3 = []
dX4 = []
dY4 = []

angle = [None] * 5 # empty array for averaging the degrees

maxColorOne = (8,255,255) #defines min and max for each of the colors on default
minColorOne = (2,130,55)
maxColorTwo = (90,255,255)
minColorTwo = (50,100,20)
maxColorThree = (120,255,255)
minColorThree = (100,50,0)
maxColorFour = (29,255,255)
minColorFour = (13,205,182)   

i = 0  # creates blank value for, the for loop for replaying files

while(cv2.waitKey(1) != 27):
    if(cv2.getTrackbarPos("ReWatch?","UI") == 0):#skips a ton of unnessicary logic if the slider isn't in the correct position
        ret,frame = vid.read() #read from camera
        if(not ret):#prevents throwing an error due to missing or occupied camera
            print("Broke")
            break
        ogFrame = frame.copy() # duplicates the frame for overlay purposes
        frame = cv2.blur(frame, (20,20),cv2.BORDER_DEFAULT) # blurs the frame make color detection easier and more uniform
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)#converts from the BGR to HSV colorspace
        
        colorOne = cv2.inRange(hsv,minColorOne,maxColorOne) # grabs the inRange parts of the images
        colorTwo = cv2.inRange(hsv,minColorTwo,maxColorTwo)
        colorThree = cv2.inRange(hsv,minColorThree,maxColorThree)
        colorFour = cv2.inRange(hsv,minColorFour,maxColorFour)

        cv2.imshow("colorOne",colorOne)
        cv2.imshow("colorTwo",colorTwo)
        cv2.imshow("colorThree",colorThree)
        cv2.imshow("colorFour",colorFour)


        kernel = numpy.ones((5,5),numpy.uint8)#just a 15x15 grid of ones

        colorOne = cv2.morphologyEx(colorOne, cv2.MORPH_OPEN, kernel)# deletes pixel groups less then 15x15 in size
        colorOne = cv2.morphologyEx(colorOne, cv2.MORPH_CLOSE, kernel)# fills holes pixel groups that are more then 15x15 in size with the hole being less then 15x15 in size

        colorTwo = cv2.morphologyEx(colorTwo, cv2.MORPH_OPEN, kernel)
        colorTwo = cv2.morphologyEx(colorTwo, cv2.MORPH_CLOSE, kernel)

        colorThree = cv2.morphologyEx(colorThree, cv2.MORPH_OPEN, kernel)
        colorThree = cv2.morphologyEx(colorThree, cv2.MORPH_CLOSE, kernel)

        colorFour = cv2.morphologyEx(colorFour, cv2.MORPH_OPEN, kernel)
        colorFour = cv2.morphologyEx(colorFour, cv2.MORPH_CLOSE, kernel)

        M = cv2.moments(colorOne) # nabs the moments data for the inRange calculations
        cX1 = None# this is used to tetermine if the if statement has been run
        if(M["m00"] != 0):
            cX1 = int(M["m10"] / M["m00"])# simple math to find the X location
            cY1 = int(M["m01"] / M["m00"])#yada yada Y location
            cv2.circle(ogFrame,(cX1, cY1),15,(0,0,255),-1) # put a dot on the location

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

       
    elif(cv2.getTrackbarPos("ReWatch?","UI") == 1): # math to jump straight to here if its replaying a recording
        length = len(file["Unnamed: 0"])# get the length of the file so that it can be stopped one frame before it reaches the end to prevent exceptions
        if(i > length - 3):#prior said stopper
            i = 0
            cv2.setTrackbarPos("ReWatch?","UI",0)
            continue
        else:
            i = i + 1
            
        cX1 = file["cX1"][i] # reads the locations of the points and puts them into the variables to be displayed 
        cY1 = file["cY1"][i]
        cX2 = file["cX2"][i]
        cY2 = file["cY2"][i]
        cX3 = file["cX3"][i]
        cY3 = file["cY3"][i]
        cX4 = file["cX4"][i]
        cY4 = file["cY4"][i]
        ogFrame = numpy.zeros((len(ogFrame),len(ogFrame[0]),3),dtype = numpy.uint8)
        print(ogFrame)# creates a black background so that it can put the dots on without interference
        cv2.circle(ogFrame,(cX1, cY1),15,(0,0,255),-1)#puts dots in the positions
        cv2.circle(ogFrame,(cX2, cY2),15,(0,255,0),-1)
        cv2.circle(ogFrame,(cX3, cY3),15,(255,0,0),-1)
        cv2.circle(ogFrame,(cX4, cY4),15,(78,255,237),-1)
        cv2.waitKey(file["time"][i + 1] - file["time"][i])#wait for the alotted time so that it doesn't instantly zip to the end
        
    complete = 0
    
    if(cX2 != None and cX1 != None and hide): #draw lines between the corrosponding dots
        cv2.line(ogFrame,(cX2,cY2),(cX1,cY1),(255,255,255),10)
        complete = complete + 1
        
    if(cX3 != None and cX4 != None and hide):    
        cv2.line(ogFrame,(cX3,cY3),(cX4,cY4),(255,255,255),10)
        complete = complete + 1
        
    if(complete == 2 and hide and cX1 != cX2 and cX3 != cX4): #only allow angle calculations if it can see all the color positions
        
        if(record):# only record if the slider says so
            
            dtime.append(math.floor(time()*1000)) # get the current time in millis
        
            dX1.append(cX1)# append the current dot locations to a array so they can be saved
            dY1.append(cY1)
            dX2.append(cX2)
            dY2.append(cY2)
            dX3.append(cX3)
            dY3.append(cY3)
            dX4.append(cX4)
            dY4.append(cY4)
               
        m1 = (cY1-cY2)/(cX1-cX2)# calculate slope so we can determine where the lines intercept
        m2 = (cY3-cY4)/(cX3-cX4)
        b1 = cY1 - m1 * cX1# calculated the y-intercept for each line
        b2 = cY3 - m2 * cX3
        if(m1 != m2):# if the lines are parralell stop to prevent an division by zero error
            xi = (b1 - b2) / (m2 - m1)
            yi = m1 * xi + b1
            
            cv2.circle(ogFrame,(int(xi),int(yi)),15,(150,150,150),-1)# put a circle on the intercept location
      
    
        # this function does things that are pure magic, I don't have the trig knowlegde to do this credit to https://stackoverflow.com/a/28530929 by Jason S
        
        points = numpy.array([[cX1,cY1], [xi,yi], [cX4,cY4]])
        
        A = points[2] - points[0]
        B = points[1] - points[0]
        C = points[2] - points[1]

        angles = []
        
        for e1, e2 in ((A, B), (A, C), (B, -C)):
            num = numpy.dot(e1, e2)
            denom = numpy.linalg.norm(e1) * numpy.linalg.norm(e2)
            angles.append(numpy.arccos(num/denom) * 180 / numpy.pi)
        
        #I grab angle[2] as thats the inside angle and its always that angle

        angle.append(int(str(round(angles[2],0))[:-2]))#the [:-2] deletes the degrees and decimal point on the number and appends it to angle which is my averaging array
   
        del angle[0]# deletes the first of my averaging array 
       
        if(angle[0] != None):# doesn't run this if the averaging array is still filling
            outangle = round(statistics.mean(angle))# take the average number of the whole array
            cv2.putText(ogFrame,str(outangle) + " degrees",(int(statistics.mean([cX1,int(xi),cX4])),int(statistics.mean([cY1,int(yi),cY4]))),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)
            #puts the outangle onto the screen inbetween the three points
    else:
        cv2.setTrackbarPos("Record", "UI",0) # stops recording if one of the points disappears from view
        
    cv2.imshow("LiveFeed",ogFrame)# display frame
    
    if(cv2.getTrackbarPos("Save?","UI") == 1): # if the user says to save this if statement compiles all the variables into a dicationary
        db = {"time" : dtime, "cX1" : dX1, "cY1" : dY1, "cX2" : dX2, "cY2" : dY2, "cX3" : dX3, "cY3" : dY3, "cX4" : dX4, "cY4" : dY4} # dictionary of values and each value is an array
        columns = ("time", "cX1","cY1","cX2","cY2","cX3","cY3","cX4","cY4")#headers for the .csv file
        df = pandas.DataFrame(data = db)# create a data frame with the data equal to db
        
        dPath = path.join("C:","Users",path.expanduser("~"),"Documents","CAPT") # file path
        
        if(not path.exists(dPath)): # detect if a file exists in a specific directory
           os.makedirs(dPath)   # create said file if it doesn't exist
        
        saveLocation = filedialog.asksaveasfilename(filetype = [("CSV Files [*.csv]","*.csv")], initialdir = dPath)
        #^ allow user to pick the name of the save file and the location to save it defaulting in Documents/CAPT
        
        if(len(saveLocation) != 0): #check validity of the assigned save location, if cancel was clicked instead with will not run
            df.to_csv(saveLocation)
        cv2.setTrackbarPos("Save?","UI",0) # reset the trackbar asking if you want to save the recording to exit the loop
                 
cv2.destroyAllWindows() # delete the windows and free the camera to the user again
vid.release()

