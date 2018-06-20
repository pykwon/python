#http://hero4earth.com/blog/projects/2018/01/16/MNIST_Project/  참조함
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image
import numpy as np
import sys
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)

sess = tf.InteractiveSession()  #세션 열기

new_saver = tf.train.import_meta_graph('./mnist_cnn.ckpt.meta') #모델 불러오기(저장된 변수도 함께 불러오기)
new_saver.restore(sess, './mnist_cnn.ckpt')

#경로명은 mnist_cnn.ckpt.meta 파일에서 ctrl + f 키를 눌러 'model'로 검색하면 확인할 수 있다. dense도 마찬가지
X = sess.graph.get_tensor_by_name("model0/Placeholder_1:0")
logits = sess.graph.get_tensor_by_name("model0/dense_1/BiasAdd:0")
training = sess.graph.get_tensor_by_name("model0/Placeholder:0")

#MNIST 데이터 테스트 - Validation 이미지에서 임의의 숫자를 불러온다.
image_b = mnist.validation.images[np.random.randint(0, len(mnist.validation.images))]
plt.imshow(image_b.reshape([28, 28]), cmap='Greys')
plt.show()

#불러온 숫자를 모델에 넣어 제대로 숫자가 인식되는지 확인한다.
image_b = image_b.reshape([1, 784])
result = sess.run(logits, feed_dict={X:image_b, training:False})
print("MNIST predicted Number : ", sess.run(tf.argmax(result, 1)))

#이미지 파일 테스트 - 찍은 사진을 바로 넣어서 숫자를 인식해야 한다. 따라서, MNIST 이미지가 이닌 숫자를 적은 이미지를 불러와서 인식 시켜본다.
#한번에 확인하기
result_show = []
fig = plt.figure(figsize=(15,5))
for i in range(0, 9):
    im=Image.open("./number_{}.png".format(i+1))
    img = np.array(im.resize((28, 28), Image.ANTIALIAS).convert("L"))
    data = img.reshape([1, 784])
    data = 1-(data/255)
    ax = fig.add_subplot(1,10,i+1)
    ax.imshow(img.reshape(28, 28), cmap='gray', interpolation='nearest', aspect='auto')

    result = sess.run(logits, feed_dict={X:data, training:False})
    result_show.append(sess.run(tf.argmax(result, 1)))
print("MNIST predicted Number")
print(result_show)

#이미지 하나씩 확인
im=Image.open("./number_5.png")
img = np.array(im.resize((28, 28), Image.ANTIALIAS).convert("L"))
data = img.reshape([1, 784])
data = 1-(data/255)
plt.imshow(img.reshape(28, 28), cmap='gray', interpolation='nearest')
result = sess.run(logits, feed_dict={X:data, training:False})
print("MNIST predicted Number : ", sess.run(tf.argmax(result, 1)))

#이미지 명암 조절 후 숫자 인식
im=Image.open("./number_1.png")
im_light = Image.eval(im, lambda x:x+80)
plt.imshow(im_light)
img = np.array(im_light.resize((28, 28), Image.ANTIALIAS).convert("L"))
data = img.reshape([1, 784])
data = 1-(data/255)
plt.imshow(img.reshape(28, 28), cmap='gray', interpolation='nearest')
plt.show()

result = sess.run(logits, feed_dict={X:data, training:False})
print("MNIST predicted Number : ", sess.run(tf.argmax(result, 1)))
