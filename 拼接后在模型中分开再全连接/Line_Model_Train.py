# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：codes -> Line_Model_Train
@IDE    ：PyCharm
@Author ：Blain Wu
@Date   ：2020/7/18 15:54
@Desc   ：
=================================================='''
import os
import argparse
import paddle
import paddle.fluid as fluid
import cnn_model
import Data_Reader
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--save_path',dest="save_path",default="./model_line")
parser.add_argument('--train_list',dest="train_list",default="train.list")
parser.add_argument('--test_list',dest='test_list',default="test.list")
parser.add_argument('--dataset_dir',dest='dataset_dir',default="./dataset")
parser.add_argument('--iters',dest='iters',default=50,type=int)

args = parser.parse_args()
dataset_dir = args.dataset_dir
test_list = args.test_list
train_list = args.train_list
iters = args.iters

save_path = args.save_path#模型保存文件夹
test_list_path = os.path.join(dataset_dir,test_list)
train_list_path = os.path.join(dataset_dir,train_list)

#数据尺寸设定
crop_size = 128
resize_size = 128

image_speed = fluid.layers.data(name='image_speed', shape=[3, crop_size, crop_size+1], dtype='float32')
label = fluid.layers.data(name='label', shape=[1], dtype='float32')
#模型初始化
model = cnn_model.cnn_model(image_speed)#增加速度因素
#loss设定
cost = fluid.layers.square_error_cost(input=model, label=label)
avg_cost = fluid.layers.mean(cost)

# 获取训练和测试程序
test_program = fluid.default_main_program().clone(for_test=True)
# 定义优化方法
optimizer = fluid.optimizer.AdamOptimizer(learning_rate=0.001)
opts = optimizer.minimize(avg_cost)

# 获取自定义数据
train_reader = paddle.batch(reader=Data_Reader.train_reader(train_list_path, crop_size, resize_size), batch_size=16)
test_reader = paddle.batch(reader=Data_Reader.test_reader(test_list_path, crop_size), batch_size=16)

# 定义执行器
#place = fluid.CPUPlace()  #CPU训练
place = fluid.CUDAPlace(0)
exe = fluid.Executor(place)

# 进行参数初始化
exe.run(fluid.default_startup_program())

# 定义输入数据维度
feeder = fluid.DataFeeder(place=place, feed_list=[image_speed,label])

# 训练
all_test_cost = []
for pass_id in range(iters):
    # 进行训练
    for batch_id, data in enumerate(train_reader()):
        train_cost = exe.run(program=fluid.default_main_program(),
                            feed=feeder.feed(data),
                            fetch_list=[avg_cost])
        # 每100个batch打印一次信息
        if batch_id % 100 == 0:
            print('iters:%d, Batch:%d, Cost:%0.5f' %
                  (pass_id, batch_id, train_cost[0]))

    # 进行测试
    test_costs = []

    for batch_id, data in enumerate(test_reader()):
        test_cost = exe.run(program=test_program,
                            feed=feeder.feed(data),
                            fetch_list=[avg_cost])
        test_costs.append(test_cost[0])
    # 求测试结果的平均值
    test_cost = (sum(test_costs) / len(test_costs))
    all_test_cost.append(test_cost)
    plt.plot(all_test_cost,marker = 'o') #画图
    plt.savefig('./Loss.jpg')
    print('Test:%d, Cost:%0.5f' % (pass_id, test_cost))

    # 保存预测模型
    if min(all_test_cost) >= test_cost:
        fluid.io.save_inference_model(save_path, feeded_var_names=[image_speed.name],
                                      main_program=test_program, target_vars=[model],
                                      executor=exe,params_filename='params',model_filename='model')
        print('Lowest test_cost: {}'.format(test_cost))
