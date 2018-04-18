# import the necessary packages
import numpy as np
import argparse
import cv2


'''boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])
]'''
boundaries = [
	([17, 15, 100], [50, 56, 200])
	]
cap = cv2.VideoCapture(1)
while 1:
    ret, image1 = cap.read()
    for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

    # find the colors within the specified boundaries and apply
    # the mask
        mask = cv2.inRange(image1, lower, upper)
        output = cv2.bitwise_and(image1, image1, mask=mask)

    # show the images
        cv2.imshow("image", np.hstack([image1, output]))
        cv2.waitKey(0)
        
        

cap.release()
cv2.destroyAllWindows()