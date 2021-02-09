stream 编程
```java
import java.util.function.Consumer;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;      


		Consumer<String> P = System.out::println;//消费者
//        P.andThen(P.andThen(P)).accept(2);

        /**
         * 流的创建
         */
        List<String> list = new ArrayList<>();
        //从集合创建流
        list.stream();
        list.parallelStream();

        //从数组创建
        Arrays.stream(new int[]{2,3,5});
//        P.accept(Arrays.stream(new int[]{2,3,5}).map(x->x+1).sum());

        //创建数字流
        IntStream.of(1,2,3);
        IntStream.rangeClosed(1,10);

        //从random创建一个无限流
        new Random().ints().limit(10);

        //自己产生流
        Stream.generate(()->new Random().nextInt()).limit(20);
//        P.accept(Stream.generate(()->new Random().nextInt()).limit(20).findAny().toString());


        /**
         * 中间操作
         */
        //filter操作
        Stream.of(msg.split(" ")).filter(s->s.length()>1).forEach(P);

        //flatMap :将流中的属性提取出来作为流
        //这里需要装箱,s.chars()返回IntStream,不是Stream的子类
        Stream.of(msg.split(" ")).flatMap(s->s.chars().boxed()).forEach(i->System.out.println((char)i.intValue()));

        //limit
        new Random().ints().filter(x->x>10&&x<1000).limit(10).forEach(System.out::println);

        //peek,用于debug
        Stream.of(msg.split(" ")).peek(System.out::println).forEach(P);

        /**
         * 终止操作
         */
        P.accept("----终止操作----");
        //foreach Order 用于在并行流中排序
        Stream.of(msg.split(" ")).parallel().forEach(P);
        Stream.of(msg.split(" ")).parallel().forEachOrdered(P);


        //收集器
        List<String> slist = Stream.of(msg.split(" ")).collect(Collectors.toList());
        System.out.println(slist);

        //reduce 有个初始值 .orElse(""):空判断
        String s =  Stream.of(msg.split(" ")).reduce("",(s1,s2)->s1+"|"+s2);
//        计算所有单词总长度
        Integer reduce = Stream.of(msg.split(" ")).map(x -> x.length()).reduce(0, (x1, x2) -> x1 + x2);
        P.accept(s);
        P.accept(reduce.toString());


        //max
        Optional<String> max = Stream.of(msg.split(" ")).max((x1, x2) -> x1.length() - x2.length());
        P.accept(max.get());
```



## 异步Servlet

异步是针对后端来说,这样可以让我们后端提高吞吐量



```java
@WebServlet(asyncSupported = true,urlPatterns = {"/AsyncServlet"})
public class AsyncServlet extends HttpServlet{
    protected void doGet(HttpServletRequest req,HttpServletResponse res){
        //开启异步
        AsyncContext asyncCtx = req.startAAsync();
        
        //使用线程
        CompletableFuture.runAsync(()->doing(asyncCtx,asyncCtx.getRequest(),asyncCtx.getResponse());
                             
    }
  	private void doing(AsyncContext asyncCtx,HttpServletRequest req,HttpServletResponse res){
        //异步线程中会进行一些耗时操作
        TimeUmtil.SECONDS.sleep(5);
        res.getWriter().append("done");
        //业务处理完毕,通知线程结束
        asyncCtx.complete();
        
    }
}
```

## reactor = jdk8 stream + jdk9 reactor stream

```
@RestController
@Slf4j
public class TestController {

    @GetMapping("/1")
    private String get1(){
        log.info("get1 start");
        String res = createStr();
        log.info("get1 end");
        return "getMapping";
    }

    private String createStr() {
        //睡5秒
        try {
            TimeUnit.SECONDS.sleep(5);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return "createStr";
    }

    @GetMapping("/2")
    private Mono<String> get2(){
        log.info("get2 start");
        Mono<String> res = Mono.fromSupplier(()->createStr());
        log.info("get2 end");
        return res;
    }


}
```

