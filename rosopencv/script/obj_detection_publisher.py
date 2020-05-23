#!/usr/bin/env python

from __future__ import print_function
import rospy
from sensor_msgs.msg import Image
from obj_detection_cm import detection
from rosopencv.msg import Pixel

rospy.init_node("object_detection_publisher_node")
pub = rospy.Publisher("/object",Pixel,queue_size=10)

rate = rospy.Rate(1)

x , y = detection()

obj = Pixel()
obj.x = float(x)
obj.y = float(y)

while not rospy.is_shutdown():
	pub.publish(obj)
	rate.sleep()
	print("I send >> ", obj.x , obj.y)

# def shutdown():
#   print "shutdown time!"

# rospy.on_shutdown(shutdown)

print("Detection is end")