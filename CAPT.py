# Cory Mavis

import pandas  # CSV manipulation library
import numpy
import webbrowser
from os import makedirs # creation of file to put results into
import os.path as path  # directory library
import statistics # runs median to average angles
import math # math functions for calculating angles
import time # record time between frames
import tkinter as tk  # file manipulation/selection library
from tkinter import filedialog # allows openning of files
import cv2 # camera interaction
from pysine import sine# plays sound 
import threading# allows creation of extra threads so that I can play audio without interupting the camera

webbrowser.open(url = "https://github.com/KougatCylinder5/CAPT/wiki", new = 1)


root = tk.Tk() # creates empty Tninter object
root.withdraw()  # deletes empty Tninter box

vid = cv2.VideoCapture(0) # open camera
ret,frame = vid.read() # read camera frame
vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
vid.set(cv2.CAP_PROP_GAIN, 95)
vid.set(cv2.CAP_PROP_BRIGHTNESS, 85)
vid.set(cv2.CAP_PROP_EXPOSURE, -1.0)     # camera default modifications
#vid.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
#vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


class targeting: # targeting class to contain varibles and functions
    
    def __init__(self,angle):
        self.targetRadians = angle * math.pi/180
        # converts the angle into radians for easier manipulation
        
    def Target(self,info):
        flip = 1
        removeAdding = 180
            
        if(cv2.getTrackbarPos("Flip Lineside","UI") == 1):
            flip = -1
        if(self.targetRadians != 0):
            
            slope, x, y, orientation = info#disect info which is a tuple into 4 parts
            slopeD = math.atan(slope) * 180/math.pi # covert the slope into degrees
            # add the target angle and the current angle of the stationary segment together
            if(orientation == 1):# if the stationary arm is to the left or right
                combinedD = slopeD + 180 - (self.targetRadians * flip * 180/math.pi)#specialized adding for each side
                return(round(x + (100 * math.cos(combinedD * math.pi/180))),\
                       round(y + (100 * math.sin(combinedD * math.pi/180))))
                #draws a straight line fourhundred unit lengths long from xi,yi
            elif(orientation == 0):#specialized adding for each side
                combinedD = slopeD + (self.targetRadians * flip * 180/math.pi)#specialized adding for each side
                return(round(x + (-100 * math.cos(combinedD * math.pi/180))),\
                       round(y + (-100 * math.sin((combinedD * math.pi/180)))))
                #same return function as above with -100 so it faces in the correct direction
class recording:  # stores all the recording related information

    def __init__(self):
        self.dtime = []  # array to store the length of each frame for playback
        self.dX1 = []  # blank arrays for recording values for each of the points
        self.dY1 = []
        self.dX2 = []
        self.dY2 = []
        self.dX3 = []
        self.dY3 = []
        self.dX4 = []
        self.dY4 = []
        self.targetPoint = []
        self.flip = []

    def append(self, X1, Y1, X2, Y2, X3, Y3, X4, Y4, time, targetPoint,flip):
        # all in one function to append values to an array
        self.dtime.append(time)
        self.dX1.append(X1)
        self.dY1.append(Y1)
        self.dX2.append(X2)
        self.dY2.append(Y2)
        self.dX3.append(X3)
        self.dY3.append(Y3)
        self.dX4.append(X4)
        self.dY4.append(Y4)
        self.targetPoint.append(targetPoint)
        self.flip.append(flip)


class calibrate:

    def __init__(self):  # runs on creating the instance of each class
        self.maxColorOne = (8, 255, 255)  # defines min and max for each of the colors on default
        self.minColorOne = (2, 130, 55)
        self.maxColorTwo = (90, 255, 255)
        self.minColorTwo = (50, 100, 30)
        self.maxColorThree = (130, 255, 255)
        self.minColorThree = (100, 50, 0)
        self.maxColorFour = (29, 255, 255)
        self.minColorFour = (13, 305, 182)
        self.clickNumber = 0  #records how many times the mouse has been clicked
        self.hide = True  #hides the lines this is an inverted value so !hide
        self._internalCounterOld = time.time()  #stores the time between autocalibration calls
        self.rawImg = None
    # called when calibrating color detection

    def startCalibrating(self, x, y):
        #basic math denoting just to save calibrated colors
        if(self.clickNumber == 0):
            markTwo = self.rawImg[y, x]
            #grab value of the x,y locations to calibrate
            self.maxColorTwo = numpy.array([markTwo[0] + 3, markTwo[1] + 30, markTwo[2] + 30])
            #upper limit for the colors based upon where it was clicked
            self.minColorTwo = numpy.array([markTwo[0] - 3, markTwo[1] - 30, markTwo[2] - 30])
            #lower limit for the colors based upon where it was clicked
            self.clickNumber = self.clickNumber + 1
            #adds one to the click number so it goes onto the next color
        elif(self.clickNumber == 1):
            #same process as above
            markOne = self.rawImg[y, x]
            self.maxColorOne = numpy.array([markOne[0] + 3, markOne[1] + 30, markOne[2] + 30])
            self.minColorOne = numpy.array([markOne[0] - 3, markOne[1] - 30, markOne[2] - 30])
            self.clickNumber = self.clickNumber + 1

        elif(self.clickNumber == 2):
            #same process as above
            markThree = self.rawImg[y, x]
            self.maxColorThree = numpy.array([markThree[0] + 3, markThree[1] + 30, markThree[2] + 30])  
            # defines upper and lower limit
            self.minColorThree = numpy.array([markThree[0] - 3, markThree[1] - 30, markThree[2] - 30])
            self.clickNumber = self.clickNumber + 1

        elif(self.clickNumber == 3):
            #same process as above
            markFour = self.rawImg[y, x]
            self.maxColorFour = numpy.array([markFour[0] + 3, markFour[1] + 30, markFour[2] + 30])
            self.minColorFour = numpy.array([markFour[0] - 3, markFour[1] - 30, markFour[2] - 30])
            #resets the click number back to 0
            self.clickNumber = 0
            #show the lines again between the points
            self.hide = True
            #exit the calibration mode
            cv2.setTrackbarPos("Calibrate", "UI", 0)

        else:
            #just a error catcher if it somehow skips value 3
            raise ValueError("calibrate.clickNumber exceded maximum value")

    def autoCalibrate(self, cX1, cY1, cX2, cY2, cX3, cY3, cX4, cY4):
        #calls startCalibrating every 200ms and uses the points to determine the point for the color
        listX = [cX2, cX1, cX3, cX4]
        #just a list of x locations
        listY = [cY2, cY1, cY3, cY4]
        #just a list of y locations
        if(self._internalCounterOld < time.time() - 0.2):#basic counting call
            for i in listX: #repeats itself 4 times one for each color
                Cali.startCalibrating(listX[self.clickNumber],listY[self.clickNumber])
                
            self._internalCounterOld = time.time()
            #everytime the loop loops take the current time to delay the next call by 200ms


file = None # empty file variable for the csv Playback


def rewatch(value):  # function to determine if to open a .csv file for playback
    global file# file var to be used outside of the function
    if(value == 1):
        file_path = filedialog.askopenfilename()#open file location 
        if(len(file_path) > 0):
            file = pandas.read_csv(file_path)#reads the csv file
            cv2.setTrackbarPos("Record", "UI", 0)
            # if valid path is found stop recording
        else:
            cv2.setTrackbarPos("ReWatch?", "UI", 0)
            # if the length of the file path is 0 reset it
            

def brightness(value):
    vid.set(cv2.CAP_PROP_BRIGHTNESS, value)
def gain(value):
    vid.set(cv2.CAP_PROP_GAIN, value)
def exposure(value): #exposure of the camera
    vid.set(cv2.CAP_PROP_EXPOSURE, value - 10)
    
target = targeting(0) #creates empty object and assigns a default value of 0
def targetA(value): # grabs the value of the targetangle trackbar and overwrites the angle of the target radians
    global target
    target = targeting( value)

tDif = 0 #measured in degrees from target
endThread = False # ends the tread if the main program hangs
                  # or is quit otherwise a memory leak may occur
def soundAlarm(): # alarm function
    global tDif # creates global var for the total difference in angle
    global endThread # reads the quit varible to exit the thread
    while(not endThread): # repeat until quit varible trips
        time.sleep(0.1) # slow it down to prevent camera lagging
        if(tDif > 0.1 and cv2.getTrackbarPos("Target Angle", "UI") > 0): 
            # don't a play a ton if its too close or the target angle is 0
            sine(2000,tDif/20)
            # most annoying tone I could fine to draw the most attention   
            
alarmThread = threading.Thread(target = soundAlarm) # assign a function to a thread 
alarmThread.start() # start the thread quickly atert

def camera(value):
    global vid
    try:
        vid = cv2.VideoCapture(value)
    except:
        pass
    
cv2.namedWindow("LiveFeed", cv2.WINDOW_AUTOSIZE) # create the named windows
cv2.namedWindow("UI")

cv2.imshow("UI",numpy.ones((50,300),dtype = numpy.uint8))
#show named windows


cv2.createTrackbar("Calibrate", "UI", 0, 1, lambda x: None)  # creating trackbars for grabbing user input
cv2.createTrackbar("Target Angle", "UI", 0, 200, targetA)
cv2.createTrackbar("Flip Lineside","UI", 0, 1, lambda x: None)
cv2.createTrackbar("Record", "UI", 0, 1, lambda x: None)
cv2.createTrackbar("Save?", "UI", 0, 1, lambda x: None)
cv2.createTrackbar("ReWatch?", "UI", 0, 1, rewatch)
cv2.createTrackbar("Auto Cali","UI", 0, 1,lambda x: None)
cv2.createTrackbar("Brightness", "UI",0, 200, brightness)
cv2.createTrackbar("Gain", "UI",0, 200, gain)
cv2.createTrackbar("Exposure", "UI", 0, 10, exposure)
cv2.createTrackbar("Camera", "UI", 0, 4, camera)


def callback(event, x, y, flags, params): #create clickable call back

    if(event == 1 and cv2.getTrackbarPos("Calibrate", "UI") == 1): 
        # if the mouse is clicked and calibrate is 1 call start Calibrating
        Cali.startCalibrating(x, y)
        # calls the calibrating function in Cali
cv2.setMouseCallback("LiveFeed", callback)


angle = [None] * 5  # empty array for averaging the degrees

Cali = calibrate() # save an object to a varible

record = recording() # create a recording object

i = 0  # creates blank value for, the for loop for replaying files

runTarget = False # if playing back a file don't calculate the target angle

while(cv2.waitKey(1) != 27): # loop until esc key is pressed
    
    if(cv2.getTrackbarPos("Calibrate", "UI") == 1 and Cali.hide): #reset if trackbar pos is 1
        angle = [None] * 5  # resets the angle array for averaging the angle to prevent irregulaties

        print("Choose New Points for color calibration in this order:")
        print("Green, Red, Gold, Blue")
        Cali.hide = False # hide the lines connecting the dots
    ret, frame = vid.read()
    
    if(cv2.getTrackbarPos("ReWatch?", "UI") == 0 and ret):  # skips a ton of unnessicary logic if the slider isn't in the correct position
         # read from camera

        if(not ret):  # throwing an error due to missing or occupied camera
            cv2.destroyAllWindows()
            raise Exception("Camera Not Detected or Disconnected while program is running")
        ogFrame = frame.copy()  # duplicates the frame for overlay purposes
        frame = cv2.blur(frame, (30, 30), cv2.BORDER_DEFAULT)  # blurs the frame make color detection easier and more uniform
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # converts from the BGR to HSV colorspace

        Cali.rawImg = hsv # copy the raw frame to the calibrating object

        colorOne = cv2.inRange(hsv, Cali.minColorOne, Cali.maxColorOne)  # grabs the inRange parts of the images
        colorTwo = cv2.inRange(hsv, Cali.minColorTwo, Cali.maxColorTwo)
        colorThree = cv2.inRange(hsv, Cali.minColorThree, Cali.maxColorThree)
        colorFour = cv2.inRange(hsv, Cali.minColorFour, Cali.maxColorFour)
        
        kernel = numpy.ones((15, 15), numpy.uint8)  # just a 5x5 grid of ones

        colorOne = cv2.morphologyEx(colorOne, cv2.MORPH_OPEN, kernel)  
        # deletes pixel groups less then 15x15 in size
        colorOne = cv2.morphologyEx(colorOne, cv2.MORPH_CLOSE, kernel)  
        # fills holes pixel groups that are more then 15x15 in size with the hole being less then 15x15 in size

        colorTwo = cv2.morphologyEx(colorTwo, cv2.MORPH_OPEN, kernel)
        colorTwo = cv2.morphologyEx(colorTwo, cv2.MORPH_CLOSE, kernel)

        colorThree = cv2.morphologyEx(colorThree, cv2.MORPH_OPEN, kernel)
        colorThree = cv2.morphologyEx(colorThree, cv2.MORPH_CLOSE, kernel)

        colorFour = cv2.morphologyEx(colorFour, cv2.MORPH_OPEN, kernel)
        colorFour = cv2.morphologyEx(colorFour, cv2.MORPH_CLOSE, kernel)

        M = cv2.moments(colorOne)  # nabs the moments data for the inRange calculations
        cX1 = None  # this is used to tetermine if the if statement has been run
        if(M["m00"] != 0):
            cX1 = int(M["m10"] / M["m00"])  # simple math to find the X location
            cY1 = int(M["m01"] / M["m00"])  # yada yada Y location
            cv2.circle(ogFrame, (cX1, cY1), 15, (0, 0, 255), -1)  # put a dot on the location

        M = cv2.moments(colorTwo)
        cX2 = None
        if(M["m00"] != 0):
            cX2 = int(M["m10"] / M["m00"])
            cY2 = int(M["m01"] / M["m00"])
            cv2.circle(ogFrame, (cX2, cY2), 15, (0, 255, 0), -1)

        M = cv2.moments(colorThree)
        cX3 = None
        if(M["m00"] != 0):
            cX3 = int(M["m10"] / M["m00"])
            cY3 = int(M["m01"] / M["m00"])
            cv2.circle(ogFrame, (cX3, cY3), 15, (255, 0, 0), -1)

        M = cv2.moments(colorFour)
        cX4 = None
        if(M["m00"] != 0):
            cX4 = int(M["m10"] / M["m00"])
            cY4 = int(M["m01"] / M["m00"])
            cv2.circle(ogFrame, (cX4, cY4), 15, (78, 255, 237), -1)

    elif(cv2.getTrackbarPos("ReWatch?", "UI") == 1):  # math to jump straight to here if its replaying a recording
        
        runTarget = True
        if(type(vid) is None):
            print("Can only use the replay feature due to missing camera, if this is not supposed\
            to be happening ensure camera isn't getting used by another program and restart CAPT")
        length = len(file["Unnamed: 0"])# get the length of the file so that it can be stopped one frame before it reaches the end to prevent exceptions
        if(i > length - 3):  # prior said stopper
            i = 0
            cv2.setTrackbarPos("ReWatch?", "UI", 0)
            runTarget = False
            file = None
            continue
        
        else:
            i = i + 1

        cX1 = file["cX1"][i]  # reads the locations of the points and puts them into the variables to be displayed
        cY1 = file["cY1"][i]
        cX2 = file["cX2"][i]
        cY2 = file["cY2"][i]
        cX3 = file["cX3"][i]
        cY3 = file["cY3"][i]
        cX4 = file["cX4"][i]
        cY4 = file["cY4"][i]
        targetPoint = file["targetPoint"][i]
        # slices the targetPoint (returns as a string) into a properly formated Tuple
        targetPoint = tuple((int(targetPoint[1:targetPoint.index(",")]),int(targetPoint[targetPoint.index(" "):targetPoint.index(")")])))
        cv2.setTrackbarPos("Flip Lineside","UI",1)
        #creates an empty array to put all the lines on
        ogFrame = numpy.zeros((480,640, 3), dtype = numpy.uint8)
        # creates a black background so that it can put the dots on without interference
        cv2.circle(ogFrame, (cX1, cY1), 15, (0, 0, 255), -1)  # puts dots in the positions
        cv2.circle(ogFrame, (cX2, cY2), 15, (0, 255, 0), -1)
        cv2.circle(ogFrame, (cX3, cY3), 15, (255, 0, 0), -1)
        cv2.circle(ogFrame, (cX4, cY4), 15, (78, 255, 237), -1)
        cv2.waitKey(file["time"][i + 1] - file["time"][i])  # wait for the alotted time so that it doesn't instantly zip to the end
        cv2.setTrackbarPos("Record","UI",0)
        
    complete = 0

    if(file is not None or ret): #only run if its playing a file back or the camera is running
        if(cX2 is not None and cX1 is not None and Cali.hide): # tests if all the dots are present
            cv2.line(ogFrame, (cX2, cY2), (cX1, cY1), (255, 255, 255), 10)
            complete = complete + 1 #check to ensure both lines have been drawn

        if(cX3 is not None and cX4 is not None and Cali.hide): # tests if all the dots are present
            cv2.line(ogFrame, (cX3, cY3), (cX4, cY4), (255, 255, 255), 10)
            complete = complete + 1

        if(complete == 2 and Cali.hide and cX1 != cX2 and cX3 != cX4):  # only allow angle calculations if it can see all the color positions

            
            if(cv2.getTrackbarPos("Auto Cali", "UI") == 1): # if autocali is 1 run the autocaibrate code
                
                Cali.autoCalibrate(cX1, cY1, cX2, cY2, cX3, cY3, cX4, cY4)
                
            elif(cv2.getTrackbarPos("Calibrate", "UI") == 0): # if its 0 reset the click number
                Cali.clickNumber = 0
            
            m1 = (cY1-cY2)/(cX1-cX2)  # calculate slope so we can determine where the lines intercept
            m2 = (cY3-cY4)/(cX3-cX4)
            b1 = cY1 - m1 * cX1  # calculated the y-intercept for each line
            b2 = cY3 - m2 * cX3
            if(m1 != m2):  # if the lines are parrallel stop to prevent an division by zero error
                xi = int((b1 - b2) / (m2 - m1))
                yi = int(m1 * xi + b1)

                cv2.circle(ogFrame, (xi, yi), 15, (150, 150, 150), -1)  # put a circle on the intercept location
            
            # this function does things that are pure magic, I don't have the trig knowlegde to do this credit to
            #https://stackoverflow.com/a/28530929 by Jason S

            points = numpy.array([[cX1, cY1], [xi, yi], [cX4, cY4]])
            
            B = points[1] - points[0]
            C = points[2] - points[1]

            angles = None

            num = numpy.dot(B, -C)
            denom = numpy.linalg.norm(B) * numpy.linalg.norm(-C)
            try: # this is here because a "true divide" sometimes throws a warning and this hides it
                angles = numpy.arccos(num/denom) * 180 / numpy.pi
            except RuntimeWarning:
                angles = None # pass on the exception because it has no negative effects
            if(numpy.isnan(angles)):
                angles = None
            """
            ORIGINAL
            
            points = numpy.array([[cX1, cY1], [xi, yi], [cX4, cY4]])
            
            A = points[2] - points[0]
            B = points[1] - points[0]
            C = points[2] - points[1]
            angles = []
            for e1, e2 in ((A, B), (A, C), (B, -C)):
                num = numpy.dot(e1, e2)
                denom = numpy.linalg.norm(e1) * numpy.linalg.norm(e2)
                angles.append(numpy.arccos(num/denom) * 180 / numpy.pi)
            """
            
            
            # I grab angle as thats the inside angle and its always that angle
            if(angles is not None ):
                angle.append(int(str(round(angles, 0))[:-2]))  
                # the [:-2] deletes the degrees and decimal point on the number and appends it to angle which is my averaging array

                del angle[0]  # deletes the first of my averaging array
                
                if(angle[0] is not None):  # doesn't run this if the averaging array is still filling
                    outangle = round(statistics.mean(angle))  # take the average number of the whole array
                    cv2.putText(ogFrame, str(outangle) + " degrees", (int(statistics.mean([cX1, int(xi), cX4])), \
                                                                      int(statistics.mean([cY1, int(yi), cY4]))),\
                                                                      cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
                    # puts the outangle onto the screen inbetween the three points
            
            if(statistics.mean((cX2,cX1)) < statistics.mean((cX3,cX4))): #checks if the right/left location of the stationary arm
                direction = 1#this means that its on the left arm
            else:
                direction = 0#this is on the right
            
            
            if(not runTarget):  # if its rewatching old recording don't take the new target points
                targetPoint = target.Target((m1,xi,yi,direction))# get a tuple of an x,y location to put the line and dot
                if(angle[0] is not None):
                    tDif = abs(outangle - (target.targetRadians * 180/math.pi))
            if(targetPoint is not None):
                cv2.circle(ogFrame,targetPoint,15,(150,150,150),-1)#draw aformentioned dot
                cv2.line(ogFrame,targetPoint,(xi,yi),(150,150,150),10)# draw  line
            
            if(cv2.getTrackbarPos("Record", "UI") == 1):  # only record if the slider says so
                flip = cv2.getTrackbarPos("Flip Lineside", "UI")
                record.append(cX1, cY1, cX2, cY2, cX3, cY3, cX4, cY4, math.floor(time.time()*1000), targetPoint, flip)
                #run an append on the record function which is a custom made funtion
                runTarget = False
        else:
            if(cv2.getTrackbarPos("Calibrate", "UI") == 0):
                Cali.clickNumber = 0
                Cali.hide = True

        cv2.imshow("LiveFeed", ogFrame)  # display frame

    if(cv2.getTrackbarPos("Save?", "UI") == 1 and len(record.dtime) > 0):  
        # if the user says to save this if statement compiles all the variables into a dicationary
        db = {"time": record.dtime, "cX1": record.dX1, "cY1": record.dY1, "cX2": record.dX2, "cY2":\
              record.dY2, "cX3": record.dX3, "cY3": record.dY3, "cX4": record.dX4, "cY4": record.dY4,\
              "targetPoint": record.targetPoint, "flip": record.flip}  # dictionary of values and each value is an array
        columns = ("time", "cX1", "cY1", "cX2", "cY2", "cX3", "cY3", "cX4", "cY4", "targetPoint", "flip")  # headers for the .csv file
        df = pandas.DataFrame(data = db)  # create a data frame with the data equal to db

        dPath = path.join("C:", "Users", path.expanduser("~"), "Documents", "CAPT")  # file path

        # detect if a file exists in a specific directory
        if(not path.exists(dPath)):
            makedirs(dPath)   # create said file if it doesn't exist

        saveLocation = filedialog.asksaveasfilename(filetype = [("All Files", "*")], initialdir = dPath)
        # ^ allow user to pick the name of the save
        # file and the location to save it defaulting in Documents/CAPT/

        # check validity of the assigned save location,
        # if cancel was clicked instead with will not run
        if(len(saveLocation) != 0):
            df.to_csv(saveLocation)
            record = recording()
        cv2.setTrackbarPos("Save?", "UI", 0)
        # reset the trackbar asking if you want to save the
        # recording to exit the loop
cv2.destroyAllWindows()
# delete the windows and free the camera to the user again
vid.release()
endThread = True
