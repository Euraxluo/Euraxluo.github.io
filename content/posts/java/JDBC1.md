+++
title = "JDBC1"
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


## jdbc 

> JAVA Database Connectivity java 数据库连接


* 为什么会出现JDBC



> SUN公司提供的一种数据库访问规则、规范, 由于数据库种类较多，并且java语言使用比较广泛，sun公司就提供了一种规范，让其他的数据库提供商去实现底层的访问规则。 我们的java程序只要使用sun公司提供的jdbc驱动即可。



jdbc是一种接口规范

优势:



1. 简单

2. 快捷

3. 移植性

4. 框架(在jdbc的基础上开发更好的框架)



jdbc Manager的上层JDBC API负责与java Application通信,JDBC Driver API 负责与具体的数据库通信(由数据库厂商开发和提供)



### API介绍:

Driver:接口,定义了各个驱动程序都必须要实现的功能



DriverManager:Driver的管理类

用户通过`Class.forname(DriverName)`可以向DriverManager注册一个驱动程序,然后使用`getConnection`来建立物理连接,基于物理连接没使用SQL语句



eg:

```java

Class.forName(JDBC_DRIVER);

conn= DriverManager.getConnection(DB_URL,USER,PASS);

//DB_URL:链接,USER:用户名,PASS:密码

//例如

conn= DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/test"

,USER,PASS);

//jdbc:mysql://ip:端口/数据库名;协议:子协议:主机ip:端口/数据库

```

#### 常用的3种格式

1. mysql

`jdbc:mysql://<ip>:<port>/database`

2. oracle

`jdbc:oracle:thin:@<ip>:<port>:database`

3. sqlserver

`jdbc:microsoft:sqlserver://<ip>:<port>;DatabaseName=database`



### Connection 常用方法

1. Statement对象

	1)	创建(其实是一个sql语句的容器

	​	`Statement stmt = conn.createStatement();`

	2)	使用(使用Statement对象执行sql语句,返回结果为ResultSet/int):

	​	`ResultSet rs = stmt.executeQuery("select userName from user")`

	​	查询结果是一个ResultSet对象

2. ResultSet对象(Statement对象的查询结果)

	1)	rs.next():将光标移动到下一行(默认在第一行)

	2)	rs.previous():将光标移动到上一行

	3)	rs.absolute():将光标定位到某一行

	4)	rs.beforeFirst():直接将光标定位到第一行的前一行

	5)	rs.afterLast():直接将光标移动到最后一行

	6)	rs.getString(ColumnName/Index):通过列名或者列序号取值

	7)	rs.getInt(ColumnName/Index):通过列名或者列序号取值

	8)	rs.getObject(ColumnName/Index):通过列名或者列序号取值



### 异常捕获

sql会抛出SQLException异常,我们通过捕获这个来处理异常 



### 构建步骤

1. 装在驱动程序

2. 建立数据库连接

3. 执行SQL语句

4. 获取执行结果

5. 清理环境



eg:

```java



package com.bean;



import java.sql.*;



public class Testjdbc {

    static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";

    static final String DB_URL = "jdbc:mysql://localhost/test";

    static final String USER = "euraxluo";

    static final String PASSWORD = "1234";

    public static void test() throws ClassNotFoundException{

        Connection conn = null;

        Statement stmt = null;

        ResultSet rs = null;

        //1.装载驱动程序

        Class.forName(JDBC_DRIVER);

        //2.建立数据库物理连接

        try {

            conn = DriverManager.getConnection(DB_URL,USER,PASSWORD);

            //3.创建statement容器,执行sql语句

            stmt = conn.createStatement();

            rs = stmt.executeQuery("select * from user");

            //4.获取执行结果

            while(rs.next()){

            System.out.println(rs.getString("id")+":"+rs.getString("userName"));

            }

        } catch (SQLException e) {

            //异常处理

            e.printStackTrace();

        } finally {

            //关闭连接,清理环境

            try {

                if(conn != null)

                    conn.close();

                if(stmt != null)

                    stmt.close();

                if(rs != null)

                    rs.close();

            } catch (SQLException e) {

                e.printStackTrace();

            }

        }

    }



    public static void main(String[] args) throws ClassNotFoundException{

        test();

    }



}



```



### JDBC

工具类

1. 资源释放工作的整合



```java



public class JDBCUtil {



   

    public static void release(Connection conn,PreparedStatement ptmt,ResultSet rs){

        close(rs);

        close(conn);

        close(ptmt);

    }



    public static void close(ResultSet rs){

        try {

            if(rs != null)

                rs.close();

        } catch (SQLException e) {

            e.printStackTrace();

        }finally {

            rs = null;

        }

    }

    public static void close(PreparedStatement ptmt){

        try {

            if(ptmt != null)

                ptmt.close();

        } catch (SQLException e) {

            e.printStackTrace();

        }finally {

            ptmt = null;

        }

    }

    public static void close(Statement st) {

        try {

            if (st != null)

                st.close();

        } catch (SQLException e) {

            e.printStackTrace();

        } finally {

            st = null;

        }

    }



    private static void close(Connection conn){

        try {

            if(conn != null)

                conn.close();

        } catch (SQLException e) {

            e.printStackTrace();

        }finally {

            conn = null;

        }

    }



}

```







2. 驱动防二次注册





   	DriverManager.registerDriver(new com.mysql.jdbc.Driver());



   	Driver 这个类里面有静态代码块`java.sql.DriverManager.registerDriver(new Driver());`，一上来就执行了，所以等同于我们注册了两次驱动。 其实没这个必要的。

   	//静态代码块 ---> 类加载了，就执行。 





		最后形成以下代码即可。


​	

		Class.forName("com.mysql.jdbc.Driver");	



3. 也可把我们的数据库驱动的装载放到公共类中

```java



    public static Connection getSConn(){

        Connection conn = null;

        try {

            conn = DriverManager.getConnection(DB_URL2,USER2,PASSWORD);

        } catch (SQLException e) {

            e.printStackTrace();

        }

        return conn;

    }

    public static Connection getLConn(){

        Connection conn = null;

        try {

            conn = DriverManager.getConnection(DB_URL,USER,PASSWORD);

        } catch (SQLException e) {

            e.printStackTrace();

        }

        return conn;

    }

```

4. 创建 properties

    1)  在src底下声明一个文件 jdbc.properties ，里面的内容吐下：



  ```

  JDBC_DRIVER = com.mysql.jdbc.Driver

  JDBC_DRIVER2 = com.mysql.cj.jdbc.Driver

  DB_URL = jdbc:mysql://localhost/test

  DB_URL2 = jdbc:mysql://192.168.23.1:3306/test?serverTimezone=GMT

  USER = euraxluo

  USER2 = root

  PASSWORD = 1234

  FTLE_URL = IOTEST.txt

  ```

  2) 在工具类里面，使用静态代码块，读取属性





		static{
	
			try {
	
				//1. 创建一个属性配置对象
	
				Properties properties = new Properties();
	
				//InputStream is = new FileInputStream("jdbc.properties"); //对应文件位于工程根目录


​				 

				//使用类加载器，去读取src底下的资源文件。 后面在servlet  //对应文件位于src目录底下
	
				InputStream is = JDBCUtil.class.getClassLoader().getResourceAsStream("jdbc.properties");
	
				//导入输入流。
	
				properties.load(is);


​				

				//读取属性
	
				driverClass = properties.getProperty("driverClass");
	
				url = properties.getProperty("url");
	
				name = properties.getProperty("name");
	
				password = properties.getProperty("password");


​				

			} catch (Exception e) {
	
				e.printStackTrace();
	
			}
	
		}



​	



5. 我们在文档中可以看到一句话,就是说Class.forName(),驱动加载,jdbc4中自动帮我们完成了这一步骤
