+++
title = "Ubuntu18.04安装ROS"
date = "2019-02-10"
description = "ROS安装"
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

# Ubuntu18.04安装ROS

## 源配置:


```

sudo sh -c '. /etc/lsb-release && echo "deb <http://mirrors.ustc.edu.cn/ros/ubuntu/> $DISTRIB_CODENAME main" > /etc/apt/sources.list.d/ros-latest.list'



```

## 更新:



`sudo apt-get update`



## 添加密匙:

`sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116`



## 和官网步骤一样:

`sudo apt-get install ros-melodic-desktop-full`

`sudo rosdep init`

### 报错:

由于py版本导致,网上说切换为python2.7,我失败了

```

Traceback (most recent call last):  File "/usr/bin/rosdep", line 3, in <module>    from rosdep2.main import rosdep_mainModuleNotFoundError: No module named 'rosdep2'

```

### 重头戏来了:

`sudo apt-get install python3-catkin-pkg`

` sudo apt-get install python3-rosinstall python3-rosinstall-generator python3-wstool build-essential`

### 再次运行:

`sudo rosdep init`

`rosdep update`

### 感觉没问题?

`echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc`

`source ~/.bashrc`

#### 报错:

```

没有找到 /opt/ros/melodic/setup.bash

```

### 强行来:

`roscore`

#### 报错:

```

Command 'roscore' not found, but can be installed with:

sudo apt install python-roslaunch

```

输入

`sudo apt install python-roslaunch`



发现无法定位包?



输入`sudo apt-get update`后再试,无效.....



给出的依賴要求python-roslib，可是我在安裝python3-*的指令時看到已经安好了,错误不在这里



怎么办阿...



### cd 到 /opt/ros/melodic/

`cd  /opt/ros/melodic/`



`ls -l`



发现没有sh脚本????!!!!



`sudo apt-get install ros-melodic-desktop`



我太机智了!



cd 进去再看,有了!



## OK `source ~/.bashrc`



成功了



## 安装完成,进行验证:`roscore`



### 报错:

```

raise DistributionNotFound(req, requirers)pkg_resources.DistributionNotFound: The 'rospkg==1.1.7' distribution was not found and is required by the application

```

???我最熟悉的python包报错!简单!



`pip install rospkg`



看到whl下载的进度,成了



`roscore`



 ![图片](http://a1.qpic.cn/psb?/V12PNcjx0cfqHx/wM1j7ogE*bFOc*P7dy2NSxYjqQ8KjxZMk4uHEo02*hk!/b/dPQAAAAAAAAA&ek=1&kp=1&pt=0&tl=3&su=0180658497&tm=1547877600&sce=0-12-12&rf=2-9)
