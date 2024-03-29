+++
title = "JSP"
date = "2018-10-29"
description = "JSP"
featured = false
categories = [
  "java"
]
tags = [
  "JSP"
]
series = [
  "JSP"
]
images = [
]

+++


# jsp

> Java Server Page 


* 什么是jsp



> 从用户角度看待 ，就是是一个网页 ， 从程序员角度看待 ， 其实是一个java类， 它继承了servlet，所以可以直接说jsp 就是一个Servlet.



* 为什么会有jsp?



> html 多数情况下用来显示静态内容 ， 一成不变的。 但是有时候我们需要在网页上显示一些动态数据， 比如： 查询所有的学生信息， 根据姓名去查询具体某个学生。  这些动作都需要去查询数据库，然后在网页上显示。 html是不支持写java代码  ， jsp里面可以写java代码。 

java服务器页面



* jsp = html+java+JSP tag



>处理流程：浏览器客户端向服务器发起请求，请求对应的jsp文件。然后jsp容器载入jsp文件，并且把jsp文件转化为Servlet(只是简单的把jsp文件改写为servlet语句)，然后jsp容器把servlet编译为可执行的class，然后把请求交给servlet容器，然后web组件就会调用servlet容器，载入对应的servlet实例。在执行时，会产生html页面，嵌入到response中返回给浏览器



###　jsp与servlet比较

１.	侧重点

​	jsp侧重于视图

​	servlet侧重于逻辑

２.	jsp有一些内置对象

３.	本质jsp其实是servlet的一种简化



###　jsp基本语法

1. jsp声明

`<%! int a,b,c; %>`

2. jsp表达式(表达式元素中可以包含任何符合java语言规范的表达式，但是不能使用分号来结束)

`<%= 表达式%>`

eg：输出日期`<p>Today's date:<% = (new java.util.Date()).toLocaleString()%></p>`

3. jsp脚本(可以包含任意量的java语句,变量,方法或者表达式)

`<% 代码片段 %>`

eg:打印ip`<% out.println("Your IP:"+request.getRemoteAddr()); %>`

4. jsp注释

`<-- 这部分是jsp注释 -->`

5. jsp指令

	1)	page指令(定义页面的依赖属性,比如脚本语言,error页面,缓存需求)

	2)	include指令(把其他文件包含到这个jsp中)

	3)	taglib指令(引入自定义的标签库,并且可以指定前缀)

6. jsp内置对象

	1)	request:HttpServletRequest类的实例

	2)	response:HttpServletResponse类的实例

	3)	out:PrintWriter类的实例

	4)	session:HttpSession类的实例

	5)	application:ServletContext类的实例

	6)	config:ServletConfig类的实例

	7)	page:类似于java类中的this关键字

	8)	pageContext:PageContext类的实例,提供对JSP页面所有对象以及命名空间的访问

	9)	Exception:EXception类的对象,代表发生错误的jsp页面中对应的异常对象



#### jsp指令

##### 1) page指令

> 表明jsp页面中可以写java代码



* contentType

> 其实即使说这个文件是什么类型，告诉浏览器我是什么内容类型，以及使用什么编码				`contentType="text/html; charset=UTF-8"`

	`text/html  MIMEType 这是一个文本，html网页`



* pageEncoding  jsp内容编码

* extends 用于指定jsp翻译成java文件后，继承的父类是谁，一般不用改。

* import 导包使用的，一般不用手写。

* session 

> 值可选的有true or false .

> 用于控制在这个jsp页面里面，能够直接使用session对象。

> 具体的区别是，请看翻译后的java文件   如果该值是true , 那么在代码里面会有getSession（）的调用，如果是false :  那么就不会有该方法调用，也就是没有session对象了。在页面上自然也就不能使用session了。



* errorPage

> 指的是错误的页面， 值需要给错误的页面路径



* isErrorPage

> 上面的errorPage 用于指定错误的时候跑到哪一个页面去。 那么这个isErroPage , 就是声明某一个页面到底是不是错误的页面。



##### 2) include指令

> 包含另外一个jsp的内容进来。

`<%@ include file="other02.jsp"%>`



* 背后细节:

> 把另外一个页面的所有内容拿过来一起输出。 所有的标签元素都包含进来。



##### 3) taglib指令

`<%@ taglib prefix=""  uri=""%>`

​	uri: 标签库路径

​	prefix : 标签库的别名 

​	



### JSP 动作标签

```jsp

	<jsp:include page=""></jsp:include>

	<jsp:param value="" name=""/>

	<jsp:forward page=""></jsp:forward>

```

#### jsp:include

`<jsp:include page="other02.jsp"></jsp:include>`

> 包含指定的页面， 这里是动态包含。 也就是不把包含的页面所有元素标签全部拿过来输出，而是把它的运行结果拿过来。 



#### jsp:forward

`<jsp:forward page=""></jsp:forward>`

> 前往哪一个页面。  



```jsp

	<% //请求转发

request.getRequestDispatcher("other02.jsp").forward(request, response);

	%>	

```

#### jsp:param

> 意思是： 在包含某个页面的时候，或者在跳转某个页面的时候，加入这个参数。



```jsp	

<jsp:forward page="other02.jsp">

<jsp:param value="beijing" name="address"/>

</jsp:forward>

在other02.jsp中获取参数

<br>收到的参数是：<br>

<%= request.getParameter("address")%>

```



### JSP内置对象

> 所谓内置对象，就是我们可以直接在jsp页面中使用这些对象。 不用创建。



- pageContext

- request

- session

- application



以上4个是作用域对象 , 



#### 作用域 

> 表示这些对象可以存值，他们的取值范围有限定。  setAttribute   和  getAttribute



```jsp

		使用作用域来存储数据<br>

	

		<%

			pageContext.setAttribute("name", "page");

			request.setAttribute("name", "request");

			session.setAttribute("name", "session");

			application.setAttribute("name", "application");

		%>

		

		取出四个作用域中的值<br>

		

		<%=pageContext.getAttribute("name")%>

		<%=request.getAttribute("name")%>

		<%=session.getAttribute("name")%>

		<%=application.getAttribute("name")%>

```

作用域范围大小：



	pageContext -- request --- session -- application 





#### 四个作用域的区别



* pageContext 【PageContext】



> 作用域仅限于当前的页面。  



> 还可以获取到其他八个内置对象。



* request 【HttpServletRequest】



> 作用域仅限于一次请求， 只要服务器对该请求做出了响应。 这个域中存的值就没有了。



* session 【HttpSession】



> 作用域限于一次会话（多次请求与响应） 当中。 



* application 【ServletContext】



> 整个工程都可以访问， 服务器关闭后就不能访问了。 



#### 如何使用

##### 1. 取出4个作用域中存放的值。

```jsp

<%

	pageContext.setAttribute("name", "page");

	request.setAttribute("name", "request");

	session.setAttribute("name", "session");

	application.setAttribute("name", "application");

%>

```

按普通手段取值

```jsp

		<%= pageContext.getAttribute("name")%>

		<%= request.getAttribute("name")%>

		<%= session.getAttribute("name")%>

		<%= application.getAttribute("name")%>

```

使用EL表达式取出作用域中的值

```jsp

		${ pageScope.name }

		${ requestScope.name }

		${ sessionScope.name }

		${ applicationScope.name }

```

2. 如果域中所存的是数组

```jsp

   		<%=String [] a = {"aa","bb","cc","dd"};

      		pageContext.setAttribute("array", a);

      	%>

```

>使用EL表达式取出作用域中数组的值

`${array[0] } , ${array[1] },${array[2] },${array[3] }`





3. 如果域中锁存的是集合

```jsp

<br>-------------Map数据----------------<br>

<%	Map map = new HashMap();

	map.put("name", "zhangsna");

	map.put("age",18);

	map.put("address","北京..");

	map.put("address.aa","深圳..");

	pageContext.setAttribute("map", map);

%>

```

>使用EL表达式取出作用域中集合的值

`${li[0] } , ${li[1] },${li[2] },${li[3] }`



4. 取出Map集合的值

```jsp

   	<%

      		Map map = new HashMap();

      		map.put("name", "zhangsna");

      		map.put("age",18);

      		map.put("address","北京..");



   		map.put("address.aa","深圳..");





   		pageContext.setAttribute("map", map);

   	%>

```

>使用EL表达式取出作用域中Map的值<br>

`${map.name } , ${map.age } , ${map.address }  , ${map["address.aa"] }`



### 取值细节：

1. 存值(从域中取值,先存)

```jsp

   <%//pageContext.setAttribute("name", "zhangsan");

   	session.setAttribute("name", "lisi...");

   %>



   <br>直接指定说了，到这个作用域里面去找这个name<br>

   ${ pageScope.name } 





   <br>//先从page里面找，没有去request找，去session，去application <br>

   ${ name }



   <br>指定从session中取值<br>

   ${ sessionScope.name }  

```

2. 取值方式

>如果这份值是有下标的，那么直接使用[]

```jsp

	<%	String [] array = {"aa","bb","cc"}

		session.setAttribute("array",array);

	%>

	${ array[1] } --> 这里array说的是attribute的name 

```

>如果没有下标， 直接使用 .的方式去取

```jsp

<%	User user = new User("zhangsan",18);

	session.setAttribute("u", user);

%>

${ u.name }  , ${ u.age } 

```



##　EL表达式

> 是为了简化咱们的jsp代码，具体一点就是为了简化在jsp里面写的那些java代码。



* 写法格式

`${表达式 }`



> 如果从作用域中取值，会先从小的作用域开始取，如果没有，就往下一个作用域取。  一直把四个作用域取完都没有， 就没有显示。



###　EL表达式 的11个内置对象。 

｀${ 对象名.成员 }｀



-　pageContext 



作用域相关对象

- pageScope

- requestScope

- sessionScope

- applicationScope



头信息相关对象

- header

- headerValues



参数信息相关对象

- param

- paramValues

- cookie



全局初始化参数



- initParam







## JSTL

> 全称 ： JSP Standard Tag Library  jsp标准标签库

> 简化jsp的代码编写。 替换 <%%> 写法。 一般与EL表达式配合





### 怎么使用



1. 导入jar文件到工程的WebContent/Web-Inf/lib  jstl.jar standard.jar



2. 在jsp页面上，使用taglib 指令，来引入标签库



3. 注意： 如果想支持 EL表达式，那么引入的标签库必须选择1.1的版本，1.0的版本不支持EL表达式。



	`<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>`





### 常用标签

```jsp

<c:set></c:set>

<c:if test=""></c:if>

<c:forEach></c:forEach>

```



* c:set

```jsp

<!-- 声明一个对象name,对象的值 zhangsan,存储到了page(默认),指定是session -->

		<c:set var="name" value="zhangsan" scope="session"></c:set>

		${sessionScope.name }

```



* c:if

> 判断test里面的表达式是否满足，如果满足，就执行c:if标签中的输出 ， c:if 是没有else的。 

```jsp

		<c:set var="age" value="18" ></c:set>

		<c:if test="${ age > 26 }">

			年龄大于了26岁...</c:if>

		<c:if test="${ age <= 26 }">

			年龄小于了26岁...</c:if>

		------------------------------

		<!--定义一个变量名 flag  去接收前面表达式的值，然后存在session域中-->

		<c:if test="${ age > 26 }" var="flag" scope="session">

			年龄大于了26岁...</c:if>

```



* c:forEach

```jsp

<!--从1 开始遍历到10,得到的结果,赋值给i,并且会存储到page域中,step,增幅为2-->

		<c:forEach begin="1" end="10" var="i" step="2">

			${i}</c:forEach>

		-----------------------------------------------

    <!--items : 表示遍历哪一个对象，注意，这里必须写EL表达式。 

		var: 遍历出来的每一个元素用user 去接收。 -->

		<c:forEach var="user" items="${list }">

			${user.name } ----${user.age }

		</c:forEach>

```





## 总结：

1. JSP

>三大指令

	page
	
	include
	
	taglib



>三个动作标签

	<jsp:include>
	
	<jsp:forward>
	
	<jsp:param>



>九个内置对象

>>四个作用域

	pageContext
	
	request
	
	session
	
	application



  		out

  		exception

  		response

  		page

  		config





2. EL

`${ 表达式 }`



>取4个作用域中的值

	${ name }



>有11个内置对象。

pageContext

pageScope

requestScope

sessionScope

applicationScope

header

headerValues

param

paramValues

cookie

initParam





3. JSTL

> 使用1.1的版本， 支持EL表达式， 1.0不支持EL表达式

> 拷贝jar包， 通过taglib 去引入标签库

`<c:set>`

`<c:if>`

`<c:forEach>`



eg:

```jsp



<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>

          <td>

              <!--fn:contains(stu.hobby,'游泳')->boolean 用于确定一个字符串是否包含指定的子串-->

              <input <c:if test="${fn:contains(stu.hobby,'游泳')}">checked</c:if> type="checkbox" name="hobby" value="游泳">游泳

              <input <c:if test="${fn:contains(stu.hobby,'篮球')}">checked</c:if> type="checkbox" name="hobby" value="篮球">篮球

              <input <c:if test="${fn:contains(stu.hobby,'足球')}">checked</c:if> type="checkbox" name="hobby" value="足球">足球

              <input <c:if test="${fn:contains(stu.hobby,'看书')}">checked</c:if> type="checkbox" name="hobby" value="看书">看书

              <input <c:if test="${fn:contains(stu.hobby,'写字')}">checked</c:if> type="checkbox" name="hobby" value="写字">写字

          </td>

```





#### JSP开发模式

开发模式一:

javaBean +JSP 

在jsp里面直接写java代码,维护起来比较困难.并且jsp的页面代码会面的臃肿



开发模式二:

Servlet+javaBean+JSP

使用的MVC模式:

M:model 模型层 封装数据,显示数据javaBean java类 EJB

V:View 视图层 jsp 专注于显示

C:Controller 控制层 Servlet 接受页面请求,找模型层去处理,然后响应数据给视图层



javaEE:

>客户端

>Web层  Servlet/jsp   对应MVC模式的Controller和Vew

>业务逻辑层  javaBean 对应Model

>数据访问层 Dao  对应Mode





#### 实战

学生信息管理



与以往(我写过的)的mvc有点区别,在dao与Servlet中增加了Service(业务层)层

>好处：

>>Dao只针对单一的逻辑，对数据进行操作

>>service是业务层

>>业务:分页,应该把这个事给业务处理层

>>



>需求分析

![icon](..img02/image/img02.png)





1.	先写 login.jsp , 并且搭配一个LoginServlet 去获取登录信息。



2.  创建用户表， 里面只要有id , username  和 password



3.  创建UserDao, 定义登录的方法 

```java

/**

* 该dao定义了对用户表的访问规则

*/

public interface UserDao {

/**

* 这里简单就返回一个Boolean类型， 成功或者失败即可。

* 但是开发的时候，登录的方法，一旦成功。这里应该返回该用户的个人信息

* @param userName 

* @param password

* @return true : 登录成功， false : 登录失败。

*/

	boolean login(String userName , String password);

}



```

4. 创建UserDaoImpl , 实现刚才定义的登录方法。

```java



		public class UserDaoImpl implements UserDao {

	

			@Override

			public boolean login(String userName , String password) {

				

				Connection conn = null;

				PreparedStatement ps = null;

				ResultSet rs   = null;

				try {

					//1. 得到连接对象

					conn = JDBCUtil.getConn();

					

					String sql = "select * from t_user where username=? and password=?";

					

					//2. 创建ps对象

					ps = conn.prepareStatement(sql);

					ps.setString(1, userName);

					ps.setString(2, password);





					//3. 开始执行。

					rs = ps.executeQuery();

					

					//如果能够成功移到下一条记录，那么表明有这个用户。 

					return rs.next();

					

				} catch (SQLException e) {

					e.printStackTrace();

				}finally {

					JDBCUtil.release(conn, ps, rs);

				}

				return false;

			}

		

		}

```

5. 在LoginServlet里面访问UserDao， 判断登录结果。 以区分对待



6. 创建stu_list.jsp , 让登录成功的时候跳转过去。



7. 创建学生表 ， 里面字段随意。 



8. 定义学生的Dao . StuDao  

```java

		public interface StuDao {

	

			/**

			 * 查询出来所有的学生信息

			 * @return List集合

			 */

			List<Student> findAll();

		}



```

9. 对上面定义的StuDao 做出实现 StuDaoImpl

```java

   	public class StuDaoImpl implements StuDao {



   		@Override

   		public List<Student> findAll() {

   			List<Student> list = new ArrayList<Student>();

   			Connection conn = null;

   			PreparedStatement ps = null;

   			ResultSet rs   = null;

   			try {

   				//1. 得到连接对象

   				conn = JDBCUtil.getConn();

   				

   				String sql = "select * from t_stu";

   				

   				ps = conn.prepareStatement(sql);

   				

   				rs = ps.executeQuery();



				//数据多了，用对象装， 对象也多了呢？ 用集合装。 

   				while(rs.next()){ //10 次 ，10个学生

   					

   					Student stu = new Student();

   					

   					stu.setId(rs.getInt("id"));

   					stu.setAge(rs.getInt("age"));

   					stu.setName(rs.getString("name"));

   					stu.setGender(rs.getString("gender"));

   					stu.setAddress(rs.getString("address"));

   					

   					list.add(stu);

   					

   				}

   			} catch (SQLException e) {

   				e.printStackTrace();

   			}finally {

   				JDBCUtil.release(conn, ps, rs);

   			}

   			

   			return list;

   		}

   	

   	}

```

10. 在登录成功的时候，完成三件事情。



11. 查询所有的学生



    2. 把这个所有的学生集合存储到作用域中。



    3. 跳转到stu_list.jsp



```java

			protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

	

			//提交的数据有可能有中文， 怎么处理。

			request.setCharacterEncoding("UTF-8");

			response.setContentType("text/html;charset=utf-8");

			

			//1. 获取客户端提交的信息

			String userName = request.getParameter("username");

			String password = request.getParameter("password");

			

			//2. 去访问dao ， 看看是否满足登录。

			UserDao dao = new UserDaoImpl();

			boolean isSuccess = dao.login(userName, password);

			

			//3. 针对dao的返回结果，做出响应

			if(isSuccess){

				//response.getWriter().write("登录成功.");

				

				//1. 查询出来所有的学生信息。

				StuDao stuDao = new StuDaoImpl();

				List<Student> list = stuDao.findAll();

				

				//2. 先把这个集合存到作用域中。

				request.getSession().setAttribute("list", list);

				

				//2. 重定向

				response.sendRedirect("stu_list.jsp");

				

			}else{

				response.getWriter().write("用户名或者密码错误！");

			}

		}

```

12. 在stu_list.jsp中，取出域中的集合，然后使用c标签 去遍历集合。 



```jsp

		<table border="1" width="700">

		<tr align="center">

			<td>编号</td>

			<td>姓名</td>

			<td>年龄</td>

			<td>性别</td>

			<td>住址</td>

			<td>操作</td>

		</tr>

	

		<c:forEach items="${list }" var="stu">

			<tr align="center">

				<td>${stu.id }</td>

				<td>${stu.name }</td>

				<td>${stu.age }</td>

				<td>${stu.gender }</td>

				<td>${stu.address }</td>

				<td><a href="#">更新</a>   <a href="#">删除</a></td>

			</tr>

		</c:forEach>

	</table>

```

13. 查询的细节:

    1). 查询出来的数据先放在作用域

    

    2). 在页面跳转时,应该判断,跳转的页面或者逻辑层能否有能力处理数据

    

    3). 模糊查询

    ```java

          String sql = "select * from stu where 1=1 ";//为了保留where

    

          List<String> list = new ArrayList<String>();//把参数放在list中

    

          //判断有没有姓名， 如果有，就组拼到sql语句里面

          if(!TextUtils.isEmpty(sname)){

              sql = sql + "  and sname like ?";

              list.add("%"+sname+"%");

          }

    

          //判断有没有性别，有的话，就组拼到sql语句里面。

          if(!TextUtils.isEmpty(sgender)){

              sql = sql + " and gender = ?";

              list.add(sgender);

          }

    ```

    

### 分页的拓展

>物理分页(真分页)



优点:内存中的数据量不会太大

缺点:对数据库访问频繁



>逻辑分页



一口气把所有数据全部查询出来,然后放在浏览器内存中

优点:访问速度快

缺点:如果数据量大,内存溢出



```java

物理分页:

sql:select * from stu limit 5 offset 2

  select * from stu 2,5

  显示5条,偏移2两条

```
