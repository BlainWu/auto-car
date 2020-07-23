# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> opt_tools
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/7/22 19:57
@Desc   ：
=================================================='''
# 引用Paddlelite预测库
from paddlelite.lite import *
# 1. 创建opt实例
opt=Opt()
# 2. 指定输入模型地址
model_file = './model_line/model'
param_file = './model_line/params'
opt.set_model_file(model_file)
opt.set_param_file(param_file)
# 3. 指定转化类型： arm、x86、opencl、xpu、npu
opt.set_model_dir("./model_line")
opt.set_valid_places('arm')
# 4. 指定模型转化类型： naive_buffer、protobuf
opt.set_model_type("naive_buffer")
# 4. 输出模型地址
opt.set_optimize_out("./model_line/final_model")
# 5. 执行模型优化
opt.run()