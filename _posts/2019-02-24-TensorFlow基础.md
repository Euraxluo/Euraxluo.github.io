---
layout:   post          
title:   TensorFlow基础        
date:    2019-2-24      
author:   Euraxluo           
categories: NLP
tags:  读取 队列 张量
---
* TOC
{:toc}



### 计算密集型(tensorflow)
cpu计算
### io密集型(Django,Scrapy)

http请求



## 线性回归回顾

1. 准备好特征和lable

y = x*0.7+0.8

2.建模.随机初始化一个权重w,一个偏置b

y_predict = wx+b

3. 求损失函数

less化损失函数

(y-y_predict)^2/x.shape[0]

4.梯度下降优化损失函数,我们需要查阅tensorflowAPI,制定合适的eta



### 变量作用域

tf.variable_scope



### 让变量显示可观测

1. 收集变量

- tf.summary.scalar(name='',tensor) #收集单值变量,name是变量名,tensor为值



- tf.summary.histogram(name='',tensor) #收集高纬度的变量参数



- tf.summary.image(name='',tensor) #收集输入的图片张量能显示图片

2. 合并变量写入事件文件

- merged = tf.summary.merge_all()

- summary = sess.run(merged) #每次迭代都需要运行

- FileWriter.add_summary(summary,i) #表示第几次的值



### 模型的保存和加载

tf.train.Save(var_list = None,max_to_keep = 5)

>var_list:指定将要保存和还原的变量.他可以作为一个dict或一个列表传递

>max_to_keep:指示要保留的最近检查点文件的最大数量.创建新文件时,会删除较旧文件,默认为5,即保留最近的5个检查点文件

### 定义命令行参数

- 先定义有哪些参数需要在运行时指定

- 程序中获取定义命令行参数

- 使用时` python *.py --name=参数 [--DEFINE_name=参数]`





```python



import os

import tensorflow as tf

#定义参数的名字,默认值,说明

tf.app.flags.DEFINE_integer("max_step",100,"模型的训练步数")

tf.app.flags.DEFINE_string("model_dir","","模型文件的加载路径")

#定义获取命令行参数的名字

FLAGS = tf.app.flags.FLAGS

def mylg():

    g3 = tf.get_default_graph()

    with tf.variable_scope("data"):

        # 准备特征和lablel

        x = tf.random_normal([1000,1],mean=1.75,stddev=0.5,name="X_data")

        y = tf.matmul(x,[[0.7]]) + 0.8#举证相乘必须是二维的

    with tf.variable_scope("model"):

        # 设置模型

        w = tf.Variable(tf.random_normal([1,1],mean=0.0,stddev=1.0),name="w",trainable=True)

        #trainable设置这个变量是否变化

        b = tf.Variable(0.5,name='b')

        y_predict = tf.matmul(x,w) + b

    with tf.variable_scope("loss"):

        #写损失函数

        loss = tf.reduce_mean(tf.square(y-y_predict))

    with tf.variable_scope("train"):

        train = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

    #1. 收集tensor

    tf.summary.scalar("loss",loss)

    tf.summary.histogram('weight',w)

    tf.summary.histogram('bias',b)

    #2. 合并变量

    merged = tf.summary.merge_all()

    #初始化变量

    init = tf.global_variables_initializer()

    #定义一个保存模型的实例

    saver = tf.train.Saver()

    with tf.Session(graph=g3) as sess:

        sess.run(init)

        filewriter = tf.summary.FileWriter('/home/python/jupyter/TensorFlow',graph=g3)

        #加载模型

        if os.path.exists(FLAGS.model_dir+"/checkpoint"):

            saver.restore(sess,FLAGS.model_dir+"/model")

            

        for i in range(FLAGS.max_step):

            sess.run(train)

            summary = sess.run(merged)

            filewriter.add_summary(summary,i) 

            if i%20==0:

                print("第%d次优化的参数权重为%f,偏置为%f"%(i,w.eval(),b.eval()))

            if i%200==0: 

                saver.save(sess,FLAGS.model_dir+"/model")#保存模型

mylg()

```



## graph图

创建一张图包含了一组op和tensor,上下文环境

没创建一个图就会包含一个内存地址

### 一个Session运行一张图

tf.InteractiveSession()#开启Session一个上下文环境





```python

g = tf.Graph()

with g.as_default():

    c = tf.constant(11.0)

a = tf.constant(5.0)

b = tf.constant(6.0)

sum1 = tf.add(a,b)

mul = tf.multiply(a,b)



g2 = tf.get_default_graph()

#config=tf.ConfigProto(log_device_placement=True) 可以查看运行在那些cpu

with tf.Session(graph=g2,config=tf.ConfigProto(log_device_placement=True)) as sess:

    print(sess.run(sum1))## run()方法

    print(sess.run([a,b]))

    print(sum1.eval())

```



### 重载

默认会把运算符重载为op







```python

d = tf.constant(1.0)

e = 11.0

sum2 = d+e

with tf.Session() as sess:

    print(sess.run(sum2))## run()方法

```



### 实时的提供数据进行训练

在程序执行时,不确定输入的shape

placeholder #占位符





```python

plt = tf.placeholder(tf.float32,[None,3])#样本数不固定,三列

print(plt)#打印这个张量

#使用

with tf.Session() as sess:

    print(sess.run(plt,feed_dict={plt:[[1,2,3],[4,5,6]]}))## run()方法

```



## 张量的动态形状和静态形状



Numpy:把原来的数据通过`reshape`直接改变

- 静态形状：

创建一个张量，初始化状态的形状：



    tf.Tensor.get_shape:获取静态形状

  

    tf.Tensor.set_shape():更新Tensor对象的静态形状

- 动态形状:

一种描述原始张量在执行过程中的一种形状(动态变化)



    tf.reshape:创建一个具有不同形状的新张量







```python

plt.set_shape([3,3])#把plt的shape从[?,3]变成[3,3]

```





```python

with tf.Session() as sess:

    print(sess.run(plt,feed_dict={plt:[[1,2,3],[4,5,6],[7,8,9]]}))## run()方法

```



## 变量



变量也是一种op,是一种特殊的张量,能够进行持久化,他的值就是张量,默认被训练





```python

var = tf.Variable(tf.random_normal([2,3],mean=0.0,stddev=1.0))#均值为0,标准差为1

init = tf.global_variables_initializer()

with tf.Session() as sess:

    sess.run(init)

    print(sess.run(var))

```



## Tensorboard



- 数据序列化->events文件



TensorBoard通过读取TensorFlow的事件文件来运行

- 生成文件:



tf.summary.FileWriter('dir-path',graph=g?)

返回一个filewriter

- 开启:



tensorboard --logdir='/dir-path'





```python

d = tf.constant(1.0)

e = tf.constant(1.0)

sum2 = d+e

var = tf.Variable(tf.random_normal([2,3],mean=0.0,stddev=1.0))#均值为0,标准差为1

init = tf.global_variables_initializer()

with tf.Session() as sess:

    sess.run(init)

    print(sess.run(var))

    print(sess.run(sum2))## run()方法

    filewriter = tf.summary.FileWriter('/home/python/jupyter/TensorFlow',graph=sess.graph)

```

## 文件读取



### 队列与队列管理器



1. 在训练样本的时候,希望数据有序读取

>tf.FIFOQueue(capacity,dtypes,name='fifo_queue') 先进先出队列,按顺序出队列   

   - capacity:整数,可能存储在此队列中的元素数量的上限

   - dtypes:DType对象列表,长度dtypes必须等于每个队列元素中的张量数,dtype的元素形状,决定了后面进队元素的形状

>tf.RandomShuffleQueue 随机出队列



### 异步读取,队列管理器

>tf.train.QueueRunner(queue,enqueue_ops=None)创建一个QueueRunner





### 线程协调器,实现一个简单的机制来协调一组线程的终止

>tf.train.Coordinator()

   - request_stop()

   - should_stop()检查是否要求停止

   - join(threads = None,stop_grace_period_secs=120)



### 读取文件的流程

#### 1.构建文件队列

将输出字符串到管道队列中

>tf.train.string_input_producer(string_tensor,shuffle = True)

   - string_tensor  含有文件名的1阶张量

   - num_epochs 过几遍数据,默认无线过数据

   - return:具有输出字符串的队列





#### 2.构造文件阅读器,读取队列内容(都是用read(file_queue)这个方法,从文件中读取指定数量内容)

>tf.TextLineReader(阅读文本文件csv,默认按行读取)



>tf.FixedLengthRecordReader(record_bytes):读取每个记录是固定数量的二进制文件

   - record_bytes:整形,指定每次读取的字节数



>tf.TFRecordReader: 读取TFRecords文件



#### 3.读取每个队列文件的每一个样本

>tf.decode_csv(records,record_defaults=None,field_delim=None,name=None)

   - 将csv转换为张量,与tf.TextLineReader搭配使用

   - records:tensor型字符串,每个字符串是csv中的记录行

   - field_delim:默认分隔符","

   - record_defauts:参数决定所得每一列张量的类型,并设置一个值,在输入字符串中缺少使用默认值



>tf.decode_raw(bytes,out_type,little_endian=None,name=None)

 

 将字节转换为一个数字向量表示,字节为一字符类型的张量,二进制读取为uint8



#### 4.批处理

`tf.train.batch([sentence],batch_size=30,num_threads=1,capacity=30)`

    

```python

import tensorflow as tf

import os

def myqueu():

    # 1. 定义队列

    Q = tf.FIFOQueue(1000,tf.float32)

    # 2. 定义子线程操作

    var  = tf.Variable(0.0)

    data = tf.assign_add(var,tf.constant(1.0))

    enq = Q.enqueue(data)

    # 3. 定义队列管理器,指定线程数

    qr = tf.train.QueueRunner(Q,enqueue_ops=[enq]*4)

    #初始化变量

    init = tf.global_variables_initializer()

    with tf.Session() as sess:

        sess.run(init)

        #开启线程协调管理器

        coord = tf.train.Coordinator()

        threads = qr.create_threads(sess,coord=coord,start=True)

        for i in range(300):

            print(sess.run(Q.dequeue()))

        coord.request_stop()

        coord.join(threads)



def convread(filelist):

    # 1.构造队列

    file_queue = tf.train.string_input_producer(filelist)

    # 2.构造阅读器

    reader = tf.TextLineReader()

    key, value = reader.read(file_queue)

    # 3.对每一行解码

    records = [[" "],]#以字符串读取每一行,默认值是" "

    sentence = tf.decode_csv(value,record_defaults=records)

    #开启批处理

    sentence_batch = tf.train.batch([sentence],batch_size=30,num_threads=1,capacity=30)

    return sentence#返回句子



if __name__ == "__main__":

    #构造文件列表

    file_name = os.listdir("../data/")

    filelist = [os.path.join("../data/",file) for file in file_name]

    #读取文件

    sentence_batch = convread(filelist)

    #开启会话

    with tf.Session() as sess:

        #定义一个线程协调器

        coord = tf.train.Coordinator()

        #开启读取文件的线程

        threads = tf.train.start_queue_runners(sess,coord=coord)

        print(sess.run(sentence_batch))

        #回收子线程

        coord.request_stop()

        coord.join(threads)

```

