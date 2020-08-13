# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> APF-demo
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/8/11 20:17
@Desc   ：
=================================================='''
import cv2
import  numpy as np

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
    start_point = [215,780]
    end_point = [215,50]
    obstacle_points = [[140,243],[80,243],[200,243],[260,487],[164,678]]
    map = map_init(origin_map,start_point,end_point,obstacle_points)
    start_point = np.array(start_point)
    end_point = np.array(end_point)
    robot_point = start_point

    K1,K2 = 5000,1000 #lamda1,lamda2
    P_rob2end = end_point - robot_point
    P_rob2end_distance = np.sqrt(np.sum(np.square(P_rob2end)))
    step_index = 0
    safe_distance = 100
    while(P_rob2end_distance >50):
        F_end_att = K1 * (P_rob2end/P_rob2end_distance) #attractive direction
        F_repulsion = np.array([0,0]) #repulsion direction
        for obstacle in obstacle_points:
            P_ri =  robot_point - obstacle
            P_ri_distance = np.sqrt(np.sum(np.square(P_ri)))# ||P_ri||
            if P_ri_distance > safe_distance:
                rupulsion = np.array([0,0])
            else:
                rupulsion = K2/P_ri_distance
            F_repulsion = F_repulsion + rupulsion*(P_ri/P_ri_distance)
        F = F_end_att/P_rob2end_distance + F_repulsion
        robot_point = robot_point +  F
        robot_point = robot_point.astype(int)
        cv2.circle(map,tuple(robot_point), 20, color=(255,255, 0), thickness=-1)
        P_rob2end = end_point - robot_point #update position
        P_rob2end_distance = np.sqrt(np.sum(np.square(P_rob2end)))#update distance
        step_index += 1
        print("step:{},distance:{}".format(step_index,P_rob2end_distance))
        cv2.imshow("result",origin_map)
        cv2.waitKey(10)

    cv2.imshow("result",origin_map)
    cv2.waitKey(0)