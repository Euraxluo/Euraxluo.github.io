+++
title = "Shell 基础"
date = "2019-03-10"
description = "Shell 基础学习"
featured = false
categories = [
  "Shell"
]
tags = [
  "Shell"
]
series = [
  "Shell"
]
images = [
]

+++

# shell 基础

在终端输入:`sh`进入脚本界面
## helloworld



编辑内容

```

#!/bin/bash

echo "hello world!"

```

保存退出:

`w ~/helloworld.sh`

运行:

```

chmod +x ~/helloworld.sh

cd ~

./helloworld.sh

```

执行结果:

`hello world!`



### 分析:



第一行中`#!`是一个约定的标记,告诉系统脚本需要使用什么解释器来执行,即使用哪一种shell



这种在第一行指定了解释器信息的方式,需要让脚本作为可执行程序执行



还有第二种运行方式,即作为解释器参数,这时,第一行的解释器信息,失效

eg:`python test.py`



## shell 变量

显式赋值:

`a="abc"`

用语句:

```shell

for file in `ls /etc/` 

```

或者

`for file in $(ls /etc)`



### 使用变量:

使用一个定义过的变量:



```shell

file="test"

echo $file

echo ${file}

```

花括弧是为了帮助解释器识别变量的边界:

```shell

for skill in Ada Coffe Action java;do

	echo "I am good at ${skill}Script"

done

```

### 只读变量

使用readonly :

```shell

#!/bin/bash

myUrl='http://euraxluo.github.io'

readonly myUrl

```

### 删除变量

unset:

`unset variable_name`

变量被删除后不能再次使用,unset 命令不能删除只读变量

```shell

#!/bin/sh

myUrl="http://euraxluo.github.io"

myname="Euraxluo"

readonle myname

unset myname

unset myUrl

echo $myUrl

echo $myname

```

## 字符串:

### 单引号

单引号字符串的限制：

>单引号里的任何字符都会原样输出，单引号字符串中的变量是无效的；

>单引号字串中不能出现单独一个的单引号（对单引号使用转义符后也不行），但可成对出现，作为字符串拼接使用。

`str='this is a string'`



### 双引号

双引号的优点：

>双引号里可以有变量

>双引号里可以出现转义字符

```shell

your_name='euraxluo'

str="Hello, I know you are \"$your_name\"! \n"

echo -e $str

```



### 拼接字符串

```shell

mynam="euraxluo"

str1="hello "word" ! from "$myname

str2="hello word ! from $myname"

echo $str1

echo $str2

str1='hello 'word' ! from '$myname

str2='hello word ! from $myname'

echo $str1

echo $str2

```

### 获取字符串长度

在变量名前加#

```shell

string="abc"

echo ${#string}

```



### 提取子字符串

#### 截取字符变量的前5位

expr substr “$a” 1 8

echo $a|cut -c1-8



```shell

string="hello world euraxluo"

#1

echo `expr substr "$string" 1 5`

#2

echo $string | cut -c1-5

```



#### 按指定的字符串截取

从左向右截取最后一个string后的字符串

${varible##*string}

从左向右截取第一个string后的字符串

${varible#*string}

从右向左截取最后一个string后的字符串

${varible%%string*}

从右向左截取第一个string后的字符串

${varible%string*}

“*”只是一个通配符可以不要

```shell

string="hello world euraxluo"

#1

echo ${string##*ld}

#2

echo ${string#*l}

#3

echo ${string%%w*}

#4

echo ${string%wo*}

```



### 查找子字符串

查找r u 的位置:

```shell

string="hello world euraxluo"

echo `expr index "$string" ru`

```

## shell数组

bash支持一维数组（不支持多维数组），并且没有限定数组的大小



## 定义数组

`数组名=(值1 值2 ... 值n)`

eg:

```shell

values=(

value1 value2 value3

)

echo $values

echo ${value[1]}

```

### 读取数组

通过下标读取

`${数组名[下标]}`

读取全部元素

`echo ${数组名[@]}`



### 获取数组的长度

```shell

# 取得数组元素的个数

length=${#array_name[@]}

# 或者

length=${#array_name[*]}

# 取得数组单个元素的长度

lengthn=${#array_name[n]}

```



## 注释:

单行注释:

`在每行开头加上#`



多行注释:

>1:

```

每一行加个#符号太费力了，可以把这一段要注释的代码用一对花括号括起来，定义成一个函数，没有地方调用这个函数，这块代码就不会执行，达到了和注释一样的效果。

```



>2:

```shell

:<<EOF

注释内容...

注释内容...

注释内容...

EOF

```

或者

```shell

:<<'

注释内容...

注释内容...

注释内容...

'

```



自动复制脚本

```shell

#!/bin/sh

#	`find /home/euraxluo/Documents/工作报告/bags -mmin +1240 -exec rm -f () \;` 这是删除21h前的

#	df 查看硬盘地址，我的是/run/media/euraxluo/72c7944d-f7e1-4cb9-a431-6b0285044d79/

#	/home/euraxluo/Documents/工作报告/bags 是我的 bag存放地址

if [ ! -d "/run/media/euraxluo/72c7944d-f7e1-4cb9-a431-6b0285044d79" ];then

	echo "硬盘还没插"

else

	echo "删除一天前拷贝过来的文件"

	`find /home/euraxluo/Documents/工作报告/bags -mtime 1 -exec rm -f {} \;`

	echo "硬盘插入，自动拷贝中！"

	for var in `cd /run/media/euraxluo/72c7944d-f7e1-4cb9-a431-6b0285044d79/ && ls *.bag`

	do 

		strcp="cd /run/media/euraxluo/72c7944d-f7e1-4cb9-a431-6b0285044d79/ && cp -i $var /home/euraxluo/Documents/工作报告/bags/${var##*/}"

		`awk "BEGIN { cmd=\"$strcp\"; print "n" | cmd; }"`

	done

	echo "拷贝完成"

	`cd /home/euraxluo/Documents/工作报告/bags`

fi





```



批量修改文件后缀的shell

```

#!/bin/bash

# -*- coding: UTF-8 -*-

oldext="apng"

newext="png"

dir=$(eval pwd)

for file in $(ls $dir | grep .$oldext)

        do

        name=$(ls $file | cut -d. -f1)

        mv $file ${name}.$newext

        done

echo "change apng=====>png done!"

```

