+++
title = "XML"
date = "2020-10-22"
description = "java解析XML"
featured = false
categories = [
  "java"
]
tags = [
  "java"
]
series = [
  "java"
]
images = [
]
+++



# Xml 

## Xml


>eXtendsible  markup language  可扩展的标记语言



### XML 有什么用?



1. 可以用来保存数据



2. 可以用来做配置文件



3. 数据传输载体



## 定义xml



> 其实就是一个文件，文件的后缀为 .xml



###  文档声明

1. 简单声明， version : 解析这个xml的时候，使用什么版本的解析器解析

		`<?xml version="1.0" ?>`

2. encoding : 解析xml中的文字的时候，使用什么编码来翻译

		`<?xml version="1.0" encoding="gbk" ?>`

3. standalone  : no - 该文档会依赖关联其他文档 ，  yes-- 这是一个独立的文档

		`<?xml version="1.0" encoding="gbk" standalone="no" ?>`



### encoding详解

	在解析这个xml的时候，使用什么编码去解析。   ---解码。 



文本存储时不直接存储文字， 而是存储这些文字对应的二进制 。 那么这些文字对应的二进制到底是多少呢？ 根据文件使用的编码 来得到。 



> 默认文件保存的时候，使用的是GBK的编码保存。 



所以要想让我们的xml能够正常的显示中文,解决方法:



1. 让encoding也是GBK 或者 gb2312 . 



2. 如果encoding是 utf-8 ， 那么保存文件的时候也必须使用utf-8



3. 保存的时候见到的ANSI 对应的其实是我们的本地编码 GBK。



为了通用，建议使用UTF-8编码保存，以及encoding 都是 utf-8





### 元素定义（标签）



1.  其实就是里面的标签， <> 括起来的都叫元素 。 成对出现。  如下： 

`<stu> </stu>`



2.  文档声明下来的第一个元素叫做根元素 (根标签)



3.  标签里面可以嵌套标签



4.  空标签:既是开始也是结束。 一般配合属性来用。

`<age/>`



eg:

```xml

		<stu>

			<name>张三</name>

			<age/>

		</stu>

```

5. 标签可以自定义。 

XML 元素必须遵循以下命名规则：

   ​	1. 名称可以含字母、数字以及其他的字符 

   ​	2. 名称不能以数字或者标点符号开始 

   ​	3. 名称不能以字符 “xml”（或者 XML、Xml）开始 

   ​	4. 名称不能包含空格 

   ​	5. 命名尽量简单，做到见名知义





### 简单元素  & 复杂元素 



* 简单元素 



> 元素里面包含了普通的文字



* 复杂元素



> 元素里面还可以嵌套其他的元素





### 属性的定义



> 定义在元素里面， <元素名称  属性名称="属性的值"></元素名称>

```xmlxml

		<stus>

			<stu id="10086">

				<name>张三</name>

				<age>18</age>

			</stu>

			<stu id="10087">

				<name>李四</name>

				<age>28</age>

			</stu>

		</stus>





```

## xml注释：



> 与html的注释一样。 

｀<!-- --> ｀

如： 



```xml

		<?xml version="1.0" encoding="UTF-8"?>

		<!-- 

			//这里有两个学生

			//一个学生，名字叫张三， 年龄18岁， 学号：10086

			//另外一个学生叫李四  。。。

		 -->

```

> xml的注释，不允许放置在文档的第一行。 必须在文档声明的下面。



## CDATA区



####　非法字符



  严格地讲，在 XML 中仅有字符 "<"和"&" 是非法的。省略号、引号和大于号是合法的，但是把它们替换为实体引用是个好的习惯。 

```xml

  <   &lt;

  &   &amp;

  "   &quot;

```

如果某段字符串里面有过多的字符， 并且里面包含了类似标签或者关键字的这种文字，不想让xml的解析器去解析。 那么可以使用CDATA来包装。  不过这个CDATA 一般比较少看到。 通常在服务器给客户端返回数据的时候。

`<des><![CDATA[<a href="http://www.baidu.com">我爱黑马训练营</a>]]></des>`





## XML 解析



> 其实就是获取元素里面的字符数据或者属性数据。



### XML解析方式(面试常问)



> 有很多种，但是常用的有两种。



* DOM:把所有的文件全部读取到内存中,形成树状结构.整个文档称为document对象.,属性对应Attribute对象,所有的元素节点对应Element对象,文本也可以称为Text对象 ,以上所有对象都可以称为Node节点,如果xml特别大,就会造成内存溢出.优点:可以对文档进行增删操作



* SAX:Simple API for XML 基于事件驱动,读取一行,解析一行,不会造成内存泄漏,不可以增删,只能查询 



![icon](img/parse_type.png)



### 针对这两种解析方式的API



> 一些组织或者公司， 针对以上两种解析方式， 给出的解决方案有哪些？

>

> 1. jaxp  sun公司。 比较繁琐

2. jdom

3. dom4j  使用比较广泛,对SAX进行了增强,也可以完成增删操作 



### Dom4j 基本用法

```xml

		element.element("stu") ;// 返回该元素下的第一个stu元素

		element.elements();// 返回该元素下的所有子元素。 

```

1. 创建SaxReader对象



   `SAXReader reader= newSAXReader();`



2. 指定解析的xml



   `Document document = reader.read(path|file|inputStream);`



3. 获取根元素。



   `Elemennt rootElement = document.getRootElement();`



4. 根据根元素获取子元素或者下面的子孙元素



   `rootElement.element("age") `

   `rootElement.element("stu").element("age").getText();`



```xml

		try {

			//1. 创建sax读取对象

			SAXReader reader = new SAXReader(); //jdbc -- classloader

			//2. 指定解析的xml源

			Document  document  = reader.read(new File("src/xml/stus.xml"));

			

			//3. 得到元素、

			//得到根元素

			Element rootElement= document.getRootElement();

			

			//获取根元素下面的子元素 age

		//rootElement.element("age") 

			//System.out.println(rootElement.element("stu").element("age").getText());

			//获取根元素下面的所有子元素 。 stu元素

			List<Element> elements = rootElement.elements();

			//遍历所有的stu元素

			for (Element element : elements) {

				//获取stu元素下面的name元素

				String name = element.element("name").getText();

				String age = element.element("age").getText();

				String address = element.element("address").getText();

				System.out.println("name="+name+"==age+"+age+"==address="+address);

			}

			

		} catch (Exception e) {

			e.printStackTrace();

		}

```



SaxReader 创建好对象 。  



DocumentElement



1. 看文档



2. 记住关键字 。



3. 有对象先点一下。



4. 看一下方法的返回值。 



5. 根据平时的积累。  getXXX setXXX 





### Dom4j 的 Xpath使用



>  dom4j里面支持Xpath的写法。 xpath其实是xml的路径语言，支持我们在解析xml的时候，能够快速的定位到具体的某一个元素。在爬虫中经常使用.



1. 添加jar包依赖 



   jaxen-1.1-beta-6.jar



2. 在查找指定节点的时候，根据XPath语法规则来查找





```xml

			//要想使用Xpath， 还得添加支持的jar 获取的是第一个 只返回一个。 

			Element nameElement = (Element) rootElement.selectSingleNode("//name");//双斜杠不能少

	　

			//获取文档里面的所有name元素 

			List<Element> list = rootElement.selectNodes("//name");

			for (Element element : list) {

				System.out.println(element.getText());

			}





```





## XML 约束



如下的文档， 属性的ID值是一样的。 这在生活中是不可能出现的。 并且第二个学生的姓名有好几个。 一般也很少。那么怎么规定ID的值唯一， 或者是元素只能出现一次，不能出现多次？ 甚至是规定里面只能出现具体的元素名字。 

```xml

		<stus>

			<stu id="10086">

				<name>张三</name>

				<age>18</age>

				<address>深圳</address>

			</stu>

			<stu id="10086">

				<name>李四</name>

				<name>李五</name>

				<name>李六</name>

				<age>28</age>

				<address>北京</address>

			</stu>

		</stus>

```

### DTD

文档类型定义，可以定义合法的ＸＭＬ文档构建模块.

可以成行的声明于XML文档中,也可以作为外部引用

可读性比较差。 



1. 引入网络上的DTD

```xml

   	<!-- 引入dtd 来约束这个xml -->



   	<!--文档类型  根标签名字 网络上的dtd   dtd的名称    dtd的路径 -->

   	<!  DOCTYPE stus      PUBLIC    "//UNKNOWN/"  "unknown.dtd">

```



2. 引入本地的DTD

```xml

	<!-- 引入本地的DTD  忽略dtd的路径-->

      <!-- 		根标签名字 引入本地的DTD  dtd的位置 -->

     <!DOCTYPE stus 		SYSTEM 	 "stus.dtd"> 

```

3. 直接在XML里面嵌入DTD的约束规则



```xml

   	<!-- xml文档里面直接嵌入DTD的约束法则 -->

   	<!DOCTYPE stus [

   		<!ELEMENT stus (stu)+>

   		<!ELEMENT stu (name,age)>

   		<!ELEMENT name (#PCDATA)>

   		<!ELEMENT age (#PCDATA)>

   		<!ATTLIST stu id CDATA #IMPLIED>

   	]>

		

   	<stus>

   		<stu id="10086">

   			<name>张三</name>

   			<age>18</age>

   		</stu>

        <stu id="10ds">

   			<name>李四</name>

   			<age>18</age>

   		</stu>

   	</stus>



<!--

   		<!ELEMENT stus (stu)>:stus 下面有一个元素 stu  ， 但是只有一个

   		<!ELEMENT stu (name,age)>:stu下面有两个元素 name,age顺序必须name-age

   		<!ELEMENT name (#PCDATA)>:name 只有PCDATA

   		<!ELEMENT age (#PCDATA)>:age 只有PCDATA

   		<!ATTLIST stu id CDATA #IMPLIED>:stu有一个属性名为id,字符数据CDATA,该属性可有可无

		<!ELEMENT br EMPTY>:空元素,例子;<br />

-->

```







4. 元素的个数：

```

+ 一个或多个

* 零个或多个

? 零个或一个

```

5. 属性的类型定义 

```xml

CDATA : 属性是普通文字

ID : 属性的值必须唯一

```

6. 元素的选择

```xml

<!ELEMENT stu (name , age)>	<!--按照顺序来--> 

<!ELEMENT stu (name | age)> <!--两个中只能包含一个子元素-->

```



### Schema



其实就是一个xml ， 使用xml的语法规则， xml解析器解析起来比较方便 ， 是为了替代DTD 。

但是Schema 约束文本内容比DTD的内容还要多。 所以目前也没有真正意义上的替代DTD



约束文档：



```xml

<!-- xmlns  :  xml namespace : 名称空间 /  命名空间

targetNamespace :  目标名称空间 。 下面定义的那些元素都与这个名称空间绑定上。 

elementFormDefault ： 元素的格式化情况。  -->

<schema xmlns="http://www.w3.org/2001/XMLSchema" 

		argetNamespace="http://www.itheima.com/teacher" 

		elementFormDefault="qualified"

        >

	<element name="teachers">

		<complexType>

            <sequence maxOccurs="unbounded">

                <!-- 这是一个复杂元素 -->

                <element name="teacher">

                    <complexType>

                        <sequence>

                            <!-- 以下两个是简单元素 -->

                            <element name="name" type="string"></element>

                            <element name="age" type="int"></element>

                        </sequence>

                    </complexType>

                </element>

            </sequence>

		</complexType>

	</element>

</schema>

```



实例文档：



```xml

		<?xml version="1.0" encoding="UTF-8"?>

		<!-- xmlns:xsi : 这里必须是这样的写法，也就是这个值已经固定了。

		xmlns : 这里是名称空间，也固定了，写的是schema里面的顶部目标名称空间

		xsi:schemaLocation : 有两段： 前半段是名称空间，也是目标空间的值 ， 后面是约束文档的路径。

		 -->

		<teachers

			xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

			xmlns="http://www.itheima.com/teacher"

			xsi:schemaLocation="http://www.itheima.com/teacher teacher.xsd"

		>

			<teacher>

				<name>zhangsan</name>

				<age>19</age>

			</teacher>

			<teacher>

				<name>lisi</name>

				<age>29</age>

			</teacher>

			<teacher>

				<name>lisi</name>

				<age>29</age>

			</teacher>

		</teachers>

```



## 名称空间的作用



一个xml如果想指定它的约束规则， 假设使用的是DTD ，那么这个xml只能指定一个DTD  ，  不能指定多个DTD 。 但是如果一个xml的约束是定义在schema里面，并且是多个schema，那么是可以的。简单的说： 一个xml 可以引用多个schema约束。 但是只能引用一个DTD约束。



名称空间的作用就是在 写元素的时候，可以指定该元素使用的是哪一套约束规则默认情况下 ，如果只有一套规则，那么都可以这么写



```xml

	<name>张三</name>

	<aa:name></aa:name>

	<bb:name></bb:name>

```
