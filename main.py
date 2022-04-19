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
        bot_run()
    elif choice == 5:
        exit()

def menu():
    print(menu_str)
    choice = input("> ")
    if choice not in ["1", "2", "3", "4", "5"]:
        print("Invalid option.")
        choice = menu()
    else:
        return int(choice)

def bot_run():
    # Loading the latest checkpoint
    point = neat.checkpoint.Checkpointer.restore_checkpoint("checkpoints/neat-checkpoint-37999")
    print("Loaded AI")
    point.run(playgame)

def playgame(genomes, config):
    # Setting up the network to play against
    bot_id, bot = genomes[random.randint(0, len(genomes) - 1)]
    net = neat.nn.FeedForwardNetwork.create(bot, config)
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
            board_state = ai_game.get_board()
            ai_placement, ai_rotation = p2.generate_move(board_state)
            if ai.check_valid(ai_placement, ai_game):
                ai_game.place(ai_placement)
            else:
                randomGen = [random.randint(0,5), random.randint(0,5)]
                while not ai.check_valid(randomGen, ai_game):
                    randomGen = [random.randint(0,5), random.randint(0,5)]
                ai_game.place(randomGen)
            print(ai_game.print_board())
            ai_game.rotate(ai_rotation)
            print(ai_game.print_board())
            ai_game.currPlayer = 1

        win = ai_game.check_win()
    if win == 1:
        print(f"Player 1 Won!")
    elif win == 2:
        print(f"id: {ai_number} Player 2 Won!")
    elif win == -1:
        print("Double Win!")
    elif win == 0:
        print("Draw!")
    exit()
    return 0

if __name__ == "__main__":
    main()
