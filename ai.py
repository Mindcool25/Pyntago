#!/usr/bin/env python

import game
import os
import neat
import threading
import enum
import random
from queue import Queue

class input_type(enum.Enum):
    x = 0
    y = 1
    rotation_direction = 2
    rotation_quadrant = 3


class agent:

    def __init__(self, net):
        self.net = net

    # Generates placement using neural network
    def generate_placement(self, board_state):
        placement = []
        x_output = self.net.activate((board_state, 0))
        y_output = self.net.activate((board_state, 1))
        x_output[0] = int(10 * x_output[0]) % 6
        y_output[0] = int(10 * y_output[0]) % 6
        print(x_output)
        print(y_output)
        placement.append(x_output[0])
        placement.append(y_output[0])
        return placement

    def generate_rotation(self, board_state):
        rotation_direction = self.net.activate((board_state, 2))
        rotation_quadrant = self.net.activate((board_state, 3))
        rotation_direction = int(10 * rotation_direction[0]) % 2
        if rotation_direction == 0:
            rotation_direction = -1
        rotation_quadrant = int(10 * rotation_quadrant[0]) % 4 + 1
        rotation = rotation_quadrant * rotation_direction
        return rotation


def eval_genomes(genomes, config):
    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    ge = []
    agents = []
    games = []
    threads = []
    """
    Associates genes with genomes,
    genomes with networks,
    and networks with players.
    """
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        agents.append(agent)
        ge.append(genome)

    # Shuffle genomes and nets the same way to generate a shuffled list
    merged = list(zip(nets, ge))
    random.shuffle(merged)
    shuffled_nets = [item[0] for item in merged]
    shuffled_ge = [item[1] for item in merged]
    # Game creation occurs here
    for i in range(0, 50):
        train_game = game.pentago()
        games.append(train_game)

    # Thread Creation for each game, then run_game
    for i in range(0, 50):
        threads.append(threading.Thread(target=run_game, args=(games[i], nets[i], shuffled_nets[i], ge[i],
                                                               shuffled_ge[i], i,)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def run_game(train_game, net1, net2, genome1, genome2, number):
    """
    Runs simulated game
    :param net2: Player 2
    :param net1: Player 1
    :param train_game: list of both agents and game instance
    :return: Match Result
    """
    # Main game loop, prints everything
    # print(train_game.print_board())
    win = 0
    while win not in [-1, 1, 2]:
        # Switching to next player
        board_state = train_game.get_board
        # Runs Turn for Player 1
        if train_game.currPlayer == 1:

            # Place Player 1 Piece
            agent_place(agent(net1), board_state, train_game)

            # Rotate Player 1 Piece
            train_game.rotate(str(agent(net1).generate_rotation(board_state)))

            # Switches Player
            train_game.currPlayer = 2

            # Prints Board
            print(train_game.print_board())

            # Checks Win
            win = train_game.check_win()

        # Runs Turn for Player 2
        else:

            # Place Player 2 Piece
            agent_place(agent(net2), board_state, train_game)

            # Rotate Player 2 Piece
            train_game.rotate(str(agent(net2).generate_rotation(board_state)))

            # Switches Player
            train_game.currPlayer = 1

            # Prints Board
            print(train_game.print_board())

            # Checks Win
            win = train_game.check_win()

    if win == 1:
        print("Player 1 Won!")

    elif win == 2:
        print("Player 2 Won!")

    elif win == -1:
        print("Draw!")

    return win


def agent_place(agent_network, board_state, train_game):
    placement = agent_network.generate_placement(board_state)
    # Check If Good Placement
    if check_valid(placement, train_game):
        # Place Move
        train_game.place(placement)
        return
    else:
        return


def check_valid(placement, train_game):
    if train_game.matrix[placement[0]][placement[1]] != 0:
        return False
    else:
        return True


def run(config_file):
    """
    Credit to TechWithTim on YouTube for implementation tutorial, code in this method largely stolen from neat-python docs
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal, commented out for now
    """
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))
    """

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
