---
layout:     post                    # 使用的布局（不需要改）
title:      数据库               # 标题
subtitle:   RedisCluster02                #副标题
date:       2019-03-14           # 时间
author:     Euraxluo                      # 作者
header-img: img/post-bg-github-cup.jpg  #这篇文章标题背景图片
catalog: true                 # 是否归档
tags:                               #标签
    - Redis

---
## 集群伸缩
### 伸缩原理
伸：增加节点
缩：节点下线
集群伸缩：槽和数据在节点之间的移动
### 扩容集群
1. 准备新节点
- 打开集群模式
- 配置和其他节点统一
- 启动后是孤立的节点
2. 加入集群meet
- 在集群节点中配置：`cluster meet 127.1 <newnodeport>`

- 使用redis-trib.rb：
`redis-trib.rb ad-node new_host:new_port existing_host:existing_port --slave --master_id <arg>{扩展参数是配置为从节点}`

- 为它迁移槽和数据可以实现扩容
- 可以作为从节点负责故障转移
3. 迁移槽和数据
- 1). 对目标节点发送`cluster setslot <slot> importing <sourceNodeId>`,让目标节点准备导入槽的数据

- 2). 对源节点发送`cluster setslot <slot> migrating <targetNodeId>`,让源节点准备迁出槽

- 3). 源节点循环执行`cluster getkeysinslot <slot> <count>`,每次获取count个属于槽的键

- 4). 在源节点上执行`migrate <targetIp> <targetPort> key 0{对应数据库，master只有db0} <timeout>`,死循环，知道所有的key迁移完成

- 5). 重复执行3)~4)知道槽下所有的key迁移到目标节点
- 6). 向集群中的所有主节点发送`cluster setslot <slot> node <targetNode	Id>`,通知槽已经重新分配给目标节点 
- 伪代码：
```python
def move_slot(source,target,slot):
	#目标节点准备导入槽
	target.cluster("setslot",slot,"importing",source,nodeID);
	#源节点准备导出槽
	source.cluster("setslot",slot,"migrating",target,nodeId);
	while true:
		#批量从源节点获取key
		keys = source.cluster("getkeysinslot",slot,pipeline_size)
		if keys.length == 0
			#键列表为空，退出循环
			break
	#批量迁移key到目标节点
	source.call("migrate",target.host,target.port,"",0,timeout,"keys",[keys])
	#向集群所有主节点通知槽slot被分配给目标节点
	for node in nodes:
		if node.flag == "slave":
			continue
		node.cluster("setslot",slot,"node",target.nodeId)
```
- 在集群中添加两个节点7006，7007，7007 slaveof 7006

```bash
#生成配置
sed 's/7000/7006/g' redis-7000.conf > redis-7006.conf
sed 's/7000/7007/g' redis-7000.conf > redis-7007.conf
#启动孤立节点
redis-server redis-7006.conf
redis-server redis-7007.conf
#加入集群
redis-cli -p 7000 cluster meet 127.1 7006
redis-cli -p 7000 cluster meet 127.1 7007
#配置主从
redis-cli -p 7007 cluster replicate <7006.nodeId>
#reshard
redis-trib.rb reshard 127.1:7000
#输入迁移槽个数
#输入目标节点Id
#选择all或者done，确定源node
#是否继续

#查看分配的slot的结果
redis-cli -p 7000 cluster nodes |grep master
```

### 缩容集群
1. 下线迁移槽
- 下线7006，7007

```bash
#添加节点时，7006从三个node上获取槽，因此槽分为三段

#迁移槽
redis-trib.rb reshard --from <7006.nodeId> --to <7000.nodeId> --slots <slotsNums> <127.1:7006>{在哪一个端口执行}
#同意迁移计划

redis-trib.rb reshard --from <7006.nodeId> --to <7001.nodeId> --slots <slotsNums> <127.1:7006>{在哪一个端口执行}
#同意迁移计划

redis-trib.rb reshard --from <7006.nodeId> --to <7002.nodeId> --slots <slotsNums> <127.1:7006>{在哪一个端口执行}
#同意迁移计划
```
2. 忘记节点
- 忘记7006，7007

```bash
#忘记节点,先下线从节点
redis-trib.rb del-node 127.1:7000 <7007.nodeId>

#忘记节点,再下线主节点
redis-trib.rb del-node 127.1:7000 <7006.nodeId>
```