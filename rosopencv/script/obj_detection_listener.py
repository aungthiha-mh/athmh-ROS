#!/usr/bin/env python

import tf
import rospy

import roslib
roslib.load_manifest('rosopencv')


def tf_frame_listener():
	rospy.init_node('obj_detection_listener_node')
	listener = tf.TransformListener()

	transform = tf.TransformerROS()

	# waitForTransform(target_frame, source_frame, time, timeout, polling_sleep_duration = rospy.Duration(0.01))
	listener.waitForTransform("camera","base",rospy.Time(0),rospy.Duration(10))
	rate = rospy.Rate(1)

	while not rospy.is_shutdown():

		# lookupTransform(target_frame, source_frame, time) returns tuple->(translation, orientation (may be quaternion))
		translation,rotation = listener.lookupTransform("camera","base",rospy.Time(0))

		angle, direc, point = tf.transformations.rotation_from_matrix(transform.fromTranslationRotation(translation,rotation))
		print("Angle")
		print(angle)
		print("Homogeneous Transformation")
		print(transform.fromTranslationRotation(translation,rotation))
		#print("The translation is {} \nThe rotation is {} \n".format(translation,rotation))
		rate.sleep()

if __name__ == "__main__":
	tf_frame_listener()
	print("Transform frame is listening")