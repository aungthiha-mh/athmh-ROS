#!/usr/bin/env python

import rospy
import cv2
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def image_publisher():
	pub = rospy.Publisher("image_pub" , Image , queue_size = 10)
	rate = rospy.Rate(10)

	filepath = "/home/ath11/Pictures/Image Data Sets/apple.png"
	img = cv2.imread(filepath)
	#cv2.imshow("Publishing Image",img)
	#cv2.waitKey(2000)

	bridge = CvBridge()
	img_msg = bridge.cv2_to_imgmsg(img, "bgr8")

	while not rospy.is_shutdown():
		pub.publish(img_msg)
		rate.sleep()

def shutdown_image():
	cv2.destroyAllWindows()

if __name__ == "__main__":
	try:
		rospy.init_node("image_publisher_node")
		rospy.loginfo("Image Publisher Node started")
		image_publisher()
		#shutdown_image()
		
		
	except rospy.ROSInterruptException:
		rospy.logwarn("Image Publisher Node failed")