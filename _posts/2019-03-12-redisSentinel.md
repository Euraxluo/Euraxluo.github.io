---
layout:   post          
title:   RedisSentinel        
date:    2019-03-12      
author:   Euraxluo           
categories: Redis
tags:  节点 故障 客户端
---
* TOC
{:toc}


# Redis Sentinel

### 主从复制的问题
- 手动故障转移

- 写能力和存储能力受限



## Redis Sentinel架构

- 有多个Sentinel节点

- 不用来存储数据

- 多个节点判断master节点的故障，进行故障转移

- 保证高可用，即便一个Sentinel节点挂点也没事

- 客户端只会记录sentinel的地址（因为sentinel会进行故障转移，master节点地址不固定）

- 一套sentinel可以监控多套master-slave，利用master-name作为标识

## Sentinel的故障转移

1. 多个sentinel发现并确认master有问题

2. 选举出一个sentinel作为领导

3. 选出一个slave作为新的master

4. 通知其余slave成为新的master的slave

5. 通知客户端主从变化

6. 等待老的master复活成为新的master的slave

## 安装与配置

主从配置：

`sed "s/6380/6381/g" redis-6380.conf > redis-6381.conf`

查看：

`cat redis-6381.conf|grep -v "#" |grep -v "^$"`



Sentinel配置

```shell

port ${port}

dir ""

logfile "${port}.log"

sentinel monitor mastername 127.1 port{主节点端口} 2{故障发现个数}

#判断失败时间 30000毫秒

sentinel down-after-milliseconds mastername 30000

#并发度

sentinel parallel-syncs mastername 1

sentinel failover-timeout mastername 180000

```

## 客户端与sentinel连接

### 高可用

- 服务端高可用

- 客户端高可用



### 实现原理

- 获取全部的sentinel节点

- 我需要给sentinel我想连接的mastername

- 遍历sentinel节点集合，获取一个可用的sentinel节点

- 通过API`get-master-addr-by-name`来获取真正的master节点地址

- 通过`role/role replication`验证得到的master节点是否是真正的master



### jedisAPI

```java

JedisSentinelPool sentinelPool = new JedisSentinelPool(masterName,sentinelSet,poolConfig,timeout);

Jedis jedis = null;

try{

    jedis = redisSentinelPool.getResource();

}catch(Exception e){

    logger.error(e.getMessage(),e);

}finally{

    if(jedis != null)

    	jedis.close();

}



```

### redis-py

```python

from redis.sentinel import Sentinel

sentinel = Sentinel([("localhost",26379),("localhost",26380),("localhost",26381)],socket_timeout=0.1)

#获取主节点ip

sentinel.discover_master('mymaster')

#获取从节点ip

sentinel.discover_slaves('mymaster')

```

#### 如果你的Redis一直杀不死

- 检查是否开了守护进程

- 检测使用kill -9 能否杀死

- 关闭守护进程，利用`/etc/init.d/redis-sentinel stop`进行关闭

## 故障转移

```python

from redis.sentinel import Sentinel as St

import redis as rd

import time

st = St([("localhost",26379),("localhost",26379),("localhost",26379)],socket_timeout=0.1)

key = "master"

i = 0

while(True):

    try:

        masterhost,masterport = st.discover_master('mymaster')

        i +=1

        time.sleep(1)

        client = rd.StrictRedis(host=masterhost,port=masterport)

        setResult = client.set(key,"value: %d"%i)

        time.sleep(1)

        if i%3==0:

            print(client.get(key))

    except Exception as e:

        print(e)

```

运行这个程序后，kill -9 掉master

查看脚本的输出，最后查看sentinel和各个server的日志

`tail -f redis-sentinel-26379.log`



我们可以看到，投票，重写配置，主从辅助，部分复制等等一系列的过程



## sentinel的定时任务

1. 每10秒每个sentinel对master和slave执行info命令

- 发现slave节点

- 确定主从关系

2. 每2秒每个sentinel通过master节点的channel交换信息（是不是把master作为一个频道，那如果master挂掉了怎么办）

- 通过__sentinel__:hello频道交换信息

- 交互对节点的看法和自身的信息

3.每1秒每个sentinel对其他sentinel和redis执行ping

- 心跳检测，失败判定依据

- 是故障检测的基础



## 主观下线

每个sentinel节点对Redis节点失败的偏见

`sentinel down-after-milliseconds mastername 30000{超过多久未收到回复}`

## 客观下线

所有sentinel节点对redis节点失败“达成共识”（超过quorum个统一，建议sentinel/2+1）

`sentinel monitor mastername ip port quorum{法定人数}`



## 故障转移

### 领导者选举

- 原因：只有一个sentinel节点完成故障转移

- 选举：通过sentinel is-master-down-by-addr 命令

1. 这个命令会发出自己对master的主观判断，并且要求将自己设置为领导者

2. 收到命令的sentinel如果没有同意其他sentinel发出的请求，就会同意这个请求，否则拒绝

3. 如果sentinel节点超过sentinel集合半数且超过quorum数，那么它将成为领导者

4. 如果此过程有多个sentinel节点成为了领导者，那么将等待一段时间重新进行选举



### sentinel领导者节点实现故障转移

1. 从slave节点中选出一个合适的节点作为新的master

2. 对上面的slave节点执行`slaveof no one`命令让其成为master节点

3. 向剩余的slave节点发送命令，让它们成为新master节点的slave节点，复制规则和`parallel-syncs`参数有关{快速复制还是顺序复制}

4. 更新原来的master节点为slave，并对其保持关注，当其恢复后命令他去复制master



### 怎么选择合适的slave节点

1. 选择`slave-priority{slava优先级}`最高的节点，如果存在返回，不存在继续

2. 选择复制偏移量最大的slave节点{复制的最完整}，如果存在返回，不存在继续

3. 选择runID最小的slave节点



## TIPS

### 节点运维，节点的上下线

1. 节点下线

- 机器性能不足

- 节点故障

- 机器故障，过保

- `sentinel failover <masterName>`,让一个sentinel节点去完成故障转移

- 节点临时下线还是永久下线

2. 节点上线

- 主节点上线，使用`sentinel failover`

- 从节点上线，`slaveof`，sentinel节点可以感知

- sentinel上线，配置`sentinel monitor mastername 127.1 port quorum`





### 高可用读写分离

1. 从节点的作用

- 是一个副本，高可用的基础

- 读写分离

2. 依赖三个消息用于监控slave节点资源池

- +switch-master：切换主节点（从节点晋升主节点）

- +convet-to-slave：切换从节点（主节点降为从）

- +sdown：主观下线



### 实际部署

- 在同一局域网不同物理机部署redis Sentinel节点

- redis sentinel 的sentinel节点个数最好为奇数，quorum最好是（节点个数/2+1）

- 客户端初始化时连接的是sentinel节点集合，但是sentinel只是配置中心，不是代理模式

- 当客户端监控到`switch-master`时，会重新进行redis连接初始化
