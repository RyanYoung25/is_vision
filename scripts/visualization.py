#! /usr/bin/env python 
#import the necessary modules
import freenect
import cv2
import numpy as np
 
#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array
 
if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        frame = get_video()
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # define range of green color in HSV
        lower_green = np.array([30,0,0])
        upper_green = np.array([80,255,255])
        
        # Threshold the HSV image to get only green colors. This is used to find the contours
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Bitwise-AND mask and original image, only used for visualization
        res = cv2.bitwise_and(frame,frame, mask= mask)
        
        ret,thresh = cv2.threshold(mask,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)

        #Find the largest contour that is found, the rest are just noise
        bigContour = contours[0]
        maxArea = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > maxArea:
                bigContour = contour
                maxArea = area
                

        #Find and draw the rotated rectangle
        rect = cv2.minAreaRect(bigContour)
        print rect
        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(res,[box],0,(0,0,255),2)


        #Show the image
        cv2.imshow('frame',res)
        
         
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()






