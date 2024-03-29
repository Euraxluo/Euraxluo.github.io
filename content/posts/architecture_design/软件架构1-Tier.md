+++
title = "软件架构1-Tier"
date = 2020-02-03
description = "软件架构1-Tier"
featured = false
categories = [
  "architecture design"
]
tags = [
  "architecture"
]
series = [
  "软件架构"
]
images = [
]
+++

## 软件架构

### 软件开发过程的概述

在行业中，架构师、开发人员和产品所有者花费大量时间研究和讨论业务需求。在软件工程术语中，这被称为需求收集和分析。

一旦我们完成了业务需求，我们坐下来讨论我们必须实现的用例。这包括尽早找出角落的情况&将乐高积木组装在一起。

如果您是文档的爱好者，您可能还想编写高级设计文档。现在，我们已经了解了业务需求、用例、拐角用例等等。现在开始研究如何选择合适的技术堆栈来实现用例。

####　概念证明 POC

POC帮助我们对技术和基本用例实现有一个更近、更实际的了解。我们将深入了解技术、性能或其他技术限制的利弊。

如果我们使用的是全新的技术，那么学习曲线就会有所帮助，产品所有者、利益相关者等非技术人员也会有一些具体的东西可以使用，并以此为基础做出进一步的决定。

现在，这只是一个工业规模的产品。如果你是一个独立开发者或一个小团队，你可以跳过POC部分，从主代码开始。

所以，我们向利益相关者展示POC，如果每个人都满意，我们最终在GitHub上创建主回购和我们的第一个开发分支，或任何其他类似的业务喜欢的代码托管服务。

所以，到现在为止，你应该已经意识到在第一时间获得正确的架构和web架构知识对开发人员是多么的重要。



## Tier

我将从讨论软件架构中涉及的不同层次开始课程。这就像是对软件架构领域的鸟瞰，很重要的一点是要很好地理解。

### 什么是一层？

可以将层看作应用程序或服务中组件的逻辑分离。当我说分离时，我指的是**组件级**的物理分离，而不是代码级。

#### 组件的意思是什么？

- 数据库

- 后端应用服务器

- 用户界面

- 消息传递

- 缓存

![image.LN3YG1](https://euraxluo.github.io/images/picgo/image.LN3YG1.png)

### Single Tier Applications

单层应用程序是指用户界面、后端业务逻辑和数据库都驻留在同一台机器中的应用程序。

![image.YG1QG1](https://euraxluo.github.io/images/picgo/image.YG1QG1.png)

单层应用程序的典型例子是桌面应用程序，如moffice、PC游戏或图像编辑软件，如Gimp。

#### 单层应用的优点

单层应用程序的主要优点是它们没有网络延迟，因为每个组件都位于同一台机器上。这就提高了软件的性能。

没有数据请求到后端服务器不时，这将使用户体验缓慢。在单层应用中，由于数据位于同一台机器上，所以数据是很容易和快速获得的。

尽管这在很大程度上取决于机器的功能有多强大&软件的硬件要求，但要衡量单层应用程序的真正性能

此外，用户的数据保存在他的机器&不需要通过网络传输。这在最大程度上保证了数据安全。

#### 单层应用的缺点

单层应用程序的一个大缺点是业务无法控制应用程序。一旦软件交付，除非客户通过连接到远程服务器或下载并安装补丁手动更新软件，否则不可能对代码或功能进行更改。

因此，在90年代，如果一款游戏带有漏洞代码，那么工作室便无能为力。由于软件的缺陷，他们最终不得不面对相当大的压力。产品的测试必须彻底，不能有任何差错。

单层应用程序中的代码也很容易被修改和反向工程。对企业来说，安全性是最低限度的。

此外，应用程序的性能和外观可能会不一致，因为它在很大程度上取决于用户机器的配置。

### Two Tier Applications

两层应用程序包括客户机和服务器。客户端将在一台机器中包含用户界面和业务逻辑。后端服务器将是运行在不同机器上的数据库。数据库服务器由企业托管并对其进行控制。

![image.STXSG1](https://euraxluo.github.io/images/picgo/image.STXSG1.png)

为什么需要两层应用程序?为什么不将业务逻辑驻留在另一台机器上并对其进行控制呢?

优点:

1. 应用程序代码也不容易被第三方访问

2. 在某些情况下，两层应用程序会派上用场，例如，待办事项列表应用程序或类似的计划表或生产力应用程序。在这些场景中，即使代码被第三方访问，也不会对业务造成重大损害。相反，**好处是由于代码和用户界面驻留在同一台机器上，因此对后端服务器的网络调用更少，从而降低了应用程序的延迟**。只有当用户创建完待办事项列表并希望持久化更改时，应用程序才会调用数据库服务器。
3. 另一个例子便是基于浏览器和应用的在线游戏。**游戏文件非常重**，当用户第一次使用应用时，他们只需要在客户端下载一次。此外，它们进行网络调用只是为了保持游戏状态持久。
4. 经济，更少的服务器调用意味着在服务器上花费更少的钱，这自然是**经济**的。
5. 不过，这在很大程度上取决于我们的业务需求和用例，如果我们想在编写服务时选择这种类型的层。我们可以将用户界面和业务逻辑保留在客户机上，也可以将**业务逻辑移动到专用的后端服务器上**，这将使其成为一个三层应用程序。这是我接下来要讨论的

### Tree Tier Applications

三层应用程序非常流行，并在行业中广泛使用。几乎所有的简单网站，如博客，新闻网站等都属于这一类。

在一个三层的应用程序中，用户界面、应用程序逻辑和数据库都位于不同的机器上，因此有不同的层。他们是分开的。

![image.FVHPG1](https://euraxluo.github.io/images/picgo/image.FVHPG1.png)

因此，如果我们以一个简单的博客为例，用户界面将使用Html, JavaScript, CSS编写，后端应用程序逻辑将运行在服务器上，如Apache &数据库将是MySQL。三层架构最适合简单的用例。



### N Tier Applications

n层应用程序是指包含三个以上组件的应用程序。

这些组成部分是什么?

- 缓存
- 异步行为的消息队列
- 负载均衡器
- 用于搜索大量数据的服务器
- 处理大量数据的组件
- 运行异构技术(通常称为web服务)的组件等。

所有像Instagram, Facebook这样的社交应用，像Uber, Airbnb这样的大型行业服务，像Pokemon Go这样的在线大型多人游戏，具有奇特功能的应用都是n层应用。

注意:n层应用程序还有另一个名称，即分布式应用程序。但是，我认为使用“分布式”这个词还不安全，因为“分布式”这个词会带来很多复杂的东西。这只会让我们感到困惑，而不是有所帮助。虽然我将在本课程中讨论分布式架构，但现在，我们将只使用术语N层应用程序。

### 为什么软件应用程序有不同的层？

解释这一点的两个软件设计原则是单一责任原则和关注点分离原则。


#### Single Responsibility Principle

单一责任原则:单一责任原则仅仅意味着给一个组件一个责任，让它完美地执行它。它可以保存数据、运行应用程序逻辑或确保消息在整个系统中的传递。

这种方法给了我们很大的灵活性，使管理更容易。例如，升级数据库服务器时。就像安装一个新的操作系统或补丁一样，它不会影响服务的其他组件的运行&即使在操作系统安装过程中发生了一些问题，只有数据库组件会宕机。应用程序作为一个整体仍然会运行&只会影响需要数据库的特性。

我们还可以为每个组件建立专门的团队和代码库，从而保持代码整洁。



单一责任原则是我从来没有存储过程的原因

存储过程使我们能够将业务逻辑添加到数据库．如果在将来我们想要插入不同的数据库怎么办？我们在哪里采取业务逻辑？到新数据库？或者我们试图重构在存储过程逻辑中的应用程序代码．



数据库不应该保存业务逻辑，它应该只负责持久化数据。这就是单一责任原则。这就是为什么我们要为不同的组件设置不同的层。

#### Separation Of Concerns

关注点分离:分离关注点的意思是一样的，只关心你的工作&不要担心其他的事情。

这些原则在服务的所有级别上发挥作用，无论是在层级还是在代码级。

将组件分开可以使它们可重用。不同的服务可以使用相同的数据库、消息传递服务器或任何组件，只要它们之间不是紧密耦合的

应该采用松散耦合的组件。当将来业务增长到一定程度时，这种方法使得扩展服务变得容易。

#### Difference Between Layers & Tiers

注意:不要将层(tiers)与应用程序的层混淆。有些人喜欢交替使用。但在应用程序的行业层中，通常指的是用户界面层(layer)、业务层、服务层或数据访问层。![image.VG7YG1](https://euraxluo.github.io/images/picgo/image.VG7YG1.png)

图中提到的层位于代码级别。层和层之间的区别是，层表示代码的组织，并将其分解为组件。然而，层(tier)涉及组件的物理分离。
