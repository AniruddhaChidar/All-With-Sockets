#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from crpyto import *


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        s="Greetings from the cave! Now type your name and press enter!"
        client.send(enc.encrypt(s.encode('utf-8'),key))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ)
    name = enc.decrypt(name,key).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(enc.encrypt(welcome.encode('utf-8'),key))
    msg = "%s has joined the chat!" % name
    broadcast(enc.encrypt(msg.encode('utf-8'),key))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(enc.encrypt("{quit}".encode('utf-8'),key))
            client.close()
            del clients[client]
            s="%s has left the chat." % name
            broadcast(enc.encrypt(s.encode('utf-8'),key))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    # print(msg+" msg")
    for sock in clients:
        sock.send(msg)

        
clients = {}
addresses = {}

HOST = 'localhost'
PORT = 5555
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
