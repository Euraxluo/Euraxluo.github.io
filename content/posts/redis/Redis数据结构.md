+++
title = "Redis API及数据结构"
date = "2019-03-10"
description = "Redis API及数据结构"
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
本文介绍了redisApi以及数据结构
<!--more-->

# Redis的API以及数据结构详解

## 数据结构和内部编码


面向接口编程的思想	



### redisObject



- type（对外的数据类型）



- encoding（内部编码方式）



- ptr（数据指针）



- vm（虚拟内存）



#### string（二进制安全）



特性：可以包含任何数据，图片或者序列化对象，一个键最大存储512m



- raw



- int



- embstr



#### hash（键值对集合，即map类型）



特性：适合存储对象，并且可以像数据库的update一样，只修改某一个属性值



使用场景：存储，读取，修改用户属性



- hashtable



- ziplist



#### list（双向链表）



特性：增删快，提供了操作某一段元素的API



使用场景：消息队列，排行榜



- linkedlist



- ziplist



#### set（哈希表，元素不重复）



特性：添加，删除，查找的复杂度都是O1；提供了集合运算的API



使用场景：利用唯一性，统计访问网站的独立ip；好友推荐时，标签交集达到阈值就推荐



- hashtable



- intset



#### zset（将set中的元素增加一个score，元素按score有序排列）



特性：数据插入时，已经进行天然排序



使用场景：排行榜；带权重的消息队列



- skiplist



- ziplist



## redis单线程



### 特点：



- 在一个时间只会进行一个操作



- 拒绝长（慢）命令：

`keys`,`flushall`,`flushdb`,`show lua script`,`mutil/exec`,`operate big value(collection)`



- 有些命令会启新的线程：

`fysnc file descriptor`,`close file descriptor`



### redis使用单线程的原因：



- 纯内存



- 非阻塞IO



- 避免线程切换和竞态消耗



## 字符串



### 键值结构



- key：字符串



- value：字符串，整型，json串，位图



### 使用场景



- 缓存



- 计数器



- 分布式锁



### API

- get key，获取key对应的value (O1)



- set key value，设置key-value (O1)



- del key，删除 key-value (O1)



- incr key，key自增1 (O1)



- decr key，key 自减1 (O1)



- incrby key k ，key 自增 k (O1)



- decrby key k，key 自减 k (O1)



### 实战



1. 记录网站每个用户个人主页的访问量



incr userid：pageview



2. 缓存视频的基本信息(数据源在MySQL中)



```java

public VideoInfo get(long id){

    String redisKey = redisPrefix + id;//定义一个rediskey

    VedeoInfo vedeoInfo = redis.get(redisKey);

    if(videoInfo == null){

        videoInfo = mysql.get(id);

        if(videoInfo != null){

    	redis.set(key=redisKey,value=serialize(videoInfo));

		}

    }

}

```

3. 分布式id生成器



多个服务并发获取自增id



`incr id`



### 其他命令

- set key value，不管key是否存在，都设置 (O1)



- setnx  key value，key不存在，才设置（add操作）(O1)



- set key value xx，key存在，才设置（update 操作） (O1)



- setex key seconds value，`set key value` +` EXPIRE key seconds` (O1)



- mget k1 k2 ... kn,批量获取key，原子操作（On）



- mset k1 v1 k2 v2 ...,批量设置key-value（On）



- getset key newvalue，设置新的value，并返回旧的value（O1）



- append key value，将value追加到旧的value中（O1）



- strlen key，返回字符串的长度（O1）



- incrbyfloat key -1，增加key对应的值 -1.0（O1）



- getrange key start end，获取key对应value的指定下标的字符，（O1）



- setrange key index value，设置key对应的value，指定index下标的字符换成 value （O1）



## 哈希



### 键值结构



key



field:value ：是很多的键值对



```shell

#key：

userid：1

#field:value

email:xxxx@xx.com

name:euraxluo

Password:sasasasasa

id:1

```



中存储一个个属性值以及对应的value



##### 和string比较



string要实现这个方式，需要把这些键值对序列化后存到redis中，取出来的时候也要反序列化。并且属性是空值，也要序列化进去，但是我们的哈希中，如果这个属性没有，可以不写



### 特点



- 在value中，存储了一个更小的redis



- field不能相同，value可以相同



### API



- hget key field，获取hash key 对应的field的value （O1）



- hset key field value，设置hash key 对应的field的value（O1）



- hdel key field,删除hash key 对应field的value（O1）



- hexists key field，判断hash key 是否有field（O1）



- hlen key ,获取hash key field的数量（O1）



- hmset key field1 value1 field2 value2 ...fieldN valueN，批量设置hash key 的一批field value（On）



- hmget key field1 field2 ..fieldN,批量获取hash key 的一批field的值（O1）



### 实战

1. 记录每个用户主页的访问量



hash key为user:1:info的数据，为pageview属性设置自增



`hincriby user:1:info pageview count`



2. 缓存视频的基本信息



```java

public VideoInfo get(long id){

    String redisKey = redisPrefix + id;//定义一个rediskey

    Map<String,String> hashMap = redis.hgetAll(redisKey);

    VideoInfo videoInfo = transformMapToVideo(hashMap);

    if(videoInfo == null){

        videoInfo = mysql.get(id);

        if(videoInfo != null){

    	redis.hmset(key=redisKey,value=transformVideoToMap(videoInfo));

		}

    }

}

```



### 其他命令



- hgetall key，返回hash key对应的所有field和value（On）



- hvals key，返回hash key对应的所有field的key（On）



- hkeys key，返回hash key 对应的所有field （On）



- hsetnx key field value,设置hash key对应的field的value，如field已经存在，则失败（O1）



- hinrcby key field intCounter，hash key对应的field的value自增intCount（O1）



- hinrcbyfloat key field floatCount，hincrby浮点数（O1）



## 列表



### 键值结构



key-value（有序队列）



可以从左右两端进行添加，弹出



### 特点



- 有序



- 可以重复



- 左右两边插入弹出



### API



- rpush key v1 v2 ... vn,从列表右端插入值（1~n） （O1-On）

` vn ... v3 v2 v1`



- linsert key before|after value newValue,在list指定的值前|后插入newValue（O1-On）



- lpop key，从左边弹出一个item（O1）



- rpop key，从右边弹出一个item（O1）



- lrem kay count value，根据count的值，从列表中删除|count|个和value的值相等的项，`count>0表示从左到右`（On）



- ltrim key start end，保留start-end索引范围的列表项（On）



- lrange key start end ，获取列表指定索引范围的全部item，包含end（On）



- lindex key index，获取列表指定索引的item（On）



- llen key，获取列表长度（O1）



- lset key index newValue，设置列表指定索引的项为newValue（On）



### 实战



1. 时间轴功能



有你关注的人更新了微博：lpush



时间轴是一个lrange的结果



微博是一个个对象，可以存放在hashmap或者string中



lpush中存储了对象中的关键uid，可以通过关键的uid，去取微博内容



### 其他命令



- blpop keys timeout,依次检查ksys，弹出第一个非空列表的头元素，当没有任何元素时，连接被阻塞，直到等待超时（timeout），或者发现可弹出元素为止（O1）



- blpop keys timeout,依次检查ksys，弹出第一个非空列表的右边元素，当没有任何元素时，连接被阻塞，直到等待超时（timeout），或者发现可弹出元素为止（O1）



### TIPS



1. LPUSH + LPOP = Stack，左入左出是栈



2. LPUSH + RPOP = Queue，左入右出是队列



3. LPUSH + LTRIM = Capped Collection，限制长度的列表



4. LPUSH + BRPOP = Message Queue，左入阻塞式右出是消息队列



## 集合



### 键值结构



key：string



value：集合



### 特点



- 无序



- 无重复



- 集合间操作



### API

- sadd key elements，向集合kay添加elements，返回添加成功数（O1）



- srem key elements，将集合kay中的elements移除掉，返回移除成功数（O1）



- scard key，返回集合大小（O1）



- sismember key elements，判断elements是否在集合中（O1）



- srandmenmber key count，从集合key中挑出count个元素，不会删掉这些元素（O1~On）



- spop key ，从集合中随机弹出一个元素（O1）



- smembers key，无序返回集合中的所有元素（On）



- sscan key cursor count，增量式迭代从cursor开始迭代，返回count个结果。返回值是一个数组，第一个元素，指示了下一次迭代的游标，如果为0，完全迭代。第二个元素是迭代结果



### 实战



1. 抽奖系统，把参与了这个抽奖的用户放进这个集合



2. 赞，踩，转发，把参与了这个操作的用户放进这个新闻的集合中



3. tag，用户标签，可以把用户的标签放进集合中，也可以把用户放进这个标签对应的集合中，这两个是一个事务



### 集合运算API



- sdiff key1 key2,差集



- sinter key1 key2，交集



- sunion key1 key2，并集



- sdiff|sinter|sunion + store destkey,将运算结果保存在destkey中，下次就可以不用计算了



### TIPS

SADD = Tagging，可以用类做标签



SPOP/SRANDMEMBER = Random item，可以用来做随机的场景



SADD + SINTER = Social Graph，可以用来做社交的场景



## 有序集合



### 键值结构



key：string



value： score:value



按照score进行排序



### 特点



无重复元素



按照score排序



value中存储着element+score



### API



- zadd key score element[score element...]，添加score和element，score可以重复（OlogN）



- zrem key elements，删除元素 (O1)



- zscore  key element，获取key中element对应的分数（O1）



- zincrby key increScore element，为key中element对应的score加increScore（O1）



- zcard key，返回key中的元素个数（O1）



- zrange key start stop [WITHSCORES]，返回key中排序结果start~end的升序结果，是否和score一起输出（O log(N)+m,N:元素个数,m:end-start）



- zrangebyscore key minScore maxScore [WITHSCORES],返回key中score在minScore~maxScore范围的结果（O log(N)+m,N:元素个数）



- zcount key minScore maxScore，返回有序集合中，在指定分数范围内的个数 （O log(N)+m,N:元素个数）



- zremrangebyrank key start end，删除指定排名内的升序元素（O log(N)+m,N:元素个数,m:end-start）



- zremrangebyscore key minScore maxScore，删除指定分数范围内的升序元素（O log(N)+m,N:元素个数）



### 实战

1. 排行榜

score可以是时间戳，销售数，点赞数



### 其他API



- zrevrank key，返回从高到低的排名 （OlogN）



- zrevrange key start end [withscore]，从降序的结果中按照start~end返回结果，（O log(N)+m,N:元素个数,m:end-start）



- zrevrangebyscore，从降序的结果中按照分数返回结果，（O log(N)+m,N:元素个数,m:end-start）



- zinterstore destination numkeys key[key...]，计算给定的一个或多个有序集的交集，其中给定 key 的数量必须以 numkeys 参数指定，并将该交集(结果集)储存到 destination 。默认结果集中某个成员的 score 值是所有给定集下该成员 score 值之和.（O(N*K)+O(M*log(M))， N 为给定 key 中基数最小的有序集， K 为给定有序集的数量， M 为结果集的基数。）



- zunionstore destination numkeys key[key...]，计算给定的一个或多个有序集的并集，其中给定 key 的数量必须以 numkeys 参数指定，并将该并集(结果集)储存到 destination 。默认结果集中某个成员的 score 值是所有给定集下该成员 score 值之 和 。（O(N*K)+O(M*log(M))， N 为给定 key 中基数最小的有序集， K 为给定有序集的数量， M 为结果集的基数。）
