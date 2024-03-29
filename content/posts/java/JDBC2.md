+++
title = "JDBC2"
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


## 业务场景1
1. 过滤条件比较弱,一次读出多条记录
2. 读取数据库表中的所有记录
3. 海量数据读取



这些都容易产生内存溢出,为了不使得内存溢出,我们采用游标的方式



### 游标:提供一种客户端读取部分服务器端结果集的机制

一个批次的大小为:Fetch Size



#### 游标的使用

1. 开启游标,DB_URL的处理(加上`useCursorFetch=true`)

eg:

`jdbc:mysql://<ip>:<port>/<database>?useCursorFetch=true`

2. 使用PreparedStatement接口

    `PreparedStatement`接口继承自`Statement`接口,我们可以使用`PreparedStatement`替代`Statement`



  这个接口要求创建时就要传入sql语句,但是这个sql语句,参数格式化.即过滤条件用问号表示,后续再用`PreparedStatement.setString()`和`PreparedStatement.setInt()`来设置过滤条件.还可以使用`PreparedStatement.setFetchSize()`设置游标的大小.即每次从数据库服务端取回记录的数量

eg:

```java

//使用prepareStatement()接口

ptmt = conn.prepareStatement("select * from user");

ptmt.setFetchSize(1);

rs = ptmt.executeQuery();



```



## 业务场景2

1. 读取的记录字段太大(例如博文)



也是会造成内存溢出,即使读取的记录很少



### 流方式

把大字段按照二进制流的方式,分成多个区间,每次只读取一个区间的内容



### 流方式的使用

1. 利用`ResultSet.getBinaryStream();`获取对象流

2. 生成一个外部文件,把对象流采用边读边写的方式写入文件



eg:

```java

while(rs2.next()){

                //5.获取对象流

                InputStream in = rs1.getBinaryStream("userName");

                //6.将对象流写入文件

                File f = new File(FTLE_URL);

                OutputStream out = null;

                try {

                    out = new FileOutputStream(f);

                    int temp = 0;

                    while((temp = in.read()) != -1){//边读边写

                        out.write(temp);

                        System.out.println(rs2.getString("id")+":"+rs2.getString("userName"));

                        System.out.println("---rs2--");

                    }

                    in.close();

                    out.close();

                } catch (IOException e) {

                    e.printStackTrace();

                }



            }

```



## 业务场景3

1. 大量数据插入操作



数据的插入操作太慢了



### 批处理

一次操作多个SQL语句



### 利用Statement的addBatch(),实现批处理

addBatch():把多个sql打包成一个Batch()

executeBatch():执行一个Batch

clearnBatch():清除Batch(),下次使用





eg:

``` java

stmt = conn.createStatement();

for (String item:users){

    stmt.addBatch("insert into user(id,userName) values("+item.id+","+item.user+")");

}

stmt.excuteBatch();

stmt.clearBatch();

```

## 业务场景4

1. 乱码



###　编码，字符集

1. 你需要先查看数据库的内部编码

2. 编码优先级

	Server<Database<Table<column;

3. jdbc编码设置

`DB_URL = DB_URL+"characterEncoding=utf8"
