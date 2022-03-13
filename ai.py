#!/usr/bin/env python

import game
import os
import neat
import random


class AI:
    """
    AI class representing an AI, probably not complex
    enough to warrant second file, but IDK
    """

    def generate_placement(self):
        # TODO add conversion from neural network output (between zero and one)
        #  to coordinate inputs in the form of a list
        return


def eval_genomes(genomes, config):
    # generations += 1 (Uncomment if you want to keep track of generations TODO
    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    ge = []
    AIs = []
    """
    Associates genes with genomes,
    genomes with networks,
    and networks with players.
    """
    for gene in genomes:
        net = neat.nn.FeedForwardNetwork(gene, config)
        nets.append(net)
        gene.fitness = 0
        ge.append(gene)

    # Game Simulations occur here
    while run & len(AIs > 0):
        sim = game.pentago()
        sim.print_board()
        # Iterate through all the AIs to generate first move
        for x, AI in enumerate(AIs):
            ai_in = AI.generate_placement(nets[x])


def run(config_file):
    """
    Credit to TechWithTim on YouTube for implementation tutorial
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
