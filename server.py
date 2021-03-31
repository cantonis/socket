#!/usr/bin/env python3
import socket

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224
PROTOCOL = ["SYN", "SYN ACK", "ACK with DATA", "ACK for DATA"]

sock_listen = socket.socket()
sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_listen.bind((SERVER_ADDRESS, SERVER_PORT))
sock_listen.listen(5)

print("Server in ascolto su %s." % str((SERVER_ADDRESS, SERVER_PORT)))

while True:
    sock_service, addr_client = sock_listen.accept()

    print("\nConnessione ricevuta da " + str(addr_client))
    print("\nAspetto di ricevere i dati ")

    step = 0

    while True:
        dati = sock_service.recv(2048)

        if not dati:
            print("Fine dati dal client. Reset")
            break

        dati = dati.decode()
        step = int(dati)

        print("Ricevuto: " + dati + " - " + PROTOCOL[step])

        step += 1
        dati = str(step)
        dati = dati.encode()

        print("Invio:    " + str(step) + " - " + PROTOCOL[step])

        sock_service.send(dati)

    sock_service.close()
