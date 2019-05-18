## C++ 小记


### CMAKE
- 工程构建工具

#### 简单的使用
- 文件名大小写敏感
- 语法
```cmake
cmake_minimum_required(VERSION 2.8)#设置cmake的版本
set(CMAKE_BUILD_TYPE Debug )#设置为debug模式
#项目名
PROJECT(HELLO)
#设置某文件夹为头文件
include_directories("include")
#设置一个头文件，把hello.cpp编译为libfile
add_library(libfile src/hello.cpp)
SET(SRC_LIST “fu nc.c”)
#设置可执行二进制文件的输出路径和库的输出路径
SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin) SET(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)
ADD_EXECUTABLE(hello main.c;func.c;$\{RC_LIST\})
target_link_libraries(hello libfile)#链接一个lib

#设置编译的源文件在编译当前目录的bin下
ADD_SUBDIRECTORY (src bin)#修改为  SUBDIRS(src) 结果放在src中
#安装
DESTDIR= 
	install: mkdir -p $(DESTDIR)/usr/bin 
	install -m 755 hello $(DESTDIR)/usr/bin
```
#### 更像一个工程
```FILE BUILD
Hello
	- src
		- CMakeLists.txt
		- build #进去此目录进行外部编译 =》 cmake .. & make 
	- CMakeLists.txt
```
```CMAKE
project(hello)
add_executable(hello hello.c)
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)
```

### map和set

底层使用的是红黑树

查找是使用二分搜索（红黑树保有顺序性）

各种操作都是nlog

### unordered_map,unordered_set

底层都是哈希表

不保有顺序性，但是查找操作是O1