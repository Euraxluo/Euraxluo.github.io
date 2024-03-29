+++
title = "MVC分层模型"
date = 2018-11-20
description = "MVC分层模型"
featured = false
categories = [
  "architecture design"
]
tags = [
  "mvc","architecture"
]
images = [
]
+++


# MVC分层模型


## DAO 模式初识




### PO(persistant object) 持久对象



在o/r映射的时候出现的概念，如果没有o/r映射，没有这个概念存在了。通常对应数据模型(数据库),本身还有部分业务逻辑的处理。可以看成是与数据库中的表相映射的java对象。最简单的PO就是对应数据库中某个表中的一条记录，多个记录可以用PO的集合。PO中应该不包含任何对数据库的操作。

最形象的理解就是一个PO就是数据库中的一条记录。

好处是可以把一条记录作为一个对象处理，可以方便的转为其它对象。



### VO(value object) 值对象

通常用于业务层之间的数据传递，和PO一样也是仅仅包含数据而已。但应是抽象出的业务对象,可以和表对应,也可以不,这根据业务的需要.个人觉得同TO(数据传输对象),在web上传递。

主要对应界面显示的数据对象。对于一个WEB页面，或者SWT、SWING的一个界面，用一个VO对象对应整个界面的值。



### TO(Transfer Object)，数据传输对象

在应用程序不同tie(关系)之间传输的对象



### BO(business object) 业务对象

从业务模型的角度看,见UML元件领域模型中的领域对象。封装业务逻辑的java对象,通过调用DAO方法,结合PO,VO进行业务操作。



### POJO(plain ordinary java object) 简单无规则java对象

纯的传统意义的java对象。就是说在一些Object/Relation Mapping工具中，能够做到维护数据库表记录的persisent object完全是一个符合Java Bean规范的纯Java对象，没有增加别的属性和方法。我的理解就是最基本的Java Bean，只有属性字段及setter和getter方法！。



### DTO（Data Transfer Object）：数据传输对象

这个概念来源于J2EE的设计模式，原来的目的是为了EJB的分布式应用提供粗粒度的数据实体，以减少分布式调用的次数，从而提高分布式调用的性能和降低网络负载，但在这里，我泛指用于展示层与服务层之间的数据传输对象。



### DAO(data access object) 数据访问对象

是一个sun的一个标准j2ee设计模式，这个模式中有个接口就是DAO，它负持久层的操作。为业务层提供接口。此对象用于访问数据库。通常和PO结合使用，DAO中包含了各种数据库的操作方法。通过它的方法,结合PO对数据库进行相关的操作。夹在业务逻辑与数据库资源中间。配合VO, 提供数据库的CRUD操作...

这个大家最熟悉，和上面几个O区别最大，基本没有互相转化的可能性和必要.

主要用来封装对数据库的访问。通过它可以把POJO持久化为PO，用PO组装出来VO、DTO





### O/R Mapper 对象/关系 映射

定义好所有的mapping之后，这个O/R Mapper可以帮我们做很多的工作。通过这些mappings,这个O/R Mapper可以生成所有的关于对象保存，删除，读取的SQL语句，我们不再需要写那么多行的DAL代码了。

实体Model(实体模式)

DAL(数据访问层)

IDAL(接口层)

DALFactory(类工厂)

BLL(业务逻辑层)

BOF Business Object Framework 业务对象框架

SOA Service Orient Architecture 面向服务的设计

EMF Eclipse Model Framework Eclipse建模框架



## DAO模式



分为四层

1. 客户层{包括Web浏览器,Applet}

2. Web{包括Servlet,JSP}

3. 业务逻辑{EJB}

4. 数据持久层{数据库}



DAO过程

客户端向服务器发出请求,服务器端由Web层进行接收,交给业务逻辑处理层来处理,对数据的访问由业务逻辑层去访问数据持久层



## 简单的例子和结构

com.demo

>utils(工具类,公共类,模板类)



>>数据库连接池工具类



>>>static:获取配置

>>>获取数据源

>>>获取连接

>>>获取配置信息



>>DAO操作模板类IDUS{不同的impl实现类都可以用}





>dao{大部分都是一些接口}

>

>>exception:定义异常处理的接口



>>>DAO异常类



>>>>传参异常...

>>>>等等



>>>其他异常类



>>DAO#接口#:定义IDUS操作,都会和DAO异常有关系



>>>学生DAO

>>>教师DAO

>>>课程DAO



>>impl:DAO接口的具体实现



>>>DAO的具体实现时,我们先优先采用组合后考虑继承

>>>StudentDAOImpl



>>>>insert:定义我们的UpdateSQL模板,从pojo中get字段,交给DAO操作模板类,完成Update操作(把结果交给匿名类)

>>>>select:QuerySQL模板+字段->模板类的Query == 完成select(把结果交给匿名类)



>>>其他实现类



>>refactor:内部匿名类



>>>RowMapper



>>>>把从数据库中获取的结果(resultSet对象)set到pojo中

>>>>将数据中的每一行数据封装成用户定义的类。



>>>RowCall



>pojo(数据持久层)



>>学生

>>教师

>>课程

>>其他表的实体类



>>>getXXX

>>>setXXX

>>>表字段



>DAOFactory(工厂类)



>>使用单例模式,采取反射机制获取具体的DAO及其实现类的对象,在业务层就直接利用工厂类调用接口,完成业务(对DAO和业务层解耦)





