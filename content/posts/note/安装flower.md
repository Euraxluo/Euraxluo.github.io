---
title: "安装flower"
date: "2021-02-21"
description: "安装flower"
featured : false
categories: ["notes"]
tags: [ "notes" ]
series: [ "notes" ]
images: []
---

## 1.安装flower:

```
pip install flower
1
```

## 2. 启动flower

例如启动项目工程下面celery_tasks目录的main.py 异步任务启动函数

```
flower -A celery_tasks.main --port=5555
```



1.安装Celery

`pip install celery`

2.编写task

```
from celery import Celery
app = Celery('tasks', broker='amqp://guest@localhost//')
@app.task
def add(x, y):
    return x + y
```

3.运行

`$ celery -A tasks worker --loglevel=info`