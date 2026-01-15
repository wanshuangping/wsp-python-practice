import socket
import threading

host = '127.0.0.1'
port =12345

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((host,port))

server.listen(5)
print(f'服务器正在{host}:{port}运行...')

clients = []

def broadcast(message,client_socket):
    for clinet in clients:
        if clinet != client_socket:
            try:
                clinet.send(message)
            except:
                clinet.close()
                clients.remove(clinet)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f'收到消息:{message.decode()}')
                broadcast(message,client_socket)
            else:
                break
        except:
            break
    client_socket.close()


def receive_clients():
    while True:
        client_socket,client_address = server.accept()
        print(f'连接来自{client_address}')

        clients.append(client_socket)
        thread = threading.Thread(target=handle_client,
                                  args=(client_socket,))
        thread.start()
receive_clients()

