---
layout:   post          
title:   RedisCluster03        
date:    2019-03-16      
author:   Euraxluo           
categories: Redis
tags:  节点 集群 客户端
---
* TOC
{:toc}


## RedisCluster

## 客户端使用


### moved重定向



1. 对任意节点发送键命令

2. 节点会计算槽和对应节点确定这个键是否指向自身

3. 如果指向自身，就执行命令，返回key所在的槽

4. 否则就回复moved异常，客户端拿到这个moved后，重定向节点，重新发送命令



### ASK重定向



解决槽迁移时客户端的查询问题



1. 对源节点发送键命令

2. 节点发现正在进行槽迁移，回复客户端ask转向

3. 客户端对目标节点Asking，发送命令

4. 目标节点返回响应结果 



### 两者的区别



- 两者都是客户端重定向

- moved：槽已经确定迁移

- ask：槽还在迁移中



## smart客户端



目标：追求性能（不能使用代理模式）



1. 从集群中选取一个可运行节点，使用cluster slots 初始化槽和节点映射

2. 将cluster slots的结果映射到本地，为每个节点都创建一个连接池

3. 准备执行命令



### 执行命令



1. 通过key哈希模16383，得到slot，通过本地映射得到节点，再通过连接池去连接

2. 如果连接出错，可能槽迁移，也可能是连接异常，如果槽迁移，那么

3. 我们随机访问一个活跃节点，节点会返回moved异常

4. 我们得到槽迁移的结果，更新我们的slot和nodes的映射（确定槽迁移）

5. 然后再去连接目标节点

6. 如果命令发送多次未成功，显示异常`Too many cluster redirection`



### jiedisCluster使用



```java

Set<HostAndPort> nodeList = new HashSet<HostAndPort>();

nodeList.add(new HostAndPort(HOST1,PORT1));

nodeList.add(new HostAndPort(HOST2,PORT2));

nodeList.add(new HostAndPort(HOST3,PORT3));

nodeList.add(new HostAndPort(HOST4,PORT4));

nodeList.add(new HostAndPort(HOST5,PORT5));

nodeList.add(new HostAndPort(HOST6,PORT6));

JedisCluster redisCluster = new JedisCluster(nodeList,timeout,poolConfig);

```



#### TIPS



1. 单例：内置了所有节点的连接池，并可以用来做故障转移

2. 无需手动借还连接池

3. 合理设置commons-pool



#### 整合spring



```java

//工厂

import redis.client.jedis.JedisCluster;

public class JedisClusterFactory{

    private JedisCluster jedisCluster;

    private List<String> hostPoetList;

    private int timeout;

    private Logger logger = LoggerFactory.getLogger(JedisClusterFactory.class)

    public void init(){

        JedisPoolConfig jedisPoolConfig = new JedisPoolConfig();

        Set<HostAndPort> nodeSet = new HashSet<HostAndPort>();

        for(String hostPort:hostPortList){

            String[] arr = hostPort.split(":");

            if(arr.length != 2){

                continue;

            }

            nodeSet.add(new HostAndPort(arr[0],Integer.parseInt(arr[1])));

        }

        try{

            jedisCluster = new JedisCluster(nodeSet,timeout,jedisPoolConfig);

        }catch(Exception e){

            logger.error(e.getMessage(),e);

        }

    }

    public void destroy(){

        if(jedisCluster != null){

            try{

                jedisCluster.close();

            }catch(IOException e){

                logger.error(e.getMessage(),e);

            }

        }

    }

    public JedisCluster getJedisCluster(){

        return jedisCluster;

    }

    public void setHostPortList(List<String> hostPortList){

        this.hostPortList = hostPortList;

    }

    public void setTomeout(int timeout){

        this.timeout = timeout;

    }

    

}



```



```xml

<bean id="jedisClusterFactory" class="path/to/factoryClass" init-method="init" destory-method="destory">

</bean>

<bean id="jedisCluster" factory-bean="jedisClusterFactory" factory-method="getJedisCluster">

</bean>

```







### 多节点命令实现



伪代码



```java

Map<String,JedisPool> jedisPoolMap = jedisCluster.getClusterNodes();

for(Entry<String,JedisPool>entry:jedisPoolMap.entrySet()){

    //获取每个节点的Jedis连接

    Jedis.jedis = entry.getValue().getResource();

    //只删除主节点数据

    if(!isMater(jedis)){

        continue;

    }

    //finally close

}

```



## Redis Cluster的故障转移



其他主节点对集群进行监控



### 故障发现



- 通过ping/pong 消息实现故障发现，不需要sentinel



- 主观下线：某个节点认为另一个节点不可用



  ![主观下线过程](/image/clusterzgxx.png)



- 客观下线：当半数以上持有槽的主节点都标记为某节点主管下线



  ![维护故障表](/image/whgzb.png)



  ![客观下线过程](/image/clusterkgxx.png)



### 故障恢复



- 从节点资格检查



  1). 每个从节点坚检查与故障主节点的断线时间



  2). `超过cluster-node-timeout*cluster-slave-validity-factory`就取消资格



  3). `cluster-slave-validity-factory`默认为10



- 准备选举时间



  1). 给偏移量最大的节点最长的选举时间



  2). 把最接近master节点的从节点的选举延迟时间设置为最短



- 选举投票



  1). 收集到master节点数/2+1票就可以替换主节点



- 替换主节点



  1). `slaveof no one`当前从节点取消复制变为主节点



  2). 执行`clusterDelSlot`撤销故障主节点负责的槽,并执行clusterAddSlot把这些槽分配给自己



  3). 向集群中广播自己的pong消息,表明自己已经替换了故障从节点



## RedisCluster开发运维



### 集群完整性



- `cluster-require-full-converge默认为yes`



  集群中16384个槽全部可用：保证集群完整性



  节点故障或者正在故障转移，集群下线`(error)CLUSTERDOWN The cluster is down`



- 大多数业务无法容忍，`cluster-require-full-converge`设置为no



### 带宽



- 消息发送频率：节点发现与其他节点最后通信时间超过`cluster-node-timeout`会直接发送ping消息

- 消息数据量:slots槽数组（2KB空间）和整个集群1/10的状态数据（10个节点状态数据约1kb）

- 节点部署的机器规模：集群分布的机器越多且每台机器划分的节点数越均匀，则集群内整体的可用带宽越高



#### 优化



- 避免大集群：避免多业务使用一个集群，大业务可以多集群

- cluster-node-timeout：和带宽和故障转移速度都有关，需要均衡

- 尽量均匀分配到多机器上，保证高可用和带宽



### Pub/Sub广播



- publish在集群中每个节点广播：加重带宽



#### 优化



- 如果需要Pub/Sub，单独开启一套Redis Sentinel



### 集群倾斜



#### 数据倾斜：内存在每个节点中分布不均



- 节点和槽分配不均



  1).  `redis-trib.rb info ip:port`查看节点，槽，键值分布



  2). `redis-trib.rb rebalance ip:port`进行均衡 



- 不同槽对应键值数量差异较大



  1). CRC16正常情况下比较均匀



  2). 可能存在hash_tag



  3). cluster countkeysinslot {slot}获取槽对应键值个数



- 包含bigkey



  1). 在从节点运行`redis-cli --bigkeys`



  2). 优化：优化数据结构



- 内存相关配置不一致（例如每个节点哈希优化不一致）



  1). `hash-max-ziplist-value`,`set-max-intset-entries`的配置



  2). 定期检查配置的一致性



- 客户端缓冲区大小



- 哈希表大小



#### 请求倾斜：某些节点访问量很高



- 热点key：重要的key或则bigkey



  1). 避免bigkey



  2). 热键不要用hash_tag



  3). 当一致性需求不高时，可以使用本地缓存+MQ



### 读写分离



- 只读连接：集群模式的从节点不接受任何读写请求



  1). 在从节点get会重定向到负责槽的主节点



  2).readonly命令可以读：连接连接命令



- 读写分离：更加复杂



  1). 同样的问题：复制延迟，读取过期数据，从节点故障



  2). 修改客户端：cluster slaves {nodeId}



  3). 不建议使用



### 数据迁移



- 官方迁移工具：`redis-trib.rb import --from ip:port{源节点} --copy ip:port{集群节点}`



  1).只能从单机迁移到集群



  2).不支持在线迁移：source需要停写



  3).不支持断点续传



  4).单线程迁移：影响速度



- 在线迁移



  有一个中转站，这个中转站会伪装成slave节点去拿到全量更新数据



  1).redis-migrate-tool，唯品会



  2).redis-port，豌豆荚



### 集群vs单机



- 集群的限制



  1). key批量操作支持有限，mget，mset必须在一个slot



  2). key事务和lua支持有限：操作的key必须在一个节点



  3). key时数据库分区的最小粒度：不支持bigkey分区



  4). 不支持多个数据库：集群模式下只有一个db 0



  5). 复制只支持直接复制，不能更改复制的拓扑结构（树）减小压力



- Redis Cluster：满足容量和性能的扩展性，很多业务不需要



  1). 客户端性能会降低



  2). 命令无法跨节点用：mget。keys，scan，flush，sinter等



  3).Lua和事务无法跨节点使用



  4).客户端维护复杂



- Redis Sentinel：满足高可用



## 总结



1. Redis Cluster的分区规则

2. 搭建集群的步骤

3. 集群伸缩的步骤

4. smart客户端操作redis集群

5. 集群自动故障转移
