+++
title = "Linux基础"
date = "2018-10-29"
description = "Linux基础"
featured = false
categories = [
  "Linux"
]
tags = [
  "Linux"
]
series = [
  "Linux"
]
images = [
]

+++


## Linux基础

## 文件基本属性



### ll/ls -l 



显示一个文件的属性以及文件所属的用户组



#### eg:

```shell

[root@www /]# ls -l

total 64

dr-xr-xr-x   2 root root 4096 Dec 14  2012 bin

dr-xr-xr-x   4 root root 4096 Apr 19  2012 boot

……

```

bin 以d开头,表示这是一个目录

```

当为[-]是文件

当为[l]表示为link file

当为[b]表示为可以进行存取的接口设备

当为[c]表示为串行端口设备

```

接下来以3个为一组,且均为[rwx]的组合,位置次序不变



[r]表示可读,[w]可写,[x]可执行,如果没有这个权限,就会用[-]代替.



```

第0位确定文件类型.

第1-3位确定属主（该文件的所有者）拥有该文件的权限

第4-6位确定属组（所有者的同组用户）拥有该文件的权限

第7-9位确定其他用户拥有该文件的权限

```

属主:对文件具有所有权的用户 



属组:用户按组分类,一个用户属于一个或者多个组



所以,文件按照[文件所有者|所有者同组用户|所有着不同组用户]来规定访问权限



对于root用户,权限对他无效



### 2. 更改属性



#### chgrp [-R] 属组名 文件名

更改文件属组

`sudo chgrp name test`



#### chown [-R] 属主名 : 属组名 文件名

更改文件属主,也可以同时修改文件属组

`sudo chown 770:euraxluo test`



#### chmod [-R] xyz 文件或者目录

>r:4

w:2

x:1



>xyz:

x = owner = rwx = 4+2+1

y = group = rwx = 4+2+1

z = others = rwx = 4+2+1



eg:

`sudo chmod 670 test`

##### 使用符号类型改变文件权限





|       |          |          |      |                |

| :---- | -------- | -------- | ---- | -------------- |

| chmod | u=user   | +(加入)  | r    | 文件或者文件名 |

|       | g=group  | - (减少) | w    |                |

|       | o=others | =(设定)  | x    |                |

|       | a=all    |          |      |                |



所以刚刚我们的代码也可以是

`sudo chmod u=rw,g=rwx,o= test`



## 文件目录的处理



### ls [-adl] 目录名:

-a:全部文件



-d:列出目录本身



-l:详细列出



`ls -al ~`



### cd 切换目录

cd ~ :回到xxx@www的/xxx下(家目录)



cd .. 返回上一级



cd ./xxx 使用相对路径切换



### pwd [-P] (显示当前所在的目录)

-P:针对联接档,可以显示出真的路径



### mkdir [-mp] 目录名:

创建新的目录



-m: 配置文件的权限 



-p:你就可以使用 xxx/xxx/xxx的方式创建目录



eg:

`mkdir -m 440 -p test1/test2`



### rmdir [-p] 目录名

删除*空的目录*



-p:连同上级的空目录也删除



eg:



```shell

$ rmdir -p test1/test2/test3/test4

$ ls -l

总用量 4

drwxrwxr-x 5 euraxluo euraxluo 4096 1月  15 11:14 'Tencent Files'

-r--r--r-- 1      770 euraxluo    0 1月  17 15:06  test

```



### cp [-adfilprsu] source destination

-i:destination已经存在,先询问



-r:force ,目标已经存在,强制覆盖



-p:连同文件的属性一起copy过去



-d:若source是一个连接档(link file),就copy连接档



-r:递归copy,用于copy目录



-a:-all=-pdr



-u:若 destination 比 source 旧才覆盖 destination



-s:复制成为符号连结档 (symbolic link)，亦即(link)文件；



-l:不是copy文件本身,而是copy连接档



eg:

```shell

$ cp -sf test test1

$ cat test1

test

$ ls -l

total 8

drwxrwxr-x 5 euraxluo euraxluo 4096 1月  15 11:14 'Tencent Files'

-rwxrwxrwx 1      770 euraxluo    5 1月  17 16:09  test

lrwxrwxrwx 1 euraxluo euraxluo    4 1月  17 16:17  test1 -> test

```

### sudo apt-get install -f 安装上一个错误



### scp [文件名][路径] 拷贝到远程

eg:

`scp test xxx@ip:`拷贝到home



### rm [-fir] 文件或目录

-f:force 强制删除



-i:会询问一下



-r:递归删除



### cat  [-bnT]

从第一行开始显示文件内容



-b:列出行号



-n:列出列号



-T:打印tap



### tac [-bnT]

从最后一行显示



-b:列出行号



-n:列出列号



-T:打印tap



### nl [-bnw]

显示的时候,输出行号

>-b ：指定行号指定的方式，主要有两种：

-b a ：表示不论是否为空行，也同样列出行号(类似 cat -n)；

-b t ：如果有空行，空的那一行不要列出行号(默认值)；



>-n ：列出行号表示的方法，主要有三种：

-n ln ：行号在荧幕的最左方显示；

-n rn ：行号在自己栏位的最右方显示，且不加 0 ；

-n rz ：行号在自己栏位的最右方显示，且加 0 ；



>-w ：行号栏位的占用的位数。



### more 

一页一页显示



### less 

和more一样,并且可以向前翻页



### head [-n]

显示头几行



-n:number



### tail [-n]

显示尾行



-n:number



### man {命令}

查看命令的文档



### linux  链接

1.硬连接



硬连接指通过索引节点来进行连接,两个文件具有完全一样的地位

删除原始文件,硬链接文件不受影响

主要用于关键文件的保护



2.软连接



软链接文件类似于 Windows 的快捷方式,保存的是原始文件的位置信息.

删除原始文件,软链接文件无效



### 文件系統的索引

在 Linux 的文件系统中，保存在磁盘分区中的文件不管是什么类型都给它分配一个编号，称为索引节点号(Inode Index)。在 Linux 中，多个文件名指向同一索引节点是存在的.硬连接通过索引实现



## 用户管理



### useradd [-cdgsu] 用户名

添加新的用户:



-c comment



-d 目录 指定用户主目录，若目录不存在,使用-m选项，来创建。



-g 用户组 指定用户所属的用户组。



-G 用户组，用户组 指定用户所属的附加组。



-s Shell文件 指定用户的登录Shell。



-u 用户号 指定用户号，同时-o，则可以使用其他用户的标识号



eg:

`$ useradd –d /usr/test -m test`



### userdel [-r] 用户名

删除账号



-r:同时删除用户的主目录



### usermod [-cdmGusol] 用户名

参数与useradd一样



-l:制定新的用户名,就是更改名字



### passwd [-ludf] 用户名

修改用户的pwd



-l:锁定口令，即禁用账号。



-u:口令解锁。



-d: 使账号无口令。



-f: 强迫用户下次登录时修改口令。



## 用户组管理



### groupadd [-go] 用户组

-g:指定新用戶組的GID



-o:一般和-g一起使用，表示新的用戶組可以和別人相同



### groupdel 用户组

刪除一個用戶組



### groupmod [-gon] 用戶組

-g:设置GID



-o:与groupadd相同



-n:更名



### newgrp [目标用户组名]

用户可以在登录后，使用命令newgrp切换到其他用户组



eg:`$ newgrp root`



### 用户标识号

>是一个整数，系统内部用它来标识用户。



>一般情况下它与用户名是一一对应的。如果几个用户名对应的用户标识号是一样的，系统内部将把它们视为同一个用户，但是它们可以有不同的口令、不同的主目录以及不同的登录Shell等。



>0是超级用户root的标识号，1～99由系统保留，作为管理账号，普通用户的标识号从100开始。在Linux系统中，这个界限是500。 



### /etc/shadow

>/etc/shadow中的记录行与/etc/passwd中的一一对应，它由pwconv命令根据/etc/passwd中的数据自动产生



它的文件格式与/etc/passwd类似，由若干个字段组成，字段之间用":"隔开。这些字段是：

`登录名:加密口令:最后一次修改时间:最小时间间隔:最大时间间隔:警告时间:不活动时间:失效时间:标志`



## 磁盘管理



### df [-ahikHTm] 目录或用户名

-a:all,列出全部



-k:用kb显示



-m:用mb显示



-h:自己显示



-H:用M=1000k来显示



-T:显示文件系统的分区名



-i:用inode(索引节点)的数量显示



### du [-ahskm] 目录或用户名

参数和df一样



-s:列出总量,不列出占用容量



-S:不包括子目录的总计



### fdisk [-l] 磁盘名

输出各装置的分区



### mkfs [-t] 装置文件名

格式化这个分区



eg:格式化为fat32



`$ mkfs.fat -F32 /dev/sda1`



### mount [-t 文件系统] [-L Label名] [-o 额外选项] [-n]  装置文件名  挂载点

挂載分區



eg:`mount /dev/sda1 /mnt/boot/EFI`



### unmount [-fn]  装置文件名|挂载点

卸载分区



-f:強制卸載



-n:不升級/etc/mtab的情況下卸载



## VI/VIM



### 下载:

`sudo apt-get install vim`



### 命令模式

```

刚刚启动时,或者在输入模式下`ESC`,进入命令模式.

i:插入,进入输入模式

I:到行首插入

a:附加

A:到行尾附加

s:删除字符并插入

S:删除行并插入

x:删除当前光标所在的字符

r:替换当前光标所在的字符字符

R:替换模式:会把当前和后面的字符都替换

e|E:跳到这个词的末尾一个字符上

w|E:跳到下一个词的开头一个字符上

o:在这字符前分段

O:在这字符后分段

Y:拷贝行

p:在这字符后粘贴行

P:在这字符前粘贴行



(><^v:表示方向键)

d 动作:删除的范围

eg:

d l|>:删除这个字符

d h|<:删除这个字符前面的字符

d k|^:删除这个字符所在行和上一行

d j|v:删除这个字符所在行和下一行

d H:删除屏幕顶行到这个字符

d L:删除屏幕尾行到这个字符



D:从这字符一直删除到行尾

>:缩进

<:反缩进

:切换到底线模式

(:跳转到句首

):跳转到句尾巴

{:跳转到段首

}:跳转到段尾

V:让这一行高亮

```

### 输入模式

iI,aA,sS,RC进入



- **字符按键以及Shift组合**，输入字符

- **ENTER**，回车键，换行

- **BACK SPACE**，退格键，删除光标前一个字符

- **DEL**，删除键，删除光标后一个字符

- **方向键**，在文本中移动光标

- **HOME**/**END**，移动光标到行首/行尾

- **Page Up**/**Page Down**，上/下翻页

- **Insert**，切换光标为输入/替换模式，光标将变成竖线/下划线

- **ESC**，退出输入模式，切换到命令模式



### 底线模式



:w(保存)



:q(退出)



:q!(不保存退出)



:e f(打開文件f)



:h(幫助)



:new(新建文件 in vim)



詳見：![](http://www.runoob.com/wp-content/uploads/2015/10/vi-vim-cheat-sheet-sch.gif)



## 問題：



vim使用很不熟悉
