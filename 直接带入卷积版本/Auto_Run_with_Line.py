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
from paddlelite import *
from ctypes import *
import numpy as np
import cv2
from PIL import Image


def image_load(video):
    lower_hsv = np.array([26, 43, 46])
    upper_hsv = np.array([34, 255, 255])
    select.select((video,), (), ())
    image_data = video.read_and_queue()

    frame = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR) #（240，320，3）
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#（240，320，3）

    mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    img = Image.fromarray(mask) #(240,320)
    img = img.resize((127, 128), Image.ANTIALIAS)#(127,128)

    img = np.array(img).astype(np.float32)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)#(128,127,3)
    img = img.transpose((2, 0, 1)) 		#(3,128,127)
    img = img[(2, 1, 0), :, :] / 255.0      #(3,128,127)
    img = np.expand_dims(img, axis=0)  #(1, 3, 128, 127)
    
    return img


def load_model(model_dir):
    valid_places = (
        Place(TargetType.kFPGA, PrecisionType.kFP16, DataLayoutType.kNHWC),
        Place(TargetType.kHost, PrecisionType.kFloat),
        Place(TargetType.kARM, PrecisionType.kFloat)
    )

    config = CxxConfig()

    #config.set_model_file(model_dir + "/final_model.nb")

    config.set_model_file(model_dir + "/model")

    config.set_param_file(model_dir + "/params")

    config.set_valid_places(valid_places)

    predictor = CreatePaddlePredictor(config)
    return predictor


def predict(predictor, image,vel):

    img = image  # 输入图像数(1, 3, 128, 127)

    speed = [[(float(vel)/2200.0)] * 3*128] #转为（1，10）尺寸
    speed = np.array(speed)     #list转为arrary
    speed = speed.reshape(1,3,128,1)
    
    img_speed = np.concatenate((img, speed), axis=3)

    input = predictor.get_input(0)  # 接口参数名称0
    input.resize((1, 3, 128, 128))  # 设置接口图像大小
    input.set_data(img_speed)
    
    predictor.run()
    out = predictor.get_output(0)
    score = out.data()[0]
    print(out.data()[0])
    if score>2100:
        score = 2100
    elif score<600:
        score = 600
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', dest="model_dir", default='../model_line', type=str)
    parser.add_argument('--speed', dest='speed', default=1560, type=int)
    parser.add_argument('--camera', dest='camera', default="/dev/video2", type=str)
    args = parser.parse_args()
    camera = args.camera
    vels = args.speed
    model_dir = args.model_dir
    '''摄像头设置'''
    video = v4l2capture.Video_device(camera)
    video.set_format(424, 240, fourcc='MJPG')
    video.create_buffers(1)
    video.queue_all_buffers()
    video.start()
    '''paddle网络设置和模型读取'''
    predictor = load_model(model_dir)
    '''小车底层设置'''
    vel = int(vels)
    lib_path = "../lib/libart_driver.so"
    so = cdll.LoadLibrary
    lib = so(lib_path)
    car = "/dev/ttyUSB0"
    '''主程序'''
    try:
        if (lib.art_racecar_init(38400, car.encode("utf-8")) < 0):
            raise
            pass
        lib.send_cmd(1500, 1500)
        while 1:
            img = image_load(video)
            angle = predict(predictor, img, vel)
            a_shift = angle - 1500
            # if a_shift >0 :
            #	angle = 1500 + 1.5*a_shift
            # else:
            #    angle = 1500 + 1.7*a_shift
            a = int(angle)
            lib.send_cmd(vel, a)
            print("speed: %d, angle: %d" % (vel, a))

    except:
        print('error')
    finally:
        lib.send_cmd(1500, 1500)