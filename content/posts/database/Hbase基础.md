+++
title = "Hbase基础-概念和安装"
date = "2019-12-20"
description = "Hbase基础"
featured = false
categories = [
  "BigData"
]
tags = [
  "Hbase",
  "database"
]
images = [
]

+++


## Hbase 基本概念

Hbase 能做什么

- 海量数据存储
- 准实时查询

HBase在实际业务场景中的应用

- 交通:gps,摄像头信息
- 金融:交易信息
- 电商:交易信息,浏览信息,物流信息

HBase特点

- **容量大**:Hbase单表可以有百亿行,百万列,数据矩阵的横纵维度所支持的数据量级都十分具有弹性
- **面向列**:HBase是面向列的存储和权限控制,并支持独立检索.列式存储,其数据在表中是按照某列存储的,这样在查询只需要少数几个字段的时候,能大大减少读取的数据量.并且 可以动态增加列
- **多版本**:HBase每一列的数据存储有多个Version
- **稀疏性**:为空的列并不占用存储空间,表可以设计的很稀疏
- **扩展性**:底层依赖于HDFS(只需要增加机器就可以扩大容量)
- **高可靠性**:WAL机制保证了数据写入时不会因集群异常而导致写入数据丢失;HBase底层使用的HDFS,会有备份
- **高性能**:底层的**LSM数据结构**和Rowkey有序排列等架构的独特设计,使得HBase具有非常高的写入性能.region切分,主键索引和缓存机制使得HBase在海量数据下具备-定的随机读取性能,该性能针对Rowkey的查询能够达到毫秒级别

## HBase数据模型

列簇:

- 一张表列簇不会超过5个,多个会增加磁盘交互,降低性能
- 每个列簇中的列数没有限制
- 列只有插入数据后存在
- 列在列簇中是有序的

基本操作

```bash
hbase(main):001:0> create 'test','info'
0 row(s) in 11.7610 seconds

=> Hbase::Table - test
hbase(main):002:0> put 'test','0001','info:username','euraxluo'
0 row(s) in 6.6130 seconds

hbase(main):003:0> scan 'test'
ROW                     COLUMN+CELL
 0001                   column=info:username, timestamp=1577270839695, value=euraxluo   1 row(s) in 0.6160 seconds

hbase(main):004:0> put 'test','0001','info:age','12'
0 row(s) in 0.3720 seconds

hbase(main):005:0> scan 'test'
ROW                     COLUMN+CELL
 0001                   column=info:age, timestamp=1577270880203, value=12
 0001                   column=info:username, timestamp=1577270839695, value=euraxluo   1 row(s) in 0.0240 seconds

hbase(main):006:0> describe 'test'
Table test is ENABLED
test
COLUMN FAMILIES DESCRIPTION
{NAME => 'info', BLOOMFILTER => 'ROW', VERSIONS => '1', IN_MEMORY => 'false', KEEP_DELETED_CELLS => 'FALSE', DATA_BLOCK_ENCODING => 'NONE', TTL => 'FOREVER', COMPRESSION => 'NONE', MIN_VERSIONS => '0', BLOCKCACHE => 'true', BLOCKSIZE => '65536', REPLICATION_SCOPE => '0'}
1 row(s) in 0.3110 seconds

hbase(main):007:0> get 'test','0001','info:age'
COLUMN                  CELL
 info:age               timestamp=1577283627980, value=12
 
hbase(main):008:0> truncate 'test'
Truncating 'test' table (it may take a while):
 - Disabling table...
 - Truncating table...
0 row(s) in 4.2500 seconds


hbase(main):009:0> disable 'test'
0 row(s) in 9.8040 seconds


hbase(main):010:0> is_enabled 'test'
false
0 row(s) in 0.1060 seconds


hbase(main):011:0> drop 'test'
0 row(s) in 5.0910 seconds
```



## 安装(Hadoop,ZooKeeper,HBase,Kafka 单机伪分布式安装过程及注意事项)

- [参考链接1](https://blog.csdn.net/pig2guang/article/details/85313410) 
- [参考链接2](https://blog.csdn.net/qq_40419698/article/details/82317948)

### tar包地址
- [hadoop](https://archive.cloudera.com/cdh5/cdh/5/hadoop-2.6.0-cdh5.7.0.tar.gz)
- [hbase](https://archive.cloudera.com/cdh5/cdh/5/hbase-1.2.0-cdh5.7.0.tar.gz)
- [zookeeper](https://archive.apache.org/dist/zookeeper/zookeeper-3.4.10/zookeeper-3.4.10.tar.gz)
- [hadoop-native](http://d29vzk4ow07wi7.cloudfront.net/731a49d122fd009679c50222a9a5a4926d1a26b6?response-content-disposition=attachment%3Bfilename%3D%22hadoop-native-64-2.6.0.tar%22&Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHAqOi8vZDI5dnprNG93MDd3aTcuY2xvdWRmcm9udC5uZXQvNzMxYTQ5ZDEyMmZkMDA5Njc5YzUwMjIyYTlhNWE0OTI2ZDFhMjZiNj9yZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPWF0dGFjaG1lbnQlM0JmaWxlbmFtZSUzRCUyMmhhZG9vcC1uYXRpdmUtNjQtMi42LjAudGFyJTIyIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTc3MjQ4Mjk5fSwiSXBBZGRyZXNzIjp7IkFXUzpTb3VyY2VJcCI6IjAuMC4wLjAvMCJ9fX1dfQ__&Signature=mzwSQ4FLK3oY-gnQgJkU9mgSdImfoUf3jlG5kCzZZl6wGX-ja6fHL3f-S6AFpEc~FdFOM84zNpskbFZdMA1vpGahBHcSUt4LNIRlOsL-t1QT4H3RC00msFFB4izOCXk9jmV6nilPfG1TQdCKHUetuQu~ViTNMNIgSN9HsqKebYLNxeE-TQK7jfO15UohSuccRVGnzuwXawZhj3fKTUMiTrF6jTzbcC2xIfp7VQ6cb8eqiN7wF16sVpFpQIGukeiigKQpyWRWd0uZEeh1IrRRihVIE5mT6avy8GMMjmT~0GXvnXxoWVx1wR3bGBD-8i~bmKfW893MV76nXAbwUHK~7g__&Key-Pair-Id=APKAIFKFWOMXM2UMTSFA)
- [kafka](https://archive.apache.org/dist/kafka/0.10.2.0/kafka_2.12-0.10.2.0.tgz)



### /etc/profile 

```bash
export PATH USER LOGNAME MAIL HOSTNAME HISTSIZE HISTCONTROL
export JAVA_HOME=/home/software/app/jdk1.8.0_202
export CLASSPATH=.:${JAVA_HOME}/jre/lib/rt.jar:${JAVA_HOME}/lib/dt.jar:${JAVA_HOME}/lib/tools.jar       export PATH=$JAVA_HOME/bin:$PATH
export SCALA_HOME=/home/software/app/scala-2.12.8
export PATH=$SCALA_HOME/bin:$PATH
export MAVEN_HOME=/home/software/app/apache-maven-3.3.9
export PATH=$MAVEN_HOME/bin:$PATH
export HADOOP_HOME=/home/software/app/hadoop-2.6.0-cdh5.7.0
export CLASSPATH=$($HADOOP_HOME/bin/hadoop classpath):$CLASSPATH
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib"
export ZOOKEEPER_HOME=/home/software/app/zookeeper-3.4.10
export PATH=$ZOOKEEPER_HOME/bin:$PATH
export HBASE_HOME=/home/software/app/hbase-1.2.0-cdh5.7.0
export PATH=$HBASE_HOME/bin:$PATH
export KAFKA_HOME=/home/software/app/kafka #_2.12-0.10.2.0
export PATH=$KAFKA_HOME/bin:$PATH
export JAVA_OPTS="-server -Xms256m -Xmx512m  -XX:PermSize=128m -XX:MaxPermSize=256m"
```

### 安装JDK

- 略过,就是解压,然后配置环境变量

### Hadoop 安装配置过程:

- 选择 app 目录存放这些软件

- 解压缩 `tar -zxvf hadoop-2.6.0-cdh5.7.0.tar.gz -C app`

- 配置环境变量

- 解压缩 native 文件,因为我们的lib文件夹是空的`  tar -xvf hadoop-native-64-2.6.0.tar  -C  hadoop-2.6.0-cdh5.7.0.tar.g/lib/native/ ; tar -xvf hadoop-native-64-2.6.0.tar  -C  hadoop-2.6.0-cdh5.7.0.tar.g/lib`

- 写配置文件:

  ```xml
  <!-- app/hadoop-2.6.0-cdh5.7.0/etc/hadoop/coite.xml-->
  <configuration>
          <property>
               <name>hadoop.tmp.dir</name>
               <value>/home/software/hadoop_tmp</value>
          </property>
          <property>
               <name>fs.defaultFS</name>
               <value>hdfs://localhost:9001</value>
          </property>
  </configuration>
  ```

  ```xml
  <!--  app/hadoop-2.6.0-cdh5.7.0/etc/hadoop/hdfs-site.xml-->
  <configuration>
          <property>
               <name>dfs.replication</name>
               <value>1</value>
          </property>
           <property>
                 <name>dfs.namenode.name.dir</name>
                 <value>file:///home/software/hadoop_tmp/dfs/name</value>
           </property>
           <property>
                 <name>dfs.datanode.data.dir</name>
                 <value>file:///home/software/hadoop_tmp/dfs/data</value>
           </property>
  <!--
           <property>
                 <name>fs.checkpoint.data.dir</name>
                 <value>file:///home/software/hadoop_tmp/dfs/fcd</value>
           </property>
           <property>
                 <name>fs.checkpoint.edits.dir</name>
                 <value>file:///home/software/hadoop_tmp/dfs/fce</value>
           </property> -->
           <property>
                 <name>dfs.permissions.enabled</name>
                 <value>false</value>
           </property>
  </configuration>
  ```

  ```bash
  [software]# cat app/hadoop-2.6.0-cdh5.7.0/etc/hadoop/slaves
  localhost
  ```
  
  ```bash
  [software]# cat app/hadoop-2.6.0-cdh5.7.0/etc/hadoop/hadoop-env.sh |grep JAVA_HOME
  # The only required environment variable is JAVA_HOME.  All others are
  # set JAVA_HOME in this file, so that it is correctly defined on
  export JAVA_HOME=/home/software/app/jdk1.8.0_202
  ```
  
- 关闭防火墙

  ```bash
  firewall-cmd --state
  systemctl stop firewalld.service
  firewall-cmd --state
  ```

- 测试

  ```bash
  hdfs namenode -format>{
  查看有无报错
  }
  start-dfs.sh>{
  查看日志有无报错
  }
  jps>{
  21366 DataNode
  7958 Jps
  20888 NameNode
  21869 SecondaryNameNode
  }
  最后去网页上查看存活节点数
  ```

  

#### Hadoop 伪分布式问题

  ```bash
   17/09/22 14:53:21 WARN hdfs.DFSClient: DataStreamer Exception
    org.apache.hadoop.ipc.RemoteException(java.io.IOException): File /input/data.txt._COPYING_ could only be replicated to 0 nodes instead of minReplication (=1). There are 0 datanode(s) running and no node(s) are excluded in this operation.


    解决方案:
    看它的报错信息好像是节点没有启动，但是我的节点都启动起来了，使用jps也能查看到节点信息。
    使用hadoop dfsadmin -report命令查看磁盘使用情况，发现出现以下问题：
    Configured Capacity: 0 (0 B)Present Capacity: 0 (0 B)DFS Remaining: 0 (0 B)DFS Used: 0 (0 B)DFS Used%: NaN%Under replicated blocks: 0Blocks with corrupt replicas: 0Missing blocks: 0-------------------------------------------------Datanodes available: 0 (0 total, 0 dead)
    节点下存储空间都是空的，问题应该就是出现在这了。
           查阅资料发现造成这个问题的原因可能是使用hadoop namenode -format格式化时格式化了多次造成那么spaceID不一致，解决方案：
    1、停止集群（切换到/sbin目录下）
    stop-all.sh
    2、删除在hdfs中配置的data目录（即在core-site.xml中配置的hadoop.tmp.dir对应文件件）下面的所有数据;
    rm -rf /root/training/hadoop-2.7.3/tmp
    3、重新格式化namenode(切换到hadoop目录下的bin目录下)
    hdfs namenode -format
    4、重新启动hadoop集群（切换到hadoop目录下的sbin目录下）
    start-all.sh
  ```




### Zookeeper 安装配置

- 解压缩`tar -zxvf zookeeper-3.4.10.tar.gz -C app`

- 写配置 zoo1.cfg,zoo2.cfg,zoo3.cfg

   cat app/zookeeper-3.4.10/conf/zoo1.cfg
  ```bash
    dataDir=/home/software/zookeeper/zoo1
    clientPort=2191
    server.1=127.0.0.1:8801:7701
    server.2=127.0.0.1:8802:7702
    server.3=127.0.0.1:8803:7703
  ```
    cat app/zookeeper-3.4.10/conf/zoo2.cfg
  ```bash
    dataDir=/home/software/zookeeper/zoo2
    clientPort=2192
    server.1=127.0.0.1:8801:7701
    server.2=127.0.0.1:8802:7702
    server.3=127.0.0.1:8803:7703
  ```
    cat app/zookeeper-3.4.10/conf/zoo3.cfg
  ```bash
    dataDir=/home/software/zookeeper/zoo3
    clientPort=2193
    server.1=127.0.0.1:8801:7701
    server.2=127.0.0.1:8802:7702
    server.3=127.0.0.1:8803:7703  
  ```


- 配置myid文件

  ```bash
  echo "1" > zoo1/myid
  echo "2" > zoo2/myid
  echo "3" > zoo3/myid
  ```

- 启动zookeeper服务

  ```bash
  zkServer.sh start app/zookeeper-3.4.10/conf/zoo1.cfg
  zkServer.sh start app/zookeeper-3.4.10/conf/zoo2.cfg
  zkServer.sh start app/zookeeper-3.4.10/conf/zoo3.cfg
  ```

- 检查是否启动成功

  ```bash
  10626 QuorumPeerMain
  10568 QuorumPeerMain
  13450 Jps
  10732 QuorumPeerMain
  21366 DataNode
  20888 NameNode
  21869 SecondaryNameNode
  ```
  
  ```bash
  zkCli.sh -server 127.0.0.1:8802
  ```
  
  

### HBASE配置

- 解压缩` tar -zxvf hbase-1.2.0-cdh5.7.0.tar.gz -C app`

- 配置

  ```bash
  [software]# cat app/hbase-1.2.0-cdh5.7.0/conf/hbase-env.sh | grep ^export
  export JAVA_HOME=/home/software/app/jdk1.8.0_202
  export HBASE_OPTS="-XX:+UseConcMarkSweepGC"
  export HBASE_MASTER_OPTS="$HBASE_MASTER_OPTS -XX:PermSize=128m -XX:MaxPermSize=128m"
  export HBASE_REGIONSERVER_OPTS="$HBASE_REGIONSERVER_OPTS -XX:PermSize=128m -XX:MaxPermSize=128m"
  export HBASE_MANAGES_ZK=false
  ```
  
  ```xml
   <!--app/hbase-1.2.0-cdh5.7.0/conf/hbase-site.xml -->
    <configuration>
    <property>
        <name>hbase.rootdir</name>
        <value>hdfs://localhost:9001/hbase</value>
      </property>
      <property>
        <name>hbase.cluster.distributed</name>
        <value>true</value>
      </property>
      <property>
        <name>hbase.zookeeper.quorum</name>               
        <value>127.0.0.1:2191,127.0.0.1:2192,127.0.0.1:2193</value>
      </property>
      <property>
        <name>hbase.tmp.dir</name>
        <value>/home/software/hbase/data</value>
      </property>
    </configuration>
  ```
  
- 启动`start-hbase.sh`

- 检验

  ```bash
  21361 HMaster
  10626 QuorumPeerMain
  21366 DataNode
  20888 NameNode
  10568 QuorumPeerMain
  21512 HRegionServer
  10732 QuorumPeerMain
  21869 SecondaryNameNode
  20638 Jps
  ```

  ```bash
  #查看网页:
  http://47.107.44.224:60010/master-status
  ```

  

### Kafka 安装配置

[参考链接](https://blog.csdn.net/weixin_42207486/article/details/80635246)

- 解压 ` tar -zxvf kafka_2.12-0.10.2.0.tgz -C app`

- 环境变量

  ```bash
  export KAFKA_HOME=/home/software/app/kafka #_2.11-2.3.1
  export PATH=$KAFKA_HOME/bin:$PATH
  #export JAVA_OPTS="-server -Xms256m -Xmx512m  -XX:PermSize=128m -XX:MaxPermSize=256m"
  ```

- 修改配置

  app/kafka/config/server1.properties

  ```bash
  broker.id=1
  log.dirs=/home/software/kafka/logs1
  zookeeper.connect=localhost:2191,localhost:2192,localhost:2193
  advertised.listeners=PLAINTEXT://47.107.44.224:9011
  listeners=PLAINTEXT://172.17.50.121:9011
  ```

  app/kafka/config/server2.properties

  ```bash
  broker.id=2
  log.dirs=/home/software/kafka/logs2
  zookeeper.connect=localhost:2191,localhost:2192,localhost:2193
  advertised.listeners=PLAINTEXT://47.107.44.224:9012
  listeners=PLAINTEXT://172.17.50.121:9012
  ```

  app/kafka/config/server3.properties

  ```bash
  broker.id=3
  log.dirs=/home/software/kafka/logs3
  zookeeper.connect=localhost:2191,localhost:2192,localhost:2193
  advertised.listeners=PLAINTEXT://47.107.44.224:9013
  listeners=PLAINTEXT://172.17.50.121:9013
  ```

- 启动

  ```bash
  kafka-server-start.sh kafka/config/server1.properties &
  kafka-server-start.sh kafka/config/server2.properties &
  kafka-server-start.sh kafka/config/server3.properties &
  ```

- 检验

  ```bash
  # 创建一个topic
  kafka-topics.sh --create --zookeeper localhost:2191,localhost:2192,localhost:2193 --replication-factor 1 --partitions 1 --topic testing
  # 查看topic list
  kafka-topics.sh --list --zookeeper localhost:2192
  # 运行生产者
  kafka-console-producer.sh --broker-list localhost:9011,localhost:9012,localhost:9013 --topic testing
  #运行消费者
  kafka-console-consumer.sh --bootstrap-server localhost:9011 --topic testing --from-beginning
  ```

  

