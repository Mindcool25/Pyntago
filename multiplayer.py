#!/usr/bin/env python

import socket
import re
import game
import time

logo = """
______            _
| ___ \          | |
| |_/ /   _ ____ | |_ ____  ____  ___
|  __/ | | |  _ \| __/ _  |/ _  |/ _ \\
| |  | |_| | | | | || (_| | (_| | (_) |
\_|   \___ |_| |_|\__\__,_|\___ |\___/
       __/ |                __/ |
      |___/                |___/       """


# Function to make code cleaner when sending prints to the client
def serverPrint(string):
    string = "1" + string
    return string


# Function for server side
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

    # Create game object
    g = game.pentago()

    # Sending the board state to the client
    board = g.print_board()
    print(board)
    client.send(serverPrint(board).encode())
    turn = 1

    # Start main loop
    while True not in g.check_win():
        # Setting userIn and userRotation to false for getting input
        userIn = False
        userRotation = False
        # if turn is 1, it means server is going. else it is the clients turn.
        if turn == 1:
            # Get server input for placing a marker
            while not userIn:
                userIn = g.getUserMarker()
            g.place(userIn)
            board = g.print_board()
            print(board)
            client.send(serverPrint(board).encode())
            time.sleep(0.1)

            # Get server input for rotation
            while not userRotation:
                userRotation = g.getUserRotation()
            g.rotate(userRotation)
            board = g.print_board()
            print(board)
            client.send(serverPrint(board).encode())
            time.sleep(0.1)
        else:
            # Get client input for placing a marker
            client.send("2test".encode())
            clientIn = client.recv(1024).decode()
            clientPos = g.convertInput(clientIn)
            g.place(clientPos)
            board = g.print_board()
            print(board)
            client.send(serverPrint(board).encode())
            time.sleep(0.1)

            # Get client input for rotation
            client.send("3test".encode())
            clientRotate = client.recv(1024).decode()
            g.rotate(clientRotate)
            board = g.print_board()
            print(board)
            client.send(serverPrint(board).encode())
            time.sleep(0.1)

        # Switch game's current player
        if g.currPlayer == 1:
            g.currPlayer = 2
        else:
            g.currPlayer = 1
        # Switch multiplayer's current player
        if turn == 1:
            turn = 2
        else:
            turn = 1

    # If a player has won
    server, c = g.check_win()
    if server:
        print("You won!")
        client.send("9p1".encode())
    else:
        print(f'{p2} won!')
        client.send("9p2".encode())


# Function for clientside operations
def client(p1):
    # Creating a client socket
    client = socket.socket()
    port = 25565
    # Validating user's inputted IP
    IP = False
    while not IP:
        try:
            target = input("Enter IP or URL: ")
            IP = socket.gethostbyname(target)
        except:
            print("Invalid IP or URL. Try again")
    print(f"Connecting to {target}:{port}...")

    # Connecting to server
    client.connect((IP, port))
    client.send(p1.encode())
    p2 = client.recv(1024).decode()
    print(f'Connected to user {p2}!')

    # Creating a game object for use of the internal methods
    g = game.pentago()

    # Setting up while loop for receiving packets
    mode = "0"
    while mode != "9":
        # Get input from server, slice it down to mode and the actual input.
        serverIn = client.recv(1024).decode()
        mode = serverIn[0]
        serverIn = serverIn[1::]
        # Defining different types of packets
        # 1 - Print out the message
        # 2 - Get user input for marker
        # 3 - Get user input for rotation
        # 9 - Win condition was met
        if mode == "1":
            print(serverIn)
        elif mode == "2":
            userIn = False
            while not userIn:
                coords = input(f'Player {p1} enter coords (i.e. c4): ').lower()
                userIn = re.findall(r'[a-d][1-9]', coords)
                if not userIn:
                    print("Invalid input, try again.")
                    userIn = False
                else:
                    pos = userIn[0]
            client.send(pos.encode())
        elif mode == "3":
            userRotation = False
            while not userRotation:
                userRotation = g.getUserRotation()
            client.send(userRotation.encode())
        elif mode == "9":
            if serverIn == "p1":
                print(f"{p2} won!")
            else:
                print("You won!")


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
