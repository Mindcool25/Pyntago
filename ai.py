#!/usr/bin/env python

import game
import os
import neat
import threading
import random


class agent:
    """
    AI class representing an AI, probably not complex
    enough to warrant second file, but IDK
    """

    def __init__(self):
        return

    def generate_placement(self, nets, agents, ):
        # TODO add conversion from neural network output (between zero and one)
        #  to coordinate inputs in the form of a list
        coords = []
        x_output = nets[agents.index(agent)].activate()
        y_output = nets.activate
        coords += (x_output + y_output)
        return coords

    def generate_rotation(self, ge):
        return


def eval_genomes(genomes, config):
    # generations += 1 (Uncomment if you want to keep track of generations) TODO
    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    ge = []
    agents = []
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

    # Game Simulations occur here
    run_game = True
    while run_game & len(agents) > 0:
        agent_threads = [threading.Thread(target=run_agent, args=(agent, nets))]
        for t in agent_threads:
            t.start()


def run_agent(agent, nets):
    """
    Runs simulated game
    :param agent: AI object
    :param nets: List containing all neural networks of current generation
    :return: Match Result TODO
    """
    # Create Game Object
    sim_game = game.pentago()
    # Game loop
    play = True
    while play:
        board_state = sim_game.get_board()
        sim_game.print_board()
        # Iterate through all the AIs to generate first move
        ai_in = agent.generate_placement()
        ai_in_rotation = agent.generate_rotation()
        # TODO Add win checking function here, win checker in game.py is unhelpful because it doesn't tell AI whether
        #  it won or lost
    # Possible need to delete sim_game object at this point?


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
