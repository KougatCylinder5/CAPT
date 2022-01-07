# Cory Mavis


import pandas  # CSV manipulation library
import numpy
import sys
import subprocess
from os import makedirs
import os.path as path  # directory library
import statistics
from math import floor
from math import tan
from math import atan
from time import time
import tkinter as tk  # file manipulation/selection library
from tkinter import filedialog
import cv2

root = tk.Tk()
root.withdraw()  # deletes empty Tninter box

vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
vid.set(cv2.CAP_PROP_GAIN, 95)
vid.set(cv2.CAP_PROP_BRIGHTNESS, 85)
vid.set(cv2.CAP_PROP_EXPOSURE, -1.0)     # camera default modifications
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)

class targeting:
    
    def __inti__(self, angle):
        self.targetSlope = tan(angle)
        
    def Target(self, info1):  # slope is the line current slope of the angle, (x,y) is the starting location to draw the line 
        slope, b, x, y = info1
        slopeAngle = atan(slope)
        targetAngle = slopeAngle + self.targetSlope
        print(tan(targetAngle))
        
        
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

    def append(self, X1, Y1, X2, Y2, X3, Y3, X4, Y4, time):
        self.dtime.append(time)
        self.dX1.append(X1)
        self.dY1.append(Y1)
        self.dX2.append(X2)
        self.dY2.append(Y2)
        self.dX3.append(X3)
        self.dY3.append(Y3)
        self.dX4.append(X4)
        self.dY4.append(Y4)


class calibrate:

    def __init__(self):  # runs on creating the instance of each class
        self.maxColorOne = (8, 255, 255)  # defines min and max for each of the colors on default
        self.minColorOne = (2, 130, 55)
        self.maxColorTwo = (90, 255, 255)
        self.minColorTwo = (50, 100, 20)
        self.maxColorThree = (120, 255, 255)
        self.minColorThree = (100, 50, 0)
        self.maxColorFour = (29, 255, 255)
        self.minColorFour = (13, 205, 182)
        self.clickNumber = 0
        self.hide = True
        self._internalCounterOld = time()
    # called when calibrating color detection

    def startCalibrating(self, x, y):

        if(self.clickNumber == 0):
            markTwo = self.rawImg[y, x]
            self.maxColorTwo = numpy.array([markTwo[0] + 3, markTwo[1] + 20, markTwo[2] + 20])
            self.minColorTwo = numpy.array([markTwo[0] - 3, markTwo[1] - 20, markTwo[2] - 20])
            self.clickNumber = self.clickNumber + 1

        elif(self.clickNumber == 1):
            markOne = self.rawImg[y, x]
            self.maxColorOne = numpy.array([markOne[0] + 3, markOne[1] - 20, markOne[2] - 20])
            self.minColorOne = numpy.array([markOne[0] - 3, markOne[1] - 20, markOne[2] - 20])
            self.clickNumber = self.clickNumber + 1

        elif(self.clickNumber == 2):
            markThree = self.rawImg[y, x]
            self.maxColorThree = numpy.array([markThree[0] + 3, markThree[1] + 20, markThree[2] + 20])  # defines upper and lower limit
            self.minColorThree = numpy.array([markThree[0] - 3, markThree[1] - 20, markThree[2] - 20])
            self.clickNumber = self.clickNumber + 1

        elif(self.clickNumber == 3):
            markFour = self.rawImg[y, x]
            self.maxColorFour = numpy.array([markFour[0] + 3, markFour[1] - 20, markFour[2] - 20])
            self.minColorFour = numpy.array([markFour[0] - 3, markFour[1] - 20, markFour[2] - 20])
            self.clickNumber = 0
            self.hide = True
            cv2.setTrackbarPos("Calibrate", "UI", 0)

        else:
            raise valueError("calibrate.clickNumber exceded maximum value")

    def autoCalibrate(self, cX1, cY1, cX2, cY2, cX3, cY3, cX4, cY4):
        listX = [cX2, cX1, cX3, cX4]
        listY = [cY2, cY1, cY3, cY4]
        print(time() - 0.2)
        print(self._internalCounterOld)
        if(self._internalCounterOld < time() - 0.5):
            i = 0
            while(i < 3):
                print("test")
                Cali.startCalibrating(listX[self.clickNumber],listY[self.clickNumber])
                i = i + 1
            self._internalCounterOld = time()


file = None


def rewatch(value):  # function to determine if to open a .csv file for playback
    global file
    if(value == 1):
        file_path = filedialog.askopenfilename()
        if(len(file_path) > 0):
            file = pandas.read_csv(file_path)
            cv2.setTrackbarPos("Record", "UI", 0)
        else:
            cv2.setTrackbarPos("ReWatch?", "UI", 0)

            
def tripTarget(value):
    global target
    if(value != 0):
        target = targeting(value)
    else:
        target = None
    
    
cv2.namedWindow("LiveFeed", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("UI")

cv2.imshow("UI",numpy.ones((50,200),dtype = numpy.uint8))

cv2.createTrackbar("Calibrate", "UI", 0, 1, lambda x: None)  # creating trackbars for grabbing user input
cv2.createTrackbar("Record", "UI", 0, 1, lambda x: None)
cv2.createTrackbar("Save?", "UI", 0, 1, lambda x: None)
cv2.createTrackbar("ReWatch?", "UI", 0, 1, rewatch)
cv2.createTrackbar("Auto Cali","UI", 0, 1,lambda x: None)
cv2.createTrackbar("Target Ang", "UI",0,180, tripTarget)


def callback(event, x, y, flags, params):

    if(event == 1 and cv2.getTrackbarPos("Calibrate", "UI") == 1):
        Cali.startCalibrating(x, y)

cv2.setMouseCallback("LiveFeed", callback)


angle = [None] * 5  # empty array for averaging the degrees

Cali = calibrate()

record = recording()

target = None

i = 0  # creates blank value for, the for loop for replaying files

while(cv2.waitKey(1) != 27):
    
    if(cv2.getTrackbarPos("Calibrate", "UI") == 1 and Cali.hide):
        angle = [None] * 5  # resets the angle array for averaging the angle to prevent irregulaties

        print("Choose New Points for color calibration in this order:")
        print("Green, Red, Gold, Blue")
        Cali.hide = False

    if(cv2.getTrackbarPos("ReWatch?", "UI") == 0 and type(vid) is not None):  # skips a ton of unnessicary logic if the slider isn't in the correct position
        ret, frame = vid.read()  # read from camera

        if(not ret):  # prevents throwing an error due to missing or occupied camera
            print("Broke")
            break
        ogFrame = frame.copy()  # duplicates the frame for overlay purposes
        frame = cv2.blur(frame, (20, 20), cv2.BORDER_DEFAULT)  # blurs the frame make color detection easier and more uniform
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # converts from the BGR to HSV colorspace

        Cali.rawImg = hsv

        colorOne = cv2.inRange(hsv, Cali.minColorOne, Cali.maxColorOne)  # grabs the inRange parts of the images
        colorTwo = cv2.inRange(hsv, Cali.minColorTwo, Cali.maxColorTwo)
        colorThree = cv2.inRange(hsv, Cali.minColorThree, Cali.maxColorThree)
        colorFour = cv2.inRange(hsv, Cali.minColorFour, Cali.maxColorFour)

        kernel = numpy.ones((5, 5), numpy.uint8)  # just a 5x5 grid of ones

        colorOne = cv2.morphologyEx(colorOne, cv2.MORPH_OPEN, kernel)  # deletes pixel groups less then 15x15 in size
        colorOne = cv2.morphologyEx(colorOne, cv2.MORPH_CLOSE, kernel)  # fills holes pixel groups that are more then 15x15 in size with the hole being less then 15x15 in size

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
        if(type(vid) is not None):
            print("Can only use the replay feature due to missing camera, if this is not supposed to be happening ensure camera isn't getting used by another program and restart CAPT")
        length = len(file["Unnamed: 0"])  # get the length of the file so that it can be stopped one frame before it reaches the end to prevent exceptions
        if(i > length - 3):  # prior said stopper
            i = 0
            cv2.setTrackbarPos("ReWatch?", "UI", 0)
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
        ogFrame = numpy.zeros((len(ogFrame), len(ogFrame[0]), 3), dtype = numpy.uint8)
        # creates a black background so that it can put the dots on without interference
        cv2.circle(ogFrame, (cX1, cY1), 15, (0, 0, 255), -1)  # puts dots in the positions
        cv2.circle(ogFrame, (cX2, cY2), 15, (0, 255, 0), -1)
        cv2.circle(ogFrame, (cX3, cY3), 15, (255, 0, 0), -1)
        cv2.circle(ogFrame, (cX4, cY4), 15, (78, 255, 237), -1)
        cv2.waitKey(file["time"][i + 1] - file["time"][i])  # wait for the alotted time so that it doesn't instantly zip to the end

    complete = 0

    if(cX2 is not None and cX1 is not None and Cali.hide):  # draw lines between the corrosponding dots
        cv2.line(ogFrame, (cX2, cY2), (cX1, cY1), (255, 255, 255), 10)
        complete = complete + 1

    if(cX3 is not None and cX4 is not None and Cali.hide):
        cv2.line(ogFrame, (cX3, cY3), (cX4, cY4), (255, 255, 255), 10)
        complete = complete + 1

    if(complete == 2 and Cali.hide and cX1 != cX2 and cX3 != cX4):  # only allow angle calculations if it can see all the color positions

        if(cv2.getTrackbarPos("Record", "UI") == 1):  # only record if the slider says so
            # get the current time in millis
            record.append(cX1, cY1, cX2, cY2, cX3, cY3, cX4, cY4, floor(time()*1000))
        if(cv2.getTrackbarPos("Auto Cali", "UI") == 1):
            
            Cali.autoCalibrate(cX1, cY1, cX2, cY2, cX3, cY3, cX4, cY4)
            print("called")
        
        m1 = (cY1-cY2)/(cX1-cX2)  # calculate slope so we can determine where the lines intercept
        m2 = (cY3-cY4)/(cX3-cX4)
        b1 = cY1 - m1 * cX1  # calculated the y-intercept for each line
        b2 = cY3 - m2 * cX3
        if(m1 != m2):  # if the lines are parralell stop to prevent an division by zero error
            xi = (b1 - b2) / (m2 - m1)
            yi = m1 * xi + b1

            cv2.circle(ogFrame, (int(xi), int(yi)), 15, (150, 150, 150), -1)  # put a circle on the intercept location

        # this function does things that are pure magic, I don't have the trig knowlegde to do this credit to https://stackoverflow.com/a/28530929 by Jason S

        points = numpy.array([[cX1, cY1], [xi, yi], [cX4, cY4]])

        A = points[2] - points[0]
        B = points[1] - points[0]
        C = points[2] - points[1]

        angles = []

        for e1, e2 in ((A, B), (A, C), (B, -C)):
            num = numpy.dot(e1, e2)
            denom = numpy.linalg.norm(e1) * numpy.linalg.norm(e2)
            angles.append(numpy.arccos(num/denom) * 180 / numpy.pi)

        # I grab angle[2] as thats the inside angle and its always that angle
        print(str(round(angles[2], 0))[:-2])
        angle.append(int(str(round(angles[2], 0))[:-2]))  # the [:-2] deletes the degrees and decimal point on the number and appends it to angle which is my averaging array

        del angle[0]  # deletes the first of my averaging array

        if(angle[0] is not None):  # doesn't run this if the averaging array is still filling
            outangle = round(statistics.mean(angle))  # take the average number of the whole array
            cv2.putText(ogFrame, str(outangle) + " degrees", (int(statistics.mean([cX1, int(xi), cX4])), int(statistics.mean([cY1, int(yi), cY4]))), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
            # puts the outangle onto the screen inbetween the three points
         
        if(target is not None):
            target.Target((m1, b1, xi, yi),)
            
    else:
        if(cv2.getTrackbarPos("Calibrate", "UI") == 0):
            Cali.clickNumber = 0
            Cali.hide = True
        cv2.setTrackbarPos("Record", "UI", 0)  # stops recording if one of the points disappears from view

    cv2.imshow("LiveFeed", ogFrame)  # display frame

    if(cv2.getTrackbarPos("Save?", "UI") == 1 and len(record.dtime) > 0):  # if the user says to save this if statement compiles all the variables into a dicationary
        db = {"time": record.dtime, "cX1": record.dX1, "cY1": record.dY1, "cX2": record.dX2, "cY2": record.dY2, "cX3": record.dX3, "cY3": record.dY3, "cX4": record.dX4, "cY4": record.dY4}  # dictionary of values and each value is an array
        columns = ("time", "cX1", "cY1", "cX2", "cY2", "cX3", "cY3", "cX4", "cY4")  # headers for the .csv file
        df = pandas.DataFrame(data = db)  # create a data frame with the data equal to db

        dPath = path.join("C:", "Users", path.expanduser("~"), "Documents", "CAPT")  # file path

        # detect if a file exists in a specific directory
        if(not path.exists(dPath)):
            makedirs(dPath)   # create said file if it doesn't exist

        saveLocation = filedialog.asksaveasfilename(filetype = [("All Files", "*")], initialdir = dPath)
        # ^ allow user to pick the name of the save
        # file and the location to save it defaulting in Documents/CAPT

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
