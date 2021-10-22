import socket, getpass, sys, random, csv

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

main_stdout = sys.stdout
sys.stdout = open('log.txt', 'w')
print("Запуск сервера")
sock = socket.socket()
port=getpass.getpass(prompt = 'Введите порт: ')
if not port:
        port = 9090
else:
    port = int(port)
# port = 9090

while True:
    try:
        sock.bind(('', port))
        print(f"Порт {port}")
        break
    except OSError as oserr:
        print(f"порт {port} недоступен")
        port = random.randint(1024,65535)

sock.listen(0)
print("Начало прослушивания порта")


def lstn():
        while True:
                #print("Прием данных от клиента")
                data = conn.recv1(1024)
                if not data:
                        print(f"Отключение клиента {addr}")
                        return False

                msg = data
                if msg == "exit":
                        print(f"Клиент попросил отключения {addr}")
                        return True
                print(msg)
                print("Введите сообщение для отправки данных клиенту")
                data = input()
                conn.send1(data)
                

sys.stdout.close()
sys.stdout = main_stdout

FLAG = False
while not FLAG:
        conn, addr = sock.accept()
        print(f"Подключение клиента {addr}")
        logins = "logins.csv"

        with open(logins, 'a+', newline = '') as login:
                login.seek(0,0)
                reader = csv.reader(login, delimiter = ';')
                for row in reader:
                        if row[0] == addr[0]:
                                password = row[2]
                                name = row[1]
                                break
                else:
                        conn.send1("Введите имя")
                        name = conn.recv1(1024)
                        conn.send1("Придумайте пароль")
                        password = conn.recv1(1024)
                        writer = csv.writer(login, delimiter = ';')
                        writer.writerow([addr[0], name, password])

        while True:
                conn.send1("Введите пароль для старта")
                password1 = conn.recv1(1024)
                if password1 == password:
                        conn.send1((f"Начинаем общение {name}"))

                        break
                else:
                        conn.send1("Неверный пароль")
        try:
                FLAG = lstn()
        except (ConnectionAbortedError, ConnectionResetError) as err:
                print(err)
        conn.close() 

print("Остановка сервера")
