#!/usr/bin/env python

import game
import os
import neat
import threading
import random

# Global List of win results for fitness:
results = []
generation = 0


class agent:

    def __init__(self, net):
        self.net = net

    # Generates placement using neural network
    def generate_move(self, board_state):
        ai_move = self.net.activate(board_state)
        placement = [0, 0]

        # X Coord from NN
        placement[0] = int(10 * ai_move[0]) % 6

        # Y Coord from NN
        placement[1] = int(10 * ai_move[1]) % 6
        print(placement)
        # Rotation Quadrant from NN
        rotation = int(10 * ai_move[3]) % 4 + 1

        # Rotation Direction from NN
        rotation_dir = int(10 * ai_move[2]) % 2
        if rotation_dir == 0:
            rotation_dir = -1

        rotation = rotation * rotation_dir
        print(rotation)
        return placement, str(rotation)


def eval_genomes(genomes, config):
    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    global results

    global generation
    generation += 1
    print("Generation ", generation)

    results = []
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

    # Game creation occurs here
    for i in range(0, 50):
        train_game = game.pentago()
        games.append(train_game)

    # Thread Creation for each game, then run_game
    for i in range(0, 50):
        threads.append(threading.Thread(target=run_game, args=(games[i], nets[i], shuffled_nets[i], i,), daemon=True))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Append Fitness Values to all AIs
    for x, result in enumerate(results):
        if results[x] == 1:
            ge[x].fitness += 1
        elif results[x] == 2:
            ge[x].fitness -= 1


def run_game(train_game, net1, net2, ai_number):
    """
    Runs simulated game
    :param ai_number: Number of Primary AI for data entry, may cause AI to be better at Player 1
    :param net2: Player 2
    :param net1: Player 1
    :param train_game: list of both agents and game instance
    :return: Match Result
    """
    win = 0
    global results

    # Create Agents representing each player
    a1 = agent(net1)
    a2 = agent(net2)

    while win not in [-1, 1, 2]:
        # Switching to next player
        board_state = train_game.get_board()
        # Runs Turn for Player 1
        if train_game.currPlayer == 1:

            # Generate AI Move
            a1_placement, a1_rotation = a1.generate_move(board_state)

            # Place Player 1 Piece
            # Check If Good Placement
            if check_valid(a1_placement, train_game):
                # Place Move
                train_game.place(a1_placement)
            else:
                # Generate Random Placement random if invalid move
                randomGen = [random.randint(0, 5), random.randint(0, 5)]
                while not check_valid(randomGen, train_game):
                    randomGen = [random.randint(0, 5), random.randint(0, 5)]
                train_game.place(randomGen)

            # Rotate Player 1 Piece
            train_game.rotate(a1_rotation)

            # Switches Player
            train_game.currPlayer = 2

            # Checks Win
            win = train_game.check_win()

        # Runs Turn for Player 2
        else:

            # Generate AI Move
            a2_placement, a2_rotation = a2.generate_move(board_state)

            # Place Player 2 Piece, random if invalid move
            if check_valid(a1_placement, train_game):
                # Place Move
                train_game.place(a1_placement)
            else:
                # Generate Random Placement
                randomGen = [random.randint(0, 5), random.randint(0, 5)]
                while not check_valid(randomGen, train_game):
                    randomGen = [random.randint(0, 5), random.randint(0, 5)]
                train_game.place(randomGen)

            # Rotate Player 2 Piece
            train_game.rotate(a2_rotation)

            # Switches Player
            train_game.currPlayer = 1

            # Checks Win
            win = train_game.check_win()

    if win == 1:
        print(f"id: {ai_number}\nPlayer 1 Won!\n{train_game.print_board()}")
        results.insert(ai_number, 1)
    elif win == 2:
        print(f"id: {ai_number}\nPlayer 2 Won!\n{train_game.print_board()}")
        results.insert(ai_number, 2)
    elif win == -1:
        print(f"id: {ai_number}\nDouble Win!\n{train_game.print_board()}")
        results.insert(ai_number, -1)
    elif win == 0:
        print(f"id: {ai_number}\nDraw!\n{train_game.print_board()}")
        results.insert(ai_number, 0)
    return


"""
def agent_move(agent_network, board_state, train_game):
    placement = agent_network.generate_placement(board_state)
    # Check If Good Placement
    if check_valid(placement, train_game):
        # Place Move
        train_game.place(placement)
        return
    else:
        # Generate Random Placement
        randomGen = [random.randint(0, 5), random.randint(0, 5)]
        while not check_valid(randomGen, train_game):
            randomGen = [random.randint(0, 5), random.randint(0, 5)]
        train_game.place(randomGen)
        return
"""


def check_valid(placement, train_game):
    if train_game.matrix[placement[0]][placement[1]] != 0:
        return False
    else:
        return True


def run(config_file):
    """
    Credit to TechWithTim on YouTube for implementation tutorial, code in this method largely stolen from neat-python docs
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param: config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal, commented out for now
    # p.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
