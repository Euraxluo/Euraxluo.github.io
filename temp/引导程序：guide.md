引导程序：guide

1. 加载配置
2. iocfactory？类注入
3. 日志系统
4. 路由控制
5. 注解解析？



首先需要根据后台的注解，生成route树，前台请求来了后，解析路由，获取最匹配的路径，并实例化对应的类

自动全局分析注解，对标了路由注解的类和方法进行解析

//存入树中？



存入缓存中，以及路由树中，路由树用于匹配请求路由，具有一定的匹配规则（是否可自定义路由规则）

route{

/lg=>{

ctrl=>app\ctrls\indexCtrl

action=>login()

type=>get

}



/home/test=>app\ctrls\testCtrl::test() =>post

}

1. 初始化，存入缓存，不设过期时间