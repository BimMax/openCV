import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER


#################
wCam, hCam = 640, 480
##########
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector()


######
from subprocess import call

####

while True:

    suc, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:

        #Filter based on size

        #Find distance benween index and thumb

        #convert volume
        
        #reduce desolution to make it smoother
        #check fingers up
        id1,x1,y1 = lmList[4]
        id2,x2,y2 = lmList[8]
        cx,cy = (x1+x2)//2, (y1+y2)//2 #center between 4 and 8 
        #print( x1,y1,z1)
        cv2.circle(img, (x1,y1), 15,(255,0,255),-1 )
        cv2.circle(img, (x2,y2), 15,(255,0,255),-1 )
        cv2.line(img, (x1,y1),(x2,y2), (255,0,255),3)
        cv2.circle(img, (cx,cy), 15,(255,0,255),-1 )


        length = math.hypot(x2-x1, y2-y1)
    
        vol = np.interp(length, [50,300], [0,100])
        #volPer = np.interp(length, [50,300], [400,150])
        #volume = length/maxVol*100
        #print( volume)
        call(["amixer", "-D", "pulse", "sset", "Master", str(vol)+"%"])

        cv2.rectangle(img, (50,150), (85,400), (0,255,0),3)
        dd = int(250*vol/100)
        v = 400 - dd
        print(v)
        cv2.rectangle(img, (50,v), (85,400), (255,255,0),-1)
        cv2.putText(img, f'{int(vol)}%', (40,450), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),2)
        if length<100:
             cv2.circle(img, (cx,cy), 15,(0,255,0),-1 )

        #print(length)

    
    
    
    cTime= time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    

    cv2.imshow('image', img)
    cv2.waitKey(1)