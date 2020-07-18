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

```Markdown
数据采集 Collect_Data.py
            ↓
数据集整合及预处理 Creat_Dataset.py
            ↓
训练集测试集分类 Creat_Data_List.py
            |
            |借助：cnn_model.py , Data_reader.py
            ↓
训练模型Line_Model_Trian.py
```

## 程序说明  
* __Creat_Dataset.py__  
```buildoutcfg
传参：  
    --origin_dir 原始数据目录，默认"./dataset_origin"  
    --target_dir 生成的最终数据文件夹，默认"./dataset"
功能：  
    默认搜索的子数据集名称为round{数字},进行数据校验，保存至目标文件夹内（不需要预先建文件夹，已有文件夹会被覆盖）。
```
* __Creat_Data_List.py__
```buildoutcfg
传参：
    --test_list     验证集列表名称，默认‘test.list’
    --train_list    训练集列表名称 ，默认'train.list'
    --data_name     数据文件名称 ，默认‘data.txt'
    --img_name      二值图文件夹名称，默认'hsv_img'
    --dataset_dir   以上文件的文件夹位置，默认'./dataset'
    --ratio         验证集占所有数据的百分比，默认20
功能：
    按照一定比率划分训练集和测试集，生成两个映射列表，列表结构为：{文件地址} {速度} {角度}
```
* __utils.py__
```buildoutcfg
通用工具函数：
    -mkdir(path)    检查是否有该文件夹，有则跳过，无则创建
    -getvalue()     获取xbox手柄数据
```
* __Data_reader.py__
```buildoutcfg
模型训练中的数据集读取的工具函数
```
可参考 API：[paddle.data_reader](https://www.paddlepaddle.org.cn/documentation/docs/zh/api_cn/data_cn/data_reader_cn/Reader_cn.html)

* __cnn_model.py__
```buildoutcfg
模型定义文件
```
* __Line_Model_Trian.py__
```buildoutcfg
车道线自动驾驶模型训练程序
模型保存在./model_line文件夹中
```
## 贡献者们  
吴沛林  
吴奕之  

## 问题日志
- [x] 采集数据的时候内存不够，导致程序崩溃，小车失灵。  
解决方法:  
使用nohup命令运行  `nohup python Collect_Data.py`

- [ ] Line_Model_Train.py训练loss在1W多降不下来。  
解决方法：  



## 有益改进
### 数据采集部分
>* 增加转弯角度挡位数量  
>通过增加转弯挡位，使得角度变化更多样，深度学习训练出的模型鲁棒性更高。

#参考资料
- [Paddle Lite 文档](https://paddle-lite.readthedocs.io/zh/latest/introduction/tech_highlights.html)
- [Linux nohup和&的功效](https://www.cnblogs.com/laoyeye/p/9346330.html)  
