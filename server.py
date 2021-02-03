#!/usr/bin/env python3
import socket


SERVER_ADDRESS = '127.0.0.1'

SERVER_PORT = 22224

sock_listen = socket.socket()

sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_listen.bind((SERVER_ADDRESS, SERVER_PORT))

sock_listen.listen(5)

print("Server in ascolto su %s." % str((SERVER_ADDRESS, SERVER_PORT)))


while True:
    sock_service, addr_client = sock_listen.accept()
    print("\nConnessione ricevuta da " + str(addr_client))
    print("\nAspetto di ricevere i dati ")
    contConn = 0
    while True:
        dati = sock_service.recv(2048)
        contConn += 1
        if not dati:
            print("Fine dati dal client. Reset")
            break

        dati = dati.decode()
        print("Ricevuto: '%s'" % dati)
        if dati == '0':
            print("Chiudo la connessione con " + str(addr_client))
            break

        dati = dati.split(";")  # piu;1;4 -> [piu][1][4]
        risposta = str()

        if dati[0] == "piu" or dati[0] == "meno" or dati[0] == "per" or dati[0] == "diviso":
            try:
                dati[1] = int(dati[1])
                dati[2] = int(dati[2])
            except ValueError:
                print("ValueError")
                risposta = "Non hai inserito i numeri correttamente."

            if risposta == "":  # I valori sono buoni
                risultato = int()

                if dati[0] == "piu":
                    risultato = dati[1] + dati[2]
                elif dati[0] == "meno":
                    risultato = dati[1] - dati[2]
                elif dati[0] == "per":
                    risultato = dati[1] * dati[2]
                else:
                    risultato = dati[1] / dati[2]

                risposta = "Il risultato dell'operazione " + \
                    str(dati[0]) + " tra " + str(dati[1]) + " e " + \
                    str(dati[2]) + " è uguale a " + str(risultato) + "."
        else:
            risposta = "Operazione non valida."

        risposta = risposta.encode()

        sock_service.send(risposta)

    sock_service.close()
