+++
title = "WebSocket"
date = "2020-10-22"
description = "WebSocket"
featured = false
categories = [
  "WebSocket"
]
tags = [
  "Java",
  "WebSocket"
]
series = [
  "WebSocket"
]
images = [
]
+++

# WebSocket
### 一、概念
1.WebSocket 是HTTP协议的补充。使用的TCP协议建立连接

2.HTML5是指一系列新API，新协议，WebSocket也是其中之一

### 二、优点

1.WebSocket是持久化协议，每次通信只需要一次连接

2.HTTP中一个request只能有一个response

3.连接过程：进行握手时，使用http协议对服务器发起连接请求，并且升级为websocket协议，确定后服务器建立连接，并且继续使用Websocket

### 三、作用

1.实现实时信息传递的其他方式

​	(1).ajax轮询：让浏览器隔个几秒就发送一次请求，询问服务器是否有新信息

​	(2).HTTP long poll：客户端发起连接后，如果没消息，就一直不返回Response给客户端。直到有消息才返回，返回完之后，客户端再次建立连接，周而复始。

​	(3).缺点：

​	ajax轮询：需要服务器有很快的处理速度和资源。（速度）

​	long poll：需要有很高的并发，也就是说同时接待客户的能力。（资源大小）

2.服务器完成协议升级后（HTTP->Websocket），服务端就可以主动推送信息给客户端啦

3.整个通讯过程是建立在一次连接/状态中，避免了HTTP的非状态性，服务端会一直知道你的信息，直到你关闭请求

### 四、特点

1.建立在 TCP 协议之上，服务器端的实现比较容易。

2.与 HTTP 协议有着良好的兼容性。默认端口也是80和443，并且握手阶段采用 HTTP 协议，因此握手时不容易屏蔽，能通过各种 HTTP 代理服务器。

3.数据格式比较轻量，性能开销小，通信高效。

4.可以发送文本，也可以发送二进制数据。

5.没有同源限制，客户端可以与任意服务器通信。

6.协议标识符是ws（如果加密，则为wss），服务器网址就是 URL。

### 五、客户端

#### 1.创建WebSocket对象：

`var Socket = new WebSocket(url,[protocol])`

url = 服务器地址，protocol是可接受的子协议

#### 2.属性：

(1)`Socket.readyState//表示连接状态：0：尚未连接，1：已经连接，2：连接正在关闭，3：连接已经关闭，或不能打开。`



(2)`Socket.buffererdAmount//表示send()放在队列正在队列中等待传输`

#### 3.事件：



| 对象触发的程序   | 描述                       |

| ---------------- | -------------------------- |

| Socket.onopen    | 连接建立时触发             |

| Socket.onmessage | 客户端接受服务端数据时触发 |

| Socket.onerror   | 通信错误时触发             |

| Socket.onclose   | 连接关闭时触发             |



#### 4.方法：



| 方法           | 描述                 |

| -------------- | -------------------- |

| Socket.send()  | 使用连接程序发送数据 |

| Socket.close() | 关闭连接             |



#### 5.实例：

##### 客户端前端：



```html

<html>

<head>

<script type="text/javascript">

</head>

<body>

<input type="button" onclick="online()" value="连接！" />

</body>

<script>

//初始化一个WebSocket对象

var ws = new WebSocket("wss://echo.websocket.org");



//建立WebSocket连接成功触发事件

ws.onopen = function online() { //js的事件写法

	alert("我是一个消息框！")

  	ws.send("Hello WebSockets!");//使用send发送数据

};



//接受服务端数据时触发的数据

ws.onmessage = function(evt) {

   var received_msg = evt.data;

  alert("数据已接收...");

  ws.close();

};



//断开WebSocket时触发的数据

ws.onclose = function(evt) {

  alert("数据已接收...");

};

</script>

</html>

```



### 六、服务器端

#### Node.js



```javascript

var ws = require('nodejs-websocket');

console.log('开始建立连接...')



ws.createServer(function (conn) {

    conn.on('text', function (str) {

        console.log('收到的信息为:' + str)

        conn.sendText(str)

    })

    conn.on('close', function (code, reason) {

        console.log('关闭连接', code, reason)

    });

    conn.on('error', function (code, reason) {

        console.log('异常关闭', code, reason)

    });

}).listen(8888)

console.log('WebSocket建立完毕');

```



#### java

1.Spring



```java

public interface WebSocketHandler {

   /**

    * 建立连接后触发的回调

    */

   void afterConnectionEstablished(WebSocketSession session) throws Exception;

   /**

    * 收到消息时触发的回调

    */

   void handleMessage(WebSocketSession session, WebSocketMessage<?> message) throws Exception;

   /**

    * 传输消息出错时触发的回调

    */

   void handleTransportError(WebSocketSession session, Throwable exception) throws Exception;

   /**

    * 断开连接后触发的回调

    */

   void afterConnectionClosed(WebSocketSession session, CloseStatus closeStatus) throws Exception;

   /**

    * 是否处理分片消息

    */

   boolean supportsPartialMessages();

}

```



2.javax.websocket



```java

// 收到消息触发事件

@OnMessage

public void onMessage(String message, Session session) throws IOException, InterruptedException {

    ...

}

// 打开连接触发事件

@OnOpen

public void onOpen(Session session, EndpointConfig config, @PathParam("id") String id) {

    ...

}

// 关闭连接触发事件

@OnClose

public void onClose(Session session, CloseReason closeReason) {

    ...

}

// 传输消息错误触发事件

@OnError

public void onError(Throwable error) {

    ...

}

```



### 七、完整实例（环境：tomcat8，idea）



#### 服务器端：



```java

/**

 * netstat -aon | findstr 1099

 * taskkill -f -pid PID

 */



package servlet;



import javax.websocket.*;

import javax.websocket.server.ServerEndpoint;

import java.io.IOException;

import java.util.concurrent.CopyOnWriteArraySet;



//指明websocket名字

@ServerEndpoint("/chat")



public class WS {

    //通过SESSION发送数据

    private Session session;



    //静态变量，用来记录当前在线连接数。应该把它设计成线程安全的。

    private static int onlineCount = 0;



    //concurrent包的线程安全Set，用来存放每个客户端对应的MyWebSocket对象。若要实现服务端与单一客户端通信的话，可以使用Map来存放，其中Key可以为用户标识

    private static CopyOnWriteArraySet<WS> webSocketSet = new CopyOnWriteArraySet<WS>();







    /*

     * 连接建立成功调用的方法

     * @param session

     */

    @OnOpen

    public void onOpen(Session session){

        this.session = session;

        webSocketSet.add(this);     //加入set中

    }



    /**

     * 收到客户端消息后调用的方法

     * @param message 客户端发送过来的消息

     * @param session 可选的参数

     */

    @OnMessage

    public void onMessage(String message, Session session) throws IOException {

        System.out.println("来自客户端的消息:" + message);

        //群发消息

        for(WS item: webSocketSet){

            try {

                item.sendMessage(message);

            } catch (IOException e) {

                e.printStackTrace();

                continue;

            }

        }

    }



    /**

     * 连接关闭调用的方法

     */

    @OnClose

    public void onClose(){

        webSocketSet.remove(this);  //从set中删除

    }





    /**

     * 发生错误时调用

     * @param session

     * @param error

     */

    @OnError

    public void onError(Session session, Throwable error){

        System.out.println("发生错误");

        error.printStackTrace();

    }





     /* 这个方法与上面几个方法不一样。没有用注解，是根据自己需要添加的方法。

     * @param message

     * @throws IOException

    */

    public void sendMessage(String message) throws IOException {

        this.session.getAsyncRemote().sendText(message);

    }





}



```







#### 浏览器端：



```java

<%--

  Created by IntelliJ IDEA.

  User: Euraxluo

  Date: 2018/7/30

  Time: 14:19

  To change this template use File | Settings | File Templates.

--%>

<!DOCTYPE html>

<%@ page contentType="text/html;charset=UTF-8" language="java" %>

<html doctype="html"><head>

    <meta http-equiv="content-type" content="text/html; charset=UTF-8">

    <meta charset="utf-8">

    <title>chat</title>

    <!-- 输入框-->

    <link href="css/vendor/bootstrap/bootstrap.min.css" rel="stylesheet">

    <link href="http://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" rel="stylesheet">

    <link rel="stylesheet" href="js/vendor/summernote/summernote.css">

    <style>

        * {

            padding: 0;

            margin: 0;

        }



        body{

            height: 100%;

            border:2px solid;

            border-radius:5px;

            background-image: url('images/bkg.jpg');

            scrollbar-face-color: #22beef;



        }

        ::-webkit-scrollbar-button{

            background-color: #1ccdaa;

        }

        ::-webkit-scrollbar-track{

            background-color: #1296db;

        }

        ::-webkit-scrollbar-thumb{

            background-color: #22beef;

        }

        <!---->

        .welcome

        {

            color:#fff;

            margin-left: -1px;

            background-color: #2cc1f0;

            border-color: #4cae4c;

            width: 100%;

            height: 70%;

            border-radius:10px;

            font-size: 30px;

        }



        header{

            border:2px solid #2a6496;

            border-radius:8px;

            height:80px;

            width: 100%;

            position: relative;

            overflow-y: auto;

            margin-top: 2%;

            padding: 5px;

        }





        <!---->

        .hist{



            margin-bottom: 2px;

            margin-left: 1px;

            width: 100%;

            overflow-y: scroll;

            background-image: url("images/bgk2.jpg");



        }

        .hist span{

            background-color: #11b4e7;

        }



        .hist li{

            list-style:none;

            margin-left: 2px;

            margin-top: 5px;

            padding: 0px;

            float:bottom;

            padding-left: 5px;

            padding-right: 3px;

            display: table;

            overflow: auto;

            min-width: 100px;

            max-width: 100vw;

            word-break: break-all;

            word-wrap: break-word;

            min-height: 100px;

            border:2px solid #2a6496;

            border-radius: 5px;

            background-image: url('images/bgk0.jpg');



        }



        .but{

            height: 30px;

            line-height: 35px;

            position: fixed;

            bottom: 180px;

            width: 100%;

            text-align: center;

            color: #fff;

            font-size: 14px;

            letter-spacing: 1px;

            background-color: #96e6f1;

        }

        .left{

            text-align: center;

            vertical-align: middle;

            cursor: pointer;

            white-space: nowrap;

            color: #fff;

            background-color: #5cb85c;

            border-color: #4cae4c;

            padding: 6px 12px;

            font-size: 14px;

            line-height: 1.5;

            border-radius: 4px;

            height: 30px;

            float: left;

            display: inline-block;

            font-weight: 400;





        }

        .right{



            text-align: center;

            vertical-align: middle;

            cursor: pointer;

            white-space: nowrap;

            color: #fff;

            background-color: #5cb85c;

            border-color: #4cae4c;

            float: right;

            display: inline-block;

            font-weight: 400;

            padding: 6px 12px;

            font-size: 14px;

            line-height: 1.5;

            border-radius: 4px;

            height: 30px;

        }

        .foot{

            height: 180px;

            line-height: 35px;

            position: fixed;

            bottom: 0;

            width: 100%;

            color: #fff;

            font-size: 14px;

            letter-spacing: 1px;

            background-image: url('images/bgk3.gif');



        }

    </style>

</head>



<header id="top">

    <button class="welcome" onclick="printme()"><strong>Welcome</strong></button>

    <!--状态栏-->

    <strong style="float: left">状态：</strong>

    <strong id="message" ></strong>

</header>



<div style="clear: both">



<div id="historyMsg"  class="hist" ></div>



</div>

    <div class="but">

        <button type="button"  class="right" onclick="send()"><strong>Send</strong></button>

        <button type="button" class="left"  onclick="closeWebSocket()"><strong>Close</strong></button>

    </div>





<div class="foot">

    <!--summernote-->

    <div id="summernote"></div>



</div>







<script src="js/jquery.js"></script>

<script src="js/vendor/bootstrap/bootstrap.min.js"></script>

<script type="text/javascript" src="js/vendor/mmenu/js/jquery.mmenu.min.js"></script>

<script type="text/javascript" src="js/vendor/sparkline/jquery.sparkline.min.js"></script>

<script type="text/javascript" src="js/vendor/nicescroll/jquery.nicescroll.min.js"></script>

<script src="js/vendor/tabdrop/bootstrap-tabdrop.min.js"></script>



<script src="js/vendor/summernote/summernote.min.js"></script>

<script src="js/minimal.min.js"></script>

<script type="text/javascript">



    window.onload = windowHeight; //页面载入完毕执行函数

    function windowHeight() {

        var h = document.documentElement.clientHeight; //获取当前窗口可视操作区域高度

        var history = document.getElementById("historyMsg");

        history.style.height = (h-294-30) + "px"; //你想要自适应高度的对象

    }

    setInterval(windowHeight, 100)//每100微秒执行一次windowHeight函数

    //精简版

    $(document).ready(function () {

        $('#summernote').summernote({

            height: 180,

            focus:true,

            toolbar: [

                ['style', ['bold', 'italic', 'underline', 'clear']],

                ['fontsize', ['fontsize']],

                ['color', ['color']],

                ['para', ['ul', 'ol', 'paragraph']],

                ['height', ['height']],

            ]/*,

            callbacks: {

                onImageUpload: function (files) { //the onImageUpload API

                    send(sendFile(files[0]));

                }

            }*/

        });

    });

/*

    function sendFile(file) {

        var data = new FormData();

        data.append("file", file);

        alert(data);

        console.log(data);

        $.ajax({

            data: data,

            type: "POST",

            url: "/upload/uploadPic.html",

            cache: false,

            contentType: false,

            processData: false,

            //dataType: "json",

            success: function (url) {//data是返回的hash,key之类的值，key是定义的文件名

                alert(url);

            $('#summernote').summernote('insertImage',url,'image name');



        },

        error:function () {

            alert("上传失败");

            },

        });

    }

    */

    //构建通道

    var websocket = new WebSocket("ws://localhost:8080/chat");



    //连接成功建立的回调方法

    websocket.onopen = function(evt){

        loginMessage("open");

    };

    var name="root";



    //连接发生错误的回调方法

    websocket.onerror = function(evt){

        loginMessage("error");



    };



    //接收到消息的回调方法

    websocket.onmessage = function(evt){

        setMessageInnerHTML("<li><sanp><strong>"+name+":</strong><br>"+evt.data+"</sanp></li>");

    };

    //连接关闭的回调方法

    websocket.onclose = function(evt){

        loginMessage("close");

    };



    //监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。

    window.onbeforeunload = function(evt){

        websocket.close();

    };

    //将消息显示在网页上

    function loginMessage(innerHTML){

        document.getElementById('message').innerHTML = innerHTML;

    }



    //将消息显示在网页上

    function setMessageInnerHTML(innerHTML){

        document.getElementById('historyMsg').innerHTML += innerHTML;

    }

    //将消息显示在网页上

    function setMessagehistory(innerHTML){

        document.getElementById('historyMsg').innerHTML += innerHTML;s

    }

    //关闭连接

    function closeWebSocket(evt){

        websocket.close();

    }



    //发送消息

    function send(evt){

        var message = $("#summernote").summernote('code');

        $("#summernote").summernote('code','');



        var regexstr =new RegExp('<(?!img|br/|p|/p).*?>'); //去除标签

        var str=message.replace(regexstr,"");

        websocket.send(str);

    }

    //发送给自己

    function printme(evt){

        alert("Welocom to chat_room!");

    }

</script>

</body>

</html>



```







































