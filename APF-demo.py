# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> APF-demo
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/8/11 20:17
@Desc   ：
=================================================='''
import cv2

def map_init(frame):
    #draw the entrance and exit point
    cv2.circle(frame,(215,50),10,color = (0,0,255),thickness=-1)
    cv2.putText(frame,"Exit",(180,30),fontScale=1,fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                thickness=2,color= (0,0,0))

    cv2.circle(frame, (215, 780), 10, color=(0, 0, 255), thickness=-1)
    cv2.putText(frame,"Entrance",(145,810),fontScale=1,fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                thickness=2,color= (0,0,0))

    return frame

if __name__ == '__main__':
    origin_map = cv2.imread('./map.png')
    map = map_init(origin_map)
    cv2.imshow("result",origin_map)
    cv2.waitKey(0)