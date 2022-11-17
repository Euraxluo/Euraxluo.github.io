+++
title = "Git学习笔记"
date = 2018-07-11
description = "git"
featured = false
categories = [
  "tools"
]
tags = [
  "git"
]
images = [
]

+++


# Git 学习笔记
## cd相对路径
cd    什么都不加 回到用户的家目录下
cd ~  回到root目录下
cd ..    进入上一级目录

cd -     返回上一次目录

cd .     当前目录

## 创建和删除目录

### 创建目录mkdir

mkdir=make directory 

mkdir dirname 创建目录 

mkdir -p /etc/dirname/test/ 级联创建目录 

mkdir -pv /etc/dirname/test/ 加上v可以看到创建的过程 

### 删除目录rmdir 

rmdir=remove directory 

rmdir dirname 可 删除空目录（下面无目录和文件） 

### 删除文件 rm = remove命令

rmdir -p 可级联删除一串目录，但是是从最开始的目录删起。比较危险，慎用

rm /tmp/ww/2/3/1.txt 会提示是否删除1.txt 

rm -f /tmp/ww/2/3/1.txt 强制删除，不给提示 

rm -r 级联删除目录，但是会提示是否删除，直接rm不能删目录

rm -rf 直接级联强制删除 

rm -rfv 加上v显示删除过程 

## 更新仓库

```bash

	//在github上创建项目

	$ git clone https://github/xx账号/xx项目.git//克隆到本地

	//编辑项目

	$ git add .//(将改动添加到暂存区)

	$ git commit –m”提交说明” //

	$ git push origin master//将本地更改推送到远程master分支

```

实例：

```bash

git clone https://github.com/Euraxluo/-.git

//我更改了一个文件的名字

cd ./-//选中我的文件目录

git add *.py//选中我要更新的文件

git commit -m "rename"//提交说明

git push -u origin master//推送

//这时，由于我的项目地址是https,而不是git，要求更新

//我打算更改路径

```
```c

git push -u origin master//重新提交

```


### 注：

1.提交：

```c



git add -A //提交所有变化

git add -u  //提交被修改(modified)和被删除(deleted)文件，不包括新文件(new)

git add . //提交新文件(new)和被修改(modified)文件，不包括被删除(deleted)文件

```

2.删除：

```c

$ git rm 我的文件//删除文件

$ git rm -r 我的文件夹//删除文件夹

$ git rm -h//git rm [<选项>] [--] <文件>...

    -n, --dry-run         演习

    -q, --quiet           不列出删除的文件

    --cached              只从索引区删除

    -f, --force           忽略文件更新状态检查

    -r                    允许递归删除

    --ignore-unmatch      即使没有匹配，也以零状态退出

```







## 创建仓库



```c

    $ makdir ~/hello-world    //创建一个项目hello-world

    $ cd~/hello-world       //打开这个项目

    $ git init             //初始化 

    $ touch README

    $ git add README        //更新README文件

    $ git commit-m 'first commit'//提交更新，并注释信息

    $ git remote add origin git@.:.git//连接远程github项目  

    $ git push -u origin master //将本地项目更新到github项目上去



```

## 删除仓库

```c

git branch//显示所有的本地分支

结果：* master

ls -a//找到目录下的.git

结果：./ ../ .git

rm -rf .git//删除操作

结果：.git 被删除，本地库删除成功

```



## 查看分支并切换

```shell

# 查看远程分支

git branch -a 

# 新建一个分支

git checkout -b <new branch name> 

# 查看本地分支

git branch

# 分支切换

git checkout version



```



## 查看当前的远程库



```shell

#不带参数，列出已经存在的远程分支

git remote



#列出详细信息，在每一个名字后面列出其远程url

#此时， -v 选项(译注:此为 –verbose 的简写,取首字母),显示对应的克隆地址

git remote -v | --verbose 

```


## 暂存修改
`git stash` 把不想提交的修改暂存起来

`git stash apply` 取回暂存修改

## git 文件过大


在频繁增删改、commit之后，.git文件会出现过大的情况。这个时候如何彻底清理以前的历史版本（也就是说只保留当前版本，不可能再回滚了）
 方法是首先建立一个分支，然后将master版本给删除，再将当前分支重命名为master，再强制push到远程仓库即可。
 具体步骤：

```bash
 第一步：
 `git checkout --orphan latest_branch`
 第二步：添加所有文件
 `git add -A`
 第三步：提交更改
 `git commit -am "commit message"`
 注意这里commit message是你提交的修改说明
 第四步：删除分支
 `git branch -D master`
 第五步：将当前分支重命名
 `git branch -m master`
 最后：强制更新存储库
 `git push -f origin master`
 就此完成。
```

 要注意尽量不要往git上提交二进制文件，二进制文件是不按diff保存的，即使提交了也不要每次改一点然后再提交一遍。

一：常规办法
1.删除无用的分支

`git branch -d <branch_name>`
2.删除无用的tag

`git tag -d <tag_name>`
3.清理本地版本库

`git gc --prune=now`
二：高级办法
注意高级办法会导致push冲突，需要强制提交，其他人pull也会遇到冲突，建议重新克隆.

1.完全重建版本库

```
rm -rf .git
git init
git add .
git commit -m "first commit"
git remote add origin <your_github_repo_url>
git push -f -u origin master
```
2.有选择性的合并历史提交

`git rebase -i <first_commit>`
会进入一个如下所示的文件

```
pick ba07c7d add bootstrap theme and format import
pick 7d905b8 add newline at file last line
pick 037313c fn up_first_char rename to caps
pick 34e647e add fn of && use for index.jsp
pick 0175f03 rename common include
pick 7f3f665 update group name && update config
```
将想合并的提交的pick改成s，如
```
pick ba07c7d add bootstrap theme and format import
pick 7d905b8 add newline at file last line
pick 037313c fn up_first_char rename to caps
s 34e647e add fn of && use for index.jsp
pick 0175f03 rename common include
pick 7f3f665 update group name && update config
```
这样第四个提交就会合并进入第三个提交。
等合并完提交之后再运行
```
git push -f
git gc --prune=now
```

三.其他方法

1. `dh -d 1 -h` 查看哪个目录最大，确认是git目录

2. `git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -5 | awk '{print$1}')"` 查看占用空间最大的5个文件

3. 重写commit，删除大文件`git filter-branch --force --index-filter 'git rm -rf --cached --ignore-unmatch big-file.jar' --prune-empty --tag-name-filter cat -- --all` big-file.jar 换成之前查询出来的大文件名

4. `git push origin master --force`以强制覆盖的方式推送repo

5. 清理空间

   ```
   rm -rf .git/refs/original/
   
   git reflog expire --expire=now --all
   
   git gc --prune=now
   ```

   

## 合并分支

###  创建与合并分支


每次提交，Git都把它们串成一条时间线，这条时间线就是一个分支。截止到目前，只有一条时间线，在Git里，这个分支叫主分支，即`master`分支。`HEAD`严格来说不是指向提交，而是指向`master`，`master`才是指向提交的，所以，`HEAD`指向的就是当前分支。

一开始的时候，`master`分支是一条线，Git用`master`指向最新的提交，再用`HEAD`指向`master`，就能确定当前分支，以及当前分支的提交点：

![git-br-initial](https://www.liaoxuefeng.com/files/attachments/919022325462368/0)

每次提交，`master`分支都会向前移动一步，这样，随着你不断提交，`master`分支的线也越来越长。

当我们创建新的分支，例如`dev`时，Git新建了一个指针叫`dev`，指向`master`相同的提交，再把`HEAD`指向`dev`，就表示当前分支在`dev`上：

![git-br-create](https://www.liaoxuefeng.com/files/attachments/919022363210080/0)

你看，Git创建一个分支很快，因为除了增加一个`dev`指针，改改`HEAD`的指向，工作区的文件都没有任何变化！

不过，从现在开始，对工作区的修改和提交就是针对`dev`分支了，比如新提交一次后，`dev`指针往前移动一步，而`master`指针不变：

![git-br-dev-fd](https://www.liaoxuefeng.com/files/attachments/919022387118368/0)

假如我们在`dev`上的工作完成了，就可以把`dev`合并到`master`上。Git怎么合并呢？最简单的方法，就是直接把`master`指向`dev`的当前提交，就完成了合并：

![git-br-ff-merge](https://www.liaoxuefeng.com/files/attachments/919022412005504/0)

所以Git合并分支也很快！就改改指针，工作区内容也不变！

合并完分支后，甚至可以删除`dev`分支。删除`dev`分支就是把`dev`指针给删掉，删掉后，我们就剩下了一条`master`分支：

![git-br-rm](https://www.liaoxuefeng.com/files/attachments/919022479428512/0)


### 实践
首先，我们创建`dev`分支，然后切换到`dev`分支：

```
$ git checkout -b dev
Switched to a new branch 'dev'
```

`git checkout`命令加上`-b`参数表示创建并切换，相当于以下两条命令：

```
$ git branch dev
$ git checkout dev
Switched to branch 'dev'
```

然后，用`git branch`命令查看当前分支：

```
$ git branch
* dev
  master
```

`git branch`命令会列出所有分支，当前分支前面会标一个`*`号。

然后，我们就可以在`dev`分支上正常提交，比如对`readme.txt`做个修改，加上一行：

```
Creating a new branch is quick.
```

然后提交：

```
$ git add readme.txt 
$ git commit -m "branch test"
[dev b17d20e] branch test
 1 file changed, 1 insertion(+)
```

现在，`dev`分支的工作完成，我们就可以切换回`master`分支：

```
$ git checkout master
Switched to branch 'master'
```

切换回`master`分支后，再查看一个`readme.txt`文件，刚才添加的内容不见了！因为那个提交是在`dev`分支上，而`master`分支此刻的提交点并没有变：

![git-br-on-master](https://www.liaoxuefeng.com/files/attachments/919022533080576/0)

现在，我们把`dev`分支的工作成果合并到`master`分支上：

```
$ git merge dev
Updating d46f35e..b17d20e
Fast-forward
 readme.txt | 1 +
 1 file changed, 1 insertion(+)
```

`git merge`命令用于合并指定分支到当前分支。合并后，再查看`readme.txt`的内容，就可以看到，和`dev`分支的最新提交是完全一样的。

注意到上面的`Fast-forward`信息，Git告诉我们，这次合并是“快进模式”，也就是直接把`master`指向`dev`的当前提交，所以合并速度非常快。

当然，也不是每次合并都能`Fast-forward`，我们后面会讲其他方式的合并。

合并完成后，就可以放心地删除`dev`分支了：

```
$ git branch -d dev
Deleted branch dev (was b17d20e).
```

删除后，查看`branch`，就只剩下`master`分支了：

```
$ git branch
* master
```

因为创建、合并和删除分支非常快，所以Git鼓励你使用分支完成某个任务，合并后再删掉分支，这和直接在`master`分支上工作效果是一样的，但过程更安全。



### 合并分支相关小结

查看分支：`git branch`

创建分支：`git branch <name>`

切换分支：`git checkout <name>`

创建+切换分支：`git checkout -b <name>`

合并某分支到当前分支：`git merge <name>`
如果遇到报错`$ git checkout dev
warning: refname 'dev' is ambiguous.`
需要查看是否有同名指针:` git show-ref --heads --tags`
然后选择需要的指针合并

删除分支：`git branch -d <name>`