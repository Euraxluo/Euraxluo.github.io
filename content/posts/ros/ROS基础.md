+++
title = "ROS基础学习1"
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


## 利用enve使用在ros中使用python3
因为ros的python有很多依赖需要使用C，python3的支持不太好。我们可以让当前的环境变量依然是python2，为ros创建一个py3的enve来给它使用


### 查看版本：

```shell

pip -V

pip3 -V

python -V

python3 -V

```

我的pip和python都是py2.7的



接下来在你的工作空间中创建enve

```shell

mkdir -p catkin_ws/src

cd catkin_ws

pip3 install virtualenv #先安装

virtualenv -p /usr/bin/python3 venv#创建一个名为enve的python3环境

source venv/bin/activate #激活enve

#创建成功，你应该会看到shell的变化，你可以在这里试一下pip和python，会发现已经变成python3了。

deactivate #关闭enve

```



## SLAM 同时定位建模

移动机器人的主要任务：定位，建模，路径规划



### slam 建模工具包：

Gmapping，Karto，Heotor，Gartographer



### ROS支持的定位工具包：

自适应蒙特卡罗定位：AMCL



### 导航工具包集

Navigation：Local，Global

Global：Dijkstra，A×

Local;DWA



### SLAM中的MAP：

本质也是一个msg

Topic：/map

Type：nav_msgs/OccupancyGrid(栅格地图)



### Gmapping Topic

输入：base到odom的tf， /scan

输出：

定位信息：map_frame>odom的tf消息

mapping:topic -/map _msg



### Karto topic

输入和Gmapping一样

输出：map_frame ->odom



![](/image/Gamapping&karto.png)



### Navigation matepkg

![](/image/Navigation.png)



