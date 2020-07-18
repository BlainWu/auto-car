# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> Dataset_unite
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/7/18 9:42
@Desc   ：
=================================================='''
import os
from utils import mkdir
import shutil
import numpy as np
import argparse
from tqdm import tqdm

def unite_all(origin_dir,target_dir,img_name = 'img',data_name = 'data.txt'):
    """
    :param origin_dir: 多数据集的文件夹位置
    :param target_dir: 最终生成数据集位置
    :param img: 图片文件夹名称，和Collect_Data一致
    :param data: 数据文件名称，和Collect_Data一致
    """
    data_sets = os.listdir(origin_dir)
    data_sets.sort(key = lambda x:int(x.split("round")[1])) #
    target_dir_img = os.path.join(target_dir,img_name).replace("\\",'/')
    print(data_sets)
    pic_ind = 0
    total_data = []
    mkdir(target_dir)
    mkdir(target_dir_img)

    for dataset in data_sets:
        imgs_path = os.path.join(origin_dir,dataset,img_name)
        imgs_path = imgs_path.replace("\\","/")#在win系统下需要此行

        data_path = os.path.join(origin_dir,dataset,data_name)
        data_path = data_path.replace("\\","/")#在win系统下需要此行

        '''数据读取和校验'''
        origin_img_list = os.listdir(imgs_path)
        origin_img_list.sort(key= lambda x : int(x.split(".")[0]))
        img_num = len(origin_img_list)

        txt_f = np.loadtxt(data_path,dtype=str)
        data_num = len(txt_f)

        '''数据集叠加'''
        if img_num == data_num:
            #Img需要忽略第一张图片，txt需要忽略最后一行
            print("\n正在处理数据集{}".format(dataset))
            for index,value in enumerate(tqdm(origin_img_list[1:])):#跳过第0张图片
                #先复制到外面，重命名后，再转入最终的dataset/img
                img_path = os.path.join(imgs_path,value)#目前图片所处位置
                img_path = img_path.replace("\\", "/")  # 在win系统下需要此行
                det_path = os.path.join(target_dir_img,"{}.jpg".format(pic_ind))
                shutil.copyfile(img_path,det_path) #重命名并且复制到img文件夹中
                pic_ind += 1
            #文本添加
            for index,value in enumerate(txt_f[:-1]):#忽略最后一个
                speed = int(value.split(',')[0])
                angle = int(value.split(',')[1])
                buffer = [speed,angle]
                total_data.append(buffer)

        else:
            print("\n数据集{0}内容不匹配->图片数：{1}，数据行数：{2}".format(dataset,img_num,data_num))

    #保存txt
    np.savetxt(os.path.join(target_dir,data_name),total_data,fmt='%d')
    print("---------------------------------------------------")
    print('\n总共保存图片{0}张，数据{1}条'.format(pic_ind,len(total_data)))



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--origin_dir',dest = "origin_dir",default="./dataset_origin",type=str)
    parser.add_argument('--target_dir',dest = "target_dir",default="./dataset",type=str)
    args = parser.parse_args()
    origin_dir = args.origin_dir
    target_dir = args.target_dir

    unite_all(origin_dir,target_dir)

