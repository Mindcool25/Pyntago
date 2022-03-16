#!/usr/bin/env python

import game
import os
import neat
import random


class ai:
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
    ais = []
    """
    Associates genes with genomes,
    genomes with networks,
    and networks with players.
    """
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)

    # Game Simulations occur here
    run_game = True
    while run_game & len(ais) > 0:
        sim_game = game.pentago()
        sim_game.print_board()
        # Iterate through all the AIs to generate first move
        for x, AI in enumerate(ais):
            ai_in = AI.generate_placement(nets[x])


def run(config_file):
    """
    Credit to TechWithTim on YouTube for implementation tutorial, code in this method stolen from neat-python docs
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
