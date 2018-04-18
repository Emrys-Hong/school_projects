''' this code is to detect the red color paste on the thymio and write it in the firebase'''
# some part of the code is from sendtex
import cv2
import numpy as np
from firebase import firebase

url = "https://dw-1d-8f3a9.firebaseio.com/" # URL to Firebase database
token = "PdWOHUtcScXODzmm8b3pSoFY78dxZQXVSpynXx1n" # unique token used for authentication
firebase = firebase.FirebaseApplication(url, token)

cap = cv2.VideoCapture(1) # this output the video capture from the web camera

''' a simple state machine '''
state = 'car_no' # the initial state is there is no_car

while(1): # the camera keeps updating new information
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # this is using opencv to convert the normal BGR 
    
    lower_red = np.array([30,150,50]) # the upper bond of red color get it by trying and error
    upper_red = np.array([255,255,180]) # the lower bond of red color 255 is the biggest and zero is the smallest. (255,255,255) is bright and (0,0,0) is dark
    
    mask = cv2.inRange(hsv, lower_red, upper_red) # if the pixel is the 'red color range'
    res = cv2.bitwise_and(frame,frame, mask= mask) # then we add the mask to the frame
   
    # state machine    
    # if there is no car, the camera continueslly checking whether there is car, if there is the state change to 'car_yes' and upload the inp1 into the firebase for thymio
    if state == 'car_no':
        threshold = len(np.nonzero(res)[0]) # this output how many red pixel there is
        # if there is no red object, the output should from 0 to 5, if there is a red object, the value is above 1000
        # we change the threshold value to 800 here to see whether there is any car
        if threshold > 800: # normally if there is no red pixels there should not be any car, but if there is a thymio(car) with a red sticker, we know that there is car
            print(True)
            state = 'car_yes'
            
            firebase.put('/','inp1',True)

# if there is a thymio(car), the camera continueslly checking whether the thymio have gone or not, if the thymio have gone, the state change to 'car_yes' and upload the inp1 into the firebase for thymio.
        if state == 'car_yes':
        threshold = len(np.nonzero(res)[0])
        
        if threshold < 800:
            print(False)
            state = 'car_no'
            firebase.put('/','inp1',False)
        
    cv2.imshow('img',frame)    # show where the camera is looking at
    k = cv2.waitKey(5) & 0xFF # stop when press control + C
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
