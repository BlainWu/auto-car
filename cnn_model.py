import paddle.fluid as fluid

def cnn_model(image,speed):
    conv1 = fluid.layers.conv2d(input=image, num_filters=24, filter_size=5, stride=2, act='relu')
    conv2 = fluid.layers.conv2d(input=conv1, num_filters=32, filter_size=5, stride=2, act='relu')
    conv3 = fluid.layers.conv2d(input=conv2, num_filters=64, filter_size=5, stride=2, act='relu')
    conv4 = fluid.layers.conv2d(input=conv3, num_filters=64, filter_size=3, stride=2, act='relu')
    conv5 = fluid.layers.conv2d(input=conv4, num_filters=64, filter_size=3, stride=1, act='relu')
    fc1 = fluid.layers.fc(input=conv5, size=100, act=None)
    drop_fc1 = fluid.layers.dropout(fc1, dropout_prob=0.1)
    fc2 = fluid.layers.fc(input=drop_fc1, size=50, act=None)
    drop_fc2 = fluid.layers.dropout(fc2, dropout_prob=0.1)
    #当前速度加入
    speed = fluid.layers.fill_constant(shape=[1], value=speed, dtype='int64')
    concat = fluid.layers.concat(input = [drop_fc2,speed],axis = -1)
    before_predict = fluid.layers.fc(input=concat, size=2, act=None)
    predict = fluid.layers.fc(input = before_predict,size = 1 ,act = None)
    return predict




