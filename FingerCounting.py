import cv2
import time
import os
import HandTrackingModule as htm
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
print(myList)

overLayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderFath}/{image}')
    overLayList.append(image)
print(len(overLayList))
pTime = 0


detector = htm.handDetector(detectionCon=1)

tipId = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []
        # Thumb
        if lmList[tipId[0]][1] > lmList[tipId[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # four Finger
        for Id in range(1, 5):
            if lmList[tipId[Id]][2] < lmList[tipId[Id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFinger = fingers.count(1)
        print(totalFinger)
        h, w, c = overLayList[0].shape
        img[0:h, 0:w] = overLayList[totalFinger-1]

        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFinger), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70),cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
