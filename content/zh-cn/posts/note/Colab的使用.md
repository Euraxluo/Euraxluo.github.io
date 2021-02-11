---
title: "Colab的使用"
date: "2019-02-21"
description: "Colab的使用"
featured : false
categories: ["notes"]
tags: [ "notes" ]
series: [ "notes" ]
images: []
---

# Colab的使用

## 首先是梯子

### 校园网改ipv6连接谷歌

1.修改SDN服务器

在ipv6的sdn中设置这两个记录，也可以只设置一个

```
2001:4860:4860::8888
2001:4860:4860::8844
```

linux:修改`/etc/resolv.conf`

2.修改hosts

windows路径：`%SystemRoot%\system32\drivers\etc\hosts`

linux:`/etc/hosts`

[ipv6 hosts](https://github.com/lennylxx/ipv6-hosts/blob/master/hosts)

## 入门：
进入[colab](colab.research.google.com)
因为我有基础，所以直接跳过了机器学习速成课部分，做了我在calab的第一个实验: 图像风格转换
## 连接Colab和google drive
```python
!apt-get install -y -qq software-properties-common python-software-properties module-init-tools
!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
!apt-get update -qq 2>&1 > /dev/null
!apt-get -y install -qq google-drive-ocamlfuse fuse
from google.colab import auth
auth.authenticate_user()
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
import getpass
!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}
```
然后会出现一个链接，点进去取得key，输入并回车
然后新建一个文件夹并挂载
```python
!mkdir -p Euraxluo
!google-drive-ocamlfuse Euraxluo
```
如果报错：`use the 'nonempty' mount option`
在第二局加参数
`!google-drive-ocamlfuse Euraxluo -o nonempty`
Euraxluo是我建立的文件夹的名字
这下挂载就可以用了

