+++
title = "ROS基础学习2"
date = "2019-03-10"
description = "ROS基础"
featured = false
categories = [
  "ROS"
]
tags = [
  "ROS"
]
series = [
  "ROS"
]
images = [
]

+++

# ROS

### 工作空间:组织和管理功能包的文件夹

catkin workspace

>build (cmake,catkin缓存中间件)



>src(package 源代码)

>>package1(是catkin编译的基本单元)

>>package2

>>folder

>>>package3

>>>package3



>devel(目标文件)

>>头文件

>>动态连接库

>>静态连接库

>>可执行文件





### catkin(编译工具)

catkin ROS定制的编译构建系统



是对CMake的扩展



常用命令:



#### catkin_make:

>初始化,建立工作空间



eg:

```shell

mkdir -p ~/catkin_ws/src

cd ~/catkin_ws/

catkin_make

```

>编译



eg:

```shell

cd ~/catkin_ws #回到工作空间

catkin_make

source ~/catkin/devel/setup.bash #编译完成后需要使用source进行刷新

```

### package 功能包

是ROS软件的基本组织形式(一个个package)



catkin编译的基本单元



一个package可以包含多个节点(可执行文件),但是至少必须含有`CMakeLists.txt和package.XML`才能认为这是一个pkg



#### CMakeLists.txt

规定了catkin编译的规则(源文件,依賴項，目標文件)



eg:

```shell

cmake_mininum_required() #指定catkin的最低版本

project() #指定軟件包的name

find_package() #指定編譯時需要的依賴項

add_message_files()/add_service_files()/add_action_files()#添加消息文件/服務文件/動作文件

generate_message() #指定catkin信息給編譯系統生成cmake文件

add_library()/add_executable() #指定生成庫文件，可執行文件

target_link_libraries() #指定可執行文件鏈接那些庫

catkin_add_gtest() #添加單元測試

install() #生成可安裝目標

```

如果編譯過程中出現問題，一般都是這個文件的原因



#### package.XML 

包的自我描述：定义了package的属性,包名,版本号,作者,依賴等

```xml

<package><!--root-->

	<name><!--包名-->

	<version><!--版本号-->

	<description><!--包描述-->

	<maintainer><!--维护者-->

	<licsense><!--软件许可-->

	<buildtool_depend><!--编译工具-->

	<build_depend><!--编译时的依賴-->

	<run_depend><!--运行时的依賴-->

</package>

```

你也可能会看到manifest.xml,这是rosbuild编译系统使用的信息清單,类似catkin的package.XML



#### 代码文件: 源文件src(*.cpp/python module),頭文件include(*.h),腳本scripts(*.sh/*.py)



#### 自定義通信格式：消息msg(*.msg),服務srv(*.srv),動作action(*.action)



#### lauch文件(*.lauch):使多个可执行文件一起运行



#### 配置文件:config(*.yaml)



### 这样一来,我们的package目录结构就变成了:

package

>CMakeList.txt

>package.XML

>script

>

>>*.py/*.sh



>include

>

>>*.h



>src

>

>>*.cpp/python modulel



>msg

>

>>*.msg



>srv

>

>>*.srv



>action

>

>>*.action



>lauch

>

>>*.lauch



>config

>

>>*.yaml



### ros文件系统

常用操作:



#### rospack

查找某个pkg的地址



`rospack find pkg_name`



列出本地全部的pkg



`rospack list`



#### roscd

跳转到pkg的路径下



`roscd pkg_name`



#### rosls

列举某个pkg下的文件信息



`rosls pkg_name`



#### rosed

编辑pkg下的文件



`rosed pkg_name file_name`



#### catkin_create_pkg

创建一个pkg



`catkin_create_pkg <pkg_name> [deps]`



deps指的是这个pkg需要安装哪些依賴



#### rosdep

安裝某個pkg所需要的依賴



`rosdep install [pkg_name]`



主要给下载的pkg安装所需要的依賴



#### 例子：

```shell

#下載tree

sudo apt insall tree

#建立一個帶src的文件目錄

mkdir -p catkin_ws/src

#cd 到workspace

cd catkin_ws/

#tree查看文件結構

tree

#初始化

catkin_make

#显示1級目录

tree -L 1

#cd到src

cd src

#新建一个pkg

catkin_create_pkg test1

#查看文件结构

tree

#在建立pkg时制定依賴(cpp依賴,py依賴,通信依賴,导航依賴)

catkin_create_pkg test2 roscpp rospy std_msgs nav_msgs

```

最后,我们的文件目录是:



catkin_ws

>build

>devel

>src

>>CMakeList.txt

>>test1

>>>CMakeList.txt

>>>package.XML



>>test2

>>>CMakeList.txt

>>>include

>>>

>>>>test2



>>>package.xml

>>>src



#### 对于外部克隆下载的文件:

```shell

#cd 到工作空间

cd ~/catkin_ws/src

#下载或者克隆

git clone ```

cd ~/catkin_ws

#安装依賴

rosdep install [pkg_name]

#编译

catkin_make

#刷新环境(一般选择在配置文件中加入这句话)

source ~/catkin_ws/devel/setup.bash

```

最后一句如果:`echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc`



这样,我们每次打开一个新的终端,就会刷新一下source



### metapackage

ros官网称作stack(软件包集),其实指的是自己没有很多内容,大量依賴了其他的包的(link包?)



主要的一些metapackage:



navigation:导航相关



moveit:控制机械臂



image_pipeline:图像获取,处理



vision_opencv:ROS与openCV交互的功能包集



turtlebot:turtlebot机器人相关的包



pr2_robot:pr2机器人驱动功能包集



### ROS通信架构



#### master

节点管理器,管理node之间的通信



每个节点node启动时都需要向master注册



node1--注册-->master---->node2



我们在启动ROS时:

1. 先启动master:



`roscore`



可以启动master(节点管理器),rosout(日志输出),parameter server(参数服务器)



2. 启动node的一些相关命令:



启动node

`rosrun [pkg_name] [node_name]`



列出当前运行的node的详细信息

`rosnode info [node_name]`



结束运行node:

`rosrun kill [node_name]`



多个node需要启动时:



使用roslaunch,可以同时启动master和多个node



`roslaunch [pkg_name] [file_name.launch]`



其中file_name.launch的写法如下:

```xml

<launch>

	<node><!--需要启动的node及其参数-->

	<include><!--包含其他launch文件-->

	<machine><!--指定运行的機器-->

	<env_loader><!--设置环境变量-->

	<param><!--定义参数到参数服务器-->

	<arg><!--定义参数传到launch文件中-->

	<remap><!--设置参数映射-->

	<group><!--设置命名空间-->

</launch>

```

eg:`roslaunch pr2_bingup pr2.launch`



## 通信方式



### Topic(主题)

ROS中的異步通信方式



node之间通过publish-subscribe通信



nodeA--发--> /Topic --订阅--> nodeB 



eg:

node1(camera)

>/camera-rgb

>/camera-depth

>这些节点的msg都通过publish上传到topic

>



node2

>diplay

>从topic订阅



node3

>image_proless

>从topic订阅



#### 总结

1. 異步通信



通過使用publish()方法,直接发送到topic



2. 多對多通信



可以发送多个msg到topic



也可以有多个node从topic上订阅消息



3. topic通信有严格的格式要求,即Message(是topic内容要求的数据类型,定义在*.msg中)

>你可以把message看作一种数据类型,也就是一个对象,publish则时操作这种数据对象的一个类



#### msg

基本的msg包括:



bool,int8,int16,int32,int64,uint,float32,float64,string,time,duration,header,array[],array[C]



msg是一个类或者说结构体,例如`/camera_rgb`的msg格式

```

std_msgs/Header header

	uint32 seq

	time stamp

	string frame_id

	uint32 height

	uint32 width

	string encoding

	uint8 is_bigendian

	uint32 step

	uint8[] data

```

#### rostopic list

列出当前的全部topic



#### rostopic info /topic_name

显示某个topic的属性信息



#### rostopic echo /topic_name

显示某个topic的内容



#### rostopic pub /topic_name...

向topic发送内容



#### rosmsg list

列出系统上所有的msg



#### rosmag show /msg_name

显示某个msg内容



>如果两个node,在运行时会占用大量的资源,并且不是每一刻都需要对进行通信,使用service更好



### Service(服务)

ROS中的同步通信方式(阻塞等待reply)



Node之間可以通過request-reply的方式通信



NodeA(Client)--Req-->|<--Reply-- /Service <===>NodeB(Server)



service通信方式使用的通信格式是srv



定义在*.srv中,和msg类似



eg:

1. my_pkg/srv/DetectHuman.srv

```

bool start_detect#请求的格式

---

my_pkg/HumanPose[] pose_data #返回的是一个坐标数组

```

2. my_pkg/msg/HumanPose.msg(里面嵌套了一个msg)

```

std_msgs/Header header

	string uuid

	int32 number_of_joints

	my_pkg/JointPose[] joint_data

```

3. my_pkg/msg/JointPose.msg

```

string joint_name

geometry_msgs/Pose pose

float32 Confidence

```

#### rosserice list

列出当前所有活跃的service



#### rosserice info /service_name

显示某个service的属性信息



#### rosserice call /service_name args

调用某个service,args是参数



#### rossrv list

列出系统上所有的srv



#### rossrv show srv_name

显示出某个srv内容



### Parameter Service(参数服务器)

用于存储各种不常改变的参数,配置,以字典的形式存储,可以用命令行,launch,node来读取



#### rosparam list

列出所有参数



#### rosparam get param_key

显示出某个参数的值



#### rosparam set param_key

设置某个参数的值



#### rosparam dump file_name

保存参数到文件



#### rosparam load file_name

从文件读取参数



#### rosparam delete param_key

删除参数



### Action(动作)

一种问答通信机制，带有连续反馈，可以在任务过程中终止运行，基于ROS的消息机制实现

类似service,带有状态反馈的通信方式



通常用在长时间,可抢占(可打断)的任务中



同理action时Action通信使用的数据格式,定义在*.action中



eg:/action/DoDishes.action(分为三部分)

```shell

#Define the goal (client发出)

uint32 dishwasher_id

#Specify which dishwasher we want to use

---

#Define the result (只回答一次,server发出)

uint32 total_dishes_cleaned

---

#Define a feedback message (实时回传多次,server发出)

float32 percent_complete

```

举一个洗碗机的例子:



Client--goal(洗碗机的Id)-->Server



Server--feedback(洗碗的进度)-->Client



Server--result(洗碗的数量,时间)-->Client



#### 常用的API

- goal:发布任务目标



- cancel:请求取消任务



- status:通知客户端当前的状态



- feedback:周期反馈任务运行的监控数据



- result:向客户端发送任务的执行结果，只发布一次





## ROS常用的工具



### 仿真工具: Gazebo,CV-rep,Carsim



### 调试,可视化工具:Rviz,rqt



#### Rviz(The Robot Visualization tool)



#### rqt



是一个可视化工具,常用的工具有:



##### rqt_graph(查看通信结构,msg的流向)



##### rqt_plot(曲线绘制的工具,可以看到,信息中的数据的变化)



##### rqt_console(查看日志)



### 命令行工具:rostopic,rosbag...



#### rosrun :可以运行node



#### rosbag:可以记录和回放数据流



使用方法:



/topic1 | /topic2-->record-->*.bag文件-->play--> /topic1 | /topic2



##### rosbag record [topic-names]

记录某些topic到bag中



##### rosbag record - a(a=all)

记录全部的topic



##### rosbag play [bag-files]

回放topic



eg:

```shell

rosbag record /camera/rgb/image_raw

roscore

rosbag play *.bag(bag-files)

rostopic list #查看回放有哪一些topic

rostopic info /camera/rgb/image_raw #查看回放中的这个topic

rosrun image_view image_view image:=/camera/rgb/image_raw #run这个节点,查看回放的图像

```

### 专用工具:Moveit(机械臂)



## Client Library

提供ROS编程的库(roscpp,rospy,roslisp等),类似接口,但是在API的基础上进行了封装

