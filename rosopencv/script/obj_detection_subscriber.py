#!/usr/bin/env python

from __future__ import print_function
import rospy
import tf
from rosopencv.msg import Pixel
import roslib
roslib.load_manifest('rosopencv')
import math

def callback(msg):
	print("I receive >> ",msg.x , msg.y)
	broadcaster = tf.TransformBroadcaster()
	rate = rospy.Rate(10)

	while not rospy.is_shutdown():

		#Broadcast the transformation from tf frame child to parent on ROS topic "/tf
		translation = (-msg.x,  -msg.y , 0.0 )
		#rotation = 	  (0.0 , 0.0 , 0.0 , 1.0)

		theta_x = 90                                                                          # this angle x are in degree
		theta_y = 45                                                                          # this angle y are in degree
		theta_z = 60                                                                          # this angle z are in degree

		# convert from degree to radians

		theta_x = math.radians(theta_x)
		theta_y = math.radians(theta_y)
		theta_z = math.radians(theta_z)
		origin, xaxis, yaxis, zaxis = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)              # this line is always constant
		#I = transformations.identity_matrix()
		Rx = tuple(tf.transformations.rotation_matrix(theta_x, xaxis))
		Ry = tuple(tf.transformations.rotation_matrix(theta_y, yaxis))
		Rz = tuple(tf.transformations.rotation_matrix(theta_z, zaxis))
		rotation = tf.transformations.concatenate_matrices(Rx, Ry, Rz)

		rotation = tf.transformations.quaternion_from_matrix(rotation)

		time = rospy.Time(0)
		child = "camera"
		parent = "base"

		# sendTransform(translation, rotation, time, child, parent)
		# rotation will be [0,0,0,1] matrix in this program because it is Quaternion matrix (rotation may be any rotational matrix)
		broadcaster.sendTransform(translation, rotation, time, child, parent)
		rate.sleep()


rospy.init_node("object_detection_subscriber_node")
sub = rospy.Subscriber("/object",Pixel,callback)
rospy.spin()