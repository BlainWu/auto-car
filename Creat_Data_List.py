# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> Creat_Data_List
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/7/15 16:01
@Desc   ：
=================================================='''
import os
import argparse
import numpy as np
from utils import mkdir

path = "./"

parser = argparse.ArgumentParser()
parser.add_argument('--test_list',dest='test_list',default="test.list",type = str)
parser.add_argument('--train_list',dest = 'train_list',default='train.list',type = str)
parser.add_argument('--data_name',dest='data_name',default='data.npy',type = str)
parser.add_argument('--img_name',dest='img_name',default='hsv_img',type = str)
args = parser.parse_args()

test_list = args.test_list
train_list = args.train_list
data_name = args.data_name
img_name = args.img_name

def create_data_list(data_name, img_name):
    with open(test_list, 'w') as f:
        pass
    with open(train_list, 'w') as f:
        pass
    data = np.load(data_name)
    data = data.astype('float32')
    print('loading image：%s' % img_name)

    class_sum = 0

    img_paths = os.listdir(img_name)
    for img_path in img_paths:
        name_path = img_name + '/' + img_path
        index = int(img_path.split('.')[0])

        if not os.path.exists(data_root_path):
            os.makedirs(data_root_path)

        if class_sum % 10 == 0:
            with open( test_list, 'a') as f:
                f.write(name_path + "\t%d" % data[index] + "\n")
        else:
            with open(train_list, 'a') as f:
                f.write(name_path + "\t%d" % data[index] + "\n")
        class_sum += 1
    print('图像列表已生成')

if __name__ == '__main__':
    data_root_path = os.path.join(path,'data')
    mkdir(data_root_path)
    test_list = os.path.join(path,'data',test_list)
    train_list = os.path.join(path,'data',train_list)
    data_name = os.path.join(path,'data',data_name)
    img_name = os.path.join(path,'data',img_name)

    create_data_list(data_name, img_name)