+++
title = "Python构建开源项目"
date = "2018-10-29"
description = "Python构建开源项目"
featured = false
categories = [
  "Python"
]
tags = [
  "Python"
]
series = [
  "Python"
]
images = [
]

+++

# Python构建开源软件

## python的构建工具setup.py的应用场景
一般在安装python模块的时候,我们会使用`pip install 模块名`进行在线安装,会安装依赖包,或者`python setup.py install`通过源码在本地安装,不会安装依赖包



### 在做一个开源项目的时候遇到了一些问题:

我的程序需要用到python的Redis等模块,以及自己写的入口文件run.py,怎么实现可以在服务器上方便的发布,也就是说,可以让依赖和自己写的程序一起安装,同时将自己写的模块变成一个可执行文件



###　setup.py

示例以及注释:

```python

from setuptools import setup, find_packages



setup(  

    name = "proxy-pool",  #包名

    version = "1.0.0",  #版本

    keywords = ("poxypool", "redis"),#关键词列表

    description = "test version proxy pool",  #程序的简单介绍

    long_description = "A proxy pool project modified from Germey/ProxyPool",  #程序的详细介绍

    url = "https://github.com/Euraxluo/ProxyPool", #程序的官网 

    download_url = "https://github.com/Euraxluo/ProxyPool.git" #程序的下载地址

    author = "Euraxluo",  #作者

    author_email = "euraxluo@qq.com",  #程序作者的邮箱

  	#maintainer 维护者

	#maintainer_email 维护者的邮箱地址

	packages=[

    	'proxy-pool'

	],

    py_modules = ['run'],#需要打包的python文件列表

    include_package_data = True,  

    platforms = "any",  #程序适用的软件平台列表

    install_requires = [#需要安装的依赖包

        'aiohttp',

        'requests',

        'flask',

        'redis',

        'pyquery'

    ],

    entry_points = {  #动态发现服务和插件

        'console_scripts': [  #指定命令行工具的名称

            'test = test.help:main'  #工具包名=程序入口

        ]

    },

    license = "apache 2.0",  #程序的授权信息

    zip_safe=False,#安装为文件夹还时打包为egg文件

    classifiers = [#程序所属的分类列表

        'Environment :: Console',

        'Programming Language :: Python :: 3.6',

        'Programming Language :: Python :: Implementation :: CPython'

    ]

    #data_files 打包时需要打包的数据文件,如图片,配置文件等

    #package_dir = {'':'lib'},#表示root pkg的模块都在lib目录中

    # requires 定义依赖哪些模块

    # provides定义可以为哪些模块提供依赖

    #scripts = [],#安装时需要执行的脚本列表

    #packages = find_packages(exclude=['*.tests']),  #需要处理的包目录,可以手动增加手动增加packages参数很容易，刚刚我们用到了这个函数，它默认在和setup.py同一目录下搜索各个含有 __init__.py的包。其实我们可以将包统一放在一个src目录中，另外，这个包内可能还有aaa.txt文件和data数据文件夹,也可以使用exclude排除一些特定的包

)

```

## requirement

python项目中必须包含一个 requirements.txt 文件，用于记录所有依赖包及其精确的版本号。以便新环境部署

示例:

```

aiohttp>=1.3.3

Flask>=0.11.1

redis>=2.10.5

requests>=2.13.0

pyquery>=1.2.17



```

生成:

`pip freeze > requirements.txt`

也可以直接`pip freeze`查看列表



安装:

可以使用pip安装requeirments.txt的依赖:

`pip install -r requirements.txt`



## LICENSE文件的生成

在开源仓库中选择create files,取名为LICENSE,会让你选择开源协议,最后选好后创建文件即可



lisence文件也可以用来对项目进行限制和控制



##　.gitignore

一般来说每个Git项目中都需要一个“.gitignore”文件，这个文件的作用就是告诉Git哪些文件不需要添加到版本管理中

添加规则

例子：

```gitinore

*.vscode

*.pyc

*.db

venv

build/ #忽略build/目录下的所有文件

/.idea #仅仅忽略项目根目录下的.idea文件

```

如果我们要排除某些文件呢？

过滤规则

加一个｀!｀，比如我们需要排除掉`/mtk/`文件夹中的`/mtk/test.txt`

```

/mtk/

!/mtk/test.txt

```



## .travis.yml

yaml语法的写出来的配置文件，用来描述如何持续构建，支持各种语言，各种系统环境



示例:

```yml

language: python

python:

  - "3.6"



services:

  - redis-server



script: 

  - python3 setup.py install

  - cd tests

  - python3 test_api.py

  - python3 test_db.py

  - python3 test_schedule.py

```







## python 命名规范

### 文件名

全小写,可使用下划线



### 包

应该是简短的、小写的名字。如果下划线可以改善可读性可以加入。如mypackage。



### 模块

与包的规范同。如mymodule。



### 类

总是使用首字母大写单词串。如MyClass。内部类可以使用额外的前导下划线。



### 函数&方法

函数名应该为小写，可以用下划线风格单词以增加可读性。如：myfunction，my_example_function。

*注意*：混合大小写仅被允许用于这种风格已经占据优势的时候，以便保持向后兼容。



函数和方法的参数

总使用“self”作为实例方法的第一个参数。总使用“cls”作为类方法的第一个参数。

如果一个函数的参数名称和保留的关键字冲突，通常使用一个后缀下划线好于使用缩写或奇怪的拼写。



### 全局变量

对于from M import *导入语句，如果想阻止导入模块内的全局变量可以使用旧有的规范，在全局变量上加一个前导的下划线。

*注意*:应避免使用全局变量



### 变量

变量名全部小写，由下划线连接各个单词。如color = WHITE，this_is_a_variable = 1

*注意*：

1.不论是类成员变量还是全局变量，均不使用 m 或 g 前缀。

2.私有类成员使用单一下划线前缀标识，多定义公开成员，少定义私有成员。

3.变量名不应带有类型信息，因为Python是动态类型语言。如 iValue、names_list、dict_obj 等都是不好的命名。



### 常量

常量名所有字母大写，由下划线连接各个单词如MAX_OVERFLOW，TOTAL。



### 异常

以“Error”作为后缀。



### 缩写

命名应当尽量使用全拼写的单词，缩写的情况有如下两种：

1.常用的缩写，如XML、ID等，在命名时也应只大写首字母，如XmlParser。

2.命名中含有长单词，对某个单词进行缩写。这时应使用约定成俗的缩写方式。

例如：

function 缩写为 fn

text 缩写为 txt

object 缩写为 obj

count 缩写为 cnt

number 缩写为 num，等。

前导后缀下划线

一个前导下划线：表示非公有。

一个后缀下划线：避免关键字冲突。

两个前导下划线：当命名一个类属性引起名称冲突时使用。

两个前导和后缀下划线：“魔”（有特殊用图）对象或者属性，例如__init__或者__file__。绝对不要创造这样的名字，而只是使用它们。

*注意*：关于下划线的使用存在一些争议。



### 特定命名方式

主要是指 __xxx__ 形式的系统保留字命名法。项目中也可以使用这种命名，它的意义在于这种形式的变量是只读的，这种形式的类成员函数尽量不要重载。如

class Base(object):

def __init__(self, id, parent = None):

self.__id__ = id

self.__parent__ = parent

def __message__(self, msgid):
