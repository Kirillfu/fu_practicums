import socket


def get_part_key(key_publ_2, key_prim, key_publ_1):
    key_part_2 = key_publ_2 ** key_prim % key_publ_1
    return key_part_2

def get_full_key(key_part_1, key_prim, key_publ_1):
    key_full = key_part_1 ** key_prim % key_publ_1
    return key_full

# преобразует unicode символов в строку байтов 
def encoding (msg, key):
    lst = list(msg)
    for i in range(len(lst)):
        variab = ord(lst[i]) + key
        variab = chr(variab)
        lst[i] = variab
    return(''.join(lst))

#выполнит неявное кодирование
def decoding (msg, key):
    lst = list(msg)
    for i in range(len(lst)):
        variab = ord(lst[i]) - key
        variab = chr(variab)
        lst[i] = variab
    return(''.join(lst))

#Производим генерацию ключей
def generation(flagg, key_prim, key_publ_2):
    global flag
    while flagg<3:
        flagg+= 1
        # 1 флаг, если ключ был неверным
        if flagg == 1:
                msg = str(key_publ_2)
                sock.send(msg.encode())
                try:
                    key_publ_1 = int(sock.recv(1024))
                except ValueError:
                    print("Ошибка: данный ключ является некорректным")
                    flag = False
                    break
        # Флаг отправление нормального ключа на сервер
        if flagg == 2:
                key_part_2 = get_part_key(key_publ_2, key_prim, key_publ_1)
                msg = str(key_part_2)
                sock.send(msg.encode())
                key_part_1 = int(sock.recv(1024))
        #при 3 флаге открываем файл и записываем туда ключи
        if flagg == 3:
                key_full_2 = get_full_key(key_part_1, key_prim, key_publ_1)
                print(key_part_1, key_prim, key_publ_1)
                msg = str(key_full_2)
                sock.send(msg.encode())
                key_full_1 = int(sock.recv(1024))
                print(key_full_1)
                with open ('client_keys.txt','w') as f:
                    f.write(str(key_full_1))
    return key_full_1

#Отправляем сообщение на сервер
def send_recv(sock, key_full_2):
    msg = input('Введите сообщение: ')
    encod_msg = encoding(msg, key_full_2)
    sock.send(encod_msg.encode())
    msg = sock.recv(1024).decode()
    decod_msg= decoding(msg,key_full_2)
    print('Сообщение от сервера: ', decod_msg)
    return decod_msg

flag = True
sock = socket.socket()
sock.setblocking(5)
sock.connect(('localhost', 9090))
print('Соединение')


#Если данные не были введены и прочитаны 
try:
    with open ('client_keys.txt','r') as f:
        for line in f:
            key_full_1 = int(line)
except:
    key_prim = 199
    key_publ_2 = 197
    flagg= 0
    msg = ''
    key_full_1 = generation(flagg, key_prim, key_publ_2)

# Если флаг true, то мы отправляем сообщение на сервер и даем подключение к клиенту
if flag:
    port = send_recv(sock, key_full_1)
    sock.close()
    sock = socket.socket()
    sock.connect(('localhost', 1024))
    while True:
        send_recv(sock, key_full_1)
sock.close()
print('Соединение остановлено')