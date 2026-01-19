import socket
import threading

# 设置服务器地址和端口
host = '127.0.0.1'
port = 12345

# 创建一个Socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务器
client.connect((host, port))

# 接收来自服务器的消息
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print(message)
        except:
            print("服务器连接中断")
            client.close()
            break

# 发送消息到服务器
def send_message():
    while True:
        message = input("")
        client.send(message.encode())

# 启动接收和发送消息的线程
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()
