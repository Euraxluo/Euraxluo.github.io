---
title: "etcd 基本使用"
date: 2022-02-10
description: "etcd 基本使用"
featured : false
categories: ["notes"]
tags: [ "etcd" ]
images: []
---


## 连接客户端

```go
config = clientv3.Config{
    Endpoints:   []string{"127.0.0.1:2379"}, // 集群列表
    DialTimeout: 5 * time.Second,
}

// 建立一个客户端
if client, err = clientv3.New(config); err != nil {
    fmt.Println(err)
    return
}
```





## put

```go
//PUT
if putResp, err = kv.Put(context.TODO(),
                         "/prefix/keys/k1", "v1",
                         clientv3.WithPrevKV(), //请求 prev KV
                        ); err != nil {
    fmt.Println(err)
} else {
    fmt.Println("Revision:", putResp.Header.Revision)   // 操作 版本号
    fmt.Println("ClusterId:", putResp.Header.ClusterId) // 交互集群id
    fmt.Println("MemberId:", putResp.Header.MemberId)   // 交互节点
    fmt.Println("RaftTerm:", putResp.Header.RaftTerm)   //raft 任期
    if putResp.PrevKv != nil {                          // 打印value
        fmt.Println("PrevValue:", string(putResp.PrevKv.Value))
    }
}
```

## get

```go
//GET KVS
if getResp, err = kv.Get(context.TODO(),
                         "/prefix/keys/k1",
                        ); err != nil {
    fmt.Println(err)
} else {
    fmt.Println("Kvs:", getResp.Kvs) //kv列表
}

//GET Count
if getResp, err = kv.Get(context.TODO(),
                         "/prefix/keys/k1",
                         clientv3.WithCountOnly(), //请求 prev KV
                        ); err != nil {
    fmt.Println(err)
} else {
    fmt.Println("Count:", getResp.Count) //KV Count
}

//GET 以前缀开始的所有key

//1. PUT
if putResp, err = kv.Put(context.TODO(),
                         "/prefix/keys/k2", "v2",
                         clientv3.WithPrevKV(), //请求 prev KV
                        ); err != nil {
    fmt.Println(err)
} else {
    fmt.Println("Revision:", putResp.Header.Revision)   // 操作 版本号
    fmt.Println("ClusterId:", putResp.Header.ClusterId) // 交互集群id
    fmt.Println("MemberId:", putResp.Header.MemberId)   // 交互节点
    fmt.Println("RaftTerm:", putResp.Header.RaftTerm)   //raft 任期
    if putResp.PrevKv != nil {                          // 打印value
        fmt.Println("PrevValue:", string(putResp.PrevKv.Value))
    }
}

//2. GET 以前缀开始的所有key
if getResp, err = kv.Get(context.TODO(),
                         "/prefix/keys/",
                         clientv3.WithPrefix(),
                        ); err != nil {
    fmt.Println(err)
} else {
    fmt.Println("Kvs:", getResp.Kvs) //kv列表
}
```

## delete

```go
//DELETE
if delResp, err = kv.Delete(context.TODO(),
                            "/prefix/keys/k2",
                            clientv3.WithPrevKV(),
                           ); err != nil {
    fmt.Println(err)
} else {
    if len(delResp.PrevKvs) != 0 {
        for idx, kvpair := range delResp.PrevKvs {
            fmt.Println("idx", idx, "kvpair", string(kvpair.Value), string(kvpair.Value)) //kv列表
        }
    }
}

//DELETE 多个

//1. PUT
if putResp, err = kv.Put(context.TODO(),
                         "/prefix/keys/k3", "v2",
                         clientv3.WithPrevKV(), //请求 prev KV
                        ); err != nil {
    fmt.Println(err)
} else {
    fmt.Println("Revision:", putResp.Header.Revision)   // 操作 版本号
    fmt.Println("ClusterId:", putResp.Header.ClusterId) // 交互集群id
    fmt.Println("MemberId:", putResp.Header.MemberId)   // 交互节点
    fmt.Println("RaftTerm:", putResp.Header.RaftTerm)   //raft 任期
    if putResp.PrevKv != nil {                          // 打印value
        fmt.Println("PrevValue:", string(putResp.PrevKv.Value))
    }
}

//2. delete
if delResp, err = kv.Delete(context.TODO(),
                            "/prefix/keys/",
                            clientv3.WithPrefix(),
                            clientv3.WithPrevKV(),
                           ); err != nil {
    fmt.Println(err)
} else {
    if len(delResp.PrevKvs) != 0 {
        for idx, kvpair := range delResp.PrevKvs {
            fmt.Println("idx", idx, "kvpair", string(kvpair.Value), string(kvpair.Value)) //kv列表
        }
    }
}
```

## lease租约

```go
var (
    lease          clientv3.Lease
    leaseGrantResp *clientv3.LeaseGrantResponse
    leaseId        clientv3.LeaseID
    keepAliveResp  *clientv3.LeaseKeepAliveResponse
    keepAliveChan  <-chan *clientv3.LeaseKeepAliveResponse
)
//lease
lease = clientv3.NewLease(client)

//1. 申请租约
if leaseGrantResp, err = lease.Grant(context.TODO(), 1); err != nil {
    fmt.Println(err)
} else {
    //2.获取租约ID
    leaseId = leaseGrantResp.ID

    //3. 自动续租
    //3.1 构造5秒过期取消的上下文
    ctx, _ := context.WithTimeout(context.TODO(), 5*time.Second)
    if keepAliveChan, err = lease.KeepAlive(ctx, leaseId); err != nil {
        fmt.Println(err)
    } else {
        // 3.2 通过keepalive返回的只读管道，获取续约时向管道返回的信息
        go func() {
            for {
                select {
                    case keepAliveResp = <-keepAliveChan:
                    if keepAliveResp == nil {
                        fmt.Println("租约失效")
                        goto END
                    } else { // 每秒会续租一次
                        fmt.Println("自动续租应答", keepAliveResp.ID)
                    }
                }
            }
            END:
        }()
    }

    //4. 获取KV对象
    kv = clientv3.NewKV(client)

    //5.PUT,并，将该put的值绑定一个租约
    if putResp, err = kv.Put(context.TODO(),
                             "/prefix/keys/k1", "",
                             clientv3.WithLease(leaseId), //绑定租约
                            ); err != nil {
        fmt.Println(err)
    } else {
        fmt.Println("Revision:", putResp.Header.Revision)   // 操作 版本号
        fmt.Println("ClusterId:", putResp.Header.ClusterId) // 交互集群id
        fmt.Println("MemberId:", putResp.Header.MemberId)   // 交互节点s
        fmt.Println("RaftTerm:", putResp.Header.RaftTerm)   //raft 任期
    }

    //6.定时查看key是否过期
    for {
        if getResp, err = kv.Get(context.TODO(),
                                 "/prefix/keys/k1",
                                ); err != nil {
            fmt.Println(err)
        } else {
            if getResp.Count == 0 {
                fmt.Println("过期了")
                break
            } else {
                fmt.Println("Kvs:", getResp.Kvs) //kv列表
            }

        }
    }
}
```

## watch 监听

```go
//watch
var (
    watcher       clientv3.Watcher
    watchRespChan clientv3.WatchChan
)

//1. 初始化监听上下文，当kv变化10次是，取消该上下文
watcherCtx, cancelFunc := context.WithCancel(context.TODO())

//2. 监听kv变化
go func() {
    i := 0
    for {
        i += 1
        kv.Put(context.TODO(), "/prefix/keys/k1", "v"+strconv.Itoa(i))
        kv.Delete(context.TODO(), "/prefix/keys/k1")
        time.Sleep(1 * time.Second)
        if i > 10 {
            println("变化结束，取消监听")
            cancelFunc()
            break
        }
    }
}()

//3. 先获取到当前的值，并进行监听
if getResp, err = kv.Get(context.TODO(), "/prefix/keys/k1"); err != nil {
    fmt.Println(err)
} else {
    if len(getResp.Kvs) != 0 {
        fmt.Println(string(getResp.Kvs[0].Value))
    }

    //3.1 定义需要监听的reversion
    watchStartRevision := getResp.Header.Revision + 1
    println("watchStartRevision", watchStartRevision)

    //3.2 创建一个watcher
    watcher = clientv3.NewWatcher(client)

    //3.3 启动监听
    watchRespChan = watcher.Watch(watcherCtx,
                                  "/prefix/keys/k1",
                                  clientv3.WithRev(watchStartRevision), //监听Revision起点
                                 )
    //3.4 处理kv变化
    for watchResp := range watchRespChan {
        for _, event := range watchResp.Events {
            switch event.Type {
                case mvccpb.PUT:
                fmt.Println("修改为", string(event.Kv.Value), "Revison", event.Kv.CreateRevision, event.Kv.ModRevision)
                case mvccpb.DELETE:
                fmt.Println("删除了", event.Kv.ModRevision)
            }
        }
    }
}
```

## 分布式锁

```go
package main

import (
	"context"
	"fmt"
	"github.com/coreos/etcd/clientv3"
	"time"
)

type HandlerFunc func() error
type LockError string

func (err LockError) Error() string {
	return string(err)
}

func Lock(endpoint []string, dialTimeout time.Duration, lockKey string, lockValue string, callback HandlerFunc) (err error) {
	var (
		client            *clientv3.Client
		leaseGrantResp    *clientv3.LeaseGrantResponse
		keepAliveRespChan <-chan *clientv3.LeaseKeepAliveResponse
		txnResp           *clientv3.TxnResponse
	)

	config := clientv3.Config{
		Endpoints:   endpoint,
		DialTimeout: dialTimeout,
	}
	if client, err = clientv3.New(config); err != nil {
		return err
	}

	//1. 上锁
	//1.1 创建租约
	lease := clientv3.NewLease(client)
	//1.2 设置租期
	leaseCtx, _ := context.WithTimeout(context.TODO(), 1*time.Second)
	if leaseGrantResp, err = lease.Grant(leaseCtx, 1); err != nil {
		return err
	}
	//1.3 获取租约id
	leaseId := leaseGrantResp.ID
	leaseRevokeCtx, _ := context.WithTimeout(context.TODO(), 1*time.Second)
	defer lease.Revoke(leaseRevokeCtx, leaseId) // 函数退出时，直接结束租约

	//1.4 准备一个用于取消租约的上下文
	cancelCtx, cancelFunc := context.WithCancel(context.TODO())
	defer cancelFunc() //退出函数后，关闭租约，此时，会导致租约监听协程退出

	//1.5 在函数退出之前持续续租
	if keepAliveRespChan, err = lease.KeepAlive(cancelCtx, leaseId); err != nil {
		return err
	}

	//1.6 启动处理续约的协程
	go func() {
		for {
			select {
			case keepAliveResp := <-keepAliveRespChan:
				if keepAliveResp == nil {
					goto KeepAliveListenEnd
				} else {
					println(keepAliveResp.ID)
				}
			}
		}
	KeepAliveListenEnd:
	}()

	//1.7 创建事务
	kv := clientv3.NewKV(client)
	txnCtx, _ := context.WithTimeout(context.TODO(), 1*time.Second)
	txn := kv.Txn(txnCtx)
	txn.If(clientv3.Compare(clientv3.CreateRevision(lockKey), "=", 0)). //如果 key 不存在
		Then(clientv3.OpPut(lockKey, lockValue, clientv3.WithLease(leaseId))). //上锁
		Else(clientv3.OpGet(locValue)) //否则抢锁失败
	//1.8 提交事务，并判断是否成功
	if txnResp, err = txn.Commit(); err != nil {
		return err
	}

	//如果失败，则锁被占用
	if !txnResp.Succeeded {
		return LockError("Lock Failed")
	}
	//否则上锁成功
	return callback()

}

func handler() error {
	fmt.Println("处理任务")
	time.Sleep(5 * time.Second)
	return nil
}

func main() {
	err := Lock([]string{"127.0.0.1:2379"}, 1*time.Second, "/prefix/lock/lock_key", "lock_value", handler)
	println(err)
	if err != nil {
		fmt.Println(err)
	}
}

```



