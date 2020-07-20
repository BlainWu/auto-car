# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> Collect_Data
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/7/13 20:05
@Desc   ：
=================================================='''
import os
import select
import multiprocessing
import v4l2capture
from ctypes import *
import struct
from utils import mkdir,getvalue
import cv2
import numpy as np
import time
import argparse

'''保存帧图片线程'''
def save_image_process(lock,n,status,start,Camera):
    global path
    global save_name
    print("Start saving imgs! \n")
    mkdir(path+"/data")
    mkdir(path+"/data/"+save_name)

    video = v4l2capture.Video_device(Camera.value)
    video.set_format(424, 240, fourcc='MJPG')
    video.create_buffers(1)
    video.queue_all_buffers()
    video.start()
    imgInd = 0 #帧序数
    print("Wait Start!")
    while(start.value == False):
        pass
    while status.value:#PS2 tr or tl control stop

        select.select((video,), (), ())
        image_data = video.read_and_queue()
        frame = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imwrite(path+"/data/"+save_name+"/{}.jpg".format(imgInd), frame)
        print("imgInd=",imgInd)
        lock.acquire()
        n.value = True
        lock.release()
        imgInd+=1
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

'''保存速度和角度'''
def save_data_process(lock,n,data,run):
    file_write = open(path+"/data/"+ output_data.value+".txt","a")
    while run.value:
        while(n.value):
            print("NING!")
            lock.acquire()
            n.value = False
            lock.release()
            print("speed=",data[0],"  angle=",data[1])
            file_write.write("{0},{1}".format(data[0],data[1]))
            file_write.write("\n")
            file_write.flush()


def control_car_process(data, status, run, start):
    max_num = 2500
    min_num = 500
    turn_ratio = 626            #转弯率
    turn_ratio_1 = 626          #一档转弯
    turn_ratio_2 = 626          #二档转弯
    turn_ratio_3 = 583          #三档转弯
    turn_ratio_4 = 583          #四档转弯
    sharp_turn = 1000            #急转弯率
    speed_offset = 20           #速度偏移量

    while run.value:
        speed_car = data[0]
        angle_car = 1500
        fn = '/dev/input/js0'
        jsdev = open(fn, 'rb')
        car = serial.value
        axis_map, axis_states, button_map, button_states = getvalue()
        lib_path = path + "/lib" + "/libart_driver.so"
        so = cdll.LoadLibrary
        lib = so(lib_path)

        try:
            if (lib.art_racecar_init(38400, car.encode("utf-8")) < 0):
                raise
                pass
            lib.send_cmd(1500, 1500)
            while run.value:
                evbuf = jsdev.read(8)
                if evbuf:
                    time, value, type, number = struct.unpack('IhBB', evbuf)
                    if type & 0x01:
                        button = button_map[number]
                        if button:
                            button_states[button] = value
                            #启动键设置为tl
                            if (button == "tl" and button_states[button] == True):
                                start.value = True
                                print("START")
                                lib.send_cmd(speed_car, angle_car)
                            #停止按键
                            if ((button == "tr" and button_states[button] == True)):
                                # Stop
                                print("Stop")
                                status.value = False
                                data[0] = 1500
                                data[1] = 1500
                                lib.send_cmd(1500, 1500)
                            #切换一档转向
                            if (button == "a" and button_states[button] == True):
                                turn_ratio = turn_ratio_1
                            # 切换二档转向
                            if (button == "b" and button_states[button] == True):
                                turn_ratio = turn_ratio_2
                            # 切换三档转向
                            if (button == "x" and button_states[button] == True):
                                turn_ratio = turn_ratio_3
                            # 切换四档转向
                            if (button == "y" and button_states[button] == True):
                                turn_ratio = turn_ratio_4
                            # 速度增加
                            if (button == "y" and button_states[button] == True):
                                turn_ratio = turn_ratio_4
                            # 速度减小
                            if (button == "y" and button_states[button] == True):
                                turn_ratio = turn_ratio_4

                    if (start.value == True):  # PS2 control speed and angle start
                        if type & 0x02:
                            axis = axis_map[number]
                            if axis:
                                #左滑轮x轴
                                if axis == "x":
                                    fvalue = value / 32767
                                    axis_states[axis] = fvalue
                                    angle1 = 1500 - (fvalue * turn_ratio)
                                    if angle1 <= min_num:
                                        angle1 = min_num
                                    if angle1 >= max_num:
                                        angle1 = max_num
                                    angle_car = int(angle1)

                                    data[0] = speed_car
                                    data[1] = angle_car
                                    lib.send_cmd(speed_car, angle_car)
                                #右滑钮x轴，控制急转弯
                                if axis == "z":
                                    fvalue = value / 32767
                                    axis_states[axis] = fvalue
                                    angle1 = 1500 - (fvalue * sharp_turn)
                                    if angle1 <= min_num:
                                        angle1 = min_num
                                    if angle1 >= max_num:
                                        angle1 = max_num
                                    angle_car = int(angle1)

                                    data[0] = speed_car
                                    data[1] = angle_car
                                    lib.send_cmd(speed_car, angle_car)

                                if axis == "rz":#右滑钮上下控制加速减速
                                    fvalue = value/32767
                                    axis_states[axis] = fvalue
                                    speed1 = args.speed - (fvalue * speed_offset)
                                    speed_car = int(speed1)
                                    data[0] = speed_car
                                    data[1] = angle_car
                                    lib.send_cmd(speed_car, angle_car)
                                #左滑钮y轴为y，右滑钮y轴为rz


        except:
            print("car run error")
        finally:
            lib.send_cmd(1500, 1500)
            print("car run finally")


if __name__ == '__main__':
    path = os.path.split(os.path.realpath(__file__))[0] + "/.."
    '''
    传参的设定，其中最终生成文件的及别
    |output_data
    |--img_dir
    |--data.npy
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--vels', dest='speed', default=1620, type=int)
    parser.add_argument('--outputs', dest='output_data', default='data', type=str)
    parser.add_argument('--serial', dest='serial', default='/dev/ttyUSB0', type=str)
    parser.add_argument('--camera', dest='camera', default='/dev/video2', type=str)
    parser.add_argument('--img_dir_name', dest='img_dir', default='img', type=str)
    args = parser.parse_args()

    '''分配共享内存空间'''
    camera = multiprocessing.Array("b", range(50))  # camera
    serial = multiprocessing.Array("b", range(50))  # serial
    output_data = multiprocessing.Array("b", range(50))  # output_data
    Speed = multiprocessing.Array("i", range(2))  # speed and angle (int)

    '''参数的设定'''
    camera.value = args.camera
    output_data.value = args.output_data
    Speed[0] = int(args.speed)
    Speed[1] = 1500  # angle initialize
    serial.value = args.serial
    save_name = args.img_dir

    '''创建一个互斥锁，默认是没有上锁的 '''
    lock = multiprocessing.Manager().Lock()

    Flag_save_data = multiprocessing.Value("i", False)  # New img save flag
    Status = multiprocessing.Value("i", True)  # Run or Stop for PS2
    START = multiprocessing.Value("i", False)  # START
    RUN = multiprocessing.Value("i", True)  # SHUTDOWN

    try:
        process_car = multiprocessing.Process(target=control_car_process,args=(Speed, Status, RUN, START))
        process_image = multiprocessing.Process(target=save_image_process,args=(lock, Flag_save_data, Status, START, camera,))
        process_data = multiprocessing.Process(target=save_data_process,args=(lock, Flag_save_data, Speed, RUN,))
        process_car.start()
        process_image.start()
        process_data.start()

        while (1):
            if (Status.value == 0):
                time.sleep(1)
                RUN.value = False
                print("STOP CAR")
                break
    except:
        RUN.value = False
        print("error")

    finally:
        RUN.value = False
        print("finally")