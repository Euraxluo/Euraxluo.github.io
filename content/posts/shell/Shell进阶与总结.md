+++
title = "Shell 进阶"
date = "2019-03-10"
description = "Shell 进阶"
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

# shell进阶

0. 破壳漏洞

   `env x='() { :;}; echo shellshocked' bash –c "echo test"`检查,如果输出了两行,那么需要升级bash的版本

1. 解释器的类型
- 系统中的shells使用`cat /etc/shells`查看:

  ```bash
  /bin/sh
  /bin/dash
  /bin/bash
  /bin/rbash
  /usr/bin/tmux
  /usr/bin/screen
  /bin/zsh
  /usr/bin/zsh
  ```

  

- 设置解释器的类型
`#!/bin/bash`在文件的开头使用,内核会根据"#!"后的解释器来确定该用那个程序解释这个脚本中的内容

2. 脚本的编辑
- vim帮助我们编辑脚本

**我的vimrc内容**

```bash
  1 set tabstop=4
  2 set shiftwidth=4
  3 set expandtab
  4 set number
  5 autocmd BufNewFile *.py,*.cc,*.sh,*.java exec ":call SetTitle()"
  6 func SetTitle()
  7         if expand("%:e") == 'sh'
  8         call setline(1,"#!/bin/bash")
  9         call setline(2,"# Author: Euraxluo")
 10         call setline(3,"# Email: Euraxluo@outlook.com")
 11         call setline(4,"# Time:" .strftime("%F %T"))
 12         call setline(5,"# Description: ")
 13         call append(line("."), "\# File Name: ".expand("%"))
 14     endif
 15     autocmd BufNewFile * normal G
 16 endfunc
```

3. 脚本的执行

   ```bash
   sh/bash   scripts.sh 
   chown +x   ./scripts.sh  && ./scripts.sh  
source scripts.sh
   .  scripts.sh
   cat oldboyedu.sh |bash  # 效率较低
   ```
   
   其中`source` 和`.` 都是在当前的shell中执行一个文件中的命令
   
   而`sh`会新建一个进程去执行一个文件中的命令
   
   sh和bash的关系:
   
   ```bash
   which sh
   > /bin/sh
   
   ll /bin/sh
   > lrwxrwxrwx 1 root root 4 Jul 25 21:47 /bin/sh -> bash
   ```
   
   


4. 变量
- 环境变量

  `env/declare/set/export -p` 这四个命令 输出的结果有些不同

  配置文件的读取顺序:

  ① /etc/profile

  ② ~/.bash_profile

  ③ ~/.bashrc

  ④ /etc/bashrc

- 普通变量

  
```bash
a=1
b='1'
c="1"
a=1
echo "$a"
> 1
echo "${b}"
> 1
echo "$c"
> 1
```
  连续普通字符串内容赋值给变量，不管用什么引号或者不用引号，它的内容是什么，打印变量就输出什么

- 位置变量

  |        |                                                              |
  | ------ | ------------------------------------------------------------ |
  | $0     | 获取当前执行shell脚本的文件名,执行时带路径,则包括路径        |
  | $n     | 获取当前执行shell脚本的第n个参数,n:1...9,如果n大于9用大括号括起来{10} |
  | $#     | 获取当前执行的shell脚本后面接的参数的个数                    |
  | \$*/$@ | 获取当前shell的所有传参的参数                                |
  | "$*"   | 将所有的参数视为单个字符串                                   |
  | "$@"   | 将所有的参数视为不同的独立字符,多用于传递参数                |

  ```bash
  #./test.sh 1s asa 2 3 4 5 6
  
  set -v #用于调试
  set -x
  test(){
      mm=$1
      echo $mm
  }
  echo $*
  + echo 1s asa 2 3 4 5 6
  1s asa 2 3 4 5 6
  test $*
  + test 1s asa 2 3 4 5 6
  + mm=1s
  echo "$*"
  + echo '1s asa 2 3 4 5 6'
  1s asa 2 3 4 5 6
  
  test "$*"
  + test '1s asa 2 3 4 5 6'
  + mm='1s asa 2 3 4 5 6'
  + echo 1s asa 2 3 4 5 6
  1s asa 2 3 4 5 6
  echo $@
  + echo 1s asa 2 3 4 5 6
  1s asa 2 3 4 5 6
  echo "$@"
  + echo 1s asa 2 3 4 5 6
  1s asa 2 3 4 5 6
  test "$@"
  + test 1s asa 2 3 4 5 6
  + mm=1s
  ```

- 进程状态变量

  |      |                                                  |
  | ---- | ------------------------------------------------ |
  | $?   | 获取上一个指令的执行状态返回值(0成功,非零为失败) |
  | $\$  | 获取当前执行的shell脚本的PID                     |
  | $!   | 获取上一个后台工作的进程的PID                    |
  | $_   | 获取在此之前执行的命令或脚本的最后一个参数       |

  

- export命令

  说明:

  1. 在当前shell窗口及子shell窗口生效

  2. 在新开的shell窗口不会生效，生效需要写入配置文件

- 反引号赋值

  ```bash
  time=`data`
  echo $time
  > Fri Jan  3 21:44:04 CST 2020
  ```

  

- TIPS

  1. 变量名通常要大写。

  2. 变量可以在**自身的Shell及子Shell**中使用。

  3. 常用export来定义环境变量。

  4. 执行env默认可以显示所有的环境变量名称及对应的值。

  5. 输出时用“$变量名”，取消时用“**unset**变量名*”。

  6. 书写crond定时任务时要注意，脚本要用到的环境变量最好先在所执行的**Shell脚本**中**重新**定义。

  6. 如果希望**环境变量永久生效**，则可以将其放在用户环境变量文件或全局环境变量文件里。
  7. 只有在变量的值中有空格时,才需要使用引号,**单引号和双引号**的区别在于是否能解析特殊符号
  8. 如果内容是纯数字简单连续的字符(不喊空格)时,可以不使用引号
  9. 没有特殊情况时,字符串一律使用双引号定义赋值
  10. 当变量中的内容需要原样输出时,使用单引号
  11. 希望变量的内容是命令的解析结果时,要使用反引号或者$()把命令括起来在赋值

5. 变量子串

- 说明

| 表达式                     | 说明                                                     |
| -------------------------- | -------------------------------------------------------- |
| ${v}                       | 返回变量$v的内容                                         |
| ${#v}                      | 返回$v的长度                                             |
| ${v:offset}                | 返回在变量${v}中，从位置offset之后开始提取子串到结尾     |
| ${v:offset:lenght}         | 在变量${v}中，从位置offset之后开始提取长度为length的子串 |
| ${v#word}                  | 从变量${v}开头开始删除最短匹配的word子串                 |
| ${v##word}                 | 从变量${v}开头开始删除最长匹配的word子串                 |
| ${v%word}                  | 从变量${v}结尾开始删除最短匹配的word子串                 |
| ${v%%word}                 | 从变量${v}结尾开始删除最长匹配的word子串                 |
| ${parameter/pattem/string} | 使用string代替第一个匹配的pattern   |
| ${parameter//pattem/string}| 使用string代替所有匹配的pattern    |

范例

```bash
# ${v:offset:lenght}
mm=0123456
echo ${mm:1:0}
> 
echo ${mm:1:1}
> 1
echo ${mm:1:2}
> 12
echo ${mm:1:-1}
> 12345

# ## 与 # 
file=/dir1/dir2/dir3/my.file.txt
> file=/dir1/dir2/dir3/my.file.txt
echo ${file#*/}
> dir1/dir2/dir3/my.file.txt
echo ${file##*/}
> my.file.txt
echo ${file#*.}
> file.txt
echo ${file##*.}
> txt

# %% 与 %
echo ${file%/*}
> /dir1/dir2/dir3
echo ${file%%/*}
> 
echo ${file%.*}
> /dir1/dir2/dir3/my.file
echo ${file%%.*}
> /dir1/dir2/dir3/my

# // 与 /

echo ${file/dir/path}
> /path1/dir2/dir3/my.file.txt
echo ${file//dir/path}
> /path1/path2/path3/my.file.txt

# // split 字符串
list=1,2,3,4,5
echo ${list//,/ }
> 1 2 3 4 5
array=(${list//,/ })
echo "${array[*]}"
> 1 2 3 4 5
```

6. 特殊扩展变量

   说明

   | 表达式     | 说明                        |
   | ---------- | --------------------------- |
   | ${v:+word} | (v != '') ?word :           |
   | ${v:-word} | (v != '') ? :word           |
   | ${v:?word} | (v != '') ? :(word;exit -1) |
   | ${v:=word} | (v != '') ? :(word;v=word)  |
   | ${v-word}  | (v not exist) ?word :v      |

7. 条件表达式

- 文件判断

| **常用文件测试操作符**                                | **说明**                                                     |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| -d文件，d的全拼为directory                      | 文件存在且为目录则为真，即测试表达式成立                     |
| -f文件，f的全拼为file             | 文件存在且为普通文件则为真，即测试表达式成立                 |
| -e文件，e的全拼为exist            | 文件存在则为真，即测试表达式成立。注意区别于“-f”，-e不辨别是目录还是文件 |
| -r文件，r的全拼为read             | 文件存在且可读则为真，即测试表达式成立                       |
| -s文件，s的全拼为size             | 文件存在且文件大小不为0则为真，即测试表达式成立              |
| -w文件，w的全拼为write            | 文件存在且可写则为真，即测试表达式成立                       |
| -x文件，x的全拼为executable       | 文件存在且可执行则为真，即测试表达式成立                     |
| -L文件，L的全拼为link             | 文件存在且为链接文件则为真，即测试表达式成立                 |
| fl -nt f2，nt 的全拼为 newer than | 文件fl比文件f2新则为真，即测试表达式成立。根据文件的修改时间来计算 |
| fl -ot f2，ot 的全拼为 older than | 文件fl比文件f2旧则为真，即测试表达式成立。根据文件的修改时间来计算 |

- 字符串判断

| **常用字符串测试操作符**                                     | **说明**                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **-n "字符串"**                                              | 若字符串的长度不为0,则为真，即测试表达式成立，n可以理解为no zero |
| **-Z "字符串"**                                              | 若字符串的长度为0,则为真，即测试表达式成立，z可以理解为zero的缩写 |
| **"串1"== "串2"**                                            | 若字符串1等于字符串2,则为真，即测试表达式成立，可使用"=="代替"=" |
| **"串1"!= "串*2"**                                           | 若字符串1不等于字符串2,则为真，即测试表达式成立，但不能用"!=="代替"!=" |
| 1.对于字符串的测试，一定要将字符串加**双引号**之后再进行比较。 | 2.空格非空                                                   |

- 整数判断

  | 在**[]**以及**test**中使用的比较符号 | 在**(())**和**[[]]**中使用的比较符号 | 说明                      |
  | ---------------------------------------------------- | ---------------------------------------------------- | ----------------------------- |
  | **-eq**                                              | **==/=**                            | 相等，全拼为equal             |
  | **-ne**                                              | **!=**                                          | 不相等，全拼为not equal       |
  | **-gt**                                              | **>**                                               | 大于，全拼为greater than      |
  | **-ge**                                              | **>=**                                               | 大于等于，全拼为greater equal |
  | **-lt**                                              | **<**                                                | 小于，全拼为丨ess than        |
  | **-le**                                              | **<=**                                               | 小于等于，全拼为less equal    |

- 逻辑符号

  | 在**[]**和**test**中使用的操作符 | **说明**                                          | 在**[[]]**和**(())**中使用的操作符 | **说明**                           |
  | -------------------------------------------- | ------------------------------------------------- | ---------------------------------- | ---------------------------------- |
  | **-a**                                       | [ 条件A -a 条件B ]A与B都要成立，整个表达式才成立  | **&&**                             | and，与，两端都为真，则结果为真    |
  | **-o**                                       | [ 条件A -o 条件B]A与B都不成立，整个表达式才不成立 | **\|\|**                           | or，或，两端有一个为真，则结果为真 |
  | **！**                                       | 非 | **!**                              | not，非，两端相反，则结果为真      |



8. if条件语句

```bash
file=$1
if [ -d $file ]
then
    echo "$file is a dir"
elif [ -f $file ]
then
    echo "$file is a file"
else
    echo "end"
fi
```



8. case条件语句

   ```bash
   # . ./test.sh -a 1 -b 2 -c 3 -d 4 -1
   # >
   # 2
   # 3
   # 4
   # e
   p(){
        str=$1
        echo "$1"
   }
   main(){
   while getopts ":a:b:c:d:e:" OPT
   do
       case $OPT in
           a) p $OPTARG;;
           b) p $OPTARG;;
           c) p $OPTARG;;
           d) p $OPTARG;;
           e) p $OPTARG;;
           :) p $OPTARG;;
           ?) p $OPTARG;;
       esac
   done
   }
   
   main "$@"
   
   
   ```

   

9. for循环

- 列表for循环

  ```bash
  # . ./test.sh 1 2 3 
  # 1 lenght: 1
  # 13 lenght: 2
  # 43 lenght: 2
  # 4 lenght: 1
  # 0 lenght: 1
  # 5 lenght: 1
  
  array=(1 13 43 4 0 5)
  main(){
      for i in ${array[*]}
      do
          echo "$i lenght: ${#i}"
      done
  }
  
  main "$@"
  ```

  

- 不带列表for循环

  ```bash
  # . ./test.sh 1 2 3 
  # 1
  # 2
  # 3
  # 1
  # 2
  # 3
  
  for i
  do
      echo $i
  done
  ## 效果等同于:
  for i in $*
  do
      echo $i
  done
  ```

  

- C风格for循环

  ```bash
  array=(1 13 43 4 0 5)
  for((i=0;i<${#array[@]};i++))
  do
      echo ${array[$i]}
  done
  ```

  

8. while循环

   ```bash
   #while :创建守护进程
   #临时监听81端口,达到服务器的效果
   # nc -l 81
   while true
   do
       echo "ok"|nc -l 81
   done
   
   ```

   

9. 文件读取

- 迭代获取文件的每一行

  ```bash
  #1
  while read line
  do
      echo $line
  done < $1
  #2
  cat $1| while read line
  do
      echo $line
  done
  #3
  exec < $1
  while read line
  do
      echo $line
  done
  ```

  

- 迭代获取每一个单词

  ```bash
  line="sasa sas as as asas"
  array=($line)
  for word in ${array[@]};
  	do
  	echo $word;
  done
  ```

  

- 迭代获取每一个字符

  ```bash
  word="wordwordword"
  for ((i=0;i<${#word};i++))
  do
      echo ${word:$i:1}
  done
  ```

- 统计文章的行数和词数,字节数

  ```bash
  exec < $1
  lines=1
  total_words=0
  bytes=0
  while read line
  do
      echo "$lines:"$line
      words=1
      array=($line)
      for word in ${array[@]};
      do
          echo "$words:"$word;
          for ((i=0;i<${#word};i++))
          do
              echo  ${word:$i:1};
          done
          ((words++))
          ((total_words+=words))
      done
      ((bytes+=${#line}))
      ((lines++))
  done
  echo "lines:$lines;total_words:$total_words;bytes:$bytes(with out ' |\r|\n')"
  ```

10. 分割字符串转为数组

- 使用{str//,/ }处理

  ```bash
  str="1,2,3,4,5"
  arr=(${str//,/})
  echo ${arr[@]}
  ```

  

- 使用tr

  ```bash
  str="1,2,3,4,5"   
  arr=(`echo $str | tr ',' ' '`)
  echo ${arr[@]} 
  ```

- awk

  ```bash
  str="1,2,3,4,5"
  arr=($(echo $str|awk 'BEGIN{FS=",";OFS=" "}{print $1,$2,$3,$4,$5}'))
  echo ${arr[@]}
  ```

  

- IFS

  ```bash
  str="1,2,3,4,5"
  IFS=","
  arr=(str)
  echo ${str[@]}
  ```

11. array

- 定义数组`arr=(001 002 003)`

- 定义数组`arr=([1]=321 [3]=ewq)`

- 命令执行结果赋值`

  ```bash
  dir=(`ls`)
  dir=($(ls))
  ```


- 数组**长度**`${#arr[@]}`

- 获取**所有元素**`${arr[@]}`

- 获取所有的**下标**`${!arr[@]}`

- 根据索引(下标)获取元素`${arr[1]}`

- **遍历数组**` for i in ${arr[@]};do echo $i;done`

- **遍历数组**`for i in ${!arr[@]};do echo ${arr[$i]};done`

- 遍历数组

  ```bash
  for i in `eval echo {1..${#arr[@]}}`;do echo ${arr[$i]};done
  ```

  

- 增加元素`arr[3]=004`

- 修改元素`arr[3]=005`

- 删除元素`unset arr[2]`
11. map

- 定义map`declare -A map=([key1]=value1 [key2]=value2 [key3]=value3)`
- 获取所有**元素**`${map[@]}`
- 获取所有**keys**`${!map[@]}`
- 根据key获取value`${map[key1]}`
- 修改元素`map[key1]="new value"`
- **遍历**map`for i in ${!map[@]};do echo ${map[$i]};done`