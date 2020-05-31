#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import cv2
import numpy as np
import rospy
from rosopencv.srv import *
import math

rospy.init_node("obj_client_node")
rospy.wait_for_service("/detection_service")
client = rospy.ServiceProxy("/detection_service",ObjLocation)

rate = rospy.Rate(10)

requesting = ObjLocationRequest()


while not rospy.is_shutdown():
	rospy.loginfo("Object Detection Client Node started")
	print(requesting.desired_x , requesting.desired_y)
	client(requesting)
	rate.sleep()

	