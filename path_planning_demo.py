# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> APF-demo
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/8/11 20:17
@Desc   ：
=================================================='''
import cv2

def map_init(frame,start_point,end_point,obstacles):
    #draw the entrance and exit point
    cv2.circle(frame,tuple(end_point),10,color = (0,255,0),thickness=-1)
    cv2.putText(frame,"Exit",(180,30),fontScale=1,fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                thickness=2,color= (0,0,0))

    cv2.circle(frame,tuple(start_point), 10, color=(0, 255, 0), thickness=-1)
    cv2.putText(frame,"Entrance",(145,810),fontScale=1,fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                thickness=2,color= (0,0,0))

    for obstacle in obstacles:
        cv2.drawMarker(frame,position=tuple(obstacle),color=(0,0,255),
                       markerType=cv2.MARKER_STAR,
                       markerSize=30,
                       thickness=2)

    return frame

if __name__ == '__main__':
    origin_map = cv2.imread('./map.png')
    start_point = [215,50]
    end_point = [215,780]
    obstacle_points = [[122,243],[311,487],[164,678],[303,165]]
    map = map_init(origin_map,start_point,end_point,obstacle_points)


    cv2.imshow("result",origin_map)
    cv2.waitKey(0)