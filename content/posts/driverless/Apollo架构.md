+++
title = "Apollo无人车架构"
date = "2019-3-14"
description = "无人驾驶"
featured = false
categories = [
  "无人驾驶"
]
tags = [
  "Apollo无人驾驶"
]
images = [
]

+++



## Apollo无人车架构
以HD-map为核心
### 线控车辆，计算机和传感器通过CAN卡进行通信
### ROTS(Ubuntu+apollo kernel)

保证实时性

### Feameworf(ROS+)

1. 共享内存

- 减少传输中的数据拷贝，提高传输效率，减少传输延迟

- 有效解决一对多传输

- 共享内存减少CPU资源占用，提高机器计算能力



2. 数据兼容

- 引入了protopuf文件格式

- 可以向后兼容

- ROS深度兼容protopuf格式



3. 去中心化，减小单点故障的影响

- 使用RTPS服务发现协议

- 以域作为划分，通过rtps相互广播，实现完全P2P

- sub节点启动，组播registerNode->节点发现及建立unicast->向新加节点发送历史消息->收发双方建立连接，开始通信



### application

- planning

- control

- end-to-end driving

- human-machine

- map-engine

- localization

- preception



## REDME：

### 定位

- GPS+IMU -> Real Time Kine

- GPS+IMU+激光雷达（光探测，测距传感器）->多传感器融合

### 预测

从感知模块接受障碍物信息（位置，方向速度，加速度）

生成不同概率的预测轨迹

- 容器

存储订阅通道的输入数据（障碍物，车辆定位，车辆规划）

- 评估器

对任何给定的障碍物分别预测路径和速度，通过模型给出的路径概率来进行评估

   1).成本评估器:概率是由成本函数给出

   2).MLP评估器:用MLP模型计算概率

   3).RNN评估器:用RNN模型计算

- 预测器

生成障碍物的预测轨迹，预测规则有很多：

   1). 单行道：在公路导航模式下障碍物沿着单条车道移动。不在车道上的障碍物将被忽略。

   2). 车道顺序：障碍物沿车道移动

   3). 移动序列：障碍物沿其运动模式沿车道移动

   4). 自由运动：障碍物自由移动

   5). 区域运动：障碍物在可能的区域中移动



### 路由

根据路由请求(开始和结束位置)以及地图数据生成高级导航信息

- 依赖路由拓扑文件



### 规划

通过配置和参数规划不同的场景

apollo是车道保持，通过障碍物，通过十字路有

- planning

   1). FSM，有限状态机

   2). Planning Dispatcher,根据车辆状态和其他信息，调用合适的planner

   3). planner获取context，确定车辆意图，执行该意图所需的规划任务，并生成规划轨迹，并更新未来作业的contxt

   4)Deciders&Optimizers：实现决策和优化的无状态库。优化器优化车辆的轨迹和速度。决策者对当前场景进行分类



### 控制

基于规划和当前的汽车状态，使用不同的控制算法，控制模块可以在正常模式和导航模式下工作

- 输入：规划轨迹，车辆状态，定位和自动模式更改请求

- 输出：给底盘的控制指令



## HD Map

1. 给出道路网的精确三维表征

2. 提供语义信息，帮助决策规划器减小选择范围

3. HD-map构建过程

- data source（百度有300辆地图车）

- data peocessing，整理，分类，清洗 ->without semantic & annotation

- obj detection

- 手动验证（apollo使用软件进行地图编辑）

- map publication（使用众包，加快构建过程，大家都可以参与）

## 定位



- GNSS RTK

- 惯性导航

- LIDAR定位

- 视觉定位

- Apollo定位



### GNSS RTK



GPS是最广泛的GNSS系统，分为三个部分：



- 卫星（Satellites），在任何时间大约有30颗GPS卫星在外太空运行

- 地面上世界各地的控制站组成（Control Stations）:用于监视和控制卫星

- GPS接收器（手机，汽车，电脑，轮船等上）



这样的话GPS是有很大的误差的，距离太远，时间太长。使用实时运动定位（或RTK）



- 可信性



RTK涉及在地面上建立几个基站，每个基站都知道自己精确的“地面实况”位置，但是每个基站也通过GPS测量自己的位置，将测出来的位置与自身位置对比得出误差，再将这个误差传给接收设备，以供其调整自身位置计算。

- 不可行性



虽然在RTK的作用下，能将车辆的位置精度确定在10厘米以内，但还是存在很多问题，比如GPS信号被高楼大厦挡住了，或者受到天气影响，导致更本无法接收到信号，另外更新频率很低，大于10赫兹或者每秒更新10次 。



### 惯性导航



- 可行性



我们需要知道将测量值转换为全局坐标系，这种转换需要一个名叫陀螺仪的传感器，三轴陀螺仪的三个外部平衡环一直在旋转， 但三轴陀螺仪的旋转轴始终固定在世界坐标系中，计算车辆在坐标系中的位置是通过测量旋转轴和三个外部平衡环的相对位置来计算的。加速度计和陀螺仪是惯性测量单元（或IMU）的主要组件，IMU的主要特征在于高频更新，更新速度达到1000赫兹，所以IMU所提供的位置几乎是实时位置信息。





- 不可行性



运动误差随时间的增加而增加



*因此可以集合GPS和IMU*



### LIDAR定位



利用激光雷达可以通过点云匹配来给车给汽车进行定位，该方法来自于激光雷达传感器的检测数据与预先存在的高精度地图连续匹配，通过这种匹配可以获得汽车在高精度地图上的全球位置及行驶方向。



**匹配点运算法很多，几个常见的算法如下**



其中：**迭代最近点（或IPC）是一种方法**。



假如我们相对两次点云扫描进行匹配，对第一次扫描的每一个点我们需要找到另一次扫描中最近的匹配点，最终我们会收都许多匹配点对，将每对点距离误差相加，然后计算平均距离误差。目标是通过点云旋转和平移来最大限度地降低这一平均误差，一旦实现，就可以在传感器扫描和地图之间找到匹配，这样我们将传感器扫描得到到的位置转换成全球地图上的位置，并计算出地图上的精度位置。



其次：**滤波算法是LIDAR定位的另一种算法。**



可消除冗余信息，并在地图上找最可能的车辆位置，Apollo采用了直方图滤波算法（有时也叫误差平方和算法（或SSD））,为了利用直方滤波，我们将通过传感器扫描的点云滑过地图的每一个位置，在每个位置，我们计算扫描的点和高精度地图上对应点之间的距离误差或距离，然后对误差的平方求和，求和的数越小说明扫描结果与地图之间的匹配越好。*在该示例中，匹配最好的点显示红色，最差的点显示蓝色，绿色代表适中的点。*

最后：**卡尔曼滤波是LIDAR的另一种定位方法。**



卡尔曼滤波是一种算法，用于根据我们在过去的状态和新的传感器测量的结果预测我们当前的状态。卡尔曼滤波使用了预测更新周期，首先我们根据之前的状态以及对移动距离和方向的估计来估计和“预测”我们新的位置。



LIDAR定位的优势：稳健性



主要缺点：难以构建高精度地图，即使能够绘制也无法跟上世界瞬时变化的速度。



### 视觉定位



图像数据是收集最容易的数据，摄像头便宜且种类繁多，还易于使用，但要用摄像头来实现高精度定位是很困难的。但是可以将摄像头数据与地图和GPS结合起来，利用*概率*来判断摄像头数据与地图或者GPS等传感器采集的数据做比对，来定位车辆或者障碍物的位置。下图为利用视觉概率思维来确定树的位置。



优点：图像易于采集



缺点：缺乏三维信息和对三维地图的依赖



### Apollo定位



Apollo使用基于GPS,IMU和激光雷达等多种传感器融合的定位系统。这种融合利用了不同传感器的互补优势，提高了稳定性和准确性。Apollo定位模块依赖于IMU,GPS,激光雷达，雷达和高精度地图，这些传感器同时支持GNSS定位和LIDAR定位，GNSS定位输出速度和位置信息，LIDAR定位输出位置和行进方向信息，融合框架通过卡尔曼滤波将这些输出结合在一起，卡尔曼滤波建立在两步预测测量周期之上。



*在Apollo中，惯性导航解决方案，用于卡尔曼滤波的预测步骤，GNSS定位和LIDAR定位用于卡尔曼滤波的测量结果更新步骤。





分类器有很多种，但他们都包含类似的步骤：**



1. 首先，计算机接收类似摄像头这样的成像设备的输入，这通常被捕获为图像或一系列图像

2. 然后，通过预处理发送每个图像，预处理对每个图片进行了标准化处理，常见的预处理步骤包括



- 调整图像大小或者旋转图像

- 将图像从一个色彩空间换到另一个色彩空间，如从全彩到灰度



预处理可以帮助我们的模型更快地处理和学习图像。



1. 提取特征，特征有助于计算机理解图片，例如：将自行车和汽车区分开来的一些特征

2. 这些特征最后被输入到分类模型中，此步骤用特征来选择图像类别。



------

## 感知



### 摄像头图像



摄像头图像是最常见的计算机视觉数据，从计算机的角度来看，图像就是一张二维网格，也被称为矩阵，矩阵中的每个单元格都包含一个数字，数字图像全由像素组成，其中包括非常小的颜色和强度单位，图像中的每个像素都只是一个数值，这些数值构成了我们的图像矩阵，甚至可以改变这些像素值，我们可以通过为每一个像素值添加一个标量整数来改变图片的亮度，向右移动每个像素，也可以执行其它的许多操作。数字网格是许多图像处理技术的基础，多数颜色和形状转换都是通过对图像进行了数学运算以及逐一像素进行更改完成的。

### 彩色图像组成



彩色图像被构建为值的三维立方， 每个立方体都有长度，宽度，高度。深度为颜色通道数量，大多数图像由三种颜色组成表示，分别为红色，绿色，蓝色，这些图像被称为RGB图像，对于RGB图像深度为3，可以将其看成一个盒子，三个颜色通道看成三层。三层叠加形成了一张彩色图片。

### LIDAR图像



感知扩展到传感器，而不仅是摄像头，激光雷达传感器创建环境的点云表征，提供了难以通过摄像头获得的信息，通过对点云信息的聚类和分析，这些数据提供里足够的对象检测，跟踪和分类信息，如距离和高度，物体形状和纹理等。



激光雷达采用光线，尤其是采用激光来测量与环境中反射该光线的物体的距离，将每个激光脉冲反射回传感器所花费的时间，反射所需的时间越长，说明物体离传感器越远，激光雷达正是通过这种方式来构建世界的视觉表征。如下图检测和聚类的结果：红点代表行人，绿点代表其它车辆。



-------



### 机器学习



机器学习是使用特殊的算法来训练计算机从数据中学习的计算机科学领域，通常，这种学习结果被存放在一个叫‘模型’的数据结构中，有很多中“模型”，事实上“模型”就是一种可以用于理解和预测世界的数据结构。



应用领域：



（1）金融领域正用机器学习来对汇率和证券交易进行预测



（2）零售业用机器学习来预测需求



（3）医生甚至运用机器学习来辅助诊断



机器学习涉及使用数据和相关的真值标记来进行模型训练



**监督学习**：可能显示车辆和行人计算机的图像，以及告诉计算机哪个是哪个的标签，我们要让计算机学习如何最好地区分两类图像，这类学习也被成为监督式学习。





**无监督学习**：没有真值标记的行人和车辆图片，让计算机自行决定，哪些图片相似，哪些图片不同。在这里我们不用提供真值标记，通过分析输入数据，在这种情况下为计算机图像，计算机凭借自己学习来区别。



**半监督学习：**将监督学习和无监督学习的特点结合在一起，使用少量的标记数据和大量的为标记数据来训练模型。



**强化学习：**强化学习涉及允许模型通过尝试许多不同的方法来解决问题，然后衡量哪种方法最为成功，计算机将尝试许多种不同的解决方案，最终使其方法与环境相适应。例如：在模拟器中，强化学习智能体可以训练汽车进行右转，智能体将在初始位置启动车辆，然后进行实验性驾驶，以多种方向和速度，如果汽车实际完成了右转，智能体会提高奖励，即得分，这是针对导致成功结果的初始化操作。最初可能车辆会出现走错的结果，多学习几次之后，汽车就不会再错了。



### 反向传播算法

学习方法也被称为训练，一般由三部循环组成：

- 前馈

- 误差测定

- 反向传播



通过前馈来输出每张图片的值，误差是输出值与输入值的差距，将误差通过与前馈相反的方向传回从而更新权重，达到误差最小化的过程叫反向传播。通过这样多次循环，得出误差最小的结果。前馈一般采用梯度下降来实现，想更多了解点击下面链接。



1. [**梯度下降**](https://www.jianshu.com/p/1eddffdcf1c0)



用梯度下降，我们通过多个小步骤来实现目标。我们希望一步一步改变权重来减小误差。误差就像是山，我们希望走到山下。下山最快的路应该是最陡峭的那个方向，因此我们也应该寻找能够使误差最小化的方向。我们可以通过计算误差平方的**梯度**来找到这个方向。



**梯度**是改变率或者斜度的另一个称呼。如果你需要回顾这个概念，可以看下可汗学院对这个问题的[讲解](https://www.khanacademy.org/math/multivariable-calculus/multivariable-derivatives/gradient-and-directional-derivatives/v/gradient)。



1. [**反向传播**](https://www.jianshu.com/p/f3f3df4f9590)



如何让多层神经网络**学习**呢？首先了解如何使用梯度下降来更新权重，反向传播算法则是它的一个延伸。以一个两层神经网络为例，可以使用**链式法则**计算输入层-隐藏层间权重的误差。



要使用梯度下降法更新隐藏层的权重，需要知道各隐藏层节点的误差对最终输出的影响。每层的输出是由两层间的权重决定的，两层之间产生的误差，按权重缩放后在网络中向前传播。既然我们知道输出误差，便可以用权重来反向传播到隐藏层。



### 卷积神经网络CNN



卷积神经网络（CNN）是一种人工神经网络，对感知问题特别有效，CNN接受多维度输入，包括大多数传感器数据的二维和三维形状。



标准神经网络：将图像矩阵重塑为一个矢量，并在一大行中链接所有列，将图像“展开”为一维像素阵列。这种方法打破了图像中的空间信息



CNN可以维持图像输入的的空间信息，CNN通过过滤器连续滑过图像来收集信息，每次收集信息只对图片的一小部分区域进行分析，这被称为卷积。



例如：CNN可以识别第一个卷积层的基本边缘和颜色信息，然后通过在第一层上卷积新过滤器，CNN可以使用边缘和颜色信息来归纳更复杂的结构，如车轮，车门和挡风玻璃，而另一个卷积可以使用车轮和车门，挡风玻璃来识别整个车，最后神经网络可以使用这一高阶信息对车辆进行分类。



------



### 检测和分类



在感知任务中，首先想到的是障碍物的检测和分类，动态的障碍物，如行走的人，车，自行车等；静态的障碍物，如树木，停好的车，自行车，建筑物等；计算机首先需要知道障碍物的位置，然后进行分类，无人驾驶车载途中会探测到许多不同物体，汽车根据检测到的物体类型来确定路径和速度。



无人车是靠什么进行检测和分类？



使用检测CNN来来查找图像中的对象位置，在对图像中的对象进行定位后，我们可以将图像发给另一个CNN进行分类。也可以用一个单一的CNN结构体系对对象进行检测和分类，在单个网络体系的末端加几个不同的“头”，一个头执行检测，一个头执行分类。一个经典结构为R-CNN及其变体Fast R-CNN和 Faster R-CNN。



**论文**



- [R-CNN](https://www.cv-foundation.org/openaccess/content_cvpr_2014/papers/Girshick_Rich_Feature_Hierarchies_2014_CVPR_paper.pdf?spm=5176.100239.blogcont55892.8.pm8zm1&file=Girshick_Rich_Feature_Hierarchies_2014_CVPR_paper.pdf)

- [Fast R-CNN](https://arxiv.org/pdf/1504.08083.pdf)

- [Faster-RCNN](https://arxiv.org/pdf/1506.01497.pdf)

- [YOLO](https://arxiv.org/pdf/1506.02640.pdf)

- [SSD](https://arxiv.org/pdf/1512.02325.pdf)



### 跟踪



在检测完对象之后我们需要追踪。



追踪的意义：对每个帧中的对象进行检测并用边界框对每个对象进行标记。



跨帧追踪的好处：



（1）追踪在检测失败时是至关重要的，如果在运用检测算法时，对象被其他对象遮挡一部分，则检测算法可能会失败，追踪可以解决这一问题。





（2）追中可以保留身份，障碍物检测的输出为包含对象的边界框，但是对象没有与任何身份关联，单独使用对象检测时，计算机不知道一帧中的哪些对象与下一帧的哪些对象相对应。



追踪步骤：



- 确认身份：通过查找对象相特征似度最高的对象，将在之前一帧中检测的所有对象与之前一帧中检测到的对象进行匹配，对象具有很多特征，一些特征可能基于颜色，一些特征可能基于形状，计算机视觉算法可以计算出复杂的图像特征。

- 快速找到匹配的对象：还要考虑连续视频帧中的。两个障碍物之间的位置和速度。由于两帧之间的对象位置和速度没有太大变化，该信息可以帮助快速找到匹配的对象。



### 分割



语义分割涉及对图像的每个像素进行分类，用于尽可能详细的了解环境，并确定车辆可行驶区域。



语义分割依赖于一种特殊的CNN，全卷积神经网络（或CFN） ,FCN用卷积层来替代传统CNN的末端平坦层，使得网络中的每一层都是卷积层。故名为全卷积网络。



CFN提供了可在原始输入图像之上叠加的逐像素输出，复杂因素是大小，传统CNN输出的图片大小比输入小得多，为了进行语义分割，我们必须得到与输入同样大小的输出。



**编码和解码**，下面图片前部分叫编码，后部分叫解码，经过这样的处理使得输入尺寸与输出尺寸相等。

### Apollo感知



**Apollo软件栈可感知障碍物**，**交通信号灯和车道**



- 对三维对象检测



Apollo在高精度地图上使用感兴趣区域（ROI）来重点关注相关对象，Apollo将ROI过滤器用于点云和图像数据以缩小搜素范围并加快感知。



然后，通过检测网络馈送已过滤的点云，输出用于构建围绕对象三维边界框 。



最后，使用被称为检测跟踪关联的算法来跨时间步识别单个对象，该算法先保留在每个时间步要跟踪的对象列表，然后在下一个时间步中找到每一个对象的最佳匹配。



- 对于交通信号灯的分类



Apollo先利用高精度地图来确认前方是否有交通信号灯，如果前方有交通信号灯，高精度地图就会返回信号灯的位置，这侧重于摄像头搜索范围，在摄像头捕捉到交通信号灯的图像后，Apollo使用检测网络对图像中的灯进行定位，然后Apollo从较大图像中提取交通灯信号，Apollo将裁剪的交通灯图像提供给分类网络， 以确定灯的颜色，如果有学多灯，系统需要选择哪些灯与其车道有关。



- **YOLO网络**



Apollo使用YOLO网络来检测车道线和动态物体，其中包括车辆，卡车，骑自行车的人和行人，在经过YOLO网络检测后，在线检测模块会并入来自其它传感器的数据，对车道线进行调整，车道线最终被并入名为“虚拟车道”的单一数据结构中，同样，也通过其它传感器的数据，对YOLO检测到的动态对象进行调整，以获得每个对象的类型，位置，速度，和前进方向。虚拟通道和动态对象都被传到规划和控制模块。



------



### 传感器数据比较



**雷达与激光雷达**



雷达已经在汽车上使用很多年，在各种系统中都需要雷达，如自适应巡航控制、盲点警告、碰撞浸膏和碰撞预防系统等。尽管雷达技术已经成熟，它仍在不断进步，作用不断提升。其他传感器测量速度的方法是计算两次读数之间的差距，而雷达则通过多普勒效应来直接测量速度。多普勒效应根据对象在远离还是接近你，测量出雷达的频率变化。就像消防车警报器一样，当车辆正在远离你和驶向你时，听起来声是不一样的。多普勒效应对传感器融合至关重要。因为它可以把速度作为独立的测量参数，从而提升了融合算法的收敛速度。雷达还可以生成环境的雷达地图，进而实现定位。因为雷达波在坚硬表面会回弹。因此，它可以直接测量对象距离，无需在视线范围内也可以。雷达可以看到其他车辆底部。并发现可能会被阻挡的建筑物和对象。在车上的所有传感器中，雷达是至不容易受雨雾影响的。而且视野宽阔，可达 150 度，距离可达200 多米。与激光雷达和摄像头相比，雷达分辨率较低，尤其是在垂直方向，分辨率非常有限。分辨率低意味着来自静态物体的反射可能产生问题。例如，街道上检修孔盖或汽水罐，可能产生很高的雷达反射率，但他们并不大。我们将其称为雷达杂波。因此，当前的车载雷达通常会忽视静态物体。



激光雷达是激光探测与测量的简称，而雷达则谁无线电探测与测量的简称。雷达使用无线电波，而激光雷达则使用红激光束来确定传感器和附近对象的距离。目前的激光雷达大多使用 900 纳米光波长度的光源。但部分激光雷达使用的光波长度更长，在雨雾中性能更好。当前的激光雷达使用旋转座架发射激光，扫描周边环境。激光室脉冲式的，脉冲被对象反射，然后返回一个点云，来代表这些物体。激光雷达的空间分辨率远远高于雷达。因为激光束越聚焦，垂直方向的扫描层数量就越多，因此每层的激光雷达的密度也越高。目前，激光雷达还不能直接测量对象的速度，必须使用两次或多次扫描之间的位置差来确定。激光雷达受天气和传感器清洁程度影响也很大，因此需要保持清洁。它们块头也比其他传感器更大，因此也很难安装，除非你只想在车顶安装一个大的激光扫描器。



------



### 感知融合策略



Apollo采用雷达和激光雷达来检测障碍物，用于融合输出的算法为卡尔曼滤波，卡尔曼滤波有两步。卡尔曼算法时预测更新步骤的无限循环。



- 第一步预测状态

- 第二部为更新测量结果



两种测量结果更新步骤



- 同步更新：同步融合同时更新来自不同传感器的测量结果



- 异步更新：异步融合则逐个更新所收到的传感器测量结果



传感器融合可提高感知性能，因为各传感器相辅相成，融合也可以减少跟踪误差。



## 预测

### **预测路径目标要求：**



- 实时性要求：想要我们的算法的延时越短越好

- 准确性要求：能让无人车尽可能准确的做出决策

- 预测模块也应该能学习新的行为



### **预测的两种不同方式：**



- 基于模型的预测



例如：怎样预测左侧的车是直行还是右转？



基于模型的预测，无人车将会提供两个模型，预测车辆直行的模型和右转的模型，然后根据预测车辆的下一步来更新模型，最终确定车辆下一步的动作。



- 数据驱动的预测



数据驱动预测使用机器学习算法，通过观察结果来训练模型，一旦机器模型训练好，就可以在现实中利用此模型去做做预测。



**数据驱动预测优点**：训练数据越多训练模型效果越好



**基于模型预测优点**：比较直观，并且结合了现有的物理知识和交通法规还有人类行为多方面知识。



### **基于车道序列的预测**



为了建立车道序列，现将车道分为多个部分，每一部分覆盖了一个易于描述车辆运动的区域，我们如果要预测别的车辆运动状态，只要预测该车在此区域的转换，而不是在某一区域的具体行为。



将车辆的行为划分为一组有限的模式组合，并将这些模式组合描述物车道的系列。例如：将直行车的路径划分为一个0-1-3-7的系列。



**障碍物状态**



为了预测物体的运动，需要了解障碍物的状态，一般人是通过物体朝向，位置，速度，加速度等来预测物体将做什么？



无人车也是同样的道理，除了朝向，位置，速度，加速度外，无人车还得考虑该段车道内物体的位置。例如：预测模块会考虑从物体到车道路线段边界的纵向和横向距离，预测模块还包括前面提到的时间间隔状态信息，以便做出更准确的信息。



**预测目标车道**



前面运用车道系列将一个复杂的问题简单化了，现在是预测车辆最有可能采取的车道系列。可以通过计算每个车道系列的概率来进行选择。我们需要一个模型，将车辆状态和车道系列作为输入，该模型用于提供车辆可能采用每个车道系列的概率，我们希望我们的模型能学习新的行为，因此应该使用观测数据对模型进行经验性训练，整改记录由一系列车道段和对象相关状态组成。



### **递归神经网络或RNN**



RNN是利用时间系列数据特征的一种预测方法，利用神经网络建立多重结构递归神经网络，称做MLP单元，从数据中提取高级特征，每个MLP单元将系列的一个元素作为一个输入，并预测系列的下一个元素作为输出，为了对元素的顺序关系建立模型，在每个单元之间建立额外的连接，这意味着每个单元根据原始输入和前一单元的输出进行预测，这就是RNN的基本结构。



**RNN在目标车道预测中的应用**



Apollo为车道系列提供一个RNN模型，为相关对象状态提供另一个RNN模型，Apollo连接这两个RNN的输出并将其馈送到另一个神经网络，该神经网络会估计每个车道系列的概率，具有最高概率的车道系列，是我们预测目标车辆将遵循的系列。



为了训练这个网络，比较真值，得出误差，反向传播更新权重，从而使得模型更好，预测结果更精确。



**轨道生成**



轨道生成是预测的最后一步，一旦我们预测到物体的车道系列，我们就可以预测物体的轨迹，在任何两个点A和,B之间，物体的行进轨迹有无限种可能。



如何确定我们想要的轨迹？可以先设置条件去除大部分的轨迹路线，我们并不是逐一排除，相反，只是在数学理论上来运用这一想法，注意车辆在两点之间的位置和方位，这两个姿势表示运动模型的初始状态和最终状态，我们可以使用这两个条件来拟合一个多项式模型，在大多数情况下，这种多项式足够满足预测。RNN在目标车道预测中的应用



Apollo为车道系列提供一个RNN模型，为相关对象状态提供另一个RNN模型，Apollo连接这两个RNN的输出并将其馈送到另一个神经网络，该神经网络会估计每个车道系列的概率，具有最高概率的车道系列，是我们预测目标车辆将遵循的系列。



为了训练这个网络，比较真值，得出误差，反向传播更新权重，从而使得模型更好，预测结果更精确。



## 规划



规划中通过结合高进度地图，定位和预测来构建车辆的轨迹。



第一步：路径导航，如从A地道B地，将地图数据作为输入，并输出可行驶路径



第二步：路径规划目标：找到从地图上的A地到B地的最佳路线。



### 路由



路线规划使用三个输入：



- 地图：地图数据包括公路网和实时交通信息

- 我们当前在地图上的位置

- 我们的目的地：通常取决于车辆的乘客



### 世界地图



从地图A-B，无人驾驶通常货沿道路搜索有没有任何路径，称作搜索。Apollo也利用搜索来查找路径，但搜索算法更智能，在搜索之前将地图重新格式化成“图形”的数据结构，该图形由“节点”和“边缘”组成。



可以对从一个节点到另一节点所需要的成本进行建模，从实际中就可以得出从1-3所需成本是比1到其它节点的要少，从上图可知，蓝色的为低成本。在计算机领域里，人们已经发现许多用于从图形中搜索路径的算法，所以将地图装换为图形有利于无人驾驶车搜索路径。



### 网格世界



从初始节点开始，还需要相邻的八个节点中哪个是最有希望的最佳候选节点，对每个候选节点都要考虑两件事：



- 首先：计算候选节点到开始节点的成本；

- 然后：计算从候选节点到最后节点的成本，可以自己定义计算成本的规则，比如有交通堵塞等情况。



定义：



g:代表从初始节点到候选节点的成本



h:表示候选节点到目标节点的成本



f:表示两个值的和，值越小，表示成本越低。



### A*算法



通过g,h值相加得到的f值来确定最佳路线，如下图，最佳路线是网右转，f值最小。



从路由到轨迹



高等级地图只是规划过程的一部分，我们需要构建沿这条道路的低等级轨迹，意味找要处理地图上没有的物体，如其它车辆，行人及自行车等。如试图与调头的车辆互动。这一级别的规划称为轨迹生成。



3D轨迹



轨迹生成目的是：生成由一系列路径点所定义的轨迹，每个路径点都分配了一个时间戳和速度，让一条曲线与这些路径点拟合，生成轨迹的几何表征，移动的障碍物可能会暂时阻挡部分路段，路段的每个路径点都有一个时间戳，将时间戳与预测模块的输出结合起来，以确保车辆在通过时，路径上的每个点都未被占用。这些时间戳创建了一个三维轨迹。



评估一条轨迹



如何评估一条轨迹，采用成函数，选择成本最低的路径。轨迹成本由各种规范和处罚组成。



例如：



- 车辆偏离中心线的距离

- 可能发生碰撞

- 速度限制

- 舒适度



通过将这些成本计算成数字，最终的出最佳的路径。



车辆甚至可以在不同环境中使用不同的成本函数。



### Frenet坐标



- 笛卡尔坐标系



通常我们使用笛卡尔坐标系来描述物体的位置，但对于车辆来说，确不是最佳的选择，我们即使能够知道车辆的(x,y)坐标，我们不知道路在哪里，很难知道车辆行驶了多远，以难以确定车辆是否偏移车道中心。



- Frenet坐标系



描述了汽车相对于车道的位置，在Frenet框架中，s代表沿道路的距离，已被称为纵坐标，d表示与纵向线的位移，已被称为横坐标，在道路的每个点，横轴与纵轴都是垂直的。



纵坐标表示车辆行驶距离，横坐标表示车辆偏离中心线的距离。



### 路径速度解耦规划



路径-速度解耦规划将轨迹规划划分为两步：



- 路径规划：生成候选曲线，这是车辆可行驶的路径，我们使用成本函数对每条路径进行成本评估，该函数包含平滑，安全性，与车道中心的偏离，以及我们想要考虑的其它的任何因素。按成本对路径进行排名，并选择成本最低的路径。

- 速度规划：路径规划之后就考虑速度的规划，我们可能希望改变在该路段是的速度，我们需要选择的事与路径点相关的一系列速度，而不是单个速度，该系列称之为“速度曲线”，可以用优化功能为路径选择，受到各种限制的良好速度曲线，通过将路径曲线和速度曲线相结合，可构建车辆的行驶轨迹。



## 控制

控制的输入和输出一样？转向角，加速度和制动？



### PID控制

**P**是比例控制器

**D**是阻尼项，让控制更加稳定，较少控制器输出的变化速度

**I**是惩罚项，对累计误差进行惩罚

### 线性二次调节器

保持误差的总和和控制输入的综合，我没听懂他在说啥。。总之就是给每一项加权重，大致有控制输入项和误差项生成一个代价函数，最小化它

x^=Ax+Bu 为状态空间方程

### 模型预测控制MPC

1. 建立汽车模型

2. 使用优化器计算有限时间范围的控制输出

3. 执行第一组控制输出

4. 每个时间段单独计算当前时间段的的控制输出，避免误差



### 车辆模型



无人车可以提供的控制输入有两个，一个是刹车|油门，反映在汽车的线性加速度上，一个是方向盘，可以控制在前轮和行驶方向的夹角。



在感知和定位之后，无人车的路线规划会选择路线。而这个时候控制模块要保证无人车安全的贴近这个预计的路线（参考路线）。一般来说一个路线可以用一个三次曲线来描述。



**Slip angle**

轮胎前进方向，和轮胎轮盘平面的夹角。也可以用轮胎平面的速度和轮胎的漂移速度的反三角来表示。不同的轮胎产生的力不同。赛车胎在同样的Slip angle会产生更大的力。（赛车抓地力更强更不容易出现漂移）



**漂移率**

轮胎在自己平面上面打滑了多少。轮胎受到的力和漂移角是非线性的。另外似乎有一个最优的转向角，那个角度上面轮胎可以提供最大的力来转向，超过那个角度力会下降。另外一般轮胎的转角有30度的限制。



**越大的漂移角会产生越大的力**

轮胎不打滑的情况下，轮胎受力的方向应该是垂直于轮胎的。打滑的话，打滑那个方向也会有一个速度。摩擦力应该和速度反向。在不打滑的时候应该有一个可以提供最大转向力的夹角，打滑的时候这个夹角应该会减小。



### MPC

MPC是一个总称，有着各种各样的算法。其动态矩阵控制（DMC）是代表作。DMC采用的是系统的阶跃响应曲线，其突出的特点是解决了约束控制问题。那么是DMC是怎么解决约束的呢？在这里只给出宏观的解释，而不做详细的说明。DMC把线性规划和控制问题结合起来，用线性规划解决输出约束的问题，同时解决了静态最优的问题

