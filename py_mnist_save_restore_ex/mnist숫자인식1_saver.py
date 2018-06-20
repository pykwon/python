#http://hero4earth.com/blog/projects/2018/01/16/MNIST_Project/

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# Hyper Prarameters
training_epochs = 15
batch_size = 100
learning_rate = 0.001

class Model:
    def __init__(self, sess, name):
        self.sess = sess
        self.name = name
        self._build_net()

    def _build_net(self):
        # 입력 받은 이름으로 변수 명을 설정한다.
        with tf.variable_scope(self.name):
            # Boolean Tensor 생성 for dropout
            # tf.layers.dropout( training= True/Fals) True/False에 따라서 학습인지 / 예측인지 선택하게 됨
            # default = False
            self.training = tf.placeholder(tf.bool)

            # 입력 그래프 생성
            self.X = tf.placeholder(tf.float32, [None, 784])
            # 28x28x1로 사이즈 변환
            X_img = tf.reshape(self.X, [-1, 28, 28, 1])
            self.Y = tf.placeholder(tf.float32, [None, 10])

            # Convolutional Layer1
            conv1 = tf.layers.conv2d(inputs=X_img, filters=32, kernel_size=[3,3], padding='SAME', activation=tf.nn.relu)
            # Pooling Layer1
            pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2,2], strides=2, padding="SAME" )
            # Dropout Layer1
            dropout1 = tf.layers.dropout(inputs=pool1, rate=0.7, training=self.training)

            # Convolutional Layer2
            conv2 = tf.layers.conv2d(inputs=dropout1, filters=64, kernel_size=[3,3], padding='SAME', activation=tf.nn.relu)
            # Pooling Layer2
            pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2,2],strides=2, padding='SAME' )
            # Dropout Layer2
            dropout2 = tf.layers.dropout(inputs=pool2, rate=0.7, training=self.training)

            # Convolutional Layer3
            conv3 = tf.layers.conv2d(inputs=dropout2, filters=128, kernel_size=[3, 3], padding='SAME', activation=tf.nn.relu)
            # Pooling Layer3
            pool3 = tf.layers.max_pooling2d(inputs=conv3, pool_size=[2,2], strides=2, padding='SAME')
            # Dropout Layer3
            dropout3 = tf.layers.dropout(inputs=pool3, rate=0.7, training=self.training)

            # Dense Layer4 with Relu
            flat = tf.reshape(dropout3, [-1, 128*4*4])
            dense4 = tf.layers.dense(inputs=flat, units=625, activation=tf.nn.relu)
            # Dropout layer4
            dropout4 = tf.layers.dropout(inputs=dense4, rate=0.5, training=self.training)

            # Dense Layer5 with Relu
            dense5 = tf.layers.dense(inputs=dropout4, units=1050, activation=tf.nn.relu)
            # Dropout Layer5
            dropout5 = tf.layers.dropout(inputs=dense5, rate=0.5, training=self.training)

            # Logits layer : Final FC Layer5 Shape = (?, 625) -> 10
            self.logits = tf.layers.dense(inputs=dropout5, units=10)

        # Cost Function
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.Y))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost)

        # Test Model
        correct_prediction = tf.equal(tf.argmax(self.logits, 1), tf.argmax(self.Y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    def train(self, x_data, y_data, training = False):
        return self.sess.run([self.cost, self.optimizer], feed_dict={self.X: x_data, self.Y:y_data, self.training:training})

    def predict(self, x_test, training = False):
        return self.sess.run(self.logits, feed_dict={self.X : x_test, self.training:training})

    def get_accuracy(self, x_test, y_test, training=False):
        return self.sess.run(self.accuracy, feed_dict={self.X: x_test, self.Y : y_test, self.training: training})
    
sess = tf.Session()

models = []
num_models = 5
for m in range(num_models):
    models.append(Model(sess, "model"+str(m)))

sess.run(tf.global_variables_initializer())

for epoch in range(training_epochs):
    avg_cost_list = np.zeros(len(models))
    total_batch = int(mnist.train.num_examples / batch_size)

    for i in range(total_batch):
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)

        # Train each model
        for m_idx, m in enumerate(models):
            c, _ = m.train(batch_xs, batch_ys)
            avg_cost_list[m_idx] += c / total_batch

    print('Epoch: ', '%04d' %(epoch + 1), 'Cost = ', avg_cost_list)
print('Training Finished')
    # Epoch:  0001 Cost =  [ 0.16365541  0.15805094  0.15816862  0.16383813  0.16415393]
    # Epoch:  0002 Cost =  [ 0.04496201  0.0429047   0.04390503  0.04575218  0.04640629]
    # Epoch:  0003 Cost =  [ 0.03376844  0.03230815  0.03093393  0.0311225   0.03254555]
    # ...
    # Epoch:  0014 Cost =  [ 0.00832863  0.00841471  0.01017939  0.00869219  0.01102423]
    # Epoch:  0015 Cost =  [ 0.00701145  0.00803191  0.00734568  0.0069111   0.00499205]
    # Training Finished

# 모델 테스트
test_size = len(mnist.test.labels)
predictions = np.zeros([test_size, 10])
best_models = []
for m_idx, m in enumerate(models):
    best_models.append(m.get_accuracy(mnist.test.images, mnist.test.labels))
    print(m_idx, 'Accuracy: ', best_models[m_idx] )
    p = m.predict(mnist.test.images)
    predictions += p
        # 0 Accuracy:  0.9925
        # 1 Accuracy:  0.9918
        # 2 Accuracy:  0.9923
        # 3 Accuracy:  0.9928
        # 4 Accuracy:  0.9901

ensemble_correct_prediction = tf.equal(tf.argmax(predictions, 1), tf.argmax(mnist.test.labels, 1))
ensemble_accuracy = tf.reduce_mean(tf.cast(ensemble_correct_prediction, tf.float32))
print('Ensemble accuracy:', sess.run(ensemble_accuracy))  #0.9954
#모델 저장 : 5개의 모델 중 가장 뛰어난 모델 선택 후 저장
best_model = models[np.argmax(best_models)]
saver = tf.train.Saver()
save_path = saver.save(best_model.sess, './mnist_cnn.ckpt')
print("Model saved to %s" % save_path)

