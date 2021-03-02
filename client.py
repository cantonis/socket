import socket
import sys
import random
import time
import threading
import multiprocessing

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 22224
NUM_WORKERS = 15


def generaRichieste(address, port):
    try:
        s = socket.socket()
        s.connect((address, port))
        print("Connessione al server: " + address + ":" + str(port))
    except socket.error as error:
        print("Errore: " + error)
        sys.exit()

    comandi = ["piu", "meno", "per", "diviso"]
    operazione = comandi[random.randint(0, len(comandi) - 1)]
    dati = operazione + ";" + \
        str(random.randint(1, 100)) + ";" + str(random.randint(1, 100))
    dati = dati.encode()
    s.send(dati)

    dati = s.recv(2048)

    if not dati:
        print("Server non risponde. Exit")
        sys.exit()

    dati = dati.decode()
    print("Ricevuto dal server:\n" + dati)

    dati = "ko"
    dati = dati.encode()
    s.send(dati)
    s.close()


if __name__ == "__main__":
    start = time.time()
    for _ in range(0, NUM_WORKERS):
        generaRichieste(SERVER_ADDRESS, SERVER_PORT)
    end = time.time()
    print("\nTempo di esecuzione sequenziale: " + str(end - start) + "\n")

    start = time.time()
    threads = [threading.Thread(target=generaRichieste, args=(
        SERVER_ADDRESS, SERVER_PORT)) for _ in range(NUM_WORKERS)]
    for t in threads:
        t.start()
        t.join()
    end = time.time()
    print("\nTempo di esecuzione multithreading: " + str(end - start) + "\n")

    start = time.time()
    processes = [multiprocessing.Process(target=generaRichieste, args=(
        SERVER_ADDRESS, SERVER_PORT)) for _ in range(NUM_WORKERS)]
    for p in processes:
        p.start()
        p.join()
    end = time.time()
    print("\nTempo di esecuzione multiprocessing: " + str(end - start) + "\n")
