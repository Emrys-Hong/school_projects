import cv2
import numpy as np
from firebase import firebase

url = "https://dw-1d-8f3a9.firebaseio.com/" # URL to Firebase database
token = "PdWOHUtcScXODzmm8b3pSoFY78dxZQXVSpynXx1n" # unique token used for authentication
firebase = firebase.FirebaseApplication(url, token)

cap = cv2.VideoCapture(1)

while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([0,100,180])
    upper_red = np.array([30,255,250])
    
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    firebase.put('/','inp1',False)
    threshold = len(np.nonzero(res)[0])
    print(threshold)
    if threshold > 900:
        print(True)
        firebase.put('/','inp1',True)
        #break
    cv2.imshow('img',frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()