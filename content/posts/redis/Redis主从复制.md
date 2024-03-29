+++
title = "Redis的主从复制"
date = "2019-03-10"
description = "Redis的主从复制"
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

# Redis的主从复制

## 单机部署的问题
1. 机器故障（高可用）

2. 容量瓶颈（分布式）

3. QPS瓶颈（分布式）



## 主从复制的作用

- 为一个数据提供了副本

- slave从master复制一个备份库

- master可以有多个slave

- 一个slave只能有一个master

- 数据流向是单向的，由master-->slave

- 扩展读性能，可以实现读写分离



## 主从复制实现

### slaveof



`slaveof 127.1 6380`

取消复制

`slaveof no one`

### 配置

```shell

#配置这个redis服务复制ip:port这个redis作为他的slave

slaveof ip port

#只读,必须保证从和主的内容一致

slave-read-only yes

```

### 两种方式的比较



| 方式 | 命令       | 配置     |

| ---- | ---------- | -------- |

| 优点 | 无需重启   | 统一配置 |

| 缺点 | 不便于管理 | 需要重启 |



#### 使用配置的方式实现主从复制，需要重启原来的redis服务器



config redis-cli -h 127.1 -p 6379 shutdown

config ps -ef |grep redis-server

```shell

xl        3963     1  0 3月09 ?       00:03:17 redis-server *:6380

xl       19626 18759  0 13:41 pts/0    00:00:00 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn redis-server

```

config redis-cli -h 127.1 -p 6380 shutdown

config ps -ef |grep redis-server

```shell

xl       19649 18759  0 13:41 pts/0    00:00:00 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn redis-server

```

config redis-server redis-6379.conf

config redis-server redis-6380.conf

config redis-cli -h 127.1 -p 6379 info replication

```

# Replication

role:master

connected_slaves:0

master_replid:8e2a95428f7fa32eb6936a052b31bcaee64d43d3

master_replid2:0000000000000000000000000000000000000000

master_repl_offset:0

second_repl_offset:-1

repl_backlog_active:0

repl_backlog_size:1048576

repl_backlog_first_byte_offset:0

repl_backlog_histlen:0

```

config redis-cli -h 127.1 -p 6380 info replication

```shell

# Replication

role:slave

master_host:127.0.0.1

master_port:6380

master_link_status:down

master_last_io_seconds_ago:-1

master_sync_in_progress:0

slave_repl_offset:1

master_link_down_since_seconds:1552282946

slave_priority:100

slave_read_only:1

connected_slaves:0

master_replid:231a9e1dffed58138ccdd5d7d48b85b332edf79b

master_replid2:0000000000000000000000000000000000000000

master_repl_offset:0

second_repl_offset:-1

repl_backlog_active:0

repl_backlog_size:1048576

repl_backlog_first_byte_offset:0

repl_backlog_histlen:0

```

查看run_id:`redis-cli -p 6379 info server |grep run`

## 通过偏移量监控主从复制



`redis-cli -p 6379 info replication`

master_repl_offset:偏移量

slave0:ip=127.1,port=6379,state=online,offset=从库的偏移量，log=1

- 通过对两个偏移量的比对，可以检测主从复制的状态

## 全量复制

![全量复制过程图](/image/master-slave.png)



### 全量复制的开销

1. bgsave时间

2. RDB文件网络传输时间

3. 从节点清空数据时间

4. 从节点加载RDB时间

5. 可能的AOF重写时间



### 全量复制的问题

网络不稳定时，丢包或者网络断开连接，数据丢失，这时候需要再进行全量复制，开销巨大



## 部分复制

![部分复制](/image/notallcopy.png)

repl_back_buffer 默认为1mb，但是实际我们会设置的较大



## 故障处理

1. 故障不可避免

2. 自动故障转移



### slave故障

- 将读取客户端指向存活的其他slave



### master故障

- 把写入客户端指向一个slave

- 更改这个slave：`slaveof no one`,恢复其写入能力

- 把其他的slave：`slaveof new master`,指向这个新的master



### 故障自动转移

- sentinel实现自动故障转移





## TPIS

### 读写分离

1. 读写分离：读流量分摊到从节点

2. 可能的问题

- 复制数据延迟（可以通过监控偏移量解决）

- 读到过期数据（操作key时才校验是否过期，定时采样校验是否过期）

- 从节点故障



### 主从配置不一致

1. maxmemory不一致：丢失数据

2. 数据结构优化参数不一致(例如hash-max-ziplist-entries)：造成内存不一致



### 规避全量复制

1. 第一次全量复制

- 第一次时不可避免

- 使用小主节点（减小maxmemory）

- 在低压，低峰时进行全量复制

2. 节点运行ID不匹配

- 大多出现在主节点重启时（会使run_id变化）

- 利用故障转移，使用哨兵或者集群 

3. 复制缓冲区不足

- 网络中断时，却无法进行部分复制（repl_back_buffer过小）

- 可以通过增大缓冲区（配置`rel_backlog_size`）,大小可以通过网络增强计算（每秒写入dps*(故障排除-故障发生)再计算大小）

### 规避复制风暴

1. 单主节点复制风暴

- 主节点重启后，多从节点请求全量复制



  可以更改复制拓扑，减轻主节点的复制压力，使用树形结构分散压力

2. 单机器复制风暴

- 一个机器上全是master节点，当机器宕机时，压力会很大



  可以通过让其他slave作为新的master来解决，当然也可以使用哨兵或者集群



