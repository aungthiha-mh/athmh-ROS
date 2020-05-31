#!/usr/bin/env python

from __future__ import print_function
import cv2
import numpy as np
import rospy
from rosopencv.msg import Pixel

cap = cv2.VideoCapture(0)

def detection():

    pixel_to_cm_x_axis = (11.3/640)
    pixel_to_cm_y_axis = (11.3/480)

    while cap.isOpened():
        ret, frame = cap.read()
        gray1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        cv2.imshow("Background", gray1)
        key = cv2.waitKey(1)
        if key == 27:
            break

    while cap.isOpened():
        _ , frame = cap.read()
        gray2 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #print(frame.shape)

        # To Find object's difference
        difference = np.absolute(np.matrix(np.int16(gray1))-np.matrix(np.int16(gray2)))
        difference[difference>255] = 255
        difference = np.uint8(difference)
        bw = difference
        bw[bw<=100] = 0
        bw[bw>100] = 1

        # To Find Object Location along X-axis
        column_sum = np.matrix(np.sum(bw, 0))
        column_num = np.matrix(np.arange(640))
        column_mul = np.multiply(column_sum, column_num)
        total_col = np.sum(column_mul)
        total1 = np.sum(bw)
        column_location = total_col / total1
        world_units_x_axis = column_location * pixel_to_cm_x_axis

        # To Find Object Location along Y-axis
        row_sum = np.matrix(np.sum(bw, 1))
        row_sum = row_sum.transpose()
        row_num = np.matrix(np.arange(480))
        row_mul = np.multiply(row_sum, row_num)
        total_row = np.sum(row_mul)
        total2 = np.sum(bw)
        row_location = total_row / total2
        world_units_y_axis = row_location * pixel_to_cm_y_axis

        print(world_units_x_axis , "cm" , world_units_y_axis , 'cm')

        cv2.imshow("ath" , difference)
        cv2.imshow("Foreground", gray2)
        key = cv2.waitKey(1)
        if key == 27:
            break
    return world_units_x_axis,world_units_y_axis

def camera_shutdown():
	cap.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
    rospy.init_node("detected_object_pub_node")
    pub = rospy.Publisher("/object",Pixel,queue_size=10)
    rate = rospy.Rate(10)

    x_value , y_value = detection()
    camera_shutdown()

    data = Pixel()
    data.x = x_value
    data.y = y_value

    while not rospy.is_shutdown():
        pub.publish(data)
        rate.sleep()
        print("I send >> ",data.x , data.y)

