+++
title = "Redis的持久化"
date = "2019-03-10"
description = "Redis的持久化"
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

# Redis的持久化

## Redis持久化作用
### 什么是持久化

redis的所有数据保存在内存中，对数据的更新回异步的保存在磁盘中



### 持久化方式

#### 快照

1. MySQL Dump

2. Redis RDB

#### 日志

1. MySQL Binlog

2. Hbase HLog

3. Redis AOF



## RDB持久化

### 什么是RDB

redis可以通过命令，把当前数据库的状态保为一个RDB文件（二进制）

也可以通过命令把硬盘上的RDB载入到redis中

同时RDB文件也是一个复制的媒介

### 触发机制

#### save

- 通过save命令让redis生成rdb文件，生成成功返回‘OK’

- 同步命令，阻塞命令，会导致服务器阻塞

- 会替换老的rdb文件

- 复杂度On

#### bgsave

- 接收到bgsave后，redis利用linux的fork()命令产生一个子进程，让产生的子进程去生成RDB文件，返回‘Backgroud saving started’

- fork()函数也是一阻塞命令，一般情况下很快

- 会替换老的rdb文件

- 复杂度On

#### save与bgsave比较



|  命令    | save     | bgsave     |

| ---- | ---- | ---- |

| io类型 |同步      |   异步   |

| 是否阻塞 |  是    |   是   |

| 时间复杂度 |  On    | On     |

| 优点 |  不会消耗额外内存      |不阻塞客户端命令    |

| 缺点 |  阻塞客户端命令    |需要fork()，消耗内存 |



#### 自动生成快照

##### 策略

满足以下三个条件就会触发创建RDB文件的行为（bgsave）

- 900 1chages

- 300 10chages

- 60 10000chages



##### 缺点

- 生成快照的频率有些时候可能过高了（写量过高的情况）



#### 配置

```shell

#自动策略，一般不配置，不使用自动生成快照

save 900 1

save 300 10

save 60 10000

#文件名，一般按照端口号区分

dbfilename dump-${port}.rdb

#rdb,log,aof文件的位置，选择一个大内存的目录，或者需要按照端口进行分盘

dir ./

#如果bgsave出现错误是否立刻停止

stop-writes-on-bgsave-error yes

#是否采用压缩格式

rdbcompression yes

#是否进行校验和验证

rdbchecksum yes

```

### 注意

1. 全量复制时，主数据库会自动生成RDB

2. debug reload，不清空数据库的重启

3. shutdown，关机时会自动生成rdb文件

4. 耗时，耗性能

5. 不可控，易丢失以前的数据（宕机与上一次dump之间的操作）



## AOF持久化

### 什么是AOF

1. 每执行一条命令，就会在AOF文件中追加写入

2. 恢复时，把AOF文件载入执行

3. 执行命令时，会把命令刷新到缓冲区，通过不同的策略，同步到AOF文件中

### AOF的执行策略

#### always

- 每个命令都会从缓冲区fsync到AOF中

#### everysec

- 每一秒从缓冲区fsync到AOF中

- 可以保护硬盘

- 刷新频率可以配置

#### no

- 由操作系统决定什么时候fsync

#### 三种策略比较



| 命令 | always     | everysec      | no     |

| ---- | ---------- | ------------- | ------ |

| 优点 | 不丢失数据 | 每秒一次fsync | 不用管 |

| 缺点 | IO开销大   | 丢失一秒数据  | 不可控 |



### AOF重写

#### 策略

- 从内存中重写

- 会把一些过期的命令删除

- 会把一些可以化简的命令化简

- 会把一些等值的命令合并

#### 优点

- 减少硬盘占用量

- 加快恢复速度

#### 实现方式

1. bgrewriteaof

- 异步操作，主进程fork一个子进程，会从内存中完成AOF重写

![bgrewriteaof](rewriteaof.png)



2. AOF重写配置

- auto-aof-rewrite-min-size，AOF文件重写需要的最小尺寸

- auto-aof-rewrite-percentage，AOF文件增长率

3. AOF统计指标

- aof_current_size,AOF当前尺寸

- aof_base_size，AOF上次启动和重写的尺寸

4. 同时满足以下两条公式

- aof_current_size>auto-aof-rewrite-min-size

- (aof_current_size-aof_base_size/aof_base_size)>auto-aof-rewrite-min-size

#### AOF配置

```shell

#是否打开aof

appendonly yes

#文件名字，使用端口进行区分

appendfilenam "appendonly-${port}.aof"

#每秒aof

appendfsync everysec

#使用大的盘

dir /bigdiskpath

#是否进行append操作，是否允许丢失数据(在重写期间关闭append操作)

no-appendfsync-on-rewrite yes

#增长率

auto-aof-rewrite-percentage 100

#最小尺寸

auto-aof-rewrite-min-size 64mb

#在加载时是否忽略文件错误

aof-load-truncated yes

```

conf文件内容

```shell

head *.aof#查看文件头部

*2#有两个指令

$6#下一行有6个字节

SELECT#指令

$1#下一行有1个字节

0#select 0 ，选择0号数据库

$3

set

$5

hello

```

## RDB和AOF的抉择



### RDB,AOF比较



| 命令       | RDB    | AOF          |

| ---------- | ------ | ------------ |

| 启动优先级 | 低     | 高           |

| 体积       | 小     | 大           |

| 恢复速度   | 快     | 慢           |

| 数据安全性 | 丢数据 | 根据策略决定 |

| 轻重       | 重     | 轻           |



### RDB最佳策略



- 关掉RDB

- 集中管理

- 主从库，从库打开，密度不要太大



### AOF最佳策略



- 开：缓存还是存储，根据功能决定是否需要这个功能

- AOF重写集中管理

- everysec



### 最佳策略

- 小分片

- 根据缓存或者存储决定是否需要这个功能

- 监控：硬盘，内存，负载，网络

- 足够的内存



## 持久化的常见问题



### fork操作的问题



1. 是一个同步操作

2. 与内存量息息相关；内存越大，耗时越长（也与机器类型有关，虚拟机，物理机）

3. info：latest_fork_usec



#### 改善fork



1. 优先使用物理机或者高效支持fork操作的虚拟化技术

2. 控制Redis实例最大可用内存：maxmemory

3. 合理配置Linux内存分配策略，让机器确保有足够的内存再fork：vm.overcommit_memory=1（默认为0，会导致内存不够时，fork阻塞）

4. 降低fork频率，放宽AOF重写自动触发时机，避免不必要的全量复制（全量复制会bgsave）



### 子进程外开销和优化



1. CPU

- 开销：RDB和AOF文件生成，属于CPU密集型

- 优化：不做CPU绑定，不和CPU密集型应用部署，单机部署时，保证不进行大量的rdb和aof文件生成

2. 内存

- 开销：fork内存开销，copy-on-write

- 优化：单机部署时，不做大量的重写；在主进程io少时去做fork；关闭大内存分配`echo never > /sys/kernel/mm/transparent_hugepage/enable`

3. 硬盘

- 开销：AOF，RDB文件写入，可以结合iostat，iotop分析

- 优化：不要和高硬盘负载服务部署在一起（存储服务，消息队列）；根据写入量决定磁盘的类型（ssd）；单机多实例持久化文件目录可以考虑分盘；`no-appendfsync-on-rewrite = yes`

### AOF追加阻塞



在AOF从缓冲区刷盘时，会启动一个线程来完成这个事，主线程会监控同步时间，如果同步时间超过2秒，即刷盘操作2秒还没有完成，主线程就会阻塞，直到刷盘完成

#### 问题



- 主进程不能阻塞

- 刷盘时可能不止丢失1秒的数据

#### 定位



- 看日志，会出现（disk is busy?）提示

- info Persistence，可以通过aof_delayed_fsync:nums,查看出现这种情况的次数



#### 优化

- 不要和高硬盘负载服务部署在一起（存储服务，消息队列）

- 根据写入量决定磁盘的类型（ssd）

- 单机多实例持久化文件目录可以考虑分盘

- `no-appendfsync-on-rewrite = yes`

