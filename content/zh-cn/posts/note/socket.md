TCP的三次握手和四次挥手

## 三次握手:
为什么需要三次握手?
客户端:我可以发东西给你(确保客户端的发送能力)
服务器:我可以收到,你能收到么?(确保服务器的接受和发送)
客户端:我能收到!(确保能收到)

连接建立!

如果是四次握手?
没必要啊,第三次已经确认可以收到消息了

如果是两次握手?
当网络阻塞时,客户端会发送两次,第一次请求到达服务器的时间慢于第二次
如果当时通信结束,服务器又收到了第一次阻塞的消息,如果是两次握手,就会分配资源
然而客户端已经完成了通信,不需要再连接了,会造成资源的浪费和安全隐患

## 四次挥手:
客户端:我说完了,我想停止发送请求了
服务器:我知道你要停止发送了,我会停止接受消息
(
服务器停止接受消息,但是可能还有很多待发送的消息

客户端:收到服务器的确认信息,于是默不作声,等待服务器发送完他的消息

)
服务器:我的东西全发完啦!,我想要停止发送消息啦!
客户端:我知道你也要停止发送了,我也要停止接收消息(实际上还等了两个最大周期才真正停止接收消息)
(
服务器:收到了客户端的确认消息,于是停止发送消息
)


[关于tcp的博客](https://blog.csdn.net/qq_38950316/article/details/81087809)


使用tcp和udp让进程之间进行通信

ip地址：用來標記網絡上的主機
動態端口：1024-65535的端口，用完就回收

tcp socket client的基本流程
```python
import socket
##創建socket
s = socket.socket(socket.af_inet,socket.sock_stream)
##使用
ipaddr = ("ip",port)#服务器的ip addr
s.connect(ipaddr)#连接服务器
### 发送数据
send_msg = "sasa"
s.send(send_msg.encode("utf-8"))
### 接受数据
recvData = s.rec(1024)#一次接收的字符数
print("recved msg:",recvData.decode(""utf-8))

##關閉
s.close()
```

tcp server的基本过程
```python
# socket创建套接字
tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 绑定端口
tcp.bind(("127.1",7788))
# 设置为被动监听
tcp.listen(128)

while True:
	#等待客户端的连接


	#tcp套接字,现在用来被动接听

	# accept阻塞等待链接
	new_client_socket,client_addr = tcp.accept()#阻塞等待一个客户端进行conect,返回元组: 新的套接字,(客户端的ip,端口)
	#有客户端connect后,阻塞解除,返回connect的一个客户端的addr,以及已经和客户端完成连接的套接字,接下来的收发都是用这个新的socket
	
	while True:

		# 处理请求,先收,再发,因此,这里会阻塞等待这个new_client_socket接收到消息
		recv_data = new_client_socket.recv(1024)
		print(recv_data)

		#当recv解阻塞时,有两种情况,1.客户端发送了消息 ;2.客户端调用了close()
		#通过判断recv_data是否为空,那么判断出客户端断开了链接
		if recv_data:
			#收到消息后,我们返回一下,非必要的
			new_client_socket.send("服务器返回的消息".encode('utf-8'))
		else:
			break

	new_client_socket.close()

tcp.close()
```



創建一個udp socket
```python
import socket

##創建
send_data = input("input:")
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#bind a port,接受方可以不绑定
s.bind("",7890)
##使用
#s.sendto(b"test",("127.1",8888))#需要使用二进制第二个参数是元组
s.sendto(send_data.encode("utf-8"),("127.1",8888))#需要编码

s.close()#关闭
```

socket.socket(AddressFamily,Type)
AddressFamily:協議族
Type:套接字類型


绑定端口接收数据
```python
import socket
def main():
	#创建套接字
	udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	#绑定端口
	localaddr = ("",7788)
	udp.bind(localaddr)
	#接收数据
	recv_data = udp.recvfrom(1024)#可以接收的最大字节数
	#打印接受的数据
	#会接收到一个元组二进制流,发送方地址
	msg =  recv_data[0]
	sendaddr = recv_data[1]
	print("%s:%s"%str(sendaddr),msg.decode("utf-8"))#需要解码
	#关闭套接字
	udp.close()
if __name__ == "__main__":
	main()
```
一个套接字可以同时接收全双工的

一个攻击
扫描端口向缓冲区发送数据


使用tcp进行文件下载

client:
```python
import socket

def main():
	#1.创建套接字
	tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#2.获取服务器的ip port
	dest_ip = input("ip:")
	dest_port = input("port:")
	#3.连接服务器
	tcp_socket.connect((dest_ip,dest_port))
	#4.获取下载的名字
	download_file_name = input("input the file name")
	#5.将名字发送到服务器
	tcp_socket.send(download_file_name.encode("utf-8"))
	#6.接受文件中的数据
	recv_data = tcp_socket.recv(1024)#1k
	if recv_data:
		#7.保存文件中的数据
		with open("[new]"+download_file_name,"wb") as f:
			f.write(recv_data)
	#8.关闭套接字
	tcp_socket.close()

if __name__ == "__main__":
	main()


```
server:
```python
import socket

def send_file2client(new_client_socket,client_addr):
	#1.接受客户端需要下载的文件名
	file_name = new_client_socket.recv(1024).decode('utf-8')
	print("客户端下载的文件是:%s"%(str(client_addr),file_name))
	#2.打开这个文件,读取数据
	file_content = None
	try:
		f = open(file_name,"rb")
		file_content = f.read()
		f.close()
	except Exception as ret:
		print("没有要下载的文件(%s)"%file_name)
	#3.发送文件的数据给客户端
	if file_content:
		new_client_socket.send(file_conect)


def main():
	# socket创建套接字
	tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	
	# 绑定端口
	tcp_socket .bind(("127.1",7788))
	
	# 设置为被动监听
	tcp_socket .listen(128)

	while True:
		# accept阻塞等待链接
		new_client_socket,client_addr = tcp_socket .accept()#阻塞等待一个客户端进行conect,返回元组: 新的套接字,(客户端的ip,端口)

		# 调用函数,发送文件
		send_file2client(new_client_socket,client_addr)

		# 关闭套接字
		new_client_socket.close()

	tcp_socket .close()


if __name__ == "__main__":
	main()
```
