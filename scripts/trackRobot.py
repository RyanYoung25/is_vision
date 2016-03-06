#! /usr/bin/env python 
#import the necessary modules

import rospy
from is_vision.msg import PioneerPos
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
 
def main():

    pub = rospy.Publisher('robot_pos', PioneerPos)
    rospy.init_node('robot_tracker', anonymous=True)
    
    


    while not rospy.is_shutdown():
        #get a frame from RGB camera
        frame = get_video()
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # define range of green color in HSV
        lower_green = np.array([30,0,0])
        upper_green = np.array([80,255,255])
        
        # Threshold the HSV image to get only green colors. This is used to find the contours
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
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
                

        #Find the rotated rectangle -> send it as a ros message
        pos, size, theta = cv2.minAreaRect(bigContour)
        print pos
        print size
        print theta
        
        #Build our message
        msg = PioneerPos()
        msg.x = float(pos[0])
        msg.y = float(pos[1])
        msg.w = float(size[0])
        msg.l = float(size[1])
        msg.theta = float(theta)

        #Publish our message to the robot_pos channel
        pub.publish(msg)
        

if __name__ == '__main__':
    main()

        
        
         
        






