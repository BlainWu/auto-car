# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> PerspectiveTrans
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/8/13 19:47
@Desc   ：
=================================================='''
import cv2
import numpy as np

if __name__ == '__main__':
    img = cv2.imread("./2.jpg")
    origin_area = np.float32([[100,100],[220,100],[0,200],[320,200]])
    dest_area = np.float32([[50,50],[350,50],[50,350],[350,350]]) #左上、右上，左下，右下
    Trans_Matrix = cv2.getPerspectiveTransform(origin_area,dest_area)
    trans_img = cv2.warpPerspective(img,Trans_Matrix,(400,400))
    cv2.imshow('transformed image', trans_img)
    cv2.imshow('origin image',img)
    cv2.waitKey(0)