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
    fc3 = fluid.layers.fc(input=drop_fc2,size = 25, act = None)
    concat = fluid.layers.concat(input=[fc3,speed], axis=1)
    #print(concat)
    #fluid.layers.Print(concat, message="Print concat:")
    predict = fluid.layers.fc(input = concat,size = 1 ,act = None)
    #fluid.layers.Print(predict, message="Print predict:")
    return predict

