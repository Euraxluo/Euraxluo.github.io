---
title: "chromedriver-安装"
date: "2019-02-21"
description: "chromedriver-安装"
featured : false
categories: ["notes"]
tags: [ "chromedriver" ]
images: []
---

![reference])(https://blog.csdn.net/shuchuan0409/article/details/101615221)

第一步：

执行 sudo apt-get update  更新apt-get，耗时可能会比较久

第二步：安装谷歌浏览器

直接下载谷歌浏览器最新版：wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

安装：dpkg -i google-chrome-stable_current_amd64.deb

如果不出意外，上面这一步一般都不会安装成功（但是也要执行），这个时候我们需要执行 ：apt-get install -f 用来下载兼容或者必须的一些软件包

等下载完成以后再重新安装谷歌浏览器，这个时候要记下谷歌浏览器的版本号，这是个很重要的信息，下面安装chromedriver的时候需要使用

Unpacking google-chrome-stable (77.0.3865.90-1) 里面的77.0.3865.90-1就是谷歌浏览器的版本号

第三步：

安装xvfb 安装这个工具是为了让我们可以无界面运行谷歌浏览器，直接apt-get安装即可

sudo apt-get install xvfb

第四步：安装chromedriver

下载chromedriver的安装包，直接访问地址：http://chromedriver.storage.googleapis.com/index.html 去下载自己浏览区对应的版本，如果找不到自己浏览器对应的版本，就找个比较接近的版本就行了，比如我这边的谷歌版本号是77.0.3865.90，但是网站上并没有找个版本对应的驱动



我这边就下载了77.0.3865.40这个版本，点击去找到linux对应的下载地址，直接使用wget进行下载

wget http://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip

下载后解压到当前目录下,如果没有安装unzip，就使用apt-get install unzip 安装解压工具

unzip 你下载的zip文件

移动文件夹到usr文件夹下面，并创建软链接，升级为全局变量

mv -f chromedriver /usr/local/share/chromedriver

ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver

ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

到此安装结束，我们执行 chromedriver --version 可以查看安装的版本号

![image-20210505142020845](/home/yons/.config/Typora/typora-user-images/image-20210505142020845.png)