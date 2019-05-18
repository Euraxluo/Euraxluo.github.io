# C语言小计

## Unix C

1. 内核-》系统调用-》shell/共用函数库-》应用程序

2. 系统调用和库函数

   - 库函数会调用系统调用来实现自己的算法

   - 公用函数库构建在系统调用之上，应用程序既可以使公用函数库，也可以使用系统调用

3. 口令文件：`/etc/passwd` 字段结构：

   `登录名：加密口令：UID：GID：注释字段：起始目录：sell`

4. 文件系统：

   - `/`是root目录
   - `/和空字符`不能出现在文件名字中，斜线用来分隔开构成路径名的各文件名，空字符用来终止一个路径名
   - 工作目录：每个进程都有一个工作目录，所有的相对路径名都从工作目录开始解释，进程可以使用`chdir()`更改工作目录,以`/`开始的路径名是绝对路径名
   - 登陆时工作目录设置为起始目录，从口令文件中取得

5. 输入输出

   - 不带缓冲区的io：`open,read,write,lseek,close`
   - `stdout > file`可以把标准输出或者符号左边的字符重定向到文件

6. 进程

   - 每个进程都有一个pid，`pid_t`保证可以用long保存

   - 进程控制：`fork,waitpid,exec(exec函数有很多变体)`

   - signal，用于通知进程发生了某种情况；进程会：

     1. 忽略信号

     2. 按系统默认方式处理
     3.  提供一个函数，信号捕捉（类似错误处理？）

7. 时间值

   - 用户cpu时间：执行用户指令所用的时间
   - 系统cpu时间：该进程执行内核程序经历的时间
   - 时钟时间：进程运行的时间总量
   - CPU时间 = time_t + clock_t
   - 问题：若日历时间放在带符号的32位int中，哪一年会溢出？怎么扩展

## 文件IO（不带缓冲的IO）

1. 不带缓冲：指的是每个read和write都调用系统调用，这些函数不是ISO C的组成部分

2. 幻数：没来由的，不利于维护的数字，最好define

   - define STDIN_FILENO 0
   - define STDOUT_FILENO 1
   - define STDERR_FILENO 3

3. `open(path，oflag)`,oflag常量很多，说明了文件的打开描述

4. `openat(path，oflag)`,oflag常量很多，说明了文件的打开描述

5. `creat(path,mode)`mode指示文件访问权限

6. `close(int fd)`关闭一个文件的同时还会释放该进程加在这个文件上的所有记录锁

7. `off_t/-1 =  lseek(int fd,off_t offset,int whence)`偏移量设置函数

   - whence == SEEK_SET,off_t = begin()+offset,文首绝对偏移量
   - whence == SEEK_CUR,off_t = off_t + offset,相对当前位置偏移
   - whence == SEEK_END,off_t = end() + offset,文尾相对位置偏移

8. `od -c file`查看文件的实际内容,`-c`以字符方式

9. `ssize_t read(int fd,void *buf,size_t nbytes)`从文件中中读取数据，`void *`通用指针

10. shell提供一种方法，从标准输入上打开一个文件用于读，在标准输出上创建/重写一个文件。因此很多程序可以不必打开输出和输入文件

11. 预读技术：检测到正在顺序读取时，系统试图读入比应用所要求的更多数据

12. `ioctl(int fd,int request,...)`:io杂物箱

    很多的设备的驱动程序可以自定义自己的一组ioctl

13. `/dev/fd`

    这个目录的目录项时0,1,2，这些等效于`/dev/stdin,/dev/stdout,/dev/stderr`，打开`/dev/fd/n`等效于复制描述符

### 文件共享

#### 数据结构

1. 记录表：每个进程在进程表中都有一个记录项，记录项中包含一个文件描述符

   a. 文件描述标志（close_no_exec）

   b. 指向一个文件表项的指针

2. 内核为所有的打开文件都维持一张文件表

   a. 文件状态标志（r,w,a,async）

   b. 当前文件偏移量

   c. 指向该文件v节点的指针

3. 每个打开文件或设备都有一个v节点结构

#### 原子操作

1. 追加，在打开文件时设置`O_APPEND`标志，使得内核在每次写操作之前，都会将文件的当前偏移量设置到文件尾端处

2. `pwrite()/pread(int fd,void *buf,size_t nbytes,off_t offset)`相当于调用lseek后调用read
   - 调用pread时，无法中断其定位和读操作
   - 不更新当前文件的偏移量
3. `dup()/dup2(int fd,int fd2)`复制文件描述符，相当于调用了close(fd2),fcntl(fd,F_DUPFD,fd2)

#### 延迟写：数据-》缓冲区-》queue-》disk

为了保证实际文件系统与缓冲区中内容的一致性，Unix系统提供了sync，fsync，fdatasync

1. `fsync(int fd)`:只对fd起作用，并且会更新文件的属性，并且等待写操作结束才返回
2. `fdatasync(int fd)`：和fsync类似，但是只影响文件的数据部分，不更新文件的数据部分
3. `void sync(void)`：将修改过的快缓冲区排入写队列，马上返回，并不等待实际写磁盘操作结束

#### fchtl(int fd,int cmd)

- 复制一个已有的文件描述符
- 获取/设置文件描述符标志
- 获取/设置文件状态标志
- 获取/设置异步IO所有权
- 获取/设置记录锁

#### 文件中的空洞

普通文件会包含空洞，是由于所设置的偏移量超过了文件的尾端，并写入了某些数据后造成的

- `ls -l file`:可以查看文件的大小

## 文件和目录

### stat函数

1. `stat(pathname,buf)`:返回与此命名文件有关的信息结构

2. `fstat(fd,buf)`：获得已在描述符fd上打开文件的信息结构

3. `lstat(pathname,buf)`：当命名文件是一个是一个符号链接时，返回链接文件的有关信息，而不是由该符号链接引用的文件的信息

4. `fstatat(fd,pathname,buf,flag)`为一个相对于当前打开目录(fd指示)的路径名返回文件统计信息

###  文件类型：stat结构的st_mode

1. 普通文件：普通文件内容的解释是由处理该文件的应用程序进行
   - 二进制可执行文件除外，遵循一种标准化的格式
2. 目录文件：包含了其他文件的名字以及指向这些文件信息的指针
   - 对一目录文件具有读权限的任一进程都可以读该目录的内容
   - 只有内核可以直接写目录文件
   - 进程只有通过特定的函数才能更改目录
3. 块特殊文件（block）：提供对设备带缓冲的，每次访问以固定长度为单位进行
4. 字符特殊文件（character）;提供对设备不带缓冲的访问
   - 系统中的设备要么是字符特殊文件，要么是块特殊文件
5. FIFO:用于进程之间的通信，也叫管道
6. 套接字：用于进程间的网络通信
7. 符号链接:指向另一个文件
8. 消息队列：进程间通信对象(IPC)
9. 信号量:进程间通信对象(IPC)
10. 共享存储对象:进程间通信对象(IPC)

### 用户id和组id

| 实际用户ID<br/>实际组ID             | 我们实际上是谁         |
| :---------------------------------- | ---------------------- |
| 有效组ID<br/>有效组ID<br/>附属组ID  | 用于文件访问权限的检查 |
| 保存的设置用户ID<br/>保存的设置组ID | 由exec函数保存         |

每个文件都有一个所有者和组所有者，所有者由stat结构中的st_uid指定，组所有者则由st_gid指定

### 文件的访问权限

- 为了在一个目录中创建一个新文件，必须对改目录具有写权限和执行权限
- 为了在open()函数中对一个文件指定O_TRUNC标志，必须对该文件具有写权限
- 为了删除以恶搞现有的文件，必须对包含该文件的目录具有写权限和执行权限，对该文件本身不需要读和写权限
- 如果用7个exec函数中的任意一个执行某个文件，都必须对该文件具有执行权限，该文件还必须是一个普通文件
- 在使用open和creat创建一个文件时，新文件的用户ID设置为进程的有效用户ID

### 权限测试

当open函数打开一个文件时，内核以进程的有效ID和有效组ID为基础执行其访问权限测试。

- `access(pathname,mode)`

- `faccessat(fd,pathname,mode,flag)`,计算相对于打开目录(fd指示)的pathname

  mode: R_OK,W_OK,X_OK

### 权限

1. umask(mode_t cmask)
   - 000 任何用户可以读文件
   - 002 阻止其他用户写入文件
   - 027 阻止同组成员写入你的文件，以及其他用户的rwx权限
2. `chmod(pathname,mode)`更改指定文件的权限
3. `fchmod(fd,mode)`针对打开的文件进行操作
4. `fchmodat(fd,pathname,made,flag)`，fd为AT_FDCWD时和chmod一致，flag改变fchmodat的行为
5. chmod函数更新的是i节点最近一次被更改的时间，ls -l 列出来的是文件最后被修改的时间
6. `fchown,fchownat,lchown,chown(pathname,owner,group)`可用于更改文件的用户ID和组ID

### 文件和目录处理

1. `truncate/ftruncate(fd,off_t length)`;截断函数，将一个现有的文件长度截断为length，如果之前该文件以前的长度大于length，则langth、以外的数据就不能再访问。如果以前的长度小于length，文件长度将增加。
2. `link/linkat(efd,existingpath,nfd,*newpath,flag)`,创建newpath，引用existingpath，如果newpath已经存在，则返回出错。
3. `renameat/rename(oldname,newname);`如果oldname是指文件，为此文件重命名。link文件的话，重命名此文件，不是链接的文件
4. `futimens,utimes,utimensat(fd,path,times,flag)`修改一个文件的访问和修改时间
5. `mkdirat，mkdir(fd,pathname,mode):`这两个函数创建一个新的空目录，所指定的文件的访问权限mode由进程的文件模式创建屏蔽字修改
6. `rmdir(const char*pathname)`删除一个空目录，空目录是只包含`.和..`两项的目录
7. 对某目录具有访问权限的任意用户都可以读该目录，但是，为了防止文件系统产生混乱，只有内核才能写目录。一个目录的的写权限位和执行权限决定了在该目录能否创建新文件以及删除文件，但是不代表可以写目录
8. `DIR *fdopendir(int fd)`表示可以把打开文件描述符转换成目录处理函数需要的DIR结构

### 标准I/O库

1. 标准输入流，标准输出流，标准错误流。一个进程预定义了3个流，并且可以自动的被进程所使用

2. 缓冲

   - 全缓冲：填满标准I/O缓冲区后才进行实际I/O操作，一般用于驻留在磁盘上的文件

     在一个流上第一次执行I/O操作时，I/O函数通常调用malloc函数获得需要的缓冲区

     **flush**:冲洗，标准I/O缓冲区的写操作，当填满一个缓冲区时，I/O例程会自动的冲洗

   - 行缓冲：当在输入和输出中遇到换行符时，标准I/O执行I/O操作，当流涉及一个终端时，通常使用行缓冲

     **限制**:缓冲区的长度固定的，所以有时没有遇到换行符，也会进行I/O操作

   - 不带缓冲：标准错误流通常不带缓冲，使得他们的错误可以尽快显示出来

3. `setbuf(fp,buf)`打开或或关闭缓冲机制，开启后一般为全缓冲

4. `setvbuf(fp,buf,mode,size)`通过设置mode精确的说明所需的缓冲类型

5. `fflush(fp)`，强制冲洗一个流

6. `FILE *fopen(pathname,type,)`打开路径名为pathname的一个文件

7. `FILE *freopen(pathname,type,fp)`重定向流，在一个指定的流上打开文件，若流已经打开，则先关闭

8. `fdopen(fd,type)`获取一个已有的文件描述符，并使一个标准I/O流与该描述符相结合，此函数常用于由管道创建和网络通信函数返回的描述符

9. 当以读和写类型打开一个文件时，如果中间没有`fflush，fseek，fsetpos或rewind`，那么在输出的后面不能直接跟随输入

10. 以读和写打开一个文件时，当中间没有`fseek,fsetpos,rewind`,或者一个输入操作没有到达文件尾端，则在输入操作之后不能直接跟随输出

11. 读和写流

    - 每次一个字符的I/O，`getc,fgetc,getchar`一次读或者写一个字符，如果流是带缓冲的，则标准I/O函数处理所有的缓冲
    - 每次一行的I/O，`fgets,fputs`,每行以一个换行符终止，当调用fgets时，应说明能处理的最大行
    - direct I/O，`fread,fwrite`每次I/O操作读或写某种数量的对象，每个对象具有指定的长度，常用于读写二进制文件
    - 压送回流，`ungetc(int c,FILE fp)`,压送回流的字符又可以

