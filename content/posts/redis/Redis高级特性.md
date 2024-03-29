+++
title = "Redis高级特性初识别"
date = "2019-03-10"
description = "Redis的高级特性初识"
featured = false
categories = [
  "redis"
]
tags = [
  "redis"
]
series = [
  "redis"
]
images = [
]

+++

# Redis高级特性初识
## 慢查询
### 客户端请求的生命周期
- 客户端发送命令



- 入队列



- 执行命令（慢查询在这一阶段）



- 返回客户端



（客户端超时，不一定是慢查询，慢查询只是客户端超时的一个可能）

### 配置

- slowlog-max-len，固定长度

- slowlog-log-slower-than，慢查询阈值（单位微秒）

    =0，记录所有命令

    <0，不记录任何命令

```shell

#1. 第一次开启配置

config get slowlog-max-len = 128

config get slowlog-log-slower-than = 10000

#2. 修改默认配置重启

#3. 动态配置

config set slowlog-max-len = 128

config set slowlog-log-slower-than = 10000

```

### API

慢查询会把命令放在内存中

- slowlog get [n]：获取慢查询队列

- slowlog len ：获取慢查询队列长度

- slowlog reset：清空慢查询队列

- 定期持久化查询

### TIPS

- slowlog-max-len 不要设置的过大，默认为10ms，通常设置为1ms

- slowlog-log-slower-than 不要设置过小，通常设置为1000左右

- 理解命令生命周期

## pipeline

### 流水线

n次通信时间=n次命令时间+n次网络时间

使用pipeline：1次网络+n次命令



### 客户端实现

maven:

```xml

<dependency>

	<groupId>redis.clients</groupId>

	<artifactId>jedis</artifactId>

	<version>2.9.0</version>

	<type>jar</type>

	<scope>compile</scope>

</dependency>

```

没有使用pipeline

```java

Jedis jedis = new Jedis('127.1',6379);

for(int i=0;i<10000;i++){

    jedis.hset("hashkey:"+i,"field"+i,"value"+i);

}

```

使用pipeline

```java

Jedis jedis = new Jedis('127.1',6379);

for(int i=0;i<100;i++){

	Pipeline pipeline = jedis.pipelined();

	for(int j=i*100;j<(i+1)*100;j++){

    pipeline.hset("hashkey:"+i,"field"+i,"value"+i);

    }

    pipeline.syncAndRetuenAll();

}

```

### 与原生M操作对比

M操作是原子的，而pipeline命令在队列中会被拆分为很多子命令，不是原子的

### TIPS

- 注意每次pipeline携带数据量

- pipeline每次只能作用在一个redis节点上

- M操作与pipeline的区别

## 发布订阅

### 角色

- 发布者

- 订阅者

- 频道

### 通信模型

- 发布者向一个频道发布消息

- 订阅者可以订阅多个频道

- 订阅者不能收到他订阅之前的消息

### API

- pushlish channel message，返回订阅者个数

- subscribe [channel] ,订阅一个或多个

- unsubscribe [channel] ,取消一个或多个订阅

- psubscribe [pattern] ，订阅指定的模式

- punsubscribe [pattern],退订指定的模式

- pubsub channels，列出至少有一个订阅者的频道

- pubsub numsub [channel...]，列出给定频道的订阅者数量

### 发布订阅与消息队列

- 发布订阅会让所有的客户端都受到消息

- 消息队列通过阻塞和list达到让多个客户端收到队列中的不同内容

- 消息队列类似于抢红包

## BitMap

因为redis可以直接操作位

### API

- setbit key offset value，给位图指定索引设置值,返回offset之前的值（不要突然在很小的位图上做很大的偏移量）

- getbit key offset，获取位图指定索引的值

- bitcount key [start end]，获取位图指定范围（start到end，单位为字节，如果不指定就是获取全部）位值为1的个数

- bitop op destkey key [key...]，做多个Bitmap的and(交)，or(并)，not(非)，xor(异或)操作并将结果保存在destkey中

- bitpos key targetBit [start] [end]，计算位图指定范围start~end，单位为字节，如果不指定就是获取全部，第一个偏移量对应的值等于targetBit的位置

### 实战

1. 独立用户统计

- 假设1亿总用户， 5千万独立用户用户



如果userid是整形，则使用set实现存储需要 32*50000000=200MB



BitMap：1*1亿=12.5MB



- 如果只有10万独立用户



如果userid是整形，则使用set实现存储需要 32*100000=4MB



BitMap：1*1亿=12.5MB

### TIPS

1. type=string，最大512MB，可能需要拆分

2. 注意setbit偏移量，可能有很大的耗时

3. 位图不是绝对的好，需要在合适的场景使用合适的数据结构

## HyperLogLog

1. 基于HypeLogLog算法：可以在极小的空间完成独立数量统计

2. 本质还是字符串

### API

- pfadd key element [element...]，向hyperloglog添加元素

- pfcount key [key...]，计算hyperloglog的独立总数

- pfmerge destkey sourcekey [sourcekey...],合并多个hyperloglog



### 实战

添加百万独立用户

```shell

elements=""

key="2019_03_09:users"

for i in `seq 1 1000000`

do

	elements="${elements} uuid-"${i}

	if [[$((i%1000)) == 0]]

	then

		redis-cli pfadd ${key} ${ellements}

		elements=""

	fi

done

```

内存消耗为15kb

### TIPS

1. 是否能容忍错误？（错误率 0.81%）

2. 是否需要单条数据？（不能）

3. 是否需要很小的内存解决问题？

## GEO

### GEO是什么

GEO（地理信息定位）：存储经纬度，计算两地距离，范围计算



### 实战

需要计算两地距离，以及需要存储用户的位置的场景

### API

- geo key longitude latitude member [longitude latitude member...]，增加地理位置信息（经纬度，名称）



- geopos key member [member ...]，通过名称获取地理位置信息



- geodist key member1 menber2 [m/km/mi(英里)/ft(尺)],获取两个地理位置的距离



- [georadius key longitude latitude radius m|km|ft|mi [WITHCOORD] [WITHDIST] [WITHHASH] [ASC|DESC] [COUNT count] ](http://redisdoc.com/geo/georadius.html)  ,获取指定位置范围内的地理位置的信息集合(O(N+logM)， 其中 N 为指定半径范围内的位置元素数量， 而 M 则是被返回位置元素的数量) 代码示例

```shell

redis> GEORADIUS Sicily 15 37 200 km WITHDIST WITHCOORD

1) 1) "Palermo"

   2) "190.4424"

   3) 1) "13.361389338970184"

      2) "38.115556395496299"

2) 1) "Catania"

   2) "56.4413"

   3) 1) "15.087267458438873"

      2) "37.50266842333162"

```

### TIPS

1. since 3.2+

2. type geoKey = zset

3. 没有删除API,可以使用`zrem key member`
