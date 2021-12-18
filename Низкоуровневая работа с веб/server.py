import json
import socket
from settings import port, port2, directory,request_size,types
import threading
import datetime
import os


def request(conn, addr, data, directory):
    msg = data.decode()
    print(msg)

    name = msg.split()[1][1:]
    name_check=name.split('.')
    if name_check[1] not in types:
        name = '403.html'
    elif name == "" or os.path.exists(name)==False:
        name = "404.html"
    name = directory + "\\" + name

    now = datetime.datetime.now()
    date = now.strftime("%a, %d %b %Y %H:%M:%S GTM")

    with open("log.txt", "a") as log:
        print(f"Date: {date}\nAddr: {addr}\nFile: {name}", file=log)

    try:
        size = os.path.getsize(name)

    except FileNotFoundError:
        resp = f"""HTTP/1.1 404 Not Found
        Date: {date}
        """
        with open("log.txt", "a") as log:
            print("Error: 404", file=log)

        resp = resp.encode()
    else:
        decr = name.split(".")[-1]
        if decr not in types:
            resp = f"""HTTP/1.1 403 Forbidden
            Date: {date}
            """
            with open("log.txt", "a") as log:
                print("Error: 403", file=log)
        else:
            try:
                with open(name, "r", encoding="utf-8") as file:
                    resp = f"""HTTP/1.1 200 OK
                    Date: {date}
                    Content-Type: text/{decr};charset=utf-8
                    Content-Length: {size}
                    """
                    resp += file.read()
                resp = resp.encode()
            except UnicodeDecodeError:
                resp = f"""HTTP/1.1 200 OK
                Date: {date}
                Content-Type: image/{decr}
                Content-Length: {size}
                """
                f = open(name, 'rb')
                c = f.read()
                f.close()
                resp=c
    conn.send(resp)
def config_reader(filename = "config.json"):
    with open(filename, "r") as jsonfile:
        config = json.load(jsonfile)
    return config["port"], config["request_volume"], config["root"]

def connection(conn, addr, directory):
    data = conn.recv(request_size)
    if not data:
        return
    request(conn, addr, data, directory)
    conn.close()

sock = socket.socket()
try:
    sock.bind(('', port))
    print('Слушаю')
    print(f"Используется порт  {port}")
except OSError:
    sock.bind(('', port2))
    print('Слушаю')
    print(f"Используется порт {port2}")
sock.listen(5)
conn, addr = sock.accept()
while True:
    print("Client>", addr, "\n")
    tr = threading.Thread(target=connection, args=(conn, addr, directory))
    tr.start()
    conn, addr = sock.accept()