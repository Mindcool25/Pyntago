#!/usr/bin/env python

import game
import multiplayer
import neat
import ai
import random

logo = """
______            _
| ___ \          | |
| |_/ /   _ ____ | |_ ____  ____  ___
|  __/ | | |  _ \| __/ _  |/ _  |/ _ \\
| |  | |_| | | | | || (_| | (_| | (_) |
\_|   \___ |_| |_|\__\__,_|\___ |\___/
       __/ |                __/ |
      |___/                |___/
Written by Mindcool24 and Mastatchi"""

menu_str = """
1.) Player v Player
2.) Host server
3.) Join server
4.) Play agianst AI
5.) Quit"""

def main():
    print(logo)
    choice = menu()
    if choice == 1:
        g = game.pentago()
        g.main_loop()
    elif choice == 2:
        p1 = input("Enter a username: ")
        multiplayer.server(p1)
    elif choice == 3:
        p2 = input("Enter a username: ")
        multiplayer.client(p2)
    elif choice == 4:
        ai()
    elif choice == 5:
        exit()

def menu():
    print(menu_str)
    choice = input("> ")
    if choice not in ["1", "2", "3", "4", "5"]:
        print("Invalid option.")
        menu()
    else:
        return int(choice)

def ai():
    # Loading the latest checkpoint
    point = neat.checkpoint.Checkpointer.restore_checkpoint("checkpoints/neat-checkpoint-34999")
    print("Loaded AI")
    point.run(playgame)

def playgame(genomes, config):
    # Setting up the network to play against
    ai_id, ai = genomes[random.randint(0, len(genomes) - 1)]
    print(ai)
    net = neat.nn.FeedForwardNetwork.create(ai, config)
    ai_game = game.pentago()

    # Setting up the agent
    p2 = ai.agent(net)

    win = 0
    while win not in [-1, 1, 2]:
        if ai_game.currPlayer == 1:
            userIn = False
            userRotation = False
            print(ai_game.print_board())

            # Getting user placement
            while not userIn:
                userIn = ai_game.getUserMarker()
            ai_game.place(userIn)
            print(ai_game.print_board())

            # Getting user rotation
            while not userRotation:
                userRotation = ai_game.getUserRotation()
            ai_game.rotate(userRotation)
            print(ai_game.print_board())
            ai_game.currPlayer = 2
        elif ai_game.currPlayer == 2:
            print("AI TURN")





if __name__ == "__main__":
    main()
