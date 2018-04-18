import cv2
import numpy as np
from firebase import firebase

url = "https://dw-1d-8f3a9.firebaseio.com/" # URL to Firebase database
token = "PdWOHUtcScXODzmm8b3pSoFY78dxZQXVSpynXx1n" # unique token used for authentication
firebase = firebase.FirebaseApplication(url, token)

cap = cv2.VideoCapture(1)
state = 'car_no'

while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([30,150,50])
    upper_red = np.array([255,255,180])
    
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    
    
    
    
    
    if state == 'car_no':
        threshold = len(np.nonzero(res)[0])
    
        if threshold > 800:
            print(True)
            state = 'car_yes'
            # car_num += 1
            firebase.put('/','inp1',True)
            # firebase.put('/','car_num',car_num)
            
    if state == 'car_yes':
        threshold = len(np.nonzero(res)[0])
        
        if threshold < 800:
            print(False)
            state = 'car_no'
            firebase.put('/','inp1',False)
        
    cv2.imshow('img',frame)    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()