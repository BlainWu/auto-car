# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> ObstacleAvoidance
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/8/11 15:10
@Desc   ：
=================================================='''
import cv2
import numpy as np
def findObstacl(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    dst = cv2.erode(mask, kernel, iterations=3)
    # dst = cv2.dilate(dst,kernel,iterations=1)

    contours, hierarchy = cv2.findContours(dst,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    return contours,hierarchy

if __name__ == '__main__':
    lower_hsv = np.array([160, 43, 46])
    upper_hsv = np.array([175, 255, 255])
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    frame = cv2.imread('./1.jpg')

    contours, hierarchy = findObstacl(frame)

    for c in contours:
        M = cv2.moments(c)
        print(M)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # calculate x,y coordinate of center
        cv2.circle(frame, (cX, cY), 3, (255, 255, 255), -1)

    cv2.imshow('show',frame)
    cv2.waitKey(0)