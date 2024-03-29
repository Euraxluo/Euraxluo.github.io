+++
title = "Servlet2"
date = "2020-10-22"
description = "Servlet"
featured = false
categories = [
  "Java"
]
tags = [
  "Java"
]
series = [
  "Java"
]
images = [
]
+++


## Cookie和Session
会话：浏览器发出http请求。服务器接受，对请求进行响应，浏览器接受http响应





### Cookie

把会话数据保存在浏览器客户端



服务器第一次访问时，服务端生成cookie，并且把这个cookie通过响应，发送给客户端，客户端把cookie保存下来，以便在最近的下一次访问中使用

缺点

1. Cookie有大小和数量的限制

2. 明文传递有风险



```java

//创建Cookie对象

        Cookie userNameCookie = new Cookie("userName",userName);

        Cookie userPasswordCookie = new Cookie("userPassword",userPassword);



```



```java

//返回给访问对象

        resp.addCookie(userNameCookie);

        resp.addCookie(userPasswordCookie);

```



```java

/、对外部浏览器返回的响应头进行处理

        Cookie[] cookies = req.getCookies();

        if(cookies != null){

            for(Cookie cookie:cookies){



                if (cookie.getName().equals("userName"))

                {

                    userName = cookie.getValue();

                }else if (cookie.getName().equals("userPassword")) {

                    userPassword = cookie.getValue();

                }

            }

        }

```

#### 例子一 显示最近访问的时间。



1. 判断账号是否正确



2. 如果正确，则获取cookie。 但是得到的cookie是一个数组， 我们要从数组里面找到我们想要的对象。



3. 如果找到的对象为空，表明是第一次登录。那么要添加cookie



4. 如果找到的对象不为空， 表明不是第一次登录。 



```java

		if("admin".equals(userName) && "123".equals(password)){

			//获取cookie last-name --- >

			Cookie [] cookies = request.getCookies();

			

			//从数组里面找出我们想要的cookie

			Cookie cookie = CookieUtil.findCookie(cookies, "last");

			

			//是第一次登录，没有cookie

			if(cookie == null){

				

				Cookie c = new Cookie("last", System.currentTimeMillis()+"");

				c.setMaxAge(60*60); //一个小时

				response.addCookie(c);

				

				response.getWriter().write("欢迎您, "+userName);

				

			}else{

				//1. 去以前的cookie第二次登录，有cookie

				long lastVisitTime = Long.parseLong(cookie.getValue());

				

				//2. 输出到界面，

				response.getWriter().write("欢迎您, "+userName +",上次来访时间是："+new Date(lastVisitTime));

                

				//3. 重置登录的时间

				cookie.setValue(System.currentTimeMillis()+"");

				response.addCookie(cookie);

			}

		}else{

			response.getWriter().write("登陆失败 ");

		}

```

#### 例子二： 显示商品浏览记录。





##### 准备工作



1. 拷贝基础课第一天的 htmll原型文件，到工程的WebContent里面。



2. 在WebContent目录下新建一个jsp文件， product_list.jsp, 然后拷贝原来product_list.html的内容到jsp里面。 建好之后，jsp里面的所有ISO-8859-1 改成 UTF-8



	拷贝html标签的所有内容。 替换jsp的html标签即可



3. 修改product_info.htm里面的手机数码超链接地址

`<li class="active"><a href="product_list.jsp">手机数码<span class="sr-only">(current)</span></a></li>`



4. 修改首页(index.html)顶部的手机数码跳转的位置为 product_list.jsp

`<li class="active"><a href="product_list.jsp">手机数码<span class="sr-only">(current)</span></a></li>`





#####分析



![icon](/image/img03.png)



##### 显示浏览记录

```java

Cookie[] cookies = request.getCookies();

Cookie cookie = CookieUtil.findCookie(cookies,"history");

//如果cookie是空的,表img01明没有浏览任何商品

if(cookie == null){

    out.println("你还没有浏览任何商品");

}else{

    //不是空,表明有浏览记录

    String[] ids = cookie,getValue().split("#");

    for(String id:ids){

        //输出浏览记录

    }

}

```





##### 清除浏览记录



> 其实就是清除Cookie， 删除cookie是没有什么delete方法的。只有设置maxAge 为0 。



```java

		Cookie cookie = new Cookie("history","");

		cookie.setMaxAge(0); //设置立即删除

		cookie.setPath("/CookieDemo02");

		response.addCookie(cookie);

```



#### Cookie总结



1. 服务器给客户端发送过来的一小份数据，并且存放在客户端上。



2. 获取cookie， 添加cookie



	request.getCookie();



	response.addCookie();



3. Cookie分类

	1)  会话Cookie

	​	默认情况下，关闭了浏览器，那么cookie就会消失。



	2)持久Cookie

	​	在一定时间内，都有效，并且会保存在客户端上。

	​	cookie.setMaxAge(0); //设置立即删除

	​	cookie.setMaxAge(100); //100 秒



4. Cookie的安全问题。



> 由于Cookie会保存在客户端上，所以有安全隐患问题。  还有一个问题， Cookie的大小与个数有限制。 为了解决这个问题 ---> Session .





### HttpSession

把会话数据保存在服务器端



客户端把请求等发送给服务器，服务器根据这个请求，生成一个session，并且，把这个Session的id处理通过cookie发送给客户端，下一次客户端访问时，就可以找到这个Session



> 会话 ， Session是基于Cookie的一种会话机制。 Cookie是服务器返回一小份数据给客户端，并且存放在客户端上。 Session是，数据存放在服务器端。





* 常用API

```java

		//得到会话ID

		String id = session.getId();

		

		//存值

		session.setAttribute(name, value);

		

		//取值

		session.getAttribute(name);

		

		//移除值

		session.removeAttribute(name);

```

* Session何时创建  ， 何时销毁?



* 创建



> 如果有在servlet里面调用了 request.getSession()



* 销毁



> session 是存放在服务器的内存中的一份数据。 当然可以持久化. Redis . 即使关了浏览器，session也不会销毁。

>销毁方式



>>1. 关闭服务器



>>2. session会话时间过期。 有效期过了，默认有效期： 30分钟。

>



* Session的优先级

	​	setMaxInaxtiveInterval　＞　部署描述符配置	

	​	invalidate使Session失效



```java

//创建session

        HttpSession session = req.getSession();

```



```java

//把表单数据放入session中

        String sessioname = (String) session.getAttribute("userName");

       

```



```java

//查看一下二次登录的session

        if(sessioname != null){

            System.out.println("second Session:");

        }

```



#### 例子三： 简单购物车。



##### CartServlet 代码

```java

		response.setContentType("text/html;charset=utf-8");

			

			//1. 获取要添加到购物车的商品id

			int id = Integer.parseInt(request.getParameter("id")); // 0 - 1- 2 -3 -4 

			String [] names = {"Iphone7","小米6","三星Note8","魅族7" , "华为9"};

			//取到id对应的商品名称

			String name = names[id];

			

			//2. 获取购物车存放东西的session  Map<String , Integer>  iphoen7 3

			//把一个map对象存放到session里面去，并且保证只存一次。 

			Map<String, Integer> map = (Map<String, Integer>) request.getSession().getAttribute("cart");

			//session里面没有存放过任何东西。

			if(map == null){

				map = new LinkedHashMap<String , Integer>();

				request.getSession().setAttribute("cart", map);

			}

			

			//3. 判断购物车里面有没有该商品

			if(map.containsKey(name)){

				//在原来的值基础上  + 1 

				map.put(name, map.get(name) + 1 );

			}else{

				//没有购买过该商品，当前数量为1 。

				map.put(name, 1);

			}

			

			//4. 输出界面。（跳转）

			response.getWriter().write("<a href='product_list.jsp'><h3>继续购物</h3></a><br>");

			response.getWriter().write("<a href='cart.jsp'><h3>去购物车结算</h3></a>");



```

##### 移除Session中的元素

```java

//强制干掉会话，里面存放的任何数据就都没有了。

session.invalidate();

//从session中移除某一个数据

//session.removeAttribute("cart");

```



## 请求转发



定义：将当前的request和response 对象交给指定的web组件进行处理



注意：

1. 请求转发时，浏览器url不会改变

2. 地址上显示的是请求servlet的地址。  返回200 ok

3. 请求次数只有一次， 因为是服务器内部帮客户端执行了后续的工作。 	

4. 只能跳转自己项目的资源路径 。  	

5. 效率上稍微高一点，因为只执行一次请求。 

6. 可以使用上一次的request对象。 



//请求转发的写法：

1. include{RequestDispatcher}

`request.getRequestDispatcher("login_success.html").forward(request, response);`

	1) 通过HttpServletRequest

	2) 通过ServletContext

2. 使用forward





```java

//3中请求转发的方式

        RequestDispatcher rd = req.getRequestDispatcher("/ServletForwardExample/*");//1

        rd = this.getServletContext().getNamedDispatcher("servletForwardExample");//2

        rd = this.getServletContext().getRequestDispatcher("/servletForwardExample/*");//3

        rd.forward(req,resp);

```

![icon](/image/img01.png)

### 请求重定向

sendRedirect

通过response对象发送给浏览器一个新的地址，让其重新请求（两次请求，两次响应）



ex：网页登录跳转：

1. 浏览器发出登录请求

2. 服务器请求转发进行登录处理

3. 服务器把请求响应发送给客户端，同事包含另一个url的响应信息

4. 浏览器接收到响应信息，得到另一个url

5. 随即，浏览器向服务器发出跳转请求

6. 服务器返回跳转结果



`resp.sendRedirect("/SendRedirectExample/*");`



注：转发和重定向的区别

1. 转发的浏览器地址栏不会发生变化，重定向则会

2. 请求转发只能在同一个web应用下进行转发。重定向可以跨web资源和地址

3. 请求转发一次请求一次响应。重定向是两次转发，两次响应



## 过滤器和监听器

1. 过滤源：请求和响应

2. 过滤规则：自己定义

3. 简单地说：过滤器会在请求发送给Servlet之前先对请求进行处理，

如果响应要发送给浏览器也需要先经过过滤器

4. 应用场景：

	1. 用户认证（验证用户是否有权限）

	2. 编解码处理

	3. 请求压缩

5. 过滤器的生命周期

	1. init - 初始化（只运行一次）

	2. doFilter - 进行过滤操作

	3. destroy - 释放资源，销毁过滤器对象（只运行一次）



```java

public class TestFilter implements Filter{



// 可以像servlet配置一样，对TestFilter的init传入FilterConfig filterConfig

    @Override

    public void init(FilterConfig filterConfig) throws ServletException {}



    @Override

    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {}



    @Override

    public void destroy() {}

}

```

filter配置：

```xml

<filter>

        <init-param>

            <param-name>filterParam</param-name>

            <param-value>euraxluo</param-value>

        </init-param>

        <filter-name>testFilter</filter-name>

        <filter-class>com.controller.filter.TestFilter</filter-class>

    </filter>



    <filter-mapping>

        <filter-name>testFilter</filter-name>

        <url-pattern>/testFilter/*</url-pattern>

    </filter-mapping>

```



在写doFilter时，参数

`ServletRequest servletRequest, ServletResponse servletResponse`



，不能直接处理Servlet中的`HttpServletRequest req, HttpServletResponse resp`



应该使用类型转换`HttpServletRequest req = (HttpServletRequest)servletRequest; `



通过过滤器验证登录的逻辑部分

```java

//通过判断是否有session来判断是否登录

        HttpSession session = req.getSession();

        if(session.getAttribute("userName")==null){

            HttpServletResponse resp = (HttpServletResponse)servletResponse;

            resp.sendRedirect("/GetPostServlet/*");

        }else{

            filterChain.doFilter(servletRequest,servletResponse);

        }

```

如果有多个filter，会根据在部署描述符中的先后顺序来决定过滤器的顺序



在第一filter被调用时会产生filterchain传递给dofilter函数即，

dofilter函数的`FilterChain filterChain`参数指的就是Filter链，



再dofilter执行快结束时，会检查Filterchain，如果filterchain还有其他的filter，就会继续执行其他filter。如果没有了，就会执行跳转，把过滤后的请求给servlet。

servlet返回响应时，也要经过filter链，并且顺序是反着的



## 监听器{监听事件发生后，在事件发生前后能够做出相应处理的web应用组件}

事件源：我们需要监听的东西

注册： 把监听器放在我们需要监听的地方

通知：如果发生了我们监听的事件，就会通知

最后监听到事件后，对其进行处理



servlet中的注册不直接注册到事件，而是交给servlet，开发人员只需要配置部署描述符，servlet会自己注册到事件源



监听器分类：

1. 监听应用程序环境：ServletContext

	1)ServletContextListener(对创建和销毁进行监听)

	2)ServletContextAttributeListener(对属性的增删改查监听)

2. 监听用户请求对象:ServletRequest

	1)ServletRequestListener(对创建和销毁进行监听)

	2)ServletRequestAttributeListener(对属性的增删改查监听)

3. 监听用户会话对象:HTTPSession

	1)HTTPSessionListener(对创建和销毁进行监听)

	2)HTTPSessionAttributeListener(对属性的增删改查监听)

	3)HTTPSessionActivationListener(对session持久化到磁盘和重新加载到JVM时监听)

	4)HTTPSessionBindingListenner(对调用Attribute和removeAttribute的方法监听)

	



使用场景：

1. 应用统计（用户登录统计）

2. 任务触发

3. 业务需求



监听器可能会有很多个，和过滤器一样，顺序由部署描述符中的部署顺序决定事件注册的顺序



eg：HTTPSessionAttributeListener，ServletContextListener，ServletRequestListener

```java

public class TestListener implements HttpSessionAttributeListener, ServletContextListener, ServletRequestListener {}

```

xml部署

```xml

<listener>

        <listener-class>com.controller.listener.TestListener</listener-class>

    </listener>



```



### 注：监听器和过滤器和servlet的启动顺序：

1. 监听器

2. 过滤器

3. Servlet







## servlet 并发处理

先了解一下servlet的处理过程





经常会出现多个客户端同事对一个servlet发起请求，

我们的处理方式一般为：

1. 串行处理，对每个客户端的请求依次处理

2. 并发处理

	1)	客户端发送请求给服务器，服务器的servlet容器将请求转发给调度器，由调度器在工作线程池中选取一个线程，把请求交个这个线程，但不关心这个请求的servlet。多个线程可以同时指向一个servlet。但是当线程池满了过后，下一个请求就必须排队，并且排队队列可以设置上限

	2)	总结：单实例，多线程，线程不安全



问题：怎么保证servlet的线程安全

1. 变量的线程安全

	1)	参数变量本地化(局部变量不会线程共享)

	2)	使用同步快synchronized(加锁处理，并且要尽量减小synchronized的范围)

2. 属性的线程安全

	1)	ServletContext线程不安全

	2)	HTTPSession理论上线程安全，但是我们一般还是会做加锁处理

	3)	ServletRequest线程安全

3. 避免在Servlet中创建线程

4. 多个Servlet需要同时访问一个web应用（访问外部对象）应该做加锁处理

5. 尽量避免使用实例变量，如果必须使用实例变量，就要用同步的操作（控制同步的范围）



```java

synchronized(this){

    //代码块

}

```
