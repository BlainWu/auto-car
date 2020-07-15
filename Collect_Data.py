# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> Collect_Data
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/7/13 20:05
@Desc   ：
=================================================='''
import os
import getopt
from sys import argv
import multiprocessing
import v4l2capture
from ctypes import *
import struct
from utils import *
import cv2
import numpy as np
import time

#os.path.split(os.path.realpath(__file__)) = ('path','Collect_Data.py')
path = os.path.split(os.path.realpath(__file__))[0] + "/.."

opts,args = getopt.getopt(argv[1:],'-hH',['vels=','output=','serial=','camera=','save_name='])

'''分配共享内存空间'''
camera = multiprocessing.Array("b",range(50))#camera
serial = multiprocessing.Array("b",range(50))#serial
output_data = multiprocessing.Array("b",range(50))#output_data
Speed = multiprocessing.Array("i",range(2))#speed and angle (int)

'''#参数的设定'''
camera.value = "/dev/video0"
output_data.value = "data"
Speed[0]  = 1560
Speed[1]  = 1500
serial.value = "/dev/ttyUSB0"
save_name="img"

'''传参的处理'''
for opt_name,opt_value in opts:
    if opt_name in ('-h','-H'):
        print("默认参数 --vels={0} --output={1} --serial={2} --camera={3}  --save_name={4}".format(Speed[0],
                                                                                                  output_data.value,
                                                                                                  serial.value,
                                                                                                  camera.value,
                                                                                                  save_name))
        exit()
    if opt_name in ('--vels'):
        Speed[0] = int(opt_value)

    if opt_name in ('--output'):
        output_data.value = opt_value

    if opt_name in ('--serial'):
        serial.value = opt_value

    if opt_name in ('--camera'):
        camera.value = opt_value
        print("camera.value=", camera.value)

    if opt_name in ('--save_name'):
        save_name = opt_value
        print("save_name=", save_name)

'''创建一个互斥锁，默认是没有上锁的 '''
lock = multiprocessing.Manager().Lock()


'''保存帧图片线程'''
def save_image_process(lock,n,status,start,Camera):
    global path
    global save_name

    mkdir(path+"/data")
    mkdir(path+"/data/"+save_name)

    #video = v4l2capture.Video_device("/dev/video0")
    video = v4l2capture.Video_device(Camera.value)
    video.set_format(1280, 720, fourcc='MJPG')
    video.create_buffers(1)
    video.queue_all_buffers()
    video.start()
    imgInd = 0 #帧序数
    print("Wait Start!")
    while(start.value == False):
        pass
    while status.value:#PS2 tr or tl control stop
        #print("status",status.value)
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
    #angledata = []
    file_write = open(path+"/data/"+ output_data.value+".txt","a")
    while run.value:
        while(n.value):
            lock.acquire()
            n.value = False
            lock.release()
            print("speed=",data[0],"  angle=",data[1])
            file_write.write(str(data[1]))
            file_write.write("\n")
            file_write.flush()


def control_car_process(data, status, run, start):
    max_num = 2100
    min_num = 700
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
                            if (button == "b" and button_states[button] == True):
                                start.value = True
                                print("START")
                                lib.send_cmd(speed_car, angle_car)
                            if ((button == "tr" and button_states[button] == True) or (
                                    button == "tl" and button_states[button] == True)):
                                # Stop
                                print("Stop")
                                status.value = False
                                data[0] = 1500
                                data[1] = 1500
                                lib.send_cmd(1500, 1500)
                            if (button == "tr2" and button_states[button] == True):
                                # speed up
                                speed1 = data[0] + 5
                                if speed1>=max_num:
                                    speed1 = max_num
                                speed_car = speed1
                                data[0] = speed_car
                                data[1] = angle_car
                                lib.send_cmd(speed_car, angle_car)
                            if (button == "tl2" and button_states[button] == True):
                                # speed down
                                speed1 = data[0] - 5
                                if speed1<=min_num:
                                    speed1 = min_num
                                speed_car = speed1
                                data[0] = speed_car
                                data[1] = angle_car
                                lib.send_cmd(speed_car, angle_car)
                    if (start.value == True):  # PS2 control speed and angle start
                        if type & 0x02:
                            axis = axis_map[number]
                            if axis:
                                if axis == "x":

                                    fvalue = value / 32767
                                    axis_states[axis] = fvalue
                                    angle1 = 1500 - (fvalue * min_num)
                                    if angle1 <= min_num:
                                        angle1 = min_num
                                    if angle1 >= max_num:
                                        angle1 = max_num
                                    angle_car = int(angle1)

                                    data[0] = speed_car
                                    data[1] = angle_car
                                    lib.send_cmd(speed_car, angle_car)

        except:
            print("car run error")
        finally:
            lib.send_cmd(1500, 1500)
            print("car run finally")

def txt_2_numpy():
    angledata = []
    data = []
    file = open(path+"/data/"+ output_data.value+".txt","r")
    for line in file.readlines():
        line = line.strip('\n')
        angledata.append(int(line))
    angle = np.array(angledata)
    np.save(path+"/data/"+ output_data.value+".npy", angle,False)
    file.close()


if __name__ == '__main__':

    Flag_save_data = multiprocessing.Value("i", False)  # New img save flag
    Status = multiprocessing.Value("i", True)  # Run or Stop for PS2
    START = multiprocessing.Value("i", False)  # START
    RUN = multiprocessing.Value("i", True)  # SHUTDOWN

    try:
        process_car = multiprocessing.Process(target=control_car_process,
                                              args=(Speed, Status, RUN, START))
        process_image = multiprocessing.Process(target=save_image_process,
                                                args=(lock, Flag_save_data, Status, START, camera,))
        process_data = multiprocessing.Process(target=save_data_process,
                                               args=(lock, Flag_save_data, Speed, RUN,))
        process_car.start()
        process_image.start()
        process_data.start()

        while (1):
            if (Status.value == 0):
                time.sleep(1)
                RUN.value = False
                print("STOP CAR")
                print("TXT to npy")
                txt_2_numpy()
                break
    except:
        RUN.value = False
        print("error")

    finally:
        RUN.value = False
        print("finally")