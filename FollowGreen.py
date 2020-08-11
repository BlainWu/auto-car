import cv2
import time
import v4l2capture
import select
import numpy as np
from ctypes import *

def image_load(video):
    select.select((video,), (), ())
    image_data = video.read_and_queue()
    frame = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    return frame

def find_center(frame):
    lower_hsv = np.array([35, 43, 46])
    upper_hsv = np.array([43, 255, 255])
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    dst = cv2.erode(mask, kernel)

    M = cv2.moments(dst)
    if (M['m00'] > 1000):
        x = int(M['m10'] / M['m00'] + 0.5)
        s = 1
    else:
        x = 0
        s = 0

    return x,s

if __name__=='__main__':
    '''摄像头初始化'''
    video = v4l2capture.Video_device('/dev/video2')
    video.set_format(320, 240, fourcc='MJPG')
    video.create_buffers(1)
    video.queue_all_buffers()
    video.start()

    '''小车底层初始化'''
    lib_path = "../lib/libart_driver.so"
    so = cdll.LoadLibrary
    lib = so(lib_path)
    car = "/dev/ttyUSB0"
    lib.art_racecar_init(38400, car.encode("utf-8"))
    lib.send_cmd(1500, 1500)

    time.sleep(9)
    frame = image_load(video)
    time.sleep(1)

    while 1:
        frame=image_load(video)
        x,s=find_center(frame)
        if(s):
            a=1500-3*(x-160)
            lib.send_cmd(1540, a)
        else:
            lib.send_cmd(1500, 1500)