---
layout:     post                    # 使用的布局（不需要改）
title:      数据库               # 标题
subtitle:   RedisSentinel                #副标题
date:       2019-03-11           # 时间
author:     Euraxluo                      # 作者
header-img: img/post-bg-github-cup.jpg  #这篇文章标题背景图片
catalog: true                 # 是否归档
tags:                               #标签
    - Redis

---
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
## 客观下线
所有sentinel节点对redis节点失败“达成共识”（超过quorum个同意）
