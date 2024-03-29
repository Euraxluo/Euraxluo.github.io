+++
title = "JDBC3"
date = "2018-12-20"
description = "JDBC"
featured = false
categories = [
  "java"
]
tags = [
  "JDBC"
]
series = [
  "JDBC"
]
images = [
]

+++



### 1. execute,executeQuery,executeUdate的区别
JDBCTM中Statement接口提供的execute,executeQuery,executeUdate之间的区别:
1. executeQuery:

    用于产生单个结果集的语句,例如SELECT语句,使用最多的方法

2. executeUpdate:

    用于执行INSERT,UPDATE,DELETE语句以及DDL语言,返回值是一个整数,指示受影响的行

3. execute:

    用于执行返回多个结果集,多个更新技术或者两者皆有的语句



### 2. SQL注入

防范措施:

1. 使用动态封装的方式会导致SQL注入的风险,我们应该使用prepareStatement提供的参数化SQL

2. 严格的数据库权限管理

	>仅给web应用访问数据库的最小权限

	>避免Drop table等权限



3. 封装数据库错误

	>不要直接将后端数据库异常信息暴露给用户

	>对后端遗产信息进行必要的封装,避免用户直接看到后端异常



4. 机密信息禁止明文存储

	>涉密信息需要加密处理

	>使用AES_ENCRYPT/AES_DECRYPT加密和解密



## 事务:{是并发控制的基本单位,指作为单个逻辑工作单位执行的一系列操作,而这些逻辑工作单元需要满足ACID特性}

ACID:原子性,一致性,隔离性,持久性  



### jdbc事务控制

connection:

>`.setAutoCommit('false')`开启事务

>`.commit()`事务执行结束提交事务

>`.rollback()`回滚到事务开始之前的状态



eg:

```java

try{

    conn = JDCBUtil.getConnection;

    conn.setAutoCommit(false);

    /**

    *sql语句

    * 

    conn.commit();

}catch(){

    //如果出错,事务回滚

    conn.rollback();

}

```



### 事务并发执行

1. 脏读:读取一个事务未提交的更新

2. 不可重复读:一个失误读取到另一个事务的更新,两次读取的结果包含的行记录的值不一样

3. 幻读:两次读取的结果包含的行记录不一样



#### 事务隔离级别



1. 读未提交{允许脏读}

2. 读提交{不允许脏读,允许重复读}

3. 重复读{不允许不可重复读,可以幻读}

4. 串行化{严格的并发控制}{如果有一个连接的隔离级别设置为了串行化 ，那么谁先打开了事务， 谁就有了先执行的权利， 谁后打开事务，谁就只能得着，等前面的那个事务，提交或者回滚后，才能执行。  但是这种隔离级别一般比较少用。 容易造成性能上的问题。 效率比较低。}



#### 例子

1. 查看隔离级别:`select @@tx_isolation`

2. 设置隔离级别为读未更新:`set session transaction isolation level read uncommitted;`

3. 开启事务:`start transaction`

4. 按效率划分,从高到低:

>读未更新>读已提交>可重复读>可串行化



5. 按拦截成都,从高到低

>可串行化 > 可重复读 > 读已提交 >  读未提交



6. 默认隔离级别:

>mySql:可重复读

>Oracle:读已提交



7. 在JDBC中使用事务

Connection

>`.getTranactionlsolation()`获取事务隔离级别

>`.setTransactionlsolation`设置事务隔离级别





##　死锁

### MySql中的锁:

|已有锁\预加锁|X{排它锁}|S{共享锁}|

|:--:|:--:|:--:|

|X|冲突|冲突|

|S|冲突|兼容|



### 加锁方式

1. 外部加锁:

>由应用程序添加,锁依赖关系较容易分析

>共享锁:`select * from table lock in share mode`

>排它锁:`select * from table for update`{解决丢失更新}



2. 内部加锁

>为了实现ACID特性,由数据库系统内部自动添加

>加锁规则繁琐,与SQL执行计划,事务隔离级别,表索引结构有关



3. SQL持有锁的情况

	快照读

	>Innodb实现了多版本控制(MVCC),支持不加锁快照读

	>`Select * from table where`

	>能够保证同一个Select结果集是一致的

	>不能够保证同一个事务内部,Select语句和其他语句的数据一致性,如果业务需要,应该通过外部显式加锁



4. 分析死锁的原因,排查出死锁的SQL

	`show engine innodb status`

	会反馈出发生死锁是等待的SQL

