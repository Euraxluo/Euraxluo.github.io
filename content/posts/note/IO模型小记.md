---
title: "IO模型小记"
date: "2019-02-21"
description: "IO模型小记"
featured : false
categories: ["notes"]
tags: [ "NIO" ]
series: [ "notes" ]
images: []
---

BIO (block io) 同步阻塞IO

线程池:伪异步IO,实际上也是同步阻塞IO



NIO(同步非阻塞)

selector会主动轮询,与客户端建立通信(channel)

每一个server会有一个selector

 

AIO(异步非阻塞)

当客户端通知我(回调),我再去连接



单线程模式:所有的IO操作都由同一个NIO线程处理

主线程组,从单线程模型

主从线程组模型,具有一个主线程族和从线程组,主线程组去建立channel,从线程组会去进行处理



 

