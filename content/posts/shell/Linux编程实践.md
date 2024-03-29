+++
title = "Unix/Linux编程实践1"
date = "2018-10-29"
description = "Unix/Linux编程实践"
featured = false
categories = [
  "读书笔记"
]
tags = [
  "读书笔记"
]
series = [
  "读书笔记"
]
images = [
]

+++

# Unix/Linux 编程實踐教程

##　什麼是系統編程
### 系统资源

1. 处理器

程序由指令构成,处理器是执行指令的硬件设备,一个系统中可能有多个处理器,内核可以安排一个程序何时开始开始执行,暂时停止,恢复执行,终止执行

2. 输入输出

程序中所有的输入输出都必须流经内核,集中处理,保证了系统的正确性,安全性,有效性

3. 进程管理

每个程序执行都必须有自己的资源,内核可以新建进程,中止进程,进程调度

4. 内存

程序必须被装载到内存中才能运行,内核可以对进程进行管理,在程序需要的时候给程序分配内存,当程序不需要时,回收内存,还可以保证内存不被其他进程非法访问.

5. 设备

各种设备的操作方式不相同,通过内核,可以屏蔽這種差异,使我们对设备的操作简单统一

6. 计时器

程序的工作和时间有关,内核可以通过系统调用向应用程序提供计时器服务

7. 进程间通信

内核可以让进程之间进行通信

8. 网络

内核可以让不同主机上的不同进程进行通信



### bc:Unix计算器,可以接受逆波兰表达式

通过他的与处理器dc,转换为逆波兰表达式,通过pip给dc

和web服务类似,web服务器作为預处理器,浏览器作为前端显示



### more:

more filename,分页显示file内容

command | more:分页显示command命令

more < filename:分页+重定向



自己写一个more

```c

//more command

#include<stdio.h>

#include<stdlib.h>

#define PAGELEN 24

#define LINELEN 512

void do_more(FILE* );

int see_more(FILE*,int );

int sum_size  = 0;

 

int main(int ac,char *av[])

{

	FILE* fp;

	if(ac == 1)

		do_more(stdin);

	else

		while(--ac)

		{

			if((fp = fopen(*++av,"r")) != NULL)

			{

				fseek(fp,0L,SEEK_END);  /*利用fseek函数将指针定位在文件结尾的位置*/

				sum_size=ftell(fp);     /*利用ftell函数返回指针相对于文件开头的位置，以字节计算*/

				printf("\n the type of file is : %d\n",sum_size);   /*进行输出文件总大小*/

				fseek(fp,0L,SEEK_SET);   /*将fp设置文件开始的位置*/

				do_more(fp);

				fclose(fp);

			}

			else

				exit(1);

		}

	return 0;

}

 

void do_more(FILE* fp)

{

	/*

		read PAGELEN lines, then call see_more() for further instructions

	*/

	char line[LINELEN];

	int num_of_lines = 0;

	int see_more(FILE*,int),reply;

	FILE* fp_tty;

	fp_tty = fopen("/dev/tty","r");

	if(fp_tty == NULL)

		exit(1);

	while(fgets(line, LINELEN,fp))

	{

		if(num_of_lines == PAGELEN)

		{

			int cur_size=ftell(fp);   /*利用ftell函数返回指针相对于文件开头的位置，以字节计算*/

			int per= (int)100* cur_size/sum_size; //计算当前占用比例。

			reply =see_more(fp_tty,per);

			if(reply == 0 )

				break;

			num_of_lines -= reply;

		}

		if(fputs(line,stdout) == EOF)

			exit(1);

		num_of_lines++;

	}

}

int see_more(FILE* cmd,int per)

{

	/*

	print message, wait for response, return # of lines to advance

	q means no, space means yes CRmeans one line

	*/

	int c;

	system("stty -icanon");//关闭缓冲区，输入字符无需回车直接接受

	printf("\033[7m more?##%d##\033[m",per);  //实现反白

	while((c=getc(cmd))!=EOF)

	{

		if(c == 'q')

			return 0;

		if(c == ' ')

			return PAGELEN;

		if(c == '\n')

			return 1;

	}

}

```

### who

查看有哪些用户在使用这台电脑



自己写一个who:

需要的步骤:

```shell

#直接运行,了解大致的功能

who

#查看文档

man who

#可以看到,大致放在utmp这个文件中

#根据关键词查看帮助

man -k utmp

#结果可以看到在帮助手册的第3节

man 3 utmp

#结果中,可以知道这是一个数据结构,定义在某个.h文件中



#从文件中读取数据结构

man -k file | egrep read

#于是我们找到了read(),进去看如何调用

#顺便,他还介绍了close()和open()



#思路:

#从utmp中读取我们需要的信息,循环输出



#关于怎么输出时间

man -k time | egrep transform

#结果你应该可以看到ctime

man 3 ctime

## 开始写吧:

```

who:

```c

#include<stdlib.h>

#include<stdio.h>

#include<utmp.h>

#include<fcntl.h>

#include<unistd.h>

#include<time.h>

#define SHOWHOST

#define USER_PROCESS 7

void showtime(long);

void show_info(struct utmp * utbufp){

	if(utbufp->ut_type != USER_PROCESS)

		return;

	printf("%-8.8s",utbufp->ut_name);

	printf(" ");

	printf("%-8.8s",utbufp->ut_line);

	printf(" ");

	showtime(utbufp->ut_time);

	#ifdef SHOWHOST

		if(utbufp->ut_host[0] != '\0')

			printf("(%s)",utbufp->ut_host);

	#endif

		printf("\n");	

}

void showtime(long timeval){

	char *cp;

	cp = ctime(&timeval);

	printf("%12.12s",cp+4);

}

int main(){

	struct	utmp current_record;

	int 	utmpfd;

	int 	reclen = sizeof(current_record);

	if((utmpfd = open(UTMP_FILE,O_RDONLY)) == -1){

		perror(UTMP_FILE);

		exit(1);}

	while (read(utmpfd,&current_record,reclen) == reclen)

		show_info(&current_record);

	close(utmpfd);

	return 0;

}

```

#使用缓冲区的who

```c

#include<stdlib.h>

#include<stdio.h>

#include<utmp.h>

#include<fcntl.h>

#include<unistd.h>

#include<time.h>

#define SHOWHOST

#define USER_PROCESS 7

#define NRECS 16

#define NULLUT ((struct utmp*)NULL)

#define UTSIZE (sizeof(struct utmp))



static char utmpbuf[NRECS * UTSIZE];

static NULLUT ()

void showtime(long);

void show_info(struct utmp * utbufp){

	if(utbufp->ut_type != USER_PROCESS)

		return;

	printf("%-8.8s",utbufp->ut_name);

	printf(" ");

	printf("%-8.8s",utbufp->ut_line);

	printf(" ");

	showtime(utbufp->ut_time);

	#ifdef SHOWHOST

		if(utbufp->ut_host[0] != '\0')

			printf("(%s)",utbufp->ut_host);

	#endif

		printf("\n");	

}

void showtime(long timeval){

	char *cp;

	cp = ctime(&timeval);

	printf("%12.12s",cp+4);

}

int main(){

	struct	utmp current_record;

	int 	utmpfd;

	int 	reclen = sizeof(current_record);

	if((utmpfd = open(UTMP_FILE,O_RDONLY)) == -1){

		perror(UTMP_FILE);

		exit(1);}

	while (read(utmpfd,&current_record,reclen) == reclen)

		show_info(&current_record);

	close(utmpfd);

	return 0;

}

```



### cp

cp命令把源文件复制到目标文件，如果目标文件不存在，就创建这个命令，如果已经存在就覆盖



创建和重写文件：

系统调用函数creat：

`int fd = creat(char *filename,mode_t mode)`

mode:如果内核成功创建了file，则把mode设置为许可位



系统调用函数write：

`ssize_t result = write(int fd,void *buf,size_t  amt)`

#### 提高文件i/o效率的方法：使用缓冲

系统调用是需要时间的：

当这个程序去调用read时，read的代码在内核中。

系统调用开销大的原因：

内核和程序之间不只是会传输数据，还会在root模和用户模式之间来回切换
