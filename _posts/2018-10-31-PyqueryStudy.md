---
layout:     post                    # 使用的布局（不需要改）
title:      爬虫學習               # 标题 
subtitle:   pyquery                #副标题
date:       2018-10-31            # 时间
author:     Euraxluo                      # 作者
header-img: img/post-bg-github-cup.jpg  #这篇文章标题背景图片
catalog: true                 # 是否归档
tags:                               #标签
    - 爬虫

---

# pyquery


## 初始化


```python
%%html
<div id = "container">
<ul class="list">
<li class = "item-0">frist item</li>
<li class = "item-1"><a href="link2.html">second item</a></li>
<li class = "item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
<li class = "item-1 active"><a href="link4.html">fourth item</a></li>
<li class = "item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>
```


<div id = "container">
<ul class="list">
<li class = "item-0">frist item</li>
<li class = "item-1"><a href="link2.html">second item</a></li>
<li class = "item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
<li class = "item-1 active"><a href="link4.html">fourth item</a></li>
<li class = "item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>


### 字符串初始化


```python
html = '''
<div id = "container">
<ul class="list">
<li class = "item-0">frist item</li>
<li class = "item-1"><a href="link2.html">second item</a></li>
<li class = "item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
<li class = "item-1 active"><a href="link4.html">fourth item</a></li>
<li class = "item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>

'''
from pyquery import PyQuery as pq
doc = pq(html)
print(doc("li"))
```

    <li class="item-0">frist item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>


​    

### URL初始化


```python
doc = pq(url="http://www.baidu.com")
print(doc("head").text().encode('iso8859-1').decode('utf8'))
```

    百度一下，你就知道


### 文件初始化


```python
doc = pq(filename = "test.html")
print(doc("li"))
```

    <li class="item-0">frist item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>


​    

## css选择器


```python
doc = pq(html)
print(doc("#container .list li"))
```

    <li class="item-0">frist item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>


​    

## 查找元素


```python
doc = pq(html)
items = doc(".list")
print(type(items))
print(items)
print("------------------")

lis = items.find("li")
print(type(lis))
print(lis)

```

    <class 'pyquery.pyquery.PyQuery'>
    <ul class="list">
    <li class="item-0">frist item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
    
    ------------------
    <class 'pyquery.pyquery.PyQuery'>
    <li class="item-0">frist item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>


​    

### 子元素


```python
lis1 = items.children()
print(lis1)
print("------------------")

lis2 = items.children(".active")
print(lis2)
```

    <li class="item-0">frist item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>
    
    ------------------
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>


​    

### 父级元素


```python
parent = items.children().parent()
print(parent)
```

    <ul class="list">
    <li class="item-0">frist item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>


​    


```python
parents =items.children().parents()
print(parents)
print("------------------")
print(parents(".list"))
```

    <div id="container">
    <ul class="list">
    <li class="item-0">frist item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
    </div><ul class="list">
    <li class="item-0">frist item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
    
    ------------------
    <ul class="list">
    <li class="item-0">frist item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>
    <ul class="list">
    <li class="item-0">frist item</li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>
    </ul>


​    

 ### 兄弟元素


```python
third = doc(".list .item-0.active")
print(third)
print("----------")
brothers = third.siblings()
print(brothers)
```

    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    
    ----------
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-0">frist item</li>
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    <li class="item-0"><a href="link5.html">fifth item</a></li>


​    

## 遍历


```python
doc = pq(html)
lis = doc("li").items()
print(type(lis))
for li in lis:
    print(li)
    print("---")
```

    <class 'generator'>
    <li class="item-0">frist item</li>
    
    ---
    <li class="item-1"><a href="link2.html">second item</a></li>
    
    ---
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    
    ---
    <li class="item-1 active"><a href="link4.html">fourth item</a></li>
    
    ---
    <li class="item-0"><a href="link5.html">fifth item</a></li>
    
    ---


## 获取信息

### 获取属性


```python
doc = pq(html)
a = doc(".item-0.active a")
print(a)
print("---")
print(a.attr("style"))
print("---")
print(a.attr.href)
```

    <a href="link3.html" style="color:black;"><span class="bold">third item</span></a>
    ---
    color:black;
    ---
    link3.html


### 获取文本


```python
texts = doc.items()
for text in texts:
    print(text.text())
```

    frist item
    second item
    third item
    fourth item
    fifth item


### 获取html


```python
a = doc(".item-0.active a")
print(a)
print("---")
print(a.html())
```

    <a href="link3.html" style="color:black;"><span class="bold">third item</span></a>
    ---
    <span class="bold">third item</span>


### addClass,removeClass


```python
doc = pq(html)
li = doc(".item-0.active")
print(li)
li.removeClass('active')
print(li)
li.addClass('active')
print(li)
```

    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    
    <li class="item-0"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    
    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>


​    

### attr,css


```python
doc = pq(html)
li = doc(".item-0.active")
print(li)
li.attr('name','link')
print(li)
li("a").css('font-size','14px')
print(li)
```

    <li class="item-0 active"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    
    <li class="item-0 active" name="link"><a href="link3.html" style="color:black;"><span class="bold">third item</span></a></li>
    
    <li class="item-0 active" name="link"><a href="link3.html" style="color:black; font-size: 14px"><span class="bold">third item</span></a></li>


​    

### remove


```python
doc =pq(html)
li = doc("li")
print(li.text())
li.find('a').remove()
print(li.text())
```

    frist item second item third item fourth item fifth item
    frist item    


### [API](http://pyquery.readthedocs.io/en/latest/api.html)


```python
%%html
<pre style="line-height: 1.25; white-space: pre;">
        \          SORRY            /
         \                         /
          \    This page does     /
           ]   not exist yet.    [    ,'|
           ]                     [   /  |
           ]___               ___[ ,'   |
           ]  ]\             /[  [ |:   |
           ]  ] \           / [  [ |:   |
           ]  ]  ]         [  [  [ |:   |
           ]  ]  ]__     __[  [  [ |:   |
           ]  ]  ] ]\ _ /[ [  [  [ |:   |
           ]  ]  ] ] (#) [ [  [  [ :===='
           ]  ]  ]_].nHn.[_[  [  [
           ]  ]  ]  HHHHH. [  [  [
           ]  ] /   `HH("N  \ [  [
           ]__]/     HHH  "  \[__[
           ]         NNN         [
           ]         N/"         [
           ]         N H         [
          /          N            \
         /           q,            \
        /                           \
</pre>
```


<pre style="line-height: 1.25; white-space: pre;">
        \          SORRY            /
         \                         /
          \    This page does     /
           ]   not exist yet.    [    ,'|
           ]                     [   /  |
           ]___               ___[ ,'   |
           ]  ]\             /[  [ |:   |
           ]  ] \           / [  [ |:   |
           ]  ]  ]         [  [  [ |:   |
           ]  ]  ]__     __[  [  [ |:   |
           ]  ]  ] ]\ _ /[ [  [  [ |:   |
           ]  ]  ] ] (#) [ [  [  [ :===='
           ]  ]  ]_].nHn.[_[  [  [
           ]  ]  ]  HHHHH. [  [  [
           ]  ] /   `HH("N  \ [  [
           ]__]/     HHH  "  \[__[
           ]         NNN         [
           ]         N/"         [
           ]         N H         [
          /          N            \
         /           q,            \
        /                           \
</pre>


## 伪类选择器


```python
doc = pq(html)
li = doc("li:first-child")
print(li.text())
li = doc("li:last-child")
print(li.text())
li = doc("li:nth-child(2)")
print(li.text())
li = doc("li:nth-child(3n)")
print(li.text())
li = doc("li:gt(3)")#取第5个,即第4个以后,第四个下标为3
print(li.text())
li = doc("li:contains(second)")#搜索文本
print(li.text())
```

    frist item
    fifth item
    second item
    third item
    fifth item
    second item


### [css选择器](http://www.w3school.com.cn/css/index.asp)
