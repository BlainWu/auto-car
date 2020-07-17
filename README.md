# 南京师范大学智能车队
## 数据集
- 车道线数据集（官方提供）
>链接：https://pan.baidu.com/s/1SdQUHOFGpLmBxOBPGgV64w  
提取码：gycw

## 程序结构图  
- 行车线检测  

```
数据采集 Collect_Data.py
            ↓
图像预处理 Img_pre_process.py
            ↓
训练集测试集分类 Creat_Data_List.py
            ↓
```


## 贡献者们  
吴沛林  
吴奕之  

## 问题日志
* ~~采集数据的时候内存不够，导致程序崩溃，小车失灵~~  
```解决方法
nohup python Collect_Data.py
```
参考： [Linux nohup和&的功效](https://www.cnblogs.com/laoyeye/p/9346330.html)