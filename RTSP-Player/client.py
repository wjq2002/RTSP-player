import socket

def start_client():
    # 创建 socket 对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # 获取本地主机名
    host = '10.26.10.103'

    # 设置端口
    port = 9999

    # 连接服务，指定主机和端口
    s.connect((host, port))
    while True:
    # 接收小于 1024 字节的数据
        msg = s.recv(1024)
        print (msg.decode('utf-8'))
        
        s.send('Data received successfully!'.encode('utf-8'))

        if msg == 'q':
            break
    # 关闭连接
    s.close()

if __name__ == '__main__':
    start_client()