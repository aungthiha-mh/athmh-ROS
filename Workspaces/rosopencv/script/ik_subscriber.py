#!/usr/bin/env python

from __future__ import print_function
import cv2
import numpy as np
import rospy
from rosopencv.msg import Pixel
import math

def object_callback(msg):

	rospy.loginfo("Image Subscriber Node started")

	X = msg.x                                                    # desired x postion of end effector in cm
	Y = msg.y                                                    # desired y postion of end effector in cm
	r1 = 0.0                                                     # to use in Equation 2
	a2 = 10                                                      # Link 2
	a4 = 8                                                       # Link 4

	# For Finding Theat 1
	r1 = math.sqrt(X**2+Y**2)                                    # Equation 2
	phil3 = math.atan(Y/X)                                       # Equation 1
	#a4**2 = (a2**2)+(r1**2)-(2*a2*r1*(math.cos(phil1)))         # Equation 3 ( It isn't used)
	phil1 = math.acos(((a2**2)+(r1**2)-(a4**2))/(2*a2*r1))       # Equation 7 ( It is derived from Equation 3)
	theta1 = phil1+phil3                                         # Equation 4 ( In radians)

	# For Finding Theta 2
	#r1**2 = (a2**2)+(a4**2)-(2*a2*a4*(math.cos(phil2)))         # Equation 5 ( It isn't used)
	phil2 = math.acos(((a2**2)+(a4**2)-(r1**2))/(2*a2*a4))       # Equation 8 ( It is derived from Equation 5)
	theta2 = phil2-np.radians(180)                               # Equation 6 ( In radians)

	theta1 = np.degrees(theta1)
	theta2 = np.degrees(theta2)
	print("First servo angle : " , theta1 , "Second Servo angle : " , theta2)

	#print("Radian : ",theta1)                    # This value is in radians
	#print("Radian : ",theta2)                    # This value is in radians

	# You need to convert theta1 and theat2 into degree to use as servo angles
	#print("Degrees : ",np.degrees(theta1))
	#print("Degrees : ",np.degrees(theta2))

rospy.init_node("detected_object_sub_node")
rospy.Subscriber("/object" , Pixel , object_callback)
rospy.spin()