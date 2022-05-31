from json import detect_encoding
from time import time
import cv2
import time
import os
import HandTracking as htm

wCam = 640
hCam = 480
pTime = 0

detector = htm.handDetector(0.75)
folderPath = 'FingerImages'
myList = os.listdir(folderPath)
overlayList = []
git 
for imPath in sorted(myList):
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

    

#print(sorted(myList))
cap = cv2.VideoCapture(0)
tipIds = [4,8,12,16,20]

cap.set(3, wCam)
cap.set(4, hCam)

while True:
    suc, img = cap.read()   
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    totalFingers = 0
    if len(lmList) != 0:
        fingers = []
        if lmList[tipIds[0]][1]> lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:   
            fingers.append(0)
        # 4 fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #s = '_'.join(fingers)

        totalFingers = fingers.count(1)
   
        cv2.putText(img, str(totalFingers), (200,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255),1)
        

    h,w,c = overlayList[0].shape
    img[:h, :w] = overlayList[totalFingers]

    


    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(img, f'FPS:{fps}', (500,30), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
    cv2.imshow('window', img)
    cv2.waitKey(1)