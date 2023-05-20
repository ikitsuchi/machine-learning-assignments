import os
# os.environ['DEVICE_ID'] = '0'
import csv
import numpy as np
from pprint import pprint

import mindspore as ms
from mindspore import nn
# from mindspore import context
from mindspore import dataset
from mindspore.train.callback import LossMonitor

def create_dataset(data_path):
    # Todo 每个类的前五个样本信息

    # Todo 分别将Iris-setosa，Iris-versicolor，Iris-virginica对应为0，1，2三类

    X = np.array([[float(x) for x in s[:-1]] for s in data[:150]], np.float32)
    Y = np.array([label_map[s[-1]] for s in data[:150]], np.int32)

    # Todo Using random choice and split dataset into train set and validation set by 8:2.
    X_train, Y_train = X[train_idx], Y[train_idx]
    X_test, Y_test = X[test_idx], Y[test_idx]

    # Convert the training data to MindSpore Dataset.
    XY_train = list(zip(X_train, Y_train))
    ds_train = dataset.GeneratorDataset(XY_train, ['x', 'y'])
    ds_train = ds_train.shuffle(buffer_size=120).batch(32, drop_remainder=True)

    # Convert the test data to MindSpore Dataset.

    return ds_train, ds_test


def softmax_regression(ds_train, ds_test):
    net = nn.Dense(4, 3)

    # Todo 使用交叉熵损失计算

    # Todo 使用动量优化器优化参数，其中学习率设置为0.05，动量设置为0.9
    opt = nn.optim.Momentum(net.trainable_params(), learning_rate=, momentum=)

    model = ms.train.Model(net, loss, opt, metrics={'acc', 'loss'})
    model.train(25, ds_train, callbacks=[LossMonitor(per_print_times=ds_train.get_dataset_size())], dataset_sink_mode=False)
    metrics = model.eval(ds_test)
    print(metrics)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_url', default='iris.data', help='Location of data.')
    args, unknown = parser.parse_known_args()


    if args.data_url.startswith('s3'):
        # Todo:设置路径
        #
        import moxing
        moxing.file.copy_parallel(src_url=os.path.join(args.data_url, 'iris.data'), dst_url=data_path)
    else:
        data_path = os.path.abspath(args.data_url)

    softmax_regression(*create_dataset(data_path))