+++
title = "Flask入门"
date = "2019-02-14"
description = "Flask"
featured = false
categories = [
  "Flask"
]
tags = [
  "python",
  "Flask"
]
series = [
  "Flask"
]
images = [
]

+++


## Flask 学习
![](http://docs.jinkan.org/docs/flask/)
## 入门：
### 最小的Flask 程序

```python

from flask import Flask # 导入flask

app = Flask(__name__)#使用单一的模块（如本例），你应该使用 __name__



@app.route('/hello') #route()装饰器 什么样子的URL能触发我们的函数

def hello_word():

    return 'Hello Word!'#返回我们想在浏览器中显示的内容



if __name__ == '__main__': #确保服务器只会在该脚本被 Python 解释器直接执行的时候才会运行，而不是作为模块导入的时候

    #app.run()#让app这个应用在本地服务器运行起来

    #app.run(host='0.0.0.0') #监听所有的公网IP

    app.debug = True

    app.run()#q启动调试器

```

### 模板渲染

Jinja2模板引擎文档

![](http://docs.jinkan.org/docs/jinja2/)

```python

from flask import Flask # 导入flask

from flask import render_template #使用Jinja2的模版渲染



app = Flask(__name__)#使用单一的模块（如本例），你应该使用 __name__



@app.route('/hello') #route()装饰器 什么样子的URL能触发我们的函数

def hello_word():

    return render_template("hello.html")#返回的模板文件（需要放在当前目录的templates文件夹内）



if __name__ == '__main__': #确保服务器只会在该脚本被 Python 解释器直接执行的时候才会运行，而不是作为模块导入的时候

    #app.run()#让app这个应用在本地服务器运行起来

    #app.run(host='0.0.0.0') #监听所有的公网IP

    app.debug = True

    app.run()#q启动调试器

```

```html

<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <title>Hello Template</title>

</head>



<body>

    <h1>Hello World!</h1>

</body>

</html>

```

### 变量规则

 URL的变量部分：`<variable_name>` 

规则可以用 `<converter:variable_name>`指定一个可选的转换器。这里有一些不错的例子:

```python

@app.route('/user/<username>')

def show_user_profile(username):

    # show the user profile for that user

    return 'User %s' % username



@app.route('/post/<int:post_id>')

def show_post(post_id):

    # show the post with the given id, the id is an integer

    return 'Post %d' % post_id

```

转换器的类型

int ： 接受整数

float ：同int，但是接受浮点数

path ：和默认的相似，但也接受浮点数







### URL规范

以这两个规则为例:

```python

@app.route('/projects/')

def projects():

    return 'The project page'



@app.route('/about')

def about():

    return 'The about page'

```

第一种情况中，指向 projects 的规范 URL 尾端有一个斜线。这种感觉很像在文件系统中的文件夹。访问一个结尾不带斜线的 URL 会被 Flask 重定向到带斜线的规范 URL 去。



第二种情况的 URL 结尾不带斜线，类似 UNIX-like 系统下的文件的路径名。访问结尾带斜线的 URL 会产生一个 404 “Not Found” 错误。



在遗忘尾斜线时，允许关联的 URL 接任工作，与 Apache 和其它的服务器的行为一样。此外，也保证了 URL 的唯一，有助于避免搜索引擎索引同一个页面两次。



#### 结论：使用不带尾斜线的url



### 构造URL

使用`url_for()` 来给指定的函数构造 URL

#### 优点

>URL 构建会转义特殊字符和 Unicode 数据



>如果你的应用不位于 URL 的根路径（比如，在 /myapplication 下，而不是 / ）， url_for() 会妥善处理这个问题



>反向构建通常比硬编码的描述性更好。更重要的是，它允许你一次性修改 URL， 而不是到处边找边改



例子：

```python

from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')

def index(): pass



@app.route('/login')

def login(): pass



@app.route('/user/<username>')

def profile(username): pass



with app.test_request_context():

'''test_request_context:即使我们正在通过 Python 的 shell 进行交互，它依然会告诉 Flask 要表现为正在处理一个请求'''

    print url_for('index')

    print url_for('login')

    print url_for('login', next='/')

    print url_for('profile', username='John Doe')

```

输出：

```

/

/login

/login?next=%2F

/user/John%20Doe

```



### HTTP方法：

 默认情况下，路由只回应 GET 请求，`route()` 装饰器传递` methods` 参数可以改变这个行为



例子：

```python

from flask import Flask # 导入flask

from flask import render_template #使用Jinja2的模版渲染

from flask import request,redirect,url_for







app = Flask(__name__)



@app.route('/login', methods=['POST','GET'])

def login():

    error = None

    if request.method == 'POST':

        if request.form['username']=='admin' and request.form['password']=='root':

            return redirect(url_for('home',username=request.form['username']))

        else:

            error = 'Invalid username/password'

    return render_template('login.html', error=error,username=request.form['username'])



@app.route('/home')

def home():

    return render_template('home.html', username=request.args.get('username'))





if __name__ == '__main__': #确保服务器只会在该脚本被 Python 解释器直接执行的时候才会运行，而不是作为模块导入的时候

    #app.run()#让app这个应用在本地服务器运行起来

    #app.run(host='0.0.0.0') #监听所有的公网IP

    app.debug = True

    app.run()#q启动调试器

```

/login.html文件:

```html

<!DOCTYPE html>

<html lang="zh-CN">

  <head>

    <meta charset="utf-8">

    <title>login</title>

  </head>

  <body>

    <form  style="margin:20px;" method="post" action="/login">

        username:<br>

        <input type="text" name="username" id="name">

        <br>

        password:<br>

        <input type="password" name="password" id="pwd">

        <br>

        <button type="submit" id="loginBtn">login</button>

    </form>



    {% if error %}

    {% if username %}

    <h1 style="color:red">Dear {{ username }}:{{ error }}!</h1>

    {% endif %}

    {% endif %}

  </body>

</html>

```

home主页：

```html

<!DOCTYPE html>

<html lang="zh-CN">

  <head>

    <meta charset="utf-8">

    <title>home</title>

  </head>

  <body>

    <h1>wlcome {{username}} , this is home</h1>

  </body>

</html>

```



#### 解析

>render_template ： 将请求定位到模板文件上，处理模板文件后，将结果作为请求的响应返回



>redirect：将请求的响应重定向到新的url上。当登录成功后，重定向到 home页面



>url_for：根据参数生成url



>request对象包含了所有的请求信息，通过它可获取所需要的请求信息:



>app.route增加了methods参数，指明该url支持的http请求方式，默认是get方式。/login即作为get，也作为post的请求目标





### 自定义错误处理程序

定制错误页面， `@errorhandle`装饰器

```python

from flask import Flask # 导入flask

from flask import render_template #使用Jinja2的模版渲染

from flask import request,redirect,url_for



app = Flask(__name__)

@app.route('/index') #route()装饰器 什么样子的URL能触发我们的函数

def index():

    return render_template("index.html")



@app.errorhandler(404)

def not_found_error(error):

	return render_template('404.html'), 404

	

@app.errorhandler(404)

def not_found(error):

    resp = make_response(render_template('404.html'), 404)

    

    resp.headers['X-Something'] = 'A value'

    return resp



@app.errorhandler(500)

def internal_error(error):

    return render_template('500.html'), 500



if __name__ == '__main__': #确保服务器只会在该脚本被 Python 解释器直接执行的时候才会运行，而不是作为模块导入的时候

    #app.run()#让app这个应用在本地服务器运行起来

    #app.run(host='0.0.0.0') #监听所有的公网IP

    app.debug = True

    app.run()#q启动调试器

```

### 静态文件

 只要在你的包中或是模块的所在目录中创建一个名为 static 的文件夹，在应用中使用 /static 即可访问CSS 和 JavaScript 静态文件

`url_for('static', filename='style.css')`



### flask的线程安全

#### 环境局部变量

一个请求传入，Web 服务器决定生成一个新线程（ 或者别的什么东西，只要这个底层的对象可以胜任并发系统，而不仅仅是线程）。 当 Flask 开始它内部的请求处理时，它认定当前线程是活动的环境，并绑定当前的应用和 WSGI 环境到那个环境上（线程）。它的实现很巧妙，能保证一个应用调用另一个应用时不会出现问题。



如果我们需要左自动化测试：

创建一个请求对象并且把它绑定到环境中：用` test_request_context()` 环境管理器。结合 with 声明.绑定一个测试请求



```python

from flask import request



with app.test_request_context('/hello', method='POST'):

    # now you can do something with the request until the

    # end of the with block, such as basic assertions:

    assert request.path == '/hello'

    assert request.method == 'POST'

```

或者传递整个WSGI环境给`request_context() `

```python

from flask import request



with app.request_context(environ):

    assert request.method == 'POST'

```



### Request的常用操作

导入`from flask import request`

通过` [method]`属性来访问不同的HTTP请求



通过:`attr:~flask.request.form` 属性来访问表单数据() POST 或 PUT 请求提交的数据)



通过args属性访问url中提交的参数

`searchword = request.args.get('q', '')`



#### others

当访问 form 属性中的不存在的键会发生什么？会抛出一个特殊的 KeyError 异常。你可以像捕获标准的 KeyError 一样来捕获它，推荐用 get 来访问 URL 参数或捕获 KeyError



#### 文件上传

1. 在html的表单中设置`enctype="multipart/form-data"`

2. 通过请求对象的 files 属性访问文件的临时存储，它是一个标准的 Python file 对象，但它还有一个 save() 方法，允许你把文件保存到服务器的文件系统上

3.` filename` 属性：上传前文件在客户端的文件名，这个值是可以伪造的





例子：把客户端上传的文件按照上传前的文件名保存在服务器上

```python

from flask import request

from werkzeug import secure_filename



@app.route('/upload', methods=['GET', 'POST'])

def upload_file():

    if request.method == 'POST':

        f = request.files['the_file']

        f.save('/var/www/uploads/' + secure_filename(f.filename))

```



#### Cookies

通过 `cookies` 属性来访问 Cookies，用响应对象的 `set_cookie `方法来设置 Cookies

读取Cookies：

```python

from flask import request



@app.route('/')

def index():

    username = request.cookies.get('username')

    # use cookies.get(key) instead of cookies[key] to not get a

    # KeyError if the cookie is missing.

```

存储Cookies

```python

from flask import make_response



@app.route('/')

def index():

    resp = make_response(render_template(...))

    '''

    Cookies 是设置在resp对象上的。由于通常视图函数只是返回字符串，之后 Flask 将字符串转换为响应对象。如果你要显式地转换，你可以使用 make_response() 函数然后再进行修改。

    '''

    resp.set_cookie('username', 'the username')

    return resp

```



#### Session

允许你在不同请求间存储特定用户的信息，是在 Cookies 的基础上实现的，并且对 Cookies 进行密钥签名。这意味着用户可以查看你 Cookie 的内容，但却不能修改它，除非用户知道签名的密钥

```python

from flask import Flask, session, redirect, url_for, escape, request



app = Flask(__name__)



@app.route('/')

def index():

    if 'username' in session:

        return 'Logged in as %s' % escape(session['username'])

    return 'You are not logged in'



@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        session['username'] = request.form['username']

        return redirect(url_for('index'))

    return '''

        <form action="" method="post">

            <p><input type=text name=username>

            <p><input type=submit value=Login>

        </form>

    '''



@app.route('/logout')

def logout():

    # remove the username from the session if it's there

    session.pop('username', None)

    return redirect(url_for('index'))



# set the secret key.  keep this really secret:

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

```

强壮的密钥

```python

import os

os.urandom(24)

```



###  响应对象

视图函数的返回值会被自动转换为一个响应对象。如果返回值是一个字符串， 它被转换为该字符串为主体的、状态码为 `200 OK`的 、 MIME 类型是 `text/html` 的响应对象。

>Flask 把返回值转换为响应对象的逻辑是这样：



1. 如果返回的是一个合法的响应对象，它会从视图直接返回。

2. 如果返回的是一个字符串，响应对象会用字符串数据和默认参数创建。

3. 如果返回的是一个元组，且元组中的元素可以提供额外的信息。这样的元组必须是 (response, status, headers) 的形式，且至少包含一个元素。 status 值会覆盖状态代码， headers 可以是一个列表或字典，作为额外的消息标头值。

4. 如果上述条件均不满足， Flask 会假设返回值是一个合法的 WSGI 应用程序，并转换为一个请求对象。



例子可以看之前的错误页面的内容



### logger

服务器错误，但要让代码继续运行，你需要日志

```python

app.logger.debug('A value for debugging')

app.logger.warning('A warning occurred (%d apples)', 42)

app.logger.error('An error occurred')

```

