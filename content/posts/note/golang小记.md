---
title: "go语言小记"
date: "2021-02-19"
description: "go学习"
featured : false
categories: ["note"]
tags: [ "go" ]
images: []
---

### 关于切片和slice的内存共享

```go
package main

import (
	"bufio"
	"bytes"
	"errors"
	"fmt"
	_errors "github.com/pkg/errors"
	"os"
	"reflect"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

func main() {
	/**
	 * @Description: foo boo内存共享
	 * @param []int
	 * @param 5
	 */
	foo := make([]int, 5)
	foo[3] = 3
	foo[4] = 4

	boo := foo[1:4]
	boo[1] = 2
	for i := 0; i < 5; i++ {
		println(foo[i])
	}

	/**
	 * @Description: 当capcity够的时候，那么就不会重新分配内存
	 * @param []int
	 * @param 8
	 */
	a := make([]int, 8)
	b := a[1:8]
	b[1] = 1         //[01...],a=[001]
	a[2] = 2         //[002...]
	a = append(a, 1) //新内存空间
	b[1] = 3         //b=[03...],a=[002]
	a[2] = 4         //a=[004]
	for i := 0; i < len(a); i++ {
		print(a[i])
	}
	println()
	for i := 0; i < len(b); i++ {
		print(b[i])
	}

	/**
	     * @Description: dir1和dir2 共享内存，虽然dir1有个append，
		 * 但是由于空间足够，所以没有重新申请空间
		 *
	*/
	println()
	path := []byte("AAAAAA/BBBBBB")
	sep := bytes.IndexByte(path, '/')
	//dir1:=path[:sep]
	dir1 := path[:sep:sep] //todo 这个语法设置了最小的cap，后续append，就会重新分配内存
	dir2 := path[sep+1:]
	println(string(dir1))
	println(string(dir2))
	dir1 = append(dir1, "/suffix"...)
	println(string(dir1))
	println(string(dir2))

	/**
	 * @Description:深度比较 deepEqual
	 */
	v1 := data{}
	v2 := data{}
	println(reflect.DeepEqual(v1, v2))

	m1 := map[string]string{"1": "a", "2": "b"}
	m2 := map[string]string{"2": "b", "1": "a"}
	println(reflect.DeepEqual(m1, m2))

	s1 := []int{1, 2, 3}
	s2 := []int{2, 3, 4}
	println(reflect.DeepEqual(s1, s2))

	/**
	 * @Description: 成员函数Receiver
	 */

	p := Persion{
		Name: "Euraxluo",
		Sex:  "Male",
		Age:  44,
	}
	p.printPersion()

	/**
	 * @Description:面向接口编程
	 */
	c := Country{"CHINA"}
	city := City{"shanghai"}
	printStr(c)
	printStr(city)

	/**
	 * @Description: 时间处理
	 */
	//now time
	now := time.Now()
	fmt.Println(now)
	str_now := time.Now().String()
	fmt.Println(str_now)

	//Unix timestamp
	unix_now := time.Now().Unix()
	fmt.Println(unix_now)
	//获取日期
	date_time := time.Now().Day()
	fmt.Println(date_time)
	//获取年份
	year := time.Now().Year()
	fmt.Println(year)
	//获取月份
	month := time.Now().Month()
	fmt.Println(month)

	//数字转字符串
	x := strconv.Itoa(32131)
	println(x)

	//避免把String转成[]Byte
	//如果需要在for循环中对某个slice使用append()，先把slice的容量整到位，避免浪费内存

	//拼接字符串 使用stringBuffer,StringBuild
	//plus 符号适合用于字面常量的拼接。编译器会直接进行优化
	//StringBuild 通过合理的内存预分配，可以减少拼接时，内存的分配次数，减少GC次数
	str_list := []string{"你好", "世界"}
	s_build := StringBuilder(str_list, 20)
	println(s_build)
	//已有字符串的情况下，使用 strings.join比较好
	s_join := strings.Join(str_list, "")
	println(s_join)
	//![](https://www.flysnow.org/2018/11/11/golang-concat-strings-performance-analysis.html)

	//使用gorouting并发，使用sync.WaitGroup同步分片
	//var wgs sync.WaitGroup
	wgs := new(sync.WaitGroup)
	for i := 0; i < 10; i++ {
		wgs.Add(1) //todo add 1
		//go download("test.com", i,&wgs)
		go download("test.com", i, wgs)
	}
	wgs.Wait()

	//避免在热代码中进行内存分配，这样会导致gc繁忙，使用sync.Pool来重用对象
	//![](https://zhuanlan.zhihu.com/p/76812714)
	//![](https://www.cnblogs.com/sunsky303/p/9706210.html)
	/**
	    * @Description: sync.Pool  的使用场景：
		× 1.最好是高并发
		× 2.最好两次GC之间的间隔长
	*/
	time1 := time.Now().Unix()
	for i := 0; i < 900000; i++ {
		obj := make([]byte, 1024)
		_ = obj
	}
	time2 := time.Now().Unix()
	for j := 0; j < 900000; j++ {
		obj := bytePool.Get().(*[]byte)
		_ = obj
		bytePool.Put(obj)
	}
	time3 := time.Now().Unix()
	println(time2 - time1)
	println("SYNC POOL", time3-time2)

	//使用lock-free操作，避免使用mutex,应该使用sync/Atomic包
	//lock free编程 https://www.cnblogs.com/gaochundong/p/lock_free_programming.html
	//todo https://coolshell.cn/articles/9703.html
	//todo https://coolshell.cn/articles/8239.html
	//提供原子操作
	//加法(add), 比较并交换(compare and swap, 简称CAS)，加载(load), 存储(store),交换(swap)
	var l uint32 = 10
	atomic_plus(&l, 10)
	fmt.Println(l)
	atomic_sub(&l, 5)
	fmt.Println(l)

	//使用I/O缓存，使用bufio.NewWrite()，bufio.NewReader()
	readBuffer()
	writeBuffer()

	//在for循环中使用正则，要使用regexp.Compile()编译正则，性能更高
	for i := 0; i < 10; i++ {
		x := re_compile("hello World", `\w+`)
		println(x)
	}

	//如果需要高性能，使用protobuf,msgp

	//使用Map时，使用整形的Key更快
	//todo https://golang.org/doc/effective_go.html
	//todo https://github.com/uber-go/guide/blob/master/style.md
	//todo http://devs.cloudimmunity.com/gotchas-and-common-mistakes-in-go-golang/
	//todo https://github.com/cristaloleg/go-advice
	//todo https://www.instana.com/blog/practical-golang-benchmarks/
	//todo https://github.com/alecthomas/go_serialization_benchmarks
	//todo https://github.com/golang/go/wiki/Performance

	//2.错误处理
	//一段代码的改进

	testa := []int{1, 2, 3, 4, 5}
	testb := []int{1, 2, 3, 4, 5}
	testc := Compares{
		V1: 2,
		V2: 2,
		V3: 2,
		V4: 2,
		V5: 4,
	}
	if err := testc.exception_handler4(testa, testb); err != nil {
		println(err.Error())
	} else {
		println("check pass")
	}

	//3.选项模式
	//建造者模式
	sb := OptionBuilder{}
	if option, err := sb.Create("127.0.0.1", "8080").WithOption3(1).WithOption4(1.1).Build(); err == nil {
		option.printOpt()
	}
	//选项模式
	op1, _ := NewSetting(Option1("localhost"), Option2("1023"))
	op1.printOpt()

	//4.嵌入和委托
	//嵌入结构多态
	button1 := Button{Label{Widget{10, 70}, "OK"}}
	button2 := Button{Label{Widget{50, 70}, "NO"}}
	listBox := ListBox{Widget{10, 40},
		[]string{"AL", "AK", "AZ", "AR"}, 0}
	println("Painters")
	for _, painter := range []Painter{listBox, button1, button2} {
		painter.Paint()
	}
	println("Painters2")
	for _, widget := range []interface{}{listBox, button1, button2} {
		widget.(Painter).Paint()
		if clicker, ok := widget.(Clicker); ok {
			clicker.Click()
		}
		fmt.Println() // print a empty line
	}

	//控制反转
	//控制逻辑依赖业务逻辑：
	intSet := NewIntSet()
	intSet.Add(1)
	intSet.Add(2)
	intSet.Add(3)
	intSet.Delete(3)
	println("intSet")
	for k, v := range intSet.data {
		fmt.Println(k, v)
	}

	undoSet := NewUndoSet()
	undoSet.Add(1)
	undoSet.Add(2)
	undoSet.Add(3)
	undoSet.Delete(3)
	undoSet.Undo()
	println("undoSet")
	for k, v := range undoSet.data {
		fmt.Println(k, v)
	}

	strSet := NewStrSet()
	strSet.Add("1")
	strSet.Add("2")
	strSet.Add("3")
	strSet.Delete("3")
	strSet.Undo()
	println("strSet")
	for k, v := range strSet.data {
		fmt.Println(k, v)
	}

	//5.1map
	list := []string{"Euraxluo", "Hello", "World"}
	var mapres []interface{}
	mapres = Map(list, func(s interface{}) interface{} {
		return strings.ToUpper(reflect.ValueOf(s).String())
	})
	for k, v := range mapres {
		fmt.Println(k, v)
	}
	mapres = Map(list, func(s interface{}) interface{} {
		return len(reflect.ValueOf(s).String())
	})

	for k, v := range mapres {
		fmt.Println(k, v)
	}
	reduceres := Reduce(list, func(s interface{}) interface{} {
		return len(reflect.ValueOf(s).String())
	})
	println(reduceres.(int64))

	reduceress := Reduce(list, func(s interface{}) interface{} {
		return reflect.ValueOf(s).String() + " "
	})
	println(reduceress.(string))

	var int_set = []int{1, 2, 3, 4, 5, 6, 7, 87, 8}
	out := Filter(int_set, func(s interface{}) bool {
		return reflect.ValueOf(s).Int()%2 == 1
	})

	for k, v := range out {
		fmt.Println(k, v)
	}

}

/**
 * @Description:  通用的map函数
 * @param arr
 * @param fn
 * @return []interface{}
 */
func Map(arr interface{}, fn func(s interface{}) interface{}) []interface{} {
	if reflect.ValueOf(arr).Kind() != reflect.Slice {
		return nil
	}
	var newArr []interface{}
	for i := 0; i < reflect.ValueOf(arr).Len(); i++ {
		newArr = append(newArr, fn(reflect.ValueOf(arr).Index(i).Interface()))
	}
	return newArr
}
/**
 * @Description: 通用的reduce函数
 * @param arr
 * @param fn
 * @return interface{}
 */
func Reduce(arr interface{}, fn func(s interface{}) interface{}) interface{} {
	if reflect.ValueOf(arr).Kind() != reflect.Slice {
		return nil
	}
	var sum interface{}

	for i := 0; i < reflect.ValueOf(arr).Len(); i++ {
		res := fn(reflect.ValueOf(arr).Index(i).Interface())
		if sum == nil {
			psum := reflect.Indirect(reflect.ValueOf(sum))
			if psum.CanSet() {
				psum.Set(reflect.ValueOf(res))
			} else {
				sum = res
			}
		} else {
			switch reflect.ValueOf(sum).Kind() {
			case reflect.Interface:
				return nil
			case reflect.Int:
				sum = reflect.ValueOf(sum).Int() + reflect.ValueOf(res).Int()
			case reflect.String:
				sum = reflect.ValueOf(sum).String() + reflect.ValueOf(res).String()
			case reflect.Ptr:
				sum = reflect.ValueOf(sum).Pointer() + reflect.ValueOf(res).Pointer()
			}
		}
	}
	return sum
}
/**
 * @Description: 通用的filter函数
 * @param arr
 * @param fn
 * @return []interface{}
 */
func Filter(arr interface{}, fn func(s interface{}) bool) []interface{} {
	if reflect.ValueOf(arr).Kind() != reflect.Slice {
		return nil
	}
	var newArr []interface{}
	for i := 0; i < reflect.ValueOf(arr).Len(); i++ {
		if fn(reflect.ValueOf(arr).Index(i).Interface()) == true {
			newArr = append(newArr, reflect.ValueOf(arr).Index(i).Interface())
		}
	}
	return newArr
}

/**
 * @Description: 控制功能Undo依赖业务功能
 */
type IntSet struct {
	data map[int]bool
}

func NewIntSet() IntSet {
	return IntSet{make(map[int]bool)}
}
func (set *IntSet) Add(x int) {
	set.data[x] = true
}
func (set *IntSet) Delete(x int) {
	delete(set.data, x)
}
func (set *IntSet) Contains(x int) bool {
	return set.data[x]
}

type UndoSet struct {
	IntSet
	functions []func()
}

func NewUndoSet() UndoSet {
	return UndoSet{NewIntSet(), nil}
}
func (set *UndoSet) Add(x int) { //重写
	if !set.Contains(x) {
		set.data[x] = true
		set.functions = append(set.functions, func() {
			set.Delete(x)
		})
	} else {
		set.functions = append(set.functions, nil)
	}
}
func (set *UndoSet) Delete(x int) { //重写
	if set.Contains(x) {
		delete(set.data, x)
		set.functions = append(set.functions, func() {
			set.Add(x)
		})
	} else {
		set.functions = append(set.functions, nil)
	}
}

func (set *UndoSet) Undo() error {
	if len(set.functions) == 0 {
		return errors.New("No functions to undo")
	}
	index := len(set.functions) - 1
	if function := set.functions[index]; function != nil {
		function()
		set.functions[index] = nil
	}
	set.functions = set.functions[:index]
	return nil
}

/**
 * @Description: 定义协议
 */
type UndoIOC []func()

func (undo *UndoIOC) Add(function func()) {
	*undo = append(*undo, function)
}

func (undo *UndoIOC) UndoIOC() error {
	functions := *undo
	if len(functions) == 0 {
		return errors.New("No functions to Undo")
	}
	index := len(functions) - 1
	if function := functions[index]; function != nil {
		function()
		functions[index] = nil
	}
	*undo = functions[:index]
	return nil
}

/**
 * @Description: 控制反转，将业务逻辑依赖控制逻辑。
 * 应该是这样 服务想实现什么控制协议，由服务决定，控制能通用
 */
type StrSet struct {
	data map[string]bool
	undo UndoIOC
}

func NewStrSet() StrSet {
	return StrSet{data: make(map[string]bool)}
}
func (set *StrSet) Undo() {
	set.undo.UndoIOC()
}
func (set *StrSet) Add(x string) {
	if !set.Contains(x) {
		set.data[x] = true
		set.undo.Add(func() {
			set.Delete(x)
		})
	} else {
		set.undo.Add(nil)
	}
}
func (set *StrSet) Delete(x string) {
	if set.Contains(x) {
		delete(set.data, x)
		set.undo.Add(func() {
			set.Add(x)
		})
	} else {
		set.undo.Add(nil)
	}
}
func (set *StrSet) Contains(x string) bool {
	return set.data[x]
}

type Painter interface {
	Paint()
}
type Clicker interface {
	Click()
}
type Widget struct {
	X, Y int
}
type Label struct {
	Widget        //嵌入
	Text   string //聚合
}

func (label Label) Paint() {
	println("Paint", &label, label.Text)
}

type Button struct {
	Label
}

func (button Button) Paint() {
	println("Paint", &button, button.Text)
}

func (button Button) Click() {
	println("Click", &button, button.Text)
}

type ListBox struct {
	Widget
	Texts []string
	Index int
}

func (listBox ListBox) Paint() {
	println("Paint", &listBox, listBox.Texts)
}

func (listBox ListBox) Click() {
	println("Click", &listBox, listBox.Texts)
}

/**
 * @Description: 选项模式
 */

type Option struct {
	option1 string
	option2 string
	option3 int
	option4 float64
}

func (p *Option) printOpt() {
	println(p.option1, p.option2, p.option3, p.option4)
}

/**
 * @Description:  第一种最复杂，最臃肿的方式进行设置
 * @param option1
 * @param option2
 * @return *Option
 * @return error
 */
func newDefaultOption(option1 string, option2 string) (*Option, error) {
	return &Option{option1, option2, 1, 1.0}, nil
}

func new2Option(option1 string, option2 string, option3 int) (*Option, error) {
	return &Option{option1, option2, option3, 1.0}, nil
}

func new3Option(option1 string, option2 string, option4 float64) (*Option, error) {
	return &Option{option1, option2, 1, option4}, nil
}

func new4Option(option1 string, option2 string, option3 int, option4 float64) (*Option, error) {
	return &Option{option1, option2, option3, option4}, nil
}

/**
 * @Description: 第二种，使用两个结构体，一个传固定参数，一个传可选参数
 */
type Config struct {
	option1 string
	option2 string
	configs *Configs
}
type Configs struct {
	option3 int
	option4 float64
}

func NewConfig(option1 string, option2 string, configs *Configs) (*Config, error) {
	return &Config{option1, option2, configs}, nil
}

/**
 * @Description: 第三种，使用builder建造者模式
 */
type OptionBuilder struct {
	Option
	err error
}

/**
 * @Description: 显式的将interface声明为Void
 */
type Void interface{}

/**
 * @Description: 实现一个指针赋值的函数
 * @param void
 * @param value
 */
func SetValue(void Void, value interface{}) {
	pvoid := reflect.Indirect(reflect.ValueOf(void))
	pvoid.Set(reflect.ValueOf(value))
}

func (b *OptionBuilder) setOption(option Void, value interface{}) {
	if b.err == nil {
		SetValue(option, value)
	}
}
func (b *OptionBuilder) Create(option1 string, option2 string) *OptionBuilder {
	b.setOption(&b.Option.option1, option1)
	b.setOption(&b.Option.option2, option2)
	return b
}
func (b *OptionBuilder) WithOption3(option3 int) *OptionBuilder {
	b.setOption(&b.Option.option3, option3)
	return b
}
func (b *OptionBuilder) WithOption4(option4 float64) *OptionBuilder {
	b.setOption(&b.Option.option4, option4)
	return b
}
func (b *OptionBuilder) Build() (Option, error) {
	return b.Option, b.err
}

/**
 * @Description: 第四种，使用Functional Options
 * @param *Option
 */
type Setting func(*Option)

func Option1(op string) Setting {
	return func(option *Option) {
		option.option1 = op
	}
}
func Option2(op string) Setting {
	return func(option *Option) {
		option.option2 = op
	}
}
func Option3(op int) Setting {
	return func(option *Option) {
		option.option3 = op
	}
}
func Option4(op float64) Setting {
	return func(option *Option) {
		option.option4 = op
	}
}

func NewSetting(options ...func(*Option)) (*Option, error) {
	opt := Option{}
	for _, option := range options {
		option(&opt)
	}
	return &opt, nil
}

/**
 * @Description:
 * 1.c语言使用返回值+errno的方式来进行异常处理，后来又使用函数参数，通过入参和出参来标识
 * 2.java语言使用try-catch-finally的方式来进行检查
 */
func check_origin(a []int, b []int, c int) ([]int, error) {
	if len(a) != len(b) {
		return nil, errors.New("len of a and len of b  not equal")
	}
	result := make([]int, len(a))
	for i := 0; i < len(a); i++ {
		res, err := add_and_compare(a[i], b[i], c)
		if err != nil {
			return nil, err
		} else {
			result[i] = res
		}
	}
	return result, nil
}

func add_and_compare(a int, b int, c int) (n int, err error) {
	if a+b >= c {
		return a + b, nil
	} else {
		return a + b, errors.New("a+b not bigger than c")
	}
}

type Compares struct {
	V1  int
	V2  int
	V3  int
	V4  int
	V5  int
	err error
}

/**
 * @Description:  我们需要将这个函数进行改进
 * @receiver c
 * @param a
 * @param b
 * @return error
 */
func (c *Compares) exception_handler1(a []int, b []int) error {
	if _, err := check_origin(a, b, c.V1); err != nil {
		return err
	}
	if _, err := check_origin(a, b, c.V2); err != nil {
		return err
	}
	if _, err := check_origin(a, b, c.V3); err != nil {
		return err
	}
	if _, err := check_origin(a, b, c.V4); err != nil {
		return err
	}
	if _, err := check_origin(a, b, c.V5); err != nil {
		return err
	}
	return nil
}

/**
 * @Description: 通过函数式编程来改进
 * @param a
 * @param b
 * @param c.V1
 */
func (c *Compares) exception_handler2(a []int, b []int) error {
	var err error
	check := func(a []int, b []int, data int) {
		if err != nil {
			return
		}
		_, err = check_origin(a, b, data)
	}
	check(a, b, c.V1)
	check(a, b, c.V2)
	check(a, b, c.V3)
	check(a, b, c.V4)
	check(a, b, c.V5)
	if err != nil {
		return err
	}
	return nil
}

/**
 * @Description: use struct handler exception
 */
type Check struct {
	err error
}

func (check *Check) check(a []int, b []int, c int) {
	if check.err == nil {
		_, check.err = check_origin(a, b, c)
	}
}

func (c *Compares) exception_handler3(a []int, b []int) error {
	check := Check{}
	check.check(a, b, c.V1)
	check.check(a, b, c.V2)
	check.check(a, b, c.V3)
	check.check(a, b, c.V4)
	check.check(a, b, c.V5)
	if check.err != nil {
		return check.err
	}
	return nil
}

/**
 * @Description:  利用流式编程实现
 * @receiver c
 * @param a
 * @param b
 * @param m
 */
func (c *Compares) check(a []int, b []int, m int) {
	if c.err == nil {
		_, c.err = check_origin(a, b, m)
	}
}
func (c *Compares) checkV1(a []int, b []int) *Compares {
	c.check(a, b, c.V1)
	return c
}

func (c *Compares) checkV2(a []int, b []int) *Compares {
	c.check(a, b, c.V2)
	return c
}

func (c *Compares) checkV3(a []int, b []int) *Compares {
	c.check(a, b, c.V3)
	return c
}

func (c *Compares) checkV4(a []int, b []int) *Compares {
	c.check(a, b, c.V4)
	return c
}

func (c *Compares) checkV5(a []int, b []int) *Compares {
	c.check(a, b, c.V5)
	return c
}

func (c *Compares) exception_handler4(a []int, b []int) error {
	c.checkV1(a, b).checkV2(a, b).checkV3(a, b).checkV4(a, b).checkV5(a, b)
	if c.err != nil {
		return _errors.Wrap(c.err, " !!chech faild")
	}
	return nil
}

func re_compile(data string, expr string) string {
	reg, err := regexp.Compile(expr)
	if err == nil {
		return reg.FindString(data)
	}
	return ""
}

func writeBuffer() {
	write_buffer := bufio.NewWriter(os.Stdout)
	fmt.Fprint(write_buffer, "hello")
	fmt.Fprint(write_buffer, "gogogog")
	write_buffer.Flush()
}
func readBuffer() {
	str_reader := strings.NewReader("buffer reader test")
	bufio_reader := bufio.NewReader(str_reader)

	//peek 只读不取
	data, _ := bufio_reader.Peek(10)
	println(string(data))            //打印，读到的内容
	println(bufio_reader.Buffered()) //显示缓存中的直字节数

	//readString 从缓存中读取
	first_black, _ := bufio_reader.ReadString(' ')
	println(first_black)             //打印，读到的内容
	println(bufio_reader.Buffered()) //显示缓存中的直字节数

	//Read指定从缓存中读取固定的字节数
	num_bytes := make([]byte, 6)
	n_bytes, err := bufio_reader.Read(num_bytes)
	println(n_bytes)
	println(num_bytes)
	println(err)

}

func atomic_plus(l *uint32, r uint32) {
	atomic.AddUint32(l, r)
}
func atomic_sub(l *uint32, r uint32) {
	atomic.AddUint32(l, ^uint32(r-1))
}

var bytePool = sync.Pool{
	New: func() interface{} {
		b := make([]byte, 1024)
		return &b
	},
}

func StringBuilder(p []string, cap int) string {
	var b strings.Builder
	l := len(p)
	b.Grow(cap)
	for i := 0; i < l; i++ {
		b.WriteString(p[i])
	}
	return b.String()
}

func download(url string, i int, wg *sync.WaitGroup) {
	println("http://" + url + "/" + strconv.Itoa(i))
	time.Sleep(time.Nanosecond)
	wg.Done()
	println("done", strconv.Itoa(i))
}
func (p *Persion) printPersion() {
	fmt.Printf("Name=%s,Sex=%s,Age=%d\n", p.Name, p.Sex, p.Age)
}

type Persion struct {
	Name string
	Sex  string
	Age  int
}
type data struct {
}

func printStr(p stringable) {
	println(p.toString())
}

type Country struct {
	Name string
}

func (c Country) toString() string {
	return "Country Name = " + c.Name
}

type City struct {
	Name string
}

func (c City) toString() string {
	return "City Name = " + c.Name
}

type stringable interface {
	toString() string
}

```

