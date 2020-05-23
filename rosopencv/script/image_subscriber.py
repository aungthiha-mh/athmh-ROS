#!/usr/bin/env python

import rospy
import cv2
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def image_subscriber_callback(image):
	bridge = CvBridge()
	cv_image = bridge.imgmsg_to_cv2(image, desired_encoding='passthrough')
	cv2.imshow("Subscriber Node",cv_image)
	cv2.waitKey(0)

def shutdown_image():
	cv2.destroyAllWindows()

if __name__ == "__main__":
	try:
		rospy.init_node("image_subscriber_node")
		rospy.loginfo("Image Subscriber Node started")

		sub = rospy.Subscriber("image_pub" , Image , image_subscriber_callback)
		rospy.spin()
		shutdown_image()
		
		
	except rospy.ROSInterruptException:
		rospy.logwarn("Image Subscriber Node failed")