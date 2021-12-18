import socket

def sending(sock, msg):
    lenght = f'{len(msg):<4}'
    sock.send(f'{lenght}{msg}'.encode())

def reciev(sock):
    recv_msg = int(sock.recv(4).decode().strip())
    data = sock.recv(recv_msg*2).decode()
    return data

sock = socket.socket()
flag = False
while not flag:
    try:
        host = input("Host using :")
        if host == "":
            host = 'localhost'
        port = input("Port using:")
        if port == "":
            port = 1024
        print('Conection...')
        sock.connect((host, int(port)))
        choise = input('Create an account - 1,  log in-2 : ')
        sending(sock, choise)

        #Check login
        msg=input("Enter your login:")
        sending(sock, msg)
        proverka = reciev(sock)
        while proverka == 'False':
            print("Wrong user name!")
            msg = input('Enter your login again:')
            sending(sock, msg)
            proverka = reciev(sock)

        #check password
        password=input("Enter password: ")
        sending(sock, password)
        proverka = reciev(sock)
        while proverka == 'False':
            print("Wrong password")
            password = input('Enter password: ')
            sending(sock, password)
            proverka = reciev(sock)

        request = ''
        while request != 'exit':
            request = input('$')
            sending(sock, request)
            response = reciev(sock)
            if request=='exit':
                print('Stop connection')
            else:
                print(response)

        flag= True
    except KeyboardInterrupt:
        sock.close()