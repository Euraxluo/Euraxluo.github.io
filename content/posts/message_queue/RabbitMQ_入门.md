+++
title = "RabbitMQ-入门"
date = 2018-10-22
description = "RabbitMQ 入门 - 以python为例"
featured = false
categories = [
  "message queue"
]
tags = [
  "RabbitMQ",
  "Python"
]
series = [
  "message queue"
]
images = [
]
+++


## RbbitMQ 学习笔记

AMQP协议组成部分
1. Module layer：协议最高层，定义了供客户端使用的命令
2. Session layer：中间层，负责将客户端的命令发送给服务端，再将服务端的命令返回给客户端，为客户端和服务端之间提供可靠的通信
3. Transport layer：最底层，包括二进制流的传输，帧处理，信道复用，错误检测

### 生产者使用AMQP的过程
1. Producter
- 建立连接
- 开启通道
- 发送消息
- 释放资源
 ### 消费者使用AMQP的过程
 1. Consumer
 - 建立连接
 - 开启通道
 - 准备接受消息
 - 发送确认
 - 释放资源

 ### AMQP命令和javaAPI的对应
 Connection.Start : factory.newConnection 新建连接
 Connection.close : connection.close 关闭连接
 Channel.Open : channel.openChannel 开启信道
 Channel.close : channel.close 关闭信道
 Exchange.Declare : channel.exchangeDeclare 声明交换器
 Exchange.Delete : channel.exchangeDelete删除交换器
 Exchange.Bind : channel.exchangeBind 交换器和交换器绑定
 Exchange.Unbind : channel.exchangeUnbind 交换器和交换器解绑
Queue.Declare : channel.queueDeclare 声明队列
Queue.Bind : channel.queueBind 队列和交换机绑定
Queue.Purge : channel.queuePurge 清除队列
Queue.Delete : channel.queueDelect 删除队列
Queue.Unbind : channel.queueUnbind 队列和交换机解绑
Basic.Qos : channel.basicQos 设置未被确认消费的个数
Basic.Consume : channel.basicConsume 消费消息（推）
Basic.Cancel : channel.basicCancel 取消
Basic.Publish : channel.basicPublish 发送消息
Basic.Get : channel.basicGet 消费消息（拉）
Basic.Ack : channel.basicAck 确认消息
Basic.Reject : channel.basicReject 拒绝单条消息
Basic.Recover : channel.basicRecover 请求Broker重新发送未被确认的消息
Tx.Select : channel.txSelect 事务开启
Tx.Commit : channel.txCommit 事务提交
Tx.Rollback : channel.txRollback,事务回滚

![rabbitmq_arc1.jpg](https://euraxluo.github.io/images/picgo/rabbitmq_arc1.jpg)

在rabbitMQ的使用中分为

**Producer（生产者）、Exchange、Binding、Queue、Consumer（消费者）** 

其中在消息路由的过程中还涉及以下关系

**Routing Key、Binding Key、Exchange Type** 的关系

![rabbitmq_arc2.png](https://euraxluo.github.io/images/picgo/rabbitmq_arc2.png)

### 客户端连接过程:
1. 客户端连接到消息服务器，打开一个channel
2. 客户端声明一个exchange，并设置相关属性
3. 客户端声明一个queue，并设置相关属性
4. 客户端使用routing key，在exchange和queue之间建立好绑定关系
5. 客户端投递消息到exchange
6. 客户端从指定的queue中消费消息

| Item        | Comment                                                      |
| :---------- | :----------------------------------------------------------- |
| Exchange    | 消息交换机，它指定消息按什么规则，路由到哪个队列             |
| Queue       | 消息队列，每个消息都会被投入到一个或多个队列                 |
| Binding     | 绑定，它的作用就是把exchange和queue按照路由规则绑定起来      |
| Routing Key | 路由关键字，exchange根据这个关键字进行消息投递               |
| Vhost       | 虚拟主机，可以开设多个vhost，用作不同用户的权限分离          |
| Producer    | 消息生产者，就是投递消息的程序                               |
| Consumer    | 消息消费者，就是接受消息的程序                               |
| Channel     | 消息通道，在客户端的每个连接里，可建立多个channel，每个channel代表一个会话任务 |

#channel 会话通道，与客户端通过socket建立长连

### 发送消息过程：
1. 生产者和Broker建立TCP链接
2. 生产者和Broker建立通道
3. 生产者通过通道将消息发送到Broker，有Exchange将消息进行转发
4. Exchange将消息转发指定的Queue

### 接受消息过程：
1. 消费者和Broker建立TCP链接
2. 消费者和Broker建立通道
3. 消费者监听指定的Queue
4. 当有消息到达Queue时，Broker默认将消息推送给消费者
5. 消费者接收到消息
6. ack回复

#### Channel信道：
Channel是创建于连接对象之上的虚拟连接，每一个信道都分配一个唯一Id，由信道完成生产者或消费者和Broker之间的连接
##### 为什么需要channel
为什么有TCP连接对象，还需要Channel信道，那是因为每一次TCP的创建都非常消耗资源，RabbitMQ采用一个NIO机制（io多路复用）进行通信连接达到减少性能消耗的目的

## RabbitMQ 工作模式
1. Work queuees工作队列
2. Publish、Subscribe 发布订阅模式
3. Routing 路由模式
4. Topics 通配符模式
5. Header Hearder转发器
6. RPC远程调用模式

### Work queues
work queues 和hello world程序相比，多了一个消费者
也就是多个消费者共同消费同一个队列中的消息
#### 特点：
1. 一个生产者讲消息发送给一个队列
2. 多个消费者共同监听一个队列的消息
3. 消息不能被重复消费
4.rabbit 采用轮询的方式将消息平均发送给消费者

### Publish/Subscribe
#### 特点：
1. 一个生产者将消息发给交换机
2. 与交换机绑定得有多个queue，每个消费者监听自己的队列
3. 生产者讲消息发送给交换机，由交换机讲消息转发给绑定词交换机的每个队列，每个绑定交换机的队列都将收到该消息
4. 如果消息发给没有绑定队列的交换机上，消息将会丢失
#### 与work queue 模式的区别
1. publish、subscribe可以定义一个交换机绑定多个队列，一个消息可以发送给多个队列
2. work queues无需定义交换机，一个消息只能发送给一个队列
3. pub/sub比work queues的功能更强大，pub/sub也可以将多个消费者监听同一个队列实现work queues的功能
4. 交换机的类型为fanout

#### 使用场景:
一个消息、任务。需要同时被多个客户端获取/执行


### Routing
#### 特点：
1. 每个消费者监听自己的队列，并且设置routingkey，可以设置多个routingkey。我看范例里面是举得log日志的例子。一个队列监听所有级别（error，info）的routingkey。另一个队列可能是告警信息业务绑定的队列，他会设置（error）的routingkey
2. 生产者将消息发送给交换机，发送消息时需要指定routingkey，由交换机根据routingkey来转发消息到指定的队列
3. 生产者将消息发给交换机，发送消息时需要指定routingkey的值，交换机来判断该routingkey的值和哪个队列的routingkey相等，如果相等则将该消息转发给该队列
#### Routing与pub/sub的区别
1. Pub/Sub模式在绑定交换机时不需要指定routingkey，交换机会将消息同时发送给绑定自己的多个队列。
2. Routing模式要求队列在绑定交换机时指定routingkey，会在exchange那里做一层direct，有选择的将消息发送到，rroutingkey对应的队列中去
3. 交换机类型为direct

### Topics
#### 特点：
1. 每个消费者监听自己的队列，并且设置带通配符的routingkey
2. 符号：① #，匹配一个或者多个词，info.# 可以匹配info.s,info.a。②*只能匹配一个词
3. 一个交换机可以绑定等多个队列，每个队列需要设置一个或者多个带通配符的routingkey。
4. 生产者将消息发送给交换机，交换机根据routingkey的值来匹配，匹配时采用通配符匹配


#### 与Routing的区别
1. Routing是完全匹配，Topics是通配符匹配
2. 交换机类型为topic



### Header
header模式与routing模式不同的是，header模式取消routingkey，使用header中的key、value 匹配队列



### RPC
RPC即客户端远程调用服务端的犯法，使用MQ可以实现RPC的远程异步调用，基于Direct交换机实现
流程如下：
1. 客户端既是消费者也是生产者，向RPC请求队列发送RPC调用信息，同时会监听RPC响应队列
2. 服务端监听RPC请求队列的消息，收到消息后执行服务端的方法，得到方法返回的结果
3. 服务端讲RPC方法的结果发送到RPC响应队列

#### 特点：
可以通过消息队列实现双方服务的异步通信


## python 例程：
```python
"""
整体实现基于同步模式：

- BlockingConnection 阻塞/连接

> 该适配器虽然是同步阻塞适配器，但是依然支持异步RPC特性
> 组成： BlockingConnection 和 BlockingChannel
> 异步适配器
> 1.Select Connection Adapter 没有第三方依赖包的异步模式
> 2.Tornado Connection Adapter 基于Tornado 的异步IO请求模式
> 3.Twisted Connection Adapter 基于Twisted’的异步IO请求模式
"""
# coding:utf8
from common.config.dev import RABBITMQ_HOST,RABBITMQ_PASS,RABBITMQ_PORT,RABBITMQ_USER
import uuid
import pika
import json
from common.utils.logger import Logger
from common.utils.helpers import JsonObject
logger = Logger()



class RabbitMQ():
    def __init__(self,v_host="/",host=RABBITMQ_HOST, port=RABBITMQ_PORT, user=RABBITMQ_USER, password=RABBITMQ_PASS):
        """
        RabbitMQ 封装
        :param v_host: 虚拟机host
        :param host: RabbitMQ 服务host
        :param port: RabbitMQ服务端口
        :param user: RabbitMq 用户认证-用户名
        :param password: RabbitMq 用户认证-密码
        """
        self._v_host = v_host
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self.exchange_type = ""
        self.exchange = ""
        self.responses = {} #rpc客户端收到的所有结果
        self.do_connection()

    def do_connection(self):
        """
        进行了连接这个动作
        :return:
        """
        try:
            self.connection = self.blocking_connection(host=self._host,
                                     port=self._port,
                                     user=self._user,
                                     password=self._password,
                                    v_host=self._v_host)
            self.channel = self.connection.channel()
        except ValueError as e:
            print(e)

    def blocking_connection(self,
                            host=RABBITMQ_HOST,
                            port=RABBITMQ_PORT,
                            user=RABBITMQ_USER,
                            password=RABBITMQ_PASS,
                            v_host="/"):
        """
        Connection Adapters 连接适配器
        pika.PlainCredentials(
        ：param str用户名：用于验证的用户名,默认为guest
        ：param str password：用于验证的密码，默认为guest
        ：param bool delete_on_connect：连接完成后，凭证将不会存储在内存中。删除连接凭据。
        )
        pika.ConnectionParameters(
        host=host
        port=port,
        virtual_host=要使用的rabbitmq虚拟主机, 一个mq服务可以设置多个虚拟机，每个虚拟机就相当于一个独立的mq
        credentials=PlainCredentials身份验证凭证,
        channel_max=允许的最大channel通道数,
        frame_max=AMQP frame的最大字节大小,
        heartbeat=AMQP callable 心跳超时协商,
        ssl_options=pika.SSLOptions`实例,
        connection_attempts=最大重试尝试次数,
        retry_delay=下一次等待的时间，以秒为单位,
        socket_timeout=套接字连接超时时间,
        stack_timeout=完整协议栈启动超时时间，应该高于socket_timeout,
        locale=设置语言环境值,
        blocked_connection_timeout=如果非负，阻止链接保持；如果
        tcp_options=为套接字设置的TCP选项的字典
        ）
        """
        credential_params = pika.PlainCredentials(user, password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host, port, v_host, credential_params)
        )
        return connection

    def model(self,exchange,model="fanout"):
        """
        可以选择，自己想构建的模式，
        然后该函数会把需要设置的交换机参数帮你设置好
        :param model:
            model_exchangeType = {
                "fanout":"fanout",
                "worker":"fanout",
                "routing":"direct",
                "direct":"direct",
                "route":"direct",
                "topic":"topic",
                "rpc":"direct"#默认为路由模式
            }
        :return:
        """
        model_exchangeType = {
            "fanout": "fanout",
            "worker": "fanout",
            "routing": "direct",
            "direct": "direct",
            "route": "direct",
            "topic": "topic",
            "rpc": "direct"
        }
        self.exchange_type = model_exchangeType[model]
        self.exchange = exchange
        return self

    def producer_init(self,exchange=None,exchange_type=None):
        """
        生产者初始化代码
        :param v_host: 默认为/，默认虚拟机
        :param exchange:交换机名字，默认为“”
        :param exchange_type:交换机类型，默认为“fanout”,广播模式
        :return: channel
        """
        try:
            self.exchange = exchange if exchange else self.exchange
            self.exchange_type = exchange_type if exchange_type else self.exchange_type
            self.check_Value(self.exchange, self.exchange_type, self.channel)
            """默认这里connection 和 channel都有了，没有raise 异常"""
            # 声明交换机
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)
            return self
        except Exception as e:
            print(e)

    def consumer_init(self,exchange=None,exchange_type=None,queue="",routings=[""]):
        """
        消费者初始化代码
        :param exchange: 交换机名字，默认为
        :param exchange_type: 交换机类型，默认为“fanout”，广播模式
        :param queue: 队列名，默认为“”，为随机队列
        :param routings: 路由key列表，默认为[""],会将这些路由key都绑定到该队列上
        :return: channel
        """
        try:
            self.exchange = exchange if exchange else self.exchange
            self.exchange_type = exchange_type if exchange_type else self.exchange_type
            self.check_Value(self.exchange,self.exchange_type,self.channel)
            """默认这里connection 和 channel都有了，没有raise 异常"""
            # 声明交换机
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)
            # 随机生成临时队列,绑定到交换机.当然也可以指定出多条名字固定的队列，exclusive设置为True当接收端退出时，自动销毁队列
            self.queue = self.channel.queue_declare(queue=queue, auto_delete=True)
            self.qname = self.queue.method.queue
            # 将这个随机队列绑定到交换机上，并设置路由键
            for routing in routings:
                self.channel.queue_bind(exchange=self.exchange,queue=self.qname,routing_key=routing)
            return self
        except Exception as e:
            print(e)

    def rpc_client_init(self,routings:list,exchange=None,exchange_type=None,queue="",auto_ack=True):
        """
        rpc 模型
        1. 先定义消费者
        2. 再定义生产者
        :param exchange: 客户端接受调用结果的交换机
        :param exchange_type: 客户端接受调用结果的交换机的类型
        :param queue: 客户端接受调用结果的队列，当为空时，该队列名字随机
        :param routings: 客户端接受调用结果的队列路由键,必选参数，客户端接受调用结果的队列的路由
        :param auto_ack: 是否自动确认
        :return:
        """
        try:
            self.consumer_init(exchange=exchange, exchange_type=exchange_type, queue=queue, routings=routings)
            self.channel.basic_consume(queue=self.qname, auto_ack=auto_ack, on_message_callback=self.rpc_client_response)
            return self
        except Exception as e:
            print(e)

    def rpc_client_response(self,ch, method, properties, body)->any:
        """
        收到结果后的回调函数
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        if self.corr_id == properties.correlation_id:
            self.response = json.loads(body)

    def rpc_client_request(self,body:any,exchange:str,routing_key:str):
        """
        启动rpc客户端请求循环，拿到消息后返回
        :param body: 请求体
        :param exchange:服务端的交换机
        :param routing_key:请求发送到服务端的哪个队列，由路由指定
        :return:
        """

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.responses[self.corr_id] = None
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   properties=pika.BasicProperties(
                                       reply_to=self.qname,
                                       correlation_id=self.corr_id
                                   ),
                                   body=json.dumps(body))
        while self.response is None:
            self.connection.process_data_events()
        self.responses[self.corr_id] = self.response
        return self.response

    def rpc_server_init(self,call=None,exchange=None,exchange_type=None,queue="",routings=[""]):
        """
        rpc服务端初始化，会初始化一条消费者队列，这个队列的到达路由需要和客户端进行约定
        :param call: 处理远程调用请求的函数
        :param exchange: 服务端的客户端约定好的交换机
        :param exchange_type: 交换机类型
        :param queue: 队列名，默认为""，为临时队列，名字随机
        :param routings:路由键，服务端的队列需要绑定到某个路由上，默认为"",即该交换机为广播模式时生效
        :return:self
        """
        try:
            #将可以主动设置处理远程调用请求的函数，也可以由回调函数rpc_server_callback自己去找
            self.remote_callback = call
            self.consumer_init(exchange=exchange,exchange_type=exchange_type,queue=queue,routings=routings)
            self.channel.basic_qos(prefetch_count=100)
            self.channel.basic_consume(queue=self.qname, auto_ack=False,on_message_callback=self.rpc_server_callback)
            return self
        except Exception as e:
            print(e)

    def rpc_server_callback(self,ch, method, properties, body):
        """
        这里应该是解析参数，寻找被调用者，然后进行调用后
        将调用结果发送会请求中要求返回的路由中
        :param ch: channel
        :param method: method
        :param properties: 客户端发的消息带的参数
        :param body: 请求体，会封装调用信息
        :return:
        """
        # 将计算结果发送回该请求体要求发送的路由中
        # 这里的发送，直接发送到请求体传过来的队列中，所以设置exchange=""
        ch.basic_publish(exchange="",
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(
                             reply_to=self.qname,
                             correlation_id=properties.correlation_id
                         ),
                         body=json.dumps(self.remote_callback(json.loads(body))),
                         )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def rpc_server_start(self):
        """
        启动rpc的服务端
        :return:
        """
        self.channel.start_consuming()

    def check_Value(self,*args):
        """参数校验"""
        for i in args:
            assert i != None


```

