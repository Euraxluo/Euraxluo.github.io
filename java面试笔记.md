## java跨平台

实现java跨平台只需要在相应的平台安装对应的虚拟机，我们就可以使用统一的接口进行开发。

java通过不同的系统，不同的版本，不同的位数，来屏蔽不同的系统指令集的差异，对外提供统一的接口

## java中int数据占几个字节

1. java中有几种基本数据类型？8种

   ```java
   
   基本类型：byte 二进制位数：8
   包装类：java.lang.Byte
   最小值：Byte.MIN_VALUE=-128
   最大值：Byte.MAX_VALUE=127
   
   基本类型：short 二进制位数：16
   包装类：java.lang.Short
   最小值：Short.MIN_VALUE=-32768
   最大值：Short.MAX_VALUE=32767
   
   基本类型：int 二进制位数：32
   包装类：java.lang.Integer
   最小值：Integer.MIN_VALUE=-2147483648
   最大值：Integer.MAX_VALUE=2147483647
   
   基本类型：long 二进制位数：64
   包装类：java.lang.Long
   最小值：Long.MIN_VALUE=-9223372036854775808
   最大值：Long.MAX_VALUE=9223372036854775807
   
   基本类型：float 二进制位数：32
   包装类：java.lang.Float
   最小值：Float.MIN_VALUE=1.4E-45
   最大值：Float.MAX_VALUE=3.4028235E38
   
   基本类型：double 二进制位数：64
   包装类：java.lang.Double
   最小值：Double.MIN_VALUE=4.9E-324
   最大值：Double.MAX_VALUE=1.7976931348623157E308
   
   基本类型：char 二进制位数：16
   包装类：java.lang.Character
   最小值：Character.MIN_VALUE=0
   最大值：Character.MAX_VALUE=65535
   ```

   ## 面向对象的特征

   ### 封装

   将对象封装成一个高度自洽相对封闭的个体，对象状态(属性)由这个对象自己的行为(方法)来读取和改变

   ### 抽象

   抽象就是找出一些事物的相似和共性之处，然后把他们抽象为类

   ### 继承

   把这个已经存在的类所定义的内容作为自己的内容，并可以加入若干新的内容，或修改原来的方法使之更适合特殊的需要

   ### 多态

   指程序中定义的引用变量所指向的具体类型和通过该引用变量发出的方法调用只有在程序运行时才确定
