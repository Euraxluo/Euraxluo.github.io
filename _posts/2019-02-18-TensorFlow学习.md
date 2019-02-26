---
layout:     post                    # 使用的布局（不需要改）
title:      TensorFlow学习               # 标题 
subtitle:   TensorFlow基础学习                #副标题
date:       2019-01-18            # 时间
author:     Euraxluo                      # 作者
header-img: img/post-bg-github-cup.jpg  #这篇文章标题背景图片
catalog: true                 # 是否归档
tags:                               #标签
    - DL

---
# TensorFlow 学习与实战

TensorFlow是一个编程系统,使用图(graphs)来表示计算任务,图(graphs)中的节点称之为op(operation),一个op获得0个或者多个Tensor,执行计算,产生0个或者多个Tensor.Tensor看做是一个n维的数组或者列表.图必须在会话Session里被启动

##基本概念

- 使用图(graphs)来表示计算任务
- 在被称为会话(Session)的上下文(context)中执行图
- 使用张量(tensor)表示数据
- 通过变量(Vatria)维护状态
- 使用feed和fetch可以为任意的操作赋值或者从中获取数据
- 张量(Tensor)
  在TensorFlow中,张量的维度被描述为"阶",但是,张量的阶和矩阵的阶并不是同一个概念,张量的阶,是张量维度的一个数量的描述
  
```python
  x=3												#零阶张量:纯量
  v=[1.,2.,3.]										#一阶张量:向量
  t=[[1,2,3],[4,5,6]]								#二阶张量:矩阵
  m=[[[1],[2],[3]],[[4],[5],[6]],[[7],[8],[9]]]		#三阶张量:立方体
```

- 图(Graph)
	代表模型的数据流,由ops和tensor组成.其中op是操作,也就是节点,而tensor是数据流,也就是边
	算法会表示为计算图(computational graphs),也称之为数据流图.我们把计算图看作为一种有向图,张量就是通过各种操作在有向图中流动
- 会话(Session)
	在TensorFlow中,要想启动一个图的前提是要创建一个会话(Session),TensorFlow的所有对图的操作,都必须放在会话中进行

## 基础使用:

### op和Session

```python
import tensorflow as tf
```


```python
#创建两个常量op
c1 = tf.constant([[1,2]])
c2 = tf.constant([[2],[1]])
#创建一个矩阵乘法op
matmulop = tf.matmul(c1,c2)
print(matmulop)
```

    Tensor("MatMul:0", shape=(1, 1), dtype=int32)



```python
#定义一个会话,启动图
sess = tf.Session()
#调用sess的run方法来运行矩阵乘法op
#run(matmulop)触发了图中的3个op
result = sess.run(matmulop)
print(result)
sess.close()
```

    [[4]]



```python
#利用with省去这个麻烦
with tf.Session() as sess:
    #调用sess的run方法执行矩阵乘法op
    result = sess.run(matmulop)
    print(result)
```

    [[4]]


### 变量


```python
#添加一个变量op
x = tf.Variable([1,2])
#添加一个常量op
c = tf.constant([2,1])
#增加一个减法op
sub = tf.subtract(x,c)#x-c
#增加一个加法op
add = tf.add(x,sub)#x+(x-c)
#初始化所有变量
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print(sess.run(sub))
    print(sess.run(add))
    
```

    [-1  1]
    [0 3]


### 实现迭代自增
```python
#创建一个变量初始化为0
state = tf.Variable(0,name='cont')
#创建一个让state加1的op
new_state = tf.add(state,1)
#赋值op
update = tf.assign(state,new_state)#把new_state的值给到state
'''
tf.assign(ref, value, validate_shape=None, use_locking=None, name=None)
函数完成了将value赋值给ref的作用。
注意:
    1. ref 必须是tf.Variable创建的tensor，如果ref=tf.constant()会报错！
    2. shape（value）==shape（ref）
'''
#变量初始化op
init = tf.global_variables_initializer()
#使用Session运行这些op

with tf.Session() as sess:
    sess.run(init)
    for _ in range(6):
        print(sess.run(state))
        sess.run(update)
```

    0
    1
    2
    3
    4
    5


### Fetch 同时运行多个op,得到他们的结果


```python
def session_run(*args):
    #初始化所有变量
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        #调用sess的run方法执行矩阵乘法op
        result = sess.run(args)
        print(result,end=' ')

```

```python
with tf.Session() as sess:
    sess.run(init)
    result = sess.run([new_state,update])
    print('feed:',result)
    
with tf.Session() as sess:
    sess.run(init)
    print('not fetch',end=': [')
    print(sess.run(state),end=',')
    print(sess.run(update),end=']\n')
    
print('session_run',end=': ')
session_run(new_state,update)#达到了和fetch一样的效果
```

    feed: [1, 1]
    not fetch: [0,1]
    session_run: (1, 1) 

### Feed


```python
#创建两个32位浮点型的占位符op
placeholder1 = tf.placeholder(tf.float32)
placeholder2 = tf.placeholder(tf.float32)
feed_output = tf.multiply(placeholder1,placeholder2)

with tf.Session() as sess:
    result=sess.run(feed_output,feed_dict={placeholder1:[8.],placeholder2:[9.1]})
    print(result)
```

    [72.8]


### demo

```python
import tensorflow as tf
import numpy as np
#使用numpy生成特征和真实值
X = np.random.rand(100)
y = X*0.1 + 0.2

#创建两个op变量,用来构造一个线性模型
b = tf.Variable(0.)
w = tf.Variable(0.)
predic = w*X+b

#设置我们的代价函数(均方差)
loss = tf.reduce_mean(tf.square(y - predic))
#定义我们的优化器(梯度下降)
gd_optimizer = tf.train.GradientDescentOptimizer(0.2)#学习率
#创建一个op,用来最小化代价函数
train = gd_optimizer.minimize(loss)
#初始化变量
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    for step in range(200):
        sess.run(train)
        if step%20 == 0:
            print(step,sess.run([w,b]))
```

    0 [0.055094976, 0.10045407]
    20 [0.10424501, 0.19765908]
    40 [0.10235276, 0.1987026]
    60 [0.101303995, 0.19928093]
    80 [0.10072273, 0.19960146]
    100 [0.10040057, 0.19977911]
    120 [0.10022201, 0.19987758]
    140 [0.10012304, 0.19993214]
    160 [0.1000682, 0.19996239]
    180 [0.1000378, 0.19997916]

