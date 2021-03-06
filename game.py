#!/usr/bin/env python

import copy
import re
import itertools


class pentago:
    """
    Pentago game class. Run main_loop to run the game.

    Game class that works with running the pentago game and handling user inputs.


    """
    # Initial board state
    coords = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    p1 = "X"
    p2 = "O"
    empty = "*"

    def __init__(self):
        self.matrix = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        self.currPlayer = 1
        self.turns = 0
        return

    def get_board(self):
        """
        Returns the current game board as a 1d list
        :return: current board as a flat matrix
        """
        flat_matrix = list(itertools.chain(*self.matrix))
        return flat_matrix

    # Main game loop, prints everything
    def main_loop(self):
        """
        Main gameplay loop
        Doesn't return anything, just runs the game in a human-readable way.
        """
        userIn = False
        userRotation = False
        print(self.print_board())
        while self.check_win() not in [-1, 1, 2]:
            # Get user input for placing marker, if failed try again
            while not userIn:
                userIn = self.getUserMarker()

            # Placing marker according to user input
            self.place(userIn)
            print(self.print_board())

            # Getting user input for rotation quadrant, if failed try again
            while not userRotation:
                userRotation = self.getUserRotation()

            # Rotating quadrant according to user input
            self.rotate(userRotation)
            print(self.print_board())

            # Resetting userIn and userRotate for next player
            userIn = False
            userRotation = False

            # Switching to next player
            if self.currPlayer == 1:
                self.currPlayer = 2
            else:
                self.currPlayer = 1
        win = self.check_win()
        if win == 1:
            print("Player 1 Won!")
        elif win == 2:
            print("Player 2 Won!")
        elif win == -1:
            print("Draw!")
        return

    # Get user input for placing a marker
    def getUserMarker(self):
        """
        Getting input from the user for placing a marker.

        :returns: user input converted into the 6x6 grid coordinates
        """
        # Getting input from user
        coords = input(f"Player {self.currPlayer} enter coords (i.e. c4): ").lower()
        userIn = re.findall(r'[a-d][1-9]', coords)  # oooOOhhHhhh spooky regex
        # Check if input is valid, both character wise and placement wise
        if not userIn:
            print("Invalid input, try again.")
            return False
        else:
            # Check if placement is valid
            pos = self.convertInput(userIn[0])
            return pos

    # Getting user input for rotating a quadrant
    def getUserRotation(self):
        """
        Getting input from the user for rotating a quadrant.

        :returns: returns valid player input
        """
        # Getting input from user
        rotation = input(f"Player {self.currPlayer} enter rotation (i.e. -1): ").lower()
        userRotation = re.findall(r'-?[1-4]', rotation)  # OoooOOooOooHHhhh even more spooky regex
        if not userRotation:
            print("Invalid input, try again.")
            return False
        else:
            return userRotation[0]

    # Check if cell is the center of a row of 5, credits to Niemmi on stackexchange for the code outline
    def winning_cell(self, row, col):
        """
        Function for checking if a cell has a winning combination.
        :param row: row of current cell
        :param col: column of current cell
        :return: boolean if the cell is winning or not
        """
        offsets = (-2, -1, +1, +2)
        diag_1 = [*zip(offsets, offsets)]
        diag_2 = [*zip(offsets, reversed(offsets))]
        # Note that when checking for a horizontal line we don't need to
        # check the first two or last two columns - the same logic applies
        # to rows and diagonals.
        colour = self.matrix[row][col]
        # check within row
        if (1 < col < len(self.matrix[0]) - 2 and
                all([self.matrix[row][col + c] == colour for c in offsets])):
            return True
        # check within column
        if (1 < row < len(self.matrix) - 2 and
                all([self.matrix[row + r][col] == colour for r in offsets])):
            return True
        # check diagonals
        if (1 < col < len(self.matrix[0]) - 2 and
                1 < row < len(self.matrix) - 2 and
                (all([self.matrix[row + r][col + c] == colour for r, c in diag_1]) or
                 all([self.matrix[row + r][col + c] == colour for r, c in diag_2]))):
            return True
        return False

    # Check if current player has won
    # DONE: Return 0 if no winner, -1 for draw, 1 for p1 win, 2 for p2 win, 3 for both win.
    # DONE: Fix main loop to work with above modification, same with multiplayer.
    def check_win(self):
        """
        Checks if a player has won
        :return: returns -1 if a draw, 0 if nothing, 1 if player 1 has won, 2 if player 2 has won
        """
        if self.turns == 36:
            return -1
        white = 1
        black = 2
        empty = 0
        black_win = False
        white_win = False
        # main loop to check cells
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                cell = self.matrix[row][col]
                if (cell == empty or
                        cell == white and white_win or
                        cell == black and black_win):
                    pass
                else:
                    if cell == white and self.winning_cell(row, col):
                        white_win = True
                    if cell == black and self.winning_cell(row, col):
                        black_win = True
                    if white_win and black_win:
                        black_win = True
                        white_win = True
        if white_win and black_win:
            return -1
        elif white_win:
            return 1
        elif black_win:
            return 2
        else:
            return 0

    # Rotate given matrix
    def rotate(self, quad):
        """
        Rotates quadrant from given input
        :param quad: positive or negative number between 1 and 4, rotates given quadrant
        """
        # If there is a "-", rotate counterclockwise, otherwise clockwise
        if quad[0] == "-":
            self.counterclockwise(int(quad[1]))
        else:
            self.clockwise(int(quad[0]))

    # Rotates matrix clockwise
    def clockwise(self, matrix_num):
        """
        Rotates given quadrant clockwise
        :param matrix_num: quadrant that needs to be rotated
        """
        temp = copy.deepcopy(self.matrix)

        # Get correct modifier per quadrant
        if matrix_num == 1:
            modx = 0
            mody = 0
        elif matrix_num == 2:
            modx = 3
            mody = 0
        elif matrix_num == 3:
            modx = 0
            mody = 3
        elif matrix_num == 4:
            modx = 3
            mody = 3

        # Rotating selected quadrant using mods
        self.matrix[0 + mody][2 + modx] = temp[0 + mody][0 + modx]
        self.matrix[1 + mody][2 + modx] = temp[0 + mody][1 + modx]
        self.matrix[2 + mody][2 + modx] = temp[0 + mody][2 + modx]
        self.matrix[0 + mody][1 + modx] = temp[1 + mody][0 + modx]
        self.matrix[2 + mody][1 + modx] = temp[1 + mody][2 + modx]
        self.matrix[0 + mody][0 + modx] = temp[2 + mody][0 + modx]
        self.matrix[1 + mody][0 + modx] = temp[2 + mody][1 + modx]
        self.matrix[2 + mody][0 + modx] = temp[2 + mody][2 + modx]

    # Rotates matrix counterclockwise
    def counterclockwise(self, matrix_num):
        """
        Rotates given quadrant counterclockwise
        :param matrix_num: quadrant that needs to be rotated
        """
        temp = copy.deepcopy(self.matrix)

        # Get correct modifier per quadrant
        if matrix_num == 1:
            modx = 0
            mody = 0
        elif matrix_num == 2:
            modx = 3
            mody = 0
        elif matrix_num == 3:
            modx = 0
            mody = 3
        elif matrix_num == 4:
            modx = 3
            mody = 3

        # Rotating selected quadrant using mods
        self.matrix[0 + mody][0 + modx] = temp[0 + mody][2 + modx]
        self.matrix[0 + mody][1 + modx] = temp[1 + mody][2 + modx]
        self.matrix[0 + mody][2 + modx] = temp[2 + mody][2 + modx]
        self.matrix[1 + mody][0 + modx] = temp[0 + mody][1 + modx]
        self.matrix[1 + mody][2 + modx] = temp[2 + mody][1 + modx]
        self.matrix[2 + mody][0 + modx] = temp[0 + mody][0 + modx]
        self.matrix[2 + mody][1 + modx] = temp[1 + mody][0 + modx]
        self.matrix[2 + mody][2 + modx] = temp[2 + mody][0 + modx]

    # Validate that the space isn't filled and change user input to coordinates
    def convertInput(self, player_in):
        """
        Coverts user inputs to valid inputs for the computer.
        :param player_in: input from the user
        :return: returns false if invalid move, otherwise returns x and y coordinates.
        """
        # Grab quadrant and position from input (example: a1, b3, c9)
        quad = player_in[0].lower()
        pos = int(player_in[1])
        newPos = [0, 0]
        # Convert letter input to quad number
        if quad == "a":
            modx = 0
            mody = 0
        elif quad == "b":
            modx = 3
            mody = 0
        elif quad == "c":
            modx = 0
            mody = 3
        elif quad == "d":
            modx = 3
            mody = 3
        # Grab actual coordinate from position, using coord matrix
        newPos = self.coords[pos - 1]
        # Check if space is already occupied
        if self.matrix[newPos[0] + mody][newPos[1] + modx] != 0:
            return False
        else:
            # Convert to actual coordinates rather than interpreted
            returnPos = [newPos[0] + mody, newPos[1] + modx]
            return returnPos

            # Places marker according to current player input

    def place(self, pos):
        """
        Places marker from given position.
        :param pos: coordinates from user
        """
        # Placing marker according to current player if spot is empty
        self.matrix[pos[0]][pos[1]] = self.currPlayer

    # Prints out board
    def print_board(self):
        """
        Prints the board out in a human-readable form
        :returns: Returns a string containing the human-readable board.
        """
        string = ""

        # Iterate through matrix, adding p1 markers, p2 markers, and empty markers accordingly
        for row in range(0, 6):
            for column in range(0, 6):
                curr = self.matrix[row][column]
                if curr == 1:
                    string += " " + self.p1 + " "
                elif curr == 2:
                    string += " " + self.p2 + " "
                elif curr == 0:
                    string += " " + self.empty + " "
                # Add middle vertical line
                if column == 2:
                    string += " ??? "

            # Adding newline
            string += "\n"

            # Print middle horizontal line
            if row == 2:
                string += "???" * 9 + " + " + "???" * 9 + "\n"
        return string
