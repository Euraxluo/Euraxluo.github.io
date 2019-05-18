---
layout:   post          
title:   RedisCluster01        
date:    2019-03-13      
author:   Euraxluo           
categories: Redis
tags:  节点 集群 哈希
---
* TOC
{:toc}


# Redis Cluster

## 背景
1. 并发量 <10万dps

2. 数据量 单机内存<256G

3. 带宽 网卡限制



### 解决方式

- 提高机器配置

- 分布式



## 数据分布



| 分布方式 | 特点              | 典型产品 |

| -------- | ----------------- | -------- |

| 哈希分布 | 数据分散度高<br>数据分布业务无关<br>无法顺序访问<br>支持批量操作 | 一致性哈希Memcache<br>Redis Cluster<br>缓存产品 |

| 顺序分布 | 数据分散度易倾斜<br>键值业务相关<br>可顺序访问<br>支持批量操作 | BigTable<br>HBase |



### 哈希分布 

1. 节点取余：hash(key)%nodes

- 客户端分片：哈希+取余

- 节点扩容：扩容时需要数据迁移

- 翻倍扩容：扩容时最好多倍扩容

2. 一致性哈希

有一个token环，节点在token环上，会为每个key分配一个token，在依据token在环上顺时针寻找最近的节点

- 客户端分片：哈希+顺时针选择节点

- 节点伸缩：扩容时减少影响的范围

- 翻倍伸缩：保证最小迁移数据和保证负载均衡

### 虚拟槽分区

- 预设虚拟槽：每个槽映射一个数据子集，一般比节点数大

- 良好的哈希函数：CRC16

- 服务端管理节点，槽，数据：例如Redis Cluster



## 搭建集群

### Redis Cluster架构

- 节点，很多节点，都负责读写

- meet，使用raft协议，是互相通信的基础

- 指派槽，把节点指派槽，才能正常读写

- 复制，保证高可用



## 安装



### 配置安装



#### 节点配置

```shell

port ${port}

daemonize yes

dir "path/to/run"

dbdilename "dump-${port}.rdb"

logfile "${port}.log"

cluster-enabled <yes/no>: 使redis实例作为集群的一个节点

cluster-config-file nodes-${port}.conf: 集群配置文件

cluster-require-full-coverage no,部分节点不可用，依然提供服务

```

#### meet操作

`cluster meet ip port`

当前节点开启meet

```shell

redis-cli -h 127.1 -p 7000 cluster meet 127.1 7001

redis-cli -h 127.1 -p 7000 cluster meet 127.1 7002

redis-cli -h 127.1 -p 7000 cluster meet 127.1 7003

redis-cli -h 127.1 -p 7000 cluster meet 127.1 7004

redis-cli -h 127.1 -p 7000 cluster meet 127.1 7005

```



#### Cluster 配置详解



- `cluster-enabled <yes/no>`: 使redis实例作为集群的一个节点



- `cluster-config-file nodes-${port}.conf`: 集群配置文件 



- `cluster-node-timeout <milliseconds>`: 这是集群中的节点能够失联的最大时间，超过这个时间，该节点就会被认为故障。如果主节点超过这个时间还是不可达，则用它的从节点将启动故障迁移，升级成主节点。注意，任何一个节点在这个时间之内如果还是没有连上大部分的主节点，则此节点将停止接收任何请求。



- `cluster-slave-validity-factor <factor>`: 如果设置成０，则无论从节点与主节点失联多久，从节点都会尝试升级成主节点。如果设置成正数，则cluster-node-timeout乘以cluster-slave-validity-factor得到的时间，是从节点与主节点失联后，此从节点数据有效的最长时间，超过这个时间，从节点不会启动故障迁移。假设cluster-node-timeout=5，cluster-slave-validity-factor=10，则如果从节点跟主节点失联超过50秒，此从节点不能成为主节点。注意，如果此参数配置为非0，将可能出现由于某主节点失联却没有从节点能顶上的情况，从而导致集群不能正常工作，在这种情况下，只有等到原来的主节点重新回归到集群，集群才恢复运作。



- `cluster-migration-barrier <count>`:主节点需要的最小从节点数，只有达到这个数，主节点失败时，它从节点才会进行迁移。更详细介绍可以看本教程后面关于副本迁移到部分。



- `cluster-require-full-coverage <yes/no>`:在部分key所在的节点不可用时，如果此参数设置为”yes”(默认值), 则整个集群停止接受操作；如果此参数设置为”no”，则集群依然为可达节点上的key提供读操作。



#### 分配槽

`cluster addslots slot [slot ...]`

分配槽，一共6个节点，三主三从：

```shell

redis-cli -h 127.1 -p 7000 cluster addslots {0...5461}

redis-cli -h 127.1 -p 7001 cluster addslots {5462...10922}

redis-cli -h 127.1 -p 7002 cluster addslots {10923...16383}

```

使用脚本来分配槽

```shell

start=$1

end=$2

port=$3

for slot in `seq ${start} ${end}`

do 

	echo "slot:${slot}"

	redis-cli -p ${port} cluster addslots ${slot}

done

if [${end}==16383]

then redis-cli -p ${port} cluster info

fi

```

### 设置主从

`cluster replicate node-id`设置不会更改的node-id

设置从节点去复制主节点

```shell

redis-cli -h 127.1 -p 7003 cluster replicate ${node-id-7000}

redis-cli -h 127.1 -p 7004 cluster replicate ${node-id-7001}

redis-cli -h 127.1 -p 7005 cluster replicate ${node-id-7002}

```

使用脚本分配主从

```shell

a=$1

b=$2

c=$3

d=$4

master_arr=($(seq ${a} 1 ${b}))

slave_arr=($(seq ${c} 1 ${d}))

for index in `seq 0 $(( ${#master_arr[*]}-1))`

do

	nodeid=`redis-cli -p ${slave_arr[index]} cluster nodes |grep ${master_arr[index]}`

	redis-cli -h 127.1 -p ${slave_arr[index]} cluster replicate ${nodeid:0:41}

done

```

最好把主从端口配置在文件中，通过脚本读取运行

### 工具安装

#### ruby环境安装

- 下载ruby

`wget https://cache.ruby-lang.org/ruby/2.3/ruby-2.3.1.tar.gz`

- 安装ruby

```shell

tar -xvf ruby-2.3.1.tar.gz

./configure -prefix=/usr/local/ruby

make

make install

cd /usr/local/ruby

cp bin/ruby /usr/local/bin

```

- 安装rubygem redis

```shell

wget http://rubygems.org/downloads/redis-3.3.0.gem

gem install -l redis-3.3.0.gem

gem list --check redis gem

```

- 安装redis-trib.rb

`cp ${REDIS_HOME}/src/redis-trib.rb /usr/local/bin`



#### 通过redis-trib搭建集群

1. 配置开启redis节点

```shell

redis-server redis-8000.conf

redis-server redis-8001.conf

redis-server redis-8002.conf

redis-server redis-8003.conf

redis-server redis-8004.conf

redis-server redis-8005.conf

```

2. 一键开启集群

`./redis-trib.rb creat --replicas 1{每个master的slave数量} [ip：port...]{前面都是master，后面的都是slave}`
