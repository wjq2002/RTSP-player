import socket

HOST = '10.26.10.103'   # 远程主机的地址
PORT = 2            # 远程主机上运行的端口号

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)
print('接收到的数据：', data.decode())