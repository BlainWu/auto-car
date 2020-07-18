# 南京师范大学智能车队
## 数据集
- 车道线数据集（官方提供）
>链接：https://pan.baidu.com/s/1SdQUHOFGpLmBxOBPGgV64w  
提取码：gycw

- 车道线数据集（自建）  

>链接：https://pan.baidu.com/s/1uLS9qDpNunyh8o83epzh-Q  
提取码：407t  

| 批次        | 基础速度   |  一级转弯  | 二级转弯 | 三级转弯 | 四级转弯 |
| --------   | -----:    | :----:   | :----:  |:----:  |:----:  |
| round1~10  | 1540   |   300   | 290     | 290    |  265   |

## 程序结构图  
- 行车线检测  

```
数据采集 Collect_Data.py
            ↓
数据集整合及预处理 Creat_Dataset.py
            ↓
训练集测试集分类 Creat_Data_List.py
            ↓
```

## 程序说明  
### Creat_Dataset.py  
```buildoutcfg
传参：  
    --origin_dir 原始数据目录，默认"./dataset_origin"  
    --target_dir 生成的最终数据文件夹，默认"./dataset"
功能：  
    默认搜索的子数据集名称为round{数字},进行数据校验，保存至目标文件夹内（不需要预先建文件夹，已有文件夹会被覆盖）。
```

## 贡献者们  
吴沛林  
吴奕之  

## 问题日志
* ~~采集数据的时候内存不够，导致程序崩溃，小车失灵~~  
解决方法:  
使用nohup命令运行  `nohup python Collect_Data.py`

参考： [Linux nohup和&的功效](https://www.cnblogs.com/laoyeye/p/9346330.html)

## 有益改进
### 数据采集部分
>* 增加转弯角度挡位数量  
>通过增加转弯挡位，使得角度变化更多样，深度学习训练出的模型鲁棒性更高。


