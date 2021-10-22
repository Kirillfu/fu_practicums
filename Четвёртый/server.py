import socket, getpass, sys, random, csv, threading, os, time
# Для блокировки сокета
block = threading.Lock()
L_FLAG = True

def sendmsg(sock, data):
    # Посылаем сообщение
    sock.send(data.encode())

def recvmsg(sock, zn):
    #Чтобы получить данные нужно воспользоваться методом recv, который в качестве аргумента принимает количество байт для чтения
    data = sock.recv(zn).decode()
    return data

socket.socket.sendmsg = sendmsg
socket.socket.recvmsg = recvmsg

def logging(*data):
    data = ' '.join((str(item) for item in data))
    global block, L_FLAG
    if L_FLAG:
        with block:
            print(data)
            # Записываем наши данные в файл
            with open("log.txt", 'a+') as file:
                file.write(data+'\n')
#Осуществляем запуск нашего сервера
logging("Запуск сервера")
sock = socket.socket()
# Имя порта
port = 9090

while True:
    try:
        #Теперь свяжем наш сокет с данными хостом и портом с помощью метода bind,
        #которому передается кортеж, первый элемент (или нулевой, если считать от нуля) которого — хост, а второй — порт:
        sock.bind(('', port))
        logging(f"Порт {port}")
        break
    # Если не можем соединиться - значит, порт уже занят, сообщаем об этом
    except OSError as oserr:
        logging(f"порт {port} недоступен")
        # Генерируем случайным образом имя порта через random
        port = random.randint(1024,65535)
'''
С помощью метода listen мы запустим для данного сокета режим прослушивания. Метод принимает один аргумент —
 максимальное количество подключений в очереди.
 '''
sock.listen(0)
logging("Начало прослушивания порта")


def listening(conn, addr):
        global users_list, block, history
        # Создаем файл в формате csv для записи пароля и имени пользователя
        logins = "logins.csv"
        try:
                with block:
                        with open(logins, 'a+', newline = '') as login:
                                login.seek(0,0)
                                # Для каждых данных используем разные ячейки
                                reader = csv.reader(login, delimiter = ';')
                                for row in reader:
                                        if row[0] == addr[0]:
                                            # Записываем пароль и имя
                                                password = row[2]
                                                name = row[1]
                                                break
                                else:
                                        conn.sendmsg("Введите Ваше имя")
                                        name = conn.recvmsg(1024)
                                        #Чтобы получить данные нужно воспользоваться методом recv, который в качестве аргумента
                                        #принимает количество байт для чтения 
                                        conn.sendmsg("Введите пароль")
                                        password = conn.recvmsg(1024)
                                        writer = csv.writer(login, delimiter = ';')
                                        writer.writerow([addr[0], name, password])

                while True:
                        conn.sendmsg("Введите пароль для начала диалога")
                        password1 = conn.recvmsg(1024)
                        if password1 == password:
                                conn.sendmsg((f"Начинаем наше общение,{name}"))
                                break
                        else:
                                conn.sendmsg("Неверный пароль")
                 #Чтобы получить данные нужно воспользоваться методом recv, который в качестве аргумента
                 #принимает количество байт для чтения
                while True:
                        data = conn.recvmsg(1024)
                        logging(name, " : ", data)
                        with block:
                                with open(history, "a+") as file:
                                        file.write(name+": "+data+"\n")
                        for conn1 in users_list:
                                if conn1 != conn:
                                    # Выводим имя пользователя и его сообщение
                                        conn1.sendmsg(name+": "+data)
                        
        except:
                users_list.remove(conn)
                raise                

def connecting():
        global users_list, CON_FLAG
        while True:
                if CON_FLAG:
                        conn, addr = sock.accept()
                        logging(f"Подключение клиента {addr}")
                        users_list.append(conn)
                        threading.Thread(target = listening, args = (conn, addr), daemon = True).start()

users_list = []
 # Выводим имя пользователя и его сообщение
CON_FLAG = True
history = f"history_{time.time()}.txt"
threading.Thread(target = connecting, daemon = True).start()

while True:
        text = input()
        if text == "выключить":
                break
        elif  text == "показывать логи":
                L_FLAG = True
        elif  text == "не показывать логи":
                L_FLAG = False
        elif text == "очистить логи":
            # Осуществляем очистку логов
                if os.name == 'nt':
                        os.system('cls')
                else:
                        os.system('clear')
                with block:
                        with open("log.txt", "w"):
                                pass
        elif text == "очистка файла идентификации":
                with block:
                        with open("logins.csv", "w"):
                                pass
        elif text == "включить паузу":
                CON_FLAG = False
        elif text == "выключить паузу":
                CON_FLAG = True
logging("Остановка сервера")
