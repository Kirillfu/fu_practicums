import socket, getpass, threading
from time import sleep

def send1(sock, data):
    length = "0"*(7-len(str(len(data)))) + str(len(data))
    data = bytearray((f'{length}{data}').encode())
    sock.send(data)

def recv1(sock, vol):
    data = sock.recv(vol).decode()
    print("Длинна сообщения:", data[:7])
    return data[7:]

socket.socket.send1 = send1
socket.socket.recv1 = recv1

def recieving():
    while True:
        data = sock.recv1(1024)
        with LOCK:
            #print("Прием данных от сервера")
            print(data)


LOCK = threading.Lock()
sock = socket.socket()
sock.setblocking(1)
port = getpass.getpass(prompt = 'Введите порт: ')
host = getpass.getpass(prompt = 'Введите хост: ')
if not port:
    port = 9090
else:
    port = int(port)
if not host:
    host = 'localhost'



# host, port = 'localhost', 9090
print("Соединение с сервером")
sock.connect((host, port))
print("Соединено с сервером")


threading.Thread(target = recieving, daemon = True).start()
while True:
    msg = input()
    # msg = "Hi!"
    print("Отправка данных серверу")
    sock.send1(msg)
    if msg == "exit":
        break
        

print("Разрыв соединения с сервером")



sock.close() 
