+++
title = "MyBatis"
date = "2018-10-29"
description = "MyBatis"
featured = false
categories = [
  "Java"
]
tags = [
  "MyBatis"
]
series = [
  "MyBatis"
]
images = [
]

+++


# MyBatis
1. 一个ORM框架,(不直接建立java对象到关系数据库表数据的映射,而是建立对对象的操作方法到SQL的映射)支持自定义SQL,存储过程和高级映射的持久化框架
2. 使用XML或者注解配置

3. 能够映射基本数据元素,接口,Java对象到数据库



## ORM(Object/Relation Mapping)

作用:持久化类与数据库表之间的映射关系,让我们对持久化对象的操作自动转换成对关系数据库操作



通过映射,我们把关系数据库中的每一行都映射为对象,数据库的每一列就映射成了对象的属性



##　三层架构：

１.	接口层(数据查询接口,数据新增接口,数据更新接口,数据删除接口,获取配置接口)

２.	数据处理层(参数映射,SQL解析,SQL执行,结果映射)

３.	基础支撑层(连接管理，事务管理，配置加载，缓存处理)



## 工作流机制:

1. 根据XM(xml中定义了连接的地址,以及对象和SQL的映射和关系)L或者注解加载SQL语句,参数映射,结果映射到内存

2. 应用程序调用API传入参数和SQL ID

3. MyBatis 自动生成SQL语句完成数据库访问,转换执行结构返回应用程序



###### 例如,完成一个数据库查询

1. 加载配置文件

>应用配置文件

>关联映射文件



2. sqlSession

>生成SqlSessionFactory

>获取SqlSession



3. 执行查询

>Session 执行SQL
