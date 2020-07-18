# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> Auto_Run_with_Line.py
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/7/18 19:15
@Desc   ：
=================================================='''
import os
import argparse
import select
import v4l2capture
import paddle.fluid as fluid
import numpy as np
import cv2
from PIL import Image

def image_load(video):
    lower_hsv = np.array([26, 43, 46])
    upper_hsv = np.array([34, 255, 255])
    select.select((video,), (), ())
    image_data = video.read_and_queue()

    frame = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    img = Image.fromarray(mask)
    img = img.resize((120, 120), Image.ANTIALIAS)
    img = np.array(img).astype(np.float32)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = img.transpose((2, 0, 1))
    img = img[(2, 1, 0), :, :] / 255.0
    img = np.expand_dims(img, axis=0)
    return img


if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path',dest = "model_path",default='./model_line/models',type=str)
    parser.add_argument('--speed',dest='speed',default=1540,type=int)
    parser.add_argument('--camera',dest='camera',default="/dev/video0",type=str)

    args = parser.parse_args()
    camera = args.camera
    vels = args.speed
    model_path =args.model_path

    '''摄像头设置'''
    video = v4l2capture.Video_device(camera)
    video.set_format(1280, 720, fourcc='MJPG')
    video.create_buffers(1)
    video.queue_all_buffers()
    video.start()

    '''paddle网络设置和模型读取'''
    place = fluid.CPUPlace()
    exe = fluid.Executor(place)
    exe.run(fluid.default_startup_program())
    [infer_program, feeded_var_names, target_var] = \
        fluid.io.load_inference_model(dirname=model_path, executor=exe)

    '''小车底层设置'''
    vel = int(vels)
    lib_path = "../lib/libart_driver.so"
    so = cdll.LoadLibrary
    lib = so(lib_path)
    car = "/dev/ttyUSB0"

    '''主程序'''
    try:
        while 1:
            img = image_load(video)
            result = exe.run(program=infer_program,feed={feeded_var_names[0]: img},fetch_list=target_var)
            angle = result[0][0][0]
            a = int(angle)
            lib.send_cmd(vel, a)
            print(cout)
            cout=cout+1
            print("angle: %d, throttle: %d" % (a, vel))

    except:
        print('error')
    finally:
        lib.send_cmd(1500, 1500)