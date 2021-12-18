import socket
import os
import threading,sys
sock = socket.socket()
file=open('Users.txt',"a")
file.close()
file=open('log.txt',"w")
file.close()
def path_(sentence):
    if os.name == 'posix':
        if sentence.find('/') == -1:
            return True
        else:
            return False
    elif os.name == 'nt':
        if sentence.find('\\') == -1:
            return True
        else:
            return False

def cat_(name):
    try:
        file = open(name)
        content = file.read()
        file.close()
        return content
    except FileNotFoundError:
        log_file = open('log.txt', 'a')
        log_file.write('File doesnt exist' + "\n")
        log_file.close()
        return "File doesnt exist"

def echo_(sentence, directory):
    try:
        if len(sentence.split(' >> ')) == 2:
            sentence2= sentence.split(' >> ')
            sentence2[1] = os.path.join(directory, sentence2[1])
            file = open(sentence2[1], 'a')
            file.write('\n')
            file.write(sentence2[0])
            file.close()
            log_file = open('log.txt', 'a')
            log_file.write('File is made')
            log_file.close()
            return f'File is made'

        elif len(sentence.split(' > ')) == 2:
            sentence2 = sentence.split(' > ')
            sentence2[1] = os.path.join(directory, sentence2[1])
            file = open(sentence2[1], 'w')
            file.write('\n')
            file.write(sentence2[0])
            file.close()
            log_file = open('log.txt', 'a')
            log_file.write('Text is written in' + str(sentence2) + "\n")
            log_file.close()
            return f'Text is written in {sentence2[1]}'
        else:
            log_file = open('log.txt', 'a')
            log_file.write('Wrong format'+ "\n")
            log_file.close()
            return 'Wrong format'
    except FileNotFoundError:
        log_file = open('log.txt', 'a')
        log_file.write('Wrong format' + "\n")
        log_file.close()
        return 'Wrong format'

def mkdir_(sentence, directory):
    if sentence[0] == ' ':
        log_file = open('log.txt', 'a')
        log_file.write('Wrong format' + "\n")
        log_file.close()
        return ('Wrong format')
    else:
        try:
            os.makedirs(os.path.join(directory, sentence))
            return 'Директория создана'
        except OSError:
            log_file = open('log.txt', 'a')
            log_file.write('Folder already exists' + "\n")
            log_file.close()
            return ('Folder already exists')

def rm_(sentence, directory):
    if sentence[0] == ' ':
        log_file = open('log.txt', 'a')
        log_file.write('Wrong format' + "\n")
        log_file.close()
        return ('Wrong format')
    else:
        try:
            os.remove(os.path.join(directory, sentence))
            return os.path.join(directory, sentence)
        except FileNotFoundError:
            log_file = open('log.txt', 'a')
            log_file.write('File already exists' + "\n")
            log_file.close()
            return ('File already exists')
        except PermissionError:
            log_file = open('log.txt', 'a')
            log_file.write('ERROR' + "\n")
            log_file.close()
            return ('ERROR')

def rmdir_(sentence, directory):
    if sentence[0] == ' ':
        log_file = open('log.txt', 'a')
        log_file.write('Wrong format' + "\n")
        log_file.close()
        return ('Wrong format')
    else:
        try:
            os.rmdir(os.path.join(directory, sentence))
            return os.path.join(directory,sentence)
        except FileNotFoundError:
            log_file = open('log.txt', 'a')
            log_file.write('Folder doesnt exist' + "\n")
            log_file.close()
            return ('Folder doesnt exist')

def cd_(sentence, directory):
    if sentence == '..':
        now_dir = os.path.split(directory)[0]
        return (now_dir)
    elif sentence[0] == ' ' or sentence[len(sentence) - 1] == ' ':
        log_file = open('log.txt', 'a')
        log_file.write('Wrong format' + "\n")
        log_file.close()
        return ('Wrong format')
    elif os.path.exists(os.path.join(directory, sentence)):
        if path_(sentence):
            return os.path.join(directory, sentence)
        else:
            log_file = open('log.txt', 'a')
            log_file.write('ERROR' + "\n")
            log_file.close()
            return 'ERROR'
    else:
        log_file = open('log.txt', 'a')
        log_file.write('Directory doesnt exist' + "\n")
        log_file.close()
        return 'Directory doesnt exist'

def send_(conn, msg):
    try:
        header = f'{len(msg):<4}'
        conn.send(f'{header}{msg}'.encode())
    except ConnectionAbortedError:
        pass

def recv_(conn):
    try:
        header = int(conn.recv(4).decode().strip())
        data = conn.recv(header * 2).decode()
        return data
    except (ValueError, ConnectionAbortedError):
        return

class Server(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.dir = ''
        self.during_dir = ''

    def run(self):
        pr=True
        avtorise = recv_(self.conn)
        name = recv_(self.conn)
        try:
            if avtorise==1:
                with open('Users.txt', 'r') as f:
                    text = f.read()
                    if name not in text:
                        pr = True
                    else:
                        pr= False
            else:
                file = open('Users.txt', 'r')
                text = file.read()
                if name in text:
                    pr = True
        except KeyError:
            pr = False
        send_(self.conn, str(pr))
        while not pr:
            name = recv_(self.conn)
            pr = True
            try:
                if avtorise == 1:
                    with open('Users.txt', 'r') as f:
                        text = f.read()
                        if name not in text:
                            pr = True
                        else:
                            pr = False
                else:
                    file = open('Users.txt', 'r')
                    text = file.read()
                    if name in text:
                        pr = True
            except KeyError:
                pr = False
            send_(self.conn, str(pr))

        # Проверка пароля
        pr = False
        pswd = recv_(self.conn)
        if avtorise == '1':
            with open('Users.txt', 'a') as f:
                f.write(name + ';')
                f.write(pswd + '\n')
                pr = True
        else:
            with open('Users.txt', 'r') as f:
                for line in f:
                    symb = line.split(';')
                    if symb[0] == name:
                        if symb[1] == pswd + '\n':
                            pr = True
        send_(self.conn, str(pr))
        while not pr:
            pswd = recv_(self.conn)
            with open('Users.txt', 'r') as f:
                for line in f:
                    symb = line.split(';')
                    if symb[0] == name:
                        if symb[1] == pswd + '\n':
                            pr = True
            send_(self.conn, str(pr))

        self.dir = os.path.join(os.getcwd(), name)
        self.during_dir = os.path.join(os.getcwd(), name)
        mkdir_(name, os.getcwd())

        while True:
            request = recv_(self.conn)
            log_file = open('log.txt', 'a')
            log_file.write(str(request) + "\n")
            log_file.close()
            print(request)
            if request:
                if request == 'pwd':
                    send_(self.conn, self.during_dir)
                elif request == 'ls':
                    send_(self.conn, '; '.join(os.listdir(self.during_dir)))
                elif request.split(' ')[0] == 'cat':
                    try:
                        send_(self.conn, cat_(os.path.join(self.during_dir, request.split(' ')[1])))
                    except IndexError:
                        send_(self.conn, "This file doesnt exit")
                elif request[:5] == 'echo ':
                    send_(self.conn, echo_(request[5:], self.during_dir))
                elif request[:6] == 'mkdir ':
                    if path_(request[6:]):
                        self.during_dir = mkdir_(request[6:], self.during_dir)
                        send_(self.conn, self.during_dir)
                    else:
                        send_(self.conn, 'You cant enter the way')

                elif request[:3] == 'rm ':
                    if path_(request[3:]):
                        send_(self.conn, rm_(request[3:], self.during_dir))
                    else:
                        send_(self.conn, 'You cant enter the way')

                elif request[:6] == 'rmdir ':
                    if path_(request[:6]):
                        send_(self.conn, rmdir_(request[6:], self.during_dir))
                    else:
                        send_(self.conn, 'You cant enter the way')

                elif request[:3] == 'cd ':
                    if (self.during_dir == self.dir and request[3:] != '..') or (self.during_dir != self.dir):
                        x = cd_(request[3:], self.during_dir)
                        if x != 'Wrong format' or x != 'Directory doesnt exist' or x != 'You cant enter the way':
                            self.during_dir = x
                            send_(self.conn, self.during_dir)
                        else:
                            send_(self.conn, x)
                    elif (self.during_dir == self.dir and request[3:] == '..'):
                        send_(self.conn, 'You arent allowed to  log out of your directory')


                else:
                    send_(self.conn, 'Request ERROR')
            elif request is None:
                break

            else:
                send_(self.conn, 'Request ERROR')

        self.conn.close()
log_file = open('log.txt', 'a')
print('Start ')
log_file.write('Start '+"\n")
port = 1024
print('Connection ')
log_file.write('Connection '+"\n")
sock.bind(('', port))
print('Port using ',port)
log_file.write('Port using '+ str(port)+"\n")
print('Start listening ')
log_file.write('Start listening '+"\n")
sock.listen()
log_file.close()
while True:
    conn, addr = sock.accept()
    print('Client is ',addr[0])
    Server(conn, addr).start()