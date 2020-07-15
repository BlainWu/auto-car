# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> Img_pro_process
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/7/15 18:23
@Desc   ：
=================================================='''
import os
import re
import argparse
import cv2
import numpy as np
from utils import mkdir

parser = argparse.ArgumentParser()
parser.add_argument('--img_dir',dest = 'img_dir',default='img',type = str)
parser.add_argument('--save_path',dest = 'save_path',default='hsv_img',type = str)
args = parser.parse_args()

img_dir = args.img_dir
save_path = args.save_path
#path = os.path.split(os.path.realpath(__file__))[0]
path = './data'

def img_extract(img_dir,save_path):
    img_names = os.listdir(img_dir)
    lower_hsv = np.array([156, 43, 46])
    upper_hsv = np.array([180, 255, 255])
    lower_hsv1 = np.array([0, 43, 46])
    upper_hsv1 = np.array([10, 255, 255])
    for img_name in img_names:
        print("正在处理：{}".format(img_name))
        img_path = os.path.join(img_dir,img_name)
        print(img_path)
        img = cv2.imread(img_path)
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        mask0 = cv2.inRange(hsv,lowerb=lower_hsv, upperb=upper_hsv)
        mask1 = cv2.inRange(hsv, lowerb=lower_hsv1, upperb=upper_hsv1)
        mask = mask0 + mask1
        ind = int(re.findall('.+(?=.jpg)', img_name)[0])
        new_name = str(ind) + '.jpg'
        cv2.imwrite(os.path.join(save_path,new_name),mask)

if __name__ == "__main__":
    img_dir = os.path.join(path,img_dir)
    save_path = os.path.join(path,save_path)

    #window下需要执行以下代码
    img_dir = img_dir.replace('\\','/')
    save_path = save_path.replace('\\', '/')

    mkdir(save_path)
    img_extract(img_dir,save_path)