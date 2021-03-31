#!/usr/bin/env python3


import socket

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224
PROTOCOL = ["SYN", "SYN ACK", "ACK with DATA", "ACK for DATA"]

sock_service = socket.socket()
sock_service.connect((SERVER_ADDRESS, SERVER_PORT))
print("Connesso a " + str((SERVER_ADDRESS, SERVER_PORT)))

step = 0
dati = str(step)

while True:
    dati = dati.encode()
    sock_service.send(dati)

    print("Invio:    " + str(step) + " - " + PROTOCOL[step])

    dati = sock_service.recv(2048)

    if not dati:
        print("Server non risponde. Exit")
        break

    dati = dati.decode()

    if dati == '3':
        print("Ricevuto: " + dati + " - " + PROTOCOL[int(dati)])
        print("Termino connessione")
        break
    else:
        step = int(dati)
        print("Ricevuto: " + str(step) + " - " + PROTOCOL[step])
        step += 1
        dati = str(step)

sock_service.close()
