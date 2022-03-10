#!/usr/bin/env python

import socket
import game


logo = """
______            _
| ___ \          | |
| |_/ /   _ ____ | |_ ____  ____  ___
|  __/ | | |  _ \| __/ _  |/ _  |/ _ \\
| |  | |_| | | | | || (_| | (_| | (_) |
\_|   \___ |_| |_|\__\__,_|\___ |\___/
       __/ |                __/ |
      |___/                |___/       """


def server(p1):
    port = 25565
    # Start server
    print(f"Starting server on port {port}...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    print("Server up, waiting for connections.")
    server.listen(1)

    # Accept client connection
    client, addr = server.accept()
    # Recive client's username
    p2 = client.recv(1024).decode()
    print(f"User {p2} has connected!")
    # Send server's username to client
    client.send(p1.encode())

def client(p1):
    # Creating a client socket
    client = socket.socket()
    port = 25565
    # Validating user's inputted IP
    IP = False
    while(not IP):
        try:
            target = input("Enter IP or URL: ")
            IP = socket.gethostbyname(target)
        except:
            print("Invalid IP or URL. Try again")
    print(f"Connecting to {target}:{port}...")

    client.connect((IP, port))
    client.send(p1.encode())
    p1 = client.recv(1024).decode()

    print(f'Connected to user {p1}!')


def main():
    # Print ascii logo and credits
    print(logo)
    print("\nWritten by Mindcool25 and Mastachi")

    # Get user's username
    p1 = input("Enter a username: ")

    # Checking for user input, either server or client
    version = ""
    options = ["server", "client"]
    while version not in options:
        version = input("Server or Client?: ").lower()
    # Runs either server function or client function based on input
    if version == "server":
        server(p1)
    else:
        client(p1)

if __name__ == "__main__":
    main()
