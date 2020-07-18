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
from tqdm import tqdm
from utils import mkdir

def create_data_list(data_name, img_name,train_list,test_list):
    with open(test_list, 'w') as f:
        pass
    with open(train_list, 'w') as f:
        pass
    data = np.loadtxt(data_name)

    class_sum = 0

    img_paths = os.listdir(img_name)
    for img_path in tqdm(img_paths):
        name_path = os.path.join(img_name ,img_path).replace('\\','/')
        index = int(img_path.split('.')[0])

        if class_sum % 10 == 0:
            with open( test_list, 'a') as f:
                line = "{0}\t{1}\t{2}\n".format(name_path,data[index][0],data[index][1])
                f.write(line)
        else:
            with open(train_list, 'a') as f:
                line = "{0}\t{1}\t{2}\n".format(name_path, data[index][0], data[index][1])
                f.write(line)
        class_sum += 1
    print('图像列表已生成')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--test_list', dest='test_list', default="test.list", type=str)
    parser.add_argument('--train_list', dest='train_list', default='train.list', type=str)
    parser.add_argument('--data_name', dest='data_name', default='data.txt', type=str)
    parser.add_argument('--img_name', dest='img_name', default='hsv_img', type=str)
    parser.add_argument('--dataset_dir', dest="dataset_dir", default='./dataset', type=str)
    args = parser.parse_args()

    test_list = args.test_list
    train_list = args.train_list
    data_name = args.data_name
    img_name = args.img_name
    dataset_dir = args.dataset_dir

    test_list = os.path.join(dataset_dir,test_list)
    train_list = os.path.join(dataset_dir,train_list)
    data_name = os.path.join(dataset_dir,data_name)
    img_name = os.path.join(dataset_dir,img_name)

    #执行
    create_data_list(data_name, img_name,train_list,test_list)