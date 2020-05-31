#!/usr/bin/env python

from __future__ import print_function
import cv2
import numpy as np
import rospy
from rosopencv.srv import *
from rosopencv.msg import Angle
import math
import time
from std_msgs.msg import Int32

def obj_callback(request):
	
	rospy.loginfo("Image Subscriber Node started")

	X = request.desired_x                                                    # desired x postion of end effector in cm
	Y = request.desired_y                                                    # desired y postion of end effector in cm
	r1 = 0.0                                                     # to use in Equation 2
	a2 = 10                                                      # Link 2
	a4 = 8                                                       # Link 4

	print("1 - Elbow Up")
	print("2 - Elbow Down")

	elbow = int(input("Enter the method you want to use : "))

	if elbow == 1:

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

	if elbow == 2:

		# For Finding Theta 1
		r1 = math.sqrt(X**2+Y**2)
		phil1 = math.acos(((a2**2)+(r1**2)-(a4**2))/(2*a2*r1))
		theta1 = (math.atan(Y/X))-phil1

		# For Finding Theta 2
		phil2 = math.acos(((a2**2)+(a4**2)-(r1**2))/(2*a2*a4))
		theta2 = np.radians(180)-phil2

		theta1 = np.degrees(theta1)
		theta2 = np.degrees(theta2)
		print("First servo angle : " , theta1 , "Second Servo angle : " , theta2)

	#print("Radian : ",theta1)                    # This value is in radians
	#print("Radian : ",theta2)                    # This value is in radians

	# You need to convert theta1 and theat2 into degree to use as servo angles
	#print("Degrees : ",np.degrees(theta1))
	#print("Degrees : ",np.degrees(theta2))

	pub = rospy.Publisher("/angle" , Angle , queue_size=10)

	msg = Angle()
	msg.x = theta1
	msg.y = theta2
	pub.publish(msg)

	return ObjLocationResponse(theta1,theta2)
	
rospy.init_node("obj_server_node")
rospy.Service("/detection_service",ObjLocation,obj_callback)
print("The object detection service is ready")
rospy.spin()