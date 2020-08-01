# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> Data_reader
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/7/18 17:10
@Desc   ：
=================================================='''

import os
import random
from multiprocessing import cpu_count
import numpy as np
import paddle
from PIL import Image
import cv2


# 训练图片的预处理，最终输出统一大小的BGR图片和一个标签
def train_mapper(sample):
    img_path, vel, label, crop_size, resize_size = sample
    try:
        img = Image.open(img_path)
        # 统一图片大小
        img = img.resize((resize_size, resize_size), Image.ANTIALIAS)
        # 把图片转换成numpy值
        img = np.array(img).astype(np.float32)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        # 转换成CHW
        img = img.transpose((2, 0, 1))
        # 转换成BGR
        img = img[(2, 1, 0), :, :] / 255.0
        speed = [float(vel)] * 25
        return img, speed, label
    except:
        print("%s 该图片错误，请删除该图片并重新创建图像数据列表" % img_path)

# 获取训练的reader
def train_reader(train_list_path, crop_size, resize_size):
    def reader():
        with open(train_list_path, 'r') as f:
            lines = f.readlines()
            # 打乱图像列表
            np.random.shuffle(lines)
            # 开始获取每张图像和标签
            for line in lines:
                img, vel, label = line.split('\t')[0], line.split('\t')[1], line.split('\t')[2]  # 取第一列（图片地址）和第三列（角度）
                yield img, vel, label, crop_size, resize_size

    # 参数1：数据映射函数，reader是产生数据的reader，cpu_count()按照满cpu核读取，待读取队列大小
    return paddle.reader.xmap_readers(train_mapper, reader, cpu_count(), 102400)


# 测试图片的预处理,最终输出统一大小的BGR图片和一个标签
# 和训练mapper不同的是没有resize
def test_mapper(sample):
    img, vel, label, crop_size = sample
    img = Image.open(img)
    # 统一图像大小
    img = img.resize((crop_size, crop_size), Image.ANTIALIAS)
    # 转换成numpy值
    img = np.array(img).astype(np.float32)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # 转换成CHW
    img = img.transpose((2, 0, 1))
    # 转换成BGR
    img = img[(2, 1, 0), :, :] / 255.0
    # speed 1*25
    speed = [float(vel)] * 25
    return img, speed, label


# 测试的图片reader
def test_reader(test_list_path, crop_size):
    def reader():
        with open(test_list_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                img, vel, label = line.split('\t')[0], line.split('\t')[1], line.split('\t')[2]  # 取第一列（图片地址）和第三列（角度）
                yield img, vel, label, crop_size

    # 参数1：数据映射函数，reader是产生数据的reader，cpu_count()按照满cpu核读取，待读取队列大小
    return paddle.reader.xmap_readers(test_mapper, reader, cpu_count(), 1024)