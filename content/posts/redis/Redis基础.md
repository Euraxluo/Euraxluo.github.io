+++
title = "Redis基础学习"
date = "2019-03-10"
description = "Redis基础学习"
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

# Redis基础学习

Redis是一个key-value存储系统。和Memcached类似，它支持存储的value类型相对更多，包括string(字符串)、list(链表)、set(集合)、zset(sorted set --有序集合)和hash（哈希类型）。这些数据类型都支持push/pop、add/remove及取交集并集和差集及更丰富的操作，而且这些操作都是原子性的。在此基础上，redis支持各种不同方式的排序。与memcached一样，为了保证效率，数据都是缓存在内存中。区别的是redis会周期性的把更新的数据写入磁盘或者把修改操作写入追加的记录文件，并且在此基础上实现了master-slave(主从)同步。
	

Redis 是一个高性能的key-value数据库。 redis的出现，很大程度补偿了memcached这类key/value存储的不足，在部 分场合可以对关系数据库起到很好的补充作用。它提供了Python，Ruby，Erlang，PHP客户端，使用很方便,Redis支持主从同步。数据可以从主服务器向任意数量的从服务器上同步，从服务器可以是关联其他从服务器的主服务器。这使得Redis可执行单层树复制。从盘可以有意无意的对数据进行写操作。由于完全实现了发布/订阅机制，使得从数据库在任何地方同步树时，可订阅一个频道并接收主服务器完整的消息发布记录。



## 安装和基本命令



### 安装：



Ubuntu18.04：`sudo apt-get install redis-server`



安装redis后会自动安装redis-cli



也可以安装图形工具

`sudo snap install redis-desktop-manager`



### 基本操作



1. 检查Redis服务器系统进程

`ps -aux |grep redis`

2. 通过启动命令检查Redis服务器状态

`netstat -nlt|grep 6379`

3. 访问Redis

最简启动

`redis-server`

指定配置文件启动

`redis-server config/redis-6380.conf`

验证

`ps -ef|grep redis`

`netstat -antpl | grep redis`

`redis-cli -h ip -p port ping`

访问

`redis-cli -a euraxluo -h 127.1 -p 6379`

###  基本命令

#### 0.keys*

时间复杂度是On

`keys xx?`

`keys xx*`

`keys xx[x-x]*`

#### 1.判断一个key是否存在 O1

`exists key`



#### 2.设置key的过期时间O1

`expire key seconds`#在seconds秒后过期

`ttl key`#查看key剩余的过期时间

`persist key`#去掉key的过期时间

查看过期时间

```shell

127.1:6380> set k1  v1

OK

127.1:6380> expire k1 20

(integer) 1

127.1:6380> ttl k1

(integer) 14

127.1:6380> ttl k1

(integer) 1

127.1:6380> ttl k1

(integer) -2（-2表示key不存在，已经过期了）

```



去掉key过期时间

```shell

127.1:6380> set k1  v1

OK

127.1:6380> ttl k1

(integer) -1

127.1:6380> expire k1 20

(integer) 1

127.1:6380> ttl k1

(integer) 18

127.1:6380> persist k1

(integer) 1

127.1:6380> ttl k1

(integer) -1(-1表示key存在，并且没有设置过期时间)

```

#### 3.查看key的数据类型O1

`type key`



#### 4. 添加一条记录



```shell

set k1 "helloworld"



get k1



```



#### 5.添加一条数字记录

```shell

set k2 1



#让数字自增

incr k2



get k2



```



#### 6.添加一个列表记录

```shell

#添加列表第一个元素

lpush k3 a

#在最左边添加第二个元素

lpush k3 b

#在最右边添加第三个元素

rpush k3 c



#打印这个列表，按从左到右的顺序，规定起点和终点

lrange k3 0 3



```



#### 7.添加一个哈希记录

```shell

#添加name

hset k4 name "euraxluo"

#添加email

hset k4 email "euraxluo@qq.com"

#打印key为name的记录的value

hget k4 name

#获取整个哈希表

hgetall k4

```



#### 8.给哈希一次一次添加多个值

```shell

#一次添加多个k-v

HMSET k5 username euraxluo password pwd age 21

#答应哈希表中，key为username，age对应的value

HMGET k5 username age

#打印完整的哈希表

HGETALL k5

```



#### 9.删除记录

```shell

#查看所有的key列表

keys ×

#删除k1,k5

del k1 k5

```



#### 10.其他设置

```shell

#使用密码



sudo vi /etc/redis/redis.conf



#取消注释requirepass，设置密码为euraxluo

requirepass euraxluo



#设置远程访问，注释bind

#bind 127.0.0.1



#重启redis

sudo /etc/init.d/redis-server restart



#使用密码，指定host来登录服务器

redis-cli -a euraxluo -h 127.1



```



## python操作redis

参考博客![https://www.cnblogs.com/koka24/p/5841826.html]





```python

import redis

```



### 连接数据库





```python

try:

    r = redis.Redis(host='127.0.0.1',password='euraxluo',port=6379,db=0)

    r.keys()

    print("connected success.")

except:

    print("could not connect to redis.")



```



    connected success.





### 通过连接池连接





```python

try:

    pool = redis.ConnectionPool(host='127.0.0.1',password='euraxluo',port=6379,db=0)

    r = redis.Redis(connection_pool=pool)

    r.keys()

    print("connected success.")

except:

    print("could not connect to redis.")





```



    connected success.





## 通过python操作redis





```python

#bytes to str

def b2s(value):

    return bytes.decode(value)



```



### string操作



#### set(name, value, ex=None, px=None, nx=False, xx=False)

```

ex，过期时间（秒）

px，过期时间（毫秒）

nx，如果设置为True，则只有name不存在时，当前set操作才执行,同setnx(name, value)

xx，如果设置为True，则只有name存在时，当前set操作才执行

```





```python

r.set('k2','10秒',10,nx=True)#添加一个记录，过期时间为20秒，如果k2不存在，就执行这个操作

r.psetex('k3', 2000, '2000毫秒')#设置过期时间为毫秒

r.setex('k1',2,"2s later")#过期时间为秒

b2s(r.get('k3'))#获取值

```









    '2000毫秒'







#### 批量添加记录：mset({key:value,*args});批量获取值：mget(key,*args)





```python

r.mset({'k7':'value5','k8':'value6'})#批量添加记录

r.mget('k1','k2','k3','k4','k5','k6','k7','k8')#批量获取值



```









    [b'2s later',
    
     b'10\xe7\xa7\x92',
    
     b'2000\xe6\xaf\xab\xe7\xa7\x92',
    
     None,
    
     None,
    
     None,
    
     b'value5',
    
     b'value6']







#### getset(name,value) 设置新值，打印旧值





```python

r.getset('k7','new')

```









    b'value5'







#### getrange(key, start, end) 根据字节获取子序列





```python

r.getrange('k8',0,-2)

```









    b'value'







#### setrange(name, offset, value) 修改字符串内容，从指定字符串索引开始向后替换，如果新值太长时，则向后添加





```python

r.set("name","zhangsan")

r.setrange("name",1,"z")

print(r.get("name")) #输出:zzangsan

r.setrange("name",6,"zzzzzzz")

print(r.get("name")) #输出:zzangszzzzzzz

```



    b'zzangsan'
    
    b'zzangszzzzzzz'





#### setbit(name, offset, value)对二进制表示位进行操作;getbit(name, offset) 获取name对应值的二进制中某位的值(0或1)

```

name，redis的name

offset，位的索引（将值对应的ASCII码变换成二进制后再进行索引）

value，值只能是 1 或 0

```





```python

str='123'

r.set('k1',str)

for i in str:

    print(i,ord(i),bin(ord(i)))#1字符串，ascii码，ascii二进制表示

```



    1 49 0b110001
    
    2 50 0b110010
    
    3 51 0b110011







```python

r.setbit('k1',6,1)#把第7位变成1

r.get('k1')

```









    b'323'









```python

r.getbit('k1',6)

```









    1







#### bitcount(key, start=None, end=None) 获取对应二进制中1的个数

```

key:Redis的name

start:字节起始位置

end:字节结束位置

```





```python

r.bitcount('k1',start=0,end=0)

```









    4







#### strlen(name) 返回name对应值的字节长度





```python

r.set('k2',"飒飒")#一个中文3个字节

r.strlen('k2')

```









    6







#### incr(self, name, amount=1)自增整数，incrbyfloat(self, name, amount=1.0)自增浮点数，decr(self, name, amount=1)自减整数





```python

r.incr("k1",amount=2)#可以对str类型的整数进行自增

```









    325









```python

r.set('k2','123.1')

r.incrbyfloat('k2',amount=1.1)#可以对str类型的浮点数进行自增

#r.decrbyfloat('k2',amount=1.1) 没有这个东西

```









    124.2









```python

r.decr('k1', amount=1)

```









    324







#### append(name,value)





```python

r.append("k3","str")#返回的是append后的value的长度

r.get('k3')

```









    b'2000\xe6\xaf\xab\xe7\xa7\x92str'







### HASH操作

redis中的Hash在内存中一个name对应一个dic来存储



#### hset(name,key,value)在name对应的hash中设置一个k-v;hget(name,key);hgetall(name)





```python

r.hset('h1','name','euraxluo')

r.hgetall('h1')

```









    {b'name': b'euraxluo'}







#### hmset(name,mapping) 在name对应的hash中用dic来填充;hmget(name, keys, *args) 从hash中获取多个key值





```python

dic={"name":"euraxluo","age":"13"}

r.hmset('h1',dic)

r.hgetall('h1')

```









    {b'name': b'euraxluo', b'age': b'13'}







#### hlen(name)获取hash中键值对的个数、hkeys(name)获取hash中所有的key的值、hvals(name)获取hash中所有的value的值





```python

r.hlen('h1')

```









    2









```python

r.hkeys('h1')

```









    [b'name', b'age']









```python

r.hvals('h1')

```









    [b'euraxluo', b'13']







#### hexists(name, key) 检查name对应的hash是否存在当前传入的key





```python

r.hexists('h1','sex')

```









    False







#### hdel(name,*keys) 删除指定name对应的keys对应的k-v





```python

r.hdel('h1','sex')

```









    0









```python

r.hdel('h1','age')

```









    1







#### hincrby(name, key, amount=1) 自增hash中key对应的值，不存在则创建key=amount(amount为整数)





```python

dic={"name":"euraxluo","age":"13",'test':'13.1'}

r.hmset('h2',dic)

r.hincrby('h2','age',amount=2)

r.hgetall('h2')

```









    {b'name': b'euraxluo', b'age': b'15', b'test': b'13.1'}







#### hincrbyfloat(name, key, amount=1.0) 自增hash中key对应的值，不存在则创建key=amount(amount为浮点数)





```python

r.hincrbyfloat('h2','test',amount=2.1)

r.hgetall('h2')

```









    {b'name': b'euraxluo', b'age': b'15', b'test': b'15.2'}







#### hscan(name, cursor=0, match=None, count=None)

增量式迭代获取，对于数据大的数据非常有用，hscan可以实现分片的获取数据，并非一次性将数据全部获取完，避免内存被撑爆

```

name，redis的name

cursor，游标（基于游标分批取获取数据）

match，匹配指定key，默认None 表示所有的key

count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数

```





```python

r.hscan('h2',cursor=1,match='*e*',count=2)

```









    (0, {b'name': b'euraxluo', b'age': b'15', b'test': b'15.2'})







#### hscan_iter(name, match=None, count=None)

利用yield封装hscan创建生成器，实现分批去redis中获取数据

```

match，匹配指定key，默认None 表示所有的key

count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数

```





```python

for i in r.hscan_iter('h2',match='*e*',count=2):print(i)

```



    (b'name', b'euraxluo')
    
    (b'age', b'15')
    
    (b'test', b'15.2')





### List操作

redis中的List在在内存中按照一个name对应一个List来存储。



#### lpush(name,values)在name对应的list中添加元素，每个新的元素都添加到列表的最左边;rpush(name, values) 表示从右向左操作





```python

r.lpush('l1','a')

```









    2







#### lpushx(name,value)在name对应的list中添加元素，只有name已经存在时，值添加到列表的最左边; rpushx(name, value) 表示从右向左操作





```python

r.lpushx('l1','b')

```









    3







#### llen(name)name对应的list的元素个数





```python

r.llen('l1')

```









    3







#### linsert(name, where, refvalue, value))在name对应的列表的某一个值前或后插入一个新值

```

name，redis的name

where，BEFORE或AFTER

refvalue，标杆值，即：在它前后插入数据

value，要插入的数据

```





```python

r.linsert('l1','BEFORE','b','c1')

r.linsert('l1','AFTER','b','c2')

```









    5







#### lset(name, index, value)对name对应的list中的某一个索引位置重新赋值

```

name，redis的name

index，list的索引位置

value，要设置的值

```







```python

r.lset('l1','0','c')

r.lrange('l1',0,-1)

```









    [b'c', b'b', b'c2', b'a', b'c']







#### lrem(name, num, value)在name对应的list中删除指定的值

```

name，redis的name

value，要删除的值

num，  num=0，删除列表中所有的指定值；

       num=2,从前到后，删除2个；

       num=-2,从后向前，删除2个

```







```python

r.lrem('l1',2,'c')

```









    2







#### lpop(name)在name对应的列表的左侧获取第一个元素并在列表中移除，返回值则是第一个元素;rpop(name) 表示从右向左操作





```python

r.lpop('l1')

r.lrange('l1',0,-1)

```









    [b'c2', b'a']







####  ltrim(name, start, end)在name对应的列表中移除没有在start-end索引之间的值

```

name，redis的name

start，索引的起始位置

end，索引结束位置

```





```python

r.ltrim('l1',0,-2)

r.lrange('l1',0,-1)

```









    [b'c2']







#### rpoplpush(src, dst)从一个列表取出最右边的元素，同时将其添加至另一个列表的最左边

```

src，要取数据的列表的name

dst，要添加数据的列表的name

```





```python

r.lpush('l2','c')

r.rpop('l1')

r.rpoplpush('l2','l1')

r.lrange('l1',0,-1)

```









    [b'c']







#### blpop(keys, timeout)将多个列表排列，按照从左到右去pop对应列表的元素;brpop(keys, timeout)，从右向左获取数据

```

keys，redis的name的集合

timeout，超时时间，当元素所有列表的元素获取完之后，阻塞等待列表内有数据的时间（秒）, 0 表示永远阻塞

```





```python

r.lpush("l3", '11', '22', '33')

r.lpush("l4", '44', '55', '66')

r.brpop(['l3','l4'],timeout=1)

```









    (b'l3', b'33')







#### lindex(name, index)在name对应的列表中根据索引获取列表元素







```python

r.lindex('l3',1)

```









    b'22'







#### 增量迭代

由于redis类库中没有提供对列表元素的增量迭代，如果想要循环name对应的列表的所有元素，那么就需要：

>1、获取name对应的所有列表



>2、循环列表



但是，如果列表非常大，那么就有可能在第一步时就将程序的内容撑爆，所有有必要自定义一个增量迭代的功能：





```python

def list_iter(name):

    """

    自定义redis列表增量迭代

    :param name: redis中的name，即：迭代name对应的列表

    :return: yield 返回 列表元素

    """

    list_count = r.llen(name)

    for index in range(list_count):

        yield r.lindex(name, index)

```





```python

for item in list_iter('l3'):print(item)

```



    b'33'
    
    b'22'
    
    b'11'
    
    b'33'
    
    b'22'
    
    b'11'
    
    b'33'
    
    b'22'
    
    b'11'
    
    b'33'
    
    b'22'
    
    b'11'
    
    b'33'
    
    b'22'
    
    b'11'
    
    b'33'
    
    b'22'
    
    b'11'
    
    b'33'
    
    b'22'
    
    b'11'
    
    b'33'
    
    b'22'
    
    b'11'





### Set操作，Set集合就是不允许重复的列表



#### sadd(name,values) name对应的集合中添加元素





```python

r.sadd('s2',"value1","2sasa","2sasa","2ssss")

```









    1







#### scard(name) 获取name对应的集合中元素个数





```python

r.scard('s1')

```









    0







#### sdiff(keys, *args)在第一个name对应的集合中且不在其他name对应的集合的元素集合





```python

r.sdiff('s1','s2')#s1对应的集合中且不在其他name对应的集合的元素集合

```









    set()







#### sdiffstore(dest, keys, *args)获取第一个name对应的集合中且不在其他name对应的集合，再将其新加入到dest对应的集合中





```python

r.sdiffstore('s3','s1','s2')

r.smembers('s3')

```









    set()







#### sinter(keys, *args)获取多个name对应集合的并集





```python

r.sinter('s1','s2')

```









    set()







#### sinterstore(dest, keys, *args)获取多一个name对应集合的并集，再讲其加入到dest对应的集合中





```python

r.sinterstore('s4','s1','s2')

r.smembers('s4')

```









    set()







#### sismember(name, value)检查value是否是name对应的集合的成员





```python

r.sismember('s1','value1')

```









    False







#### smembers(name)获取name对应的集合的所有成员





```python

r.smembers('s1')

```









    set()







#### smove(src, dst, value)将某个成员从一个集合中移动到另外一个集合





```python

r.smove('s1','s2','ssss')

r.smembers('s2')

```









    {b'2sasa', b'2ssss', b'ssss', b'value1'}







#### spop(name)从集合的右侧（尾部）移除一个成员，并将其返回





```python

r.spop('s1')

r.smembers('s1')

```









    set()







#### srandmember(name, numbers)从name对应的集合中随机获取 numbers 个元素







```python

r.srandmember('s2','2')

```









    [b'2ssss', b'2sasa']







#### srem(name, values)在name对应的集合中删除某些值







```python

r.srem('s2','2ssss')

r.smembers('s2')

```









    {b'2sasa', b'ssss', b'value1'}







#### sunion(keys, *args)获取多一个name对应的集合的并集







```python

r.sunion('s1','s2','s3')

```









    {b'2sasa', b'ssss', b'value1'}







#### sunionstore(dest,keys, *args)获取多一个name对应的集合的并集，并将结果保存到dest对应的集合中







```python

r.sunionstore('d4','s1','s2','s3')

r.smembers('d4')

```









    {b'2sasa', b'ssss', b'value1'}







#### sscan(name, cursor=0, match=None, count=None);sscan_iter(name, match=None, count=None)同字符串的操作，用于增量迭代分批获取元素，避免内存消耗太大





```python

for i in r.sscan_iter('s2',match='*v*',count=2):print(i)

```



    b'value1'





### 有序集合，在集合的基础上，为每元素排序

元素的排序需要根据另外一个值来进行比较，所以，对于有序集合，每一个元素有两个值，即：值和分数，分数专门用来做排序。







#### zadd(name, mapping, nn,nx)在name对应的有序集合中添加元素

```

zadd('zz', 'n1', 1, 'n2', 2)

或

zadd('zz', n1=11, n2=22)

```





```python

dic={'n1':1,'n2':2}

r.zadd('zz',dic)

```









    2









```python



```



#### zcard(name)获取name对应的有序集合元素的数量





```python

r.zcard('zz')

```









    2







#### zcount(name, min, max)获取name对应的有序集合中分数 在 [min,max] 之间的个数







```python

r.zcount('zz',0,1)

```









    1







#### zincrby(name, value, amount)自增name对应的有序集合的 name 对应的分数







```python

r.zincrby('zz',value='n3',amount=1)

```









    1.0







#### zrange( name, start, end, desc=False, withscores=False, score_cast_func=float)按照索引范围获取 name对应的有序集合的元素

```

name，redis的name

start，有序集合索引起始位置（非分数）

end，有序集合索引结束位置（非分数）

desc，排序规则，默认按照分数从小到大排序

withscores，是否获取元素的分数，默认只获取元素的值

score_cast_func，对分数进行数据转换的函数

```





```python

r.zrange('zz',0,-1,desc=True,withscores=True)#desc=true,排序规则从大到小

```









    [(b'n2', 2.0), (b'n3', 1.0), (b'n1', 1.0)]







#### zrevrange(name, start, end, withscores=False, score_cast_func=float) 从大到小排序





```python

r.zrevrange('zz',0,-1,withscores=True)

```









    [(b'n2', 2.0), (b'n3', 1.0), (b'n1', 1.0)]







#### zrangebyscore(name, min, max, start=None, num=None, withscores=False, score_cast_func=float 按照分数范围获取name对应的有序集合的元素

#### zrevrangebyscore(name, max, min, start=None, num=None, withscores=False) 从大到小排序





```python

r.zrangebyscore('zz',1,2,withscores=True)

```









    [(b'n1', 1.0), (b'n3', 1.0), (b'n2', 2.0)]







#### zrank(name, value)

获取某个值在 name对应的有序集合中的排行（从 0 开始）

#### zrevrank(name, value)，从大到小排序





```python

r.zrank('zz','n3')#n3最大

```









    1







####  zrangebylex(name, min, max, start=None, num=None)

当有序集合的所有成员都具有相同的分值时，有序集合的元素会根据成员的 值 （lexicographical ordering）来进行排序，而这个命令则可以返回给定的有序集合键 key 中， 元素的值介于 min 和 max 之间的成员



对集合中的每个成员进行逐个字节的对比（byte-by-byte compare）， 并按照从低到高的顺序， 返回排序后的集合成员。 如果两个字符串有一部分内容是相同的话， 那么命令会认为较长的字符串比较短的字符串要大

```

name，redis的name

min，左区间（值）。 + 表示正无限； - 表示负无限； ( 表示开区间； [ 则表示闭区间

min，右区间（值）

start，对结果进行分片处理，索引位置

num，对结果进行分片处理，索引后面的num个元素

```

#### zrevrangebylex(name, max, min, start=None, num=None)  从大到小排序





```python

dic={'aa':0,'ba':0,'ca':0,'da':0,'ea':0,'fa':0}

r.zadd('z1',dic)

r.zrangebylex('z1', "-", "[fa]")



```









    [b'aa', b'ba', b'ca', b'da', b'ea', b'fa']







#### zrem(name, values) 删除name对应的有序集合中值是values的成员





```python

r.zrem('z1', 'fa', 'ea')

```









    2







#### zremrangebyrank(name, min, max) 根据排行范围删除





```python

r.zremrangebyrank('zz',0,1)

```









    2







#### zremrangebyscore(name, min, max)根据分数范围删除





```python

r.zremrangebyscore('z1',0,3)

```









    4







#### zremrangebylex(name, min, max)根据值返回删除

ZREMRANGEBYLEX 删除名称按字典由低到高排序成员之间所有成员。

不要在成员分数不同的有序集合中使用此命令, 因为它是基于分数一致的有序集合设计的,如果使用,会导致删除的结果不正确。

待删除的有序集合中,分数最好相同,否则删除结果会不正常。





```python

dic={'aa':0,'ba':0,'ca':0,'da':0,'ea':0,'fa':0}

r.zadd('z2',dic)

r.zremrangebylex('z2','[aa','(ea')

r.zrangebylex('z2','-','+')

```









    [b'ea', b'fa']







#### zscore(name, value)获取name对应有序集合中 value 对应的分数





```python

r.zscore('z2',value='ea')

```









    0.0







#### zinterstore(dest, keys, aggregate=None)获取两个有序集合的交集，如果遇到相同值不同分数，则按照aggregate进行操作





```python

r.zinterstore('z1','z2',aggregate='MAX')

```









    0







#### zunionstore(dest, keys, aggregate=None)获取两个有序集合的并集，如果遇到相同值不同分数，则按照aggregate进行操作

>aggregate的值为:  SUM  MIN  MAX





```python

r.zinterstore('z1','z2',aggregate='MAX')

```









    0







#### zscan(name, cursor=0, match=None, count=None, score_cast_func=float)

#### zscan_iter(name, match=None, count=None,score_cast_func=float)

同字符串相似，相较于字符串新增score_cast_func，用来对分数进行操作



### 其他常用操作



#### delete(*names)根据name删除redis中的任意数据类型,返回值为删除的个数





```python

r.delete("k4",'k2','k3')

```









    1







#### exists(name)若 name 存在返回 1 ，否则返回 0 。





```python

r.exists('11')

```









    0







#### keys(pattern='*')根据pattern获取redis的name

```

KEYS * 匹配数据库中所有 key 。

KEYS h?llo 匹配 hello ， hallo 和 hxllo 等。

KEYS h*llo 匹配 hllo 和 heeeeello 等。

KEYS h[ae]llo 匹配 hello 和 hallo ，但不匹配 hillo

```





```python

r.keys("*")

```









    [b'name',
    
     b'l3',
    
     b'k7',
    
     b's2',
    
     b'z2',
    
     b'z3',
    
     b'k1',
    
     b'h2',
    
     b'd4',
    
     b'l4',
    
     b'zz',
    
     b'l1',
    
     b'k8',
    
     b'h1',
    
     b'l2']







#### expire(name ,time)为某个redis的某个name设置超时时间





```python

r.expire('name',2)

```









    True







#### rename(src, dst)对redis的name重命名为





```python

r.rename('zz','z3')

```









    True







#### move(name, db))将redis的某个值移动到指定的db下





```python

print(r.hkeys('h1'))

r.move('h1',1)

r.hkeys('h1')

```



    [b'name']











    [b'name']







#### randomkey()随机获取一个redis的name（不删除）





```python

r.randomkey()

```









    b'l3'









#### type(name) 获取name对应值的类型





```python

r.type('d4')

```









    b'set'







#### scan(cursor=0, match=None, count=None)

#### scan_iter(match=None, count=None)

同字符串操作，用于增量迭代获取key

