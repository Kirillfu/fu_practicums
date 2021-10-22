import socket, getpass, threading
from time import sleep
'''Функция getpass() модуля getpass печатает подсказку и запрашивает у пользователя пароль без повторения.
 Входные данные возвращаются в качестве строки для вызывающей стороны.'''
def sendmsg(sock, data):
    sock.send(data.encode())

def recvmsg(sock, zn):
    data = sock.recv(zn).decode()
    return data

socket.socket.sendmsg = sendmsg
socket.socket.recvmsg = recvmsg

def recieving():
    while True:
        data = sock.recvmsg(1024)
        with block:
            print(data)


block = threading.Lock()
sock = socket.socket()
sock.setblocking(1)

host, port = 'localhost', 9090
print("Выполняется соединение с сервером")
sock.connect((host, port))
print("Соединено с сервером установлено")

threading.Thread(target = recieving, daemon = True).start()
while True:
    msg = input()
    sock.sendmsg(msg)
    if msg == "выход":
        break

print("Разрыв соединения с сервером")


sock.close() 
