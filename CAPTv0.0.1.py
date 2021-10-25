#Cory Mavis
import cv2
import numpy
import os
import subprocess

stream = cv2.VideoCapture(0)

def main():
  rect, frame = stream.read()
  
  cv2.imshow('frame', frame)

if __name__ == __main__:
  main()
