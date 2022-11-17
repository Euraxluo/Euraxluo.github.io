---
title: "Scala入门"
date: "2019-02-21"
description: "Scala入门"
featured : true
categories: ["notes"]
tags: [ "notes" ]
series: [ "notes" ]
images: []
---
Scala 入门之随便写写
```Scala
import  scala.util.control._
object HelloWorld{
  def hello(name:String) = {
    s"Hello ,${name}"
  }
  def add(x: Int,y:Int) = x+y
  def main(args:Array[String]):Unit = {
    /**
      * 违反引用透明的例子:
      * 怎么样获得引用透明性:{
      * 需要具有不变性,即为了获得引用透明性,任何值都不能改变
      * }
      */
    var x = new StringBuilder("Hello ");
    println(x);
    var y = x.append(" world");
    println(y);
    var z = x.append(" world");
    println(z);


    /**
      * 递归函数:
      * 使用递归实现循环
      * 尾递归函数
      */

    /**
      * 变量:
      * val 定义immutable variable:常量
      * var 定义mutable variable:变量
      * lazy val:惰性求值常量
      * 可以再定义时不指定变量的类型,Scala会自动进行类型推导
      */
    println(hello("Euraxluo"))
    println(add(1,2))

    /**
      * for循环
      */
    val list = List("Euraxluo","xiaoli","xiaoxiong")

    //循环1
    for (
      s <- list//generator
    )println(s)
    println("")

    //循环2
    for {
      s<-list
      if  (s.length>6)//filter
    }println(s)
    println("")

    //循环3
    val res_for = for {
      s<- list
      s1 = s.toUpperCase()//变量绑定
      if(s1 != "")
    }yield (s1)//将s1放在新的collection中
    println(res_for)
    println("")


    /**
      * 无限循环
      */
//    var a = 10
//    while (true){
//      println(s"a的值:${a}")
//    }

    /**
      * 中断循环
      */
    var loop = new Breaks;
    val numl = List(0,1,2,3,6,5,6,7)
    loop.breakable{
      for(a<-numl){
        println(a)
        if(a>=6){
          loop.break()
        }
      }
    }
    println("")

    /**
      * 嵌套循环
      */
    val outer = new Breaks;
    val inner = new Breaks;
    outer.breakable{
      for (a<-numl){
        inner.breakable{
          for (b<-numl){//次数
            println(a*a)
            if (a*a > 36){
              inner.break;
            }
          }
        }
      }
    }
    println("")

    /**
      * try{}catch{}finally{}
      */
    var res_try = try {
      Integer.parseInt("sa")
    }catch {
      case _ => 2222222
    }finally {
      println("finally")
    }
    println(res_try)
    println("")


    /**
      * match
      */
    val code = 600
    var res_match = code match {
      case 200 => "OK"
      case 404 => "Not Found"
      case 400 => "Bad Request"
      case _   => "Server Error"
    }
    println(res_match)
    println("")

    /**
      * 重要概念
      * 表达式求值策略:严格求值与非严格求值
      * Scala中:Call By Value vs. Call By Name
      * 惰性求值(lazy Evluation):
      * 当定义表达式时,不会立即求值,而是当这个表达式第一次被调用时才会求值
      */
    def bar(x:Int,y: => Int) = x//Call By Value , Call By Name
    def Loop():Int= {println("...");Loop} //无限循环
//    println(bar(Loop,1))//将Loop传给call by value ,函数体中即便没有使用到,也去运行这个无限循环
    println(bar(1,Loop))//将Loop传给call by name ,函数体中没有使用到,因此不会去运行这个无限循环


    /**
      * 柯里化
      * @param a
      * @param b
      * @return
      */
    //def curriedAdd(a:Int,b:Int) = a+b
    def curriedAdd(a:Int)(b:Int) = a+b
    println(curriedAdd(2)(2))
    val addOne = curriedAdd(1)_//Int=>Int
    println(addOne(2))
    println("")

    /**
      * 递归例子
      * n!
      */
    def factorial(n:Int):Int =
      if (n<=0) 1
      else n*factorial(n-1)
    println(factorial(5))
    println("")

    /**
      * 尾递归函数
      * 尾递归函数中所有递归形式的调用都出现在函数的末尾
      * 当编译器检测到一个函数调用是尾递归的时候,
      * 他就会覆盖当前的栈,而不是在栈中创建一个新的
      *
      * 优化:把之前的递归调用的结果保存起来,而不是用栈去做这件事
      */
    @annotation.tailrec //开启尾递归调用优化
    def factorial_tailrec(n:Int,m:Int):Int =
      if (n<=0) m
      else factorial_tailrec(n-1,m*n)
    println(factorial_tailrec(5,1))
    println("")


    /**
      * 求f(x){x=a...b}的和
      * @param f :一个func
      * @param a :x=a
      * @param b :x=b
      * @return :返回和
      */
    def sum (f:Int=>Int)(a:Int)(b:Int):Int = {
      //定义一个循环
      @annotation.tailrec
      def loop(n: Int,acc:Int):Int = {
        if (n>b) acc//如果当前N大于b,返回相加结果
        else loop(n+1,acc+f(n)) //尾调用优化
      }
      loop(a,0)
    }
    println(sum(x=>x)(0)(100))
    println(sum(x=>x*x)(0)(5))

    val sumSquare = sum(x=>x*x)_ //定义一个函数,是平方的和,_通配a,b
    println(sumSquare(1)(5))
    println("")

    /**
      * list相关操作
      */

    /**
      * 连接操作
      */
    val listB = List(5,6,7):::list //连接两个list
    for (
      s <- listB//generator
    )println(s)
    println("")

    val listC = 6::list //连接一个对象和其他的对象(List/Object)
    //list是引用类型,6是值类型,因此listC的类型是List(Any)
    for (
      s <- listC//generator
    )println(s)


    val listD = "7"::"8"::Nil
    for (
      s <- listD//generator
    )println(s)
    println("")

    /**
      * head方法,获取第一个元素
      */
    println(listC.head)

    /**
      * tail方法,获取除了第一个元素以外的元素
      */
    println(listC.tail)

    /**
      * isEmpty:判断是否为空
      *
      */
    println(listC.isEmpty == Nil.isEmpty)

    /**
      * 自己的toString
      * @param l
      * @return
      */
    def walkthru(l:List[Any]) :String = {
      if (l.isEmpty) ""
      else l.head.toString+" "+walkthru(l.tail)
    }
    println(walkthru(listC))
    println("")

    /**
      * filter(func),如果func返回为true,保留此元素
      */
    val listE = List(1,2,3,4,5)
//    println(listE.filter(x=>x%2==1))
    println(listE.filter(_%2==1))

    /**
      * toList
      */
    println("Hello Scalar 666".toList.filter(x=>Character.isDigit(x)))

    /**
      * takeWhile,获取元素,指导P返回为False
      */
    println("Hello Scalar 666".toList.takeWhile(x => !Character.isDigit(x)))


    /**
      * map
      */
    println("Hello Scalar 66".toList.map(_.toUpper))

    /**
      * flatMap
      */

    val l1 = List(List(3,4),List(4,5,6))
    println(l1)
    //map 返回值与原来的类型一致
    println(l1.map(_.filter(_%2==0)))
    //会将多层的容器打平
    println(l1.flatMap(_.filter(_%2==0)))
    println("")

    /**
      * reduce
      */
    println(listE.reduce(_+_))//==reduceLeft
    println(listE.reduceLeft(_+_))

    /**
      * foldLeft
      */
    println(listE.fold(0)(_+_))
    println(listE.fold(1)(_*_))//会根据U的值进行类型改变


    /**
      * Range
      */
    /**
      * to
      */
    println((1 to 10).toList)

    /**
      * until
      */
    println((1 until 10).toList)

    /**
      * stream is a lazy List
      */
    val s1 = 1 #:: 2 #:: 3 #:: Stream.empty
    println(s1)
    val s2 = (1 to 1000000).toStream
    println(s2.tail)
    println("")

    /**
      * tuple
      */
    /**
      * paire
      */
    println((1,2))
    println(1->2)
    val t1 = (1,"Euraxluo",21,"男")
    println("Euraxluo is :"+t1._4)
    println("")

    /**
      *
      * @param l:一个List
      * @return (List元素个数,List元素和,List元素平方和)
      */
    def sumSq(l:List[Int]):(Int,Int,Int) =
      l.foldLeft((0,0,0))((t, v) => (t._1 + 1, t._2 + v, t._3 + v * v))
    println(sumSq(listE))
    println("")


    /**
      * Map
      */
    val map = Map(1->"Euraxluo",2->"hehe",4->"sa")
    println(map)
    println(map(4))//通过key获取value
    println(map.contains(3))//判断是否有这个key
    println(map.keys)//获取keys
    println(map.values)//获取values
    /**
      * +:添加一个k-v
      * 返回一个新Map
      */
    println(map+(6->"hehheheh"))
    /**
      * -:根据key删除一个k-v
      * 返回一个新Map
      */
    println(map - 1)

    /**
      * ++:添加多个
      */
    println( map ++ List(22->"alice",51->"sas"))

    /**
      * --:删除多个
      */
    println(map -- List(1,2))

    println("")

    /**
      * 递归实现的快速排序
      * @param l
      * @return
      */
    def qSort(l:List[Int]):List[Int] =
      if (l.length < 2 ) l//如果List元素小于两个,返回其自身
      else
        qSort(l.filter(_<l.head)) ++ //小于l.head的部分,然后加上剩下部分
        l.filter(_==l.head) ++ //等于l.head的部分,加上大于l.head的部分
        qSort(l.filter(_ > l.head))//大于l.head的部分

    println(qSort(List(9,3,7,6,5,4,2,8,1)))

  }
}
//函数式编程的重要概念
//引用透明:对于相同的输入,总是得到相同的输出
//如果F(x)的参数x和函数体都是引用透明的,那么函数F是纯函数
```