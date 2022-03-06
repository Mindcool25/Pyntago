#!/usr/bin/env python

import copy
import re


class pentago:
    # Initial board state

    coords = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    p1 = "X"
    p2 = "O"
    empty = "*"

    def __init__(self):
        self.matrix = [
            [0, 0, 0,  0, 0, 0],
            [0, 0, 0,  0, 0, 0],
            [0, 0, 0,  0, 0, 0],

            [0, 0, 0,  0, 0, 0],
            [0, 0, 0,  0, 0, 0],
            [0, 0, 0,  0, 0, 0]
        ]
        self.currPlayer = 1
        return

    # Main game loop, prints everything
    def main_loop(self):
        userIn = False
        userRotation = False
        while True not in self.check_win():
            # Get user input for placing marker, if failed try again
            while not userIn:
                userIn = self.getUserMarker()

            # Placing marker according to user input
            self.place(userIn)
            self.print_board()

            # Getting user input for rotatoin quadrant, if failed try again
            while not userRotation:
                userRotation = self.getUserRotation()

            # Rotating quadrant according to user input
            self.rotate(userRotation)
            self.print_board()

            # Resetting userIn and userRotate for next player
            userIn = False
            userRotation = False

            # Switching to next player
            if self.currPlayer == 1:
                self.currPlayer = 2
            else:
                self.currPlayer = 1
        p1, p2 = self.check_win()
        if p1:
            print("Player 1 Won!")
        else:
            print("Player 2 Won!")
        return

    # Main game loop, doesn't print anything
    def headless_loop(self):
        return

    # Get user input for placing a marker
    def getUserMarker(self):
        # Getting input from user
        coords = input(f"Player {self.currPlayer} enter coords (i.e. c4): ").lower()
        userIn = re.findall(r'[a-d][1-9]', coords) # oooOOhhHhhh spooky regex
        if not userIn:
            print("Invalid input, try again.")
            return False
        else:
            return userIn[0]

    # Getting user input for rotating a quadrant
    def getUserRotation(self):
        # Getting input from user
        rotation = input(f"Player {self.currPlayer} enter rotation (i.e. -1): ").lower()
        userRotation = re.findall(r'-?[1-4]', rotation) # OoooOOooOooHHhhh even more spooky regex
        if not userRotation:
            print("Invalid input, try again.")
            return False
        else:
            return userRotation[0]

    # Check if cell is the center of a row of 5
    def winning_cell(self, row, col):
        offsets = (-2, -1, +1, +2)
        diag_1 = [*zip(offsets, offsets)]
        diag_2 = [*zip(offsets, reversed(offsets))]
        """ True if the given cell is at the centre of a row of 5 """
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
    def check_win(self):
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
                        return True, True
        return white_win, black_win

    # Rotate given matrix
    def rotate(self, quad):
        # If there is a "-", rotate counterclockwise, otherwise clockwise
        if quad[0] == "-":
            self.counterclockwise(int(quad[1]))
        else:
            self.clockwise(int(quad[0]))

    # Rotates matrix clockwise
    def clockwise(self, matrix_num):
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

    # Places marker according to current player input
    def place(self, player_in):
        # Grab quadrant and position from input (example: a1, b3, c9)
        quad = player_in[0].lower()
        pos = int(player_in[1])

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
        pos = self.coords[pos - 1]

        # Placing marker according to current player if spot is empty
        if self.matrix[pos[0] + mody][pos[1] + modx] == 0:
            self.matrix[pos[0] + mody][pos[1] + modx] = self.currPlayer
            return True
        return False

    def ai_in(self, ai_in):
        self.place(ai_in[0])
        self.rotate(ai_in[1])

    # Prints out board
    def print_board(self):
        string = ""

        # Iterate through matrix, adding p1 markers, p2 markers, and empty markers accordingly
        for row in range(0, 6):
            for column in range(0, 6):
                curr = self.matrix[row][column]
                if curr == 1:
                    string += self.p1 + " "
                elif curr == 2:
                    string += self.p2 + " "
                elif curr == 0:
                    string += self.empty + " "

                # Add middle vertical line
                if column == 2:
                    string += "| "

            # Adding newline
            string += "\n"

            # Print middle horizontal line
            if row == 2:
                string += "-" * 13 + "\n"
        print(string)
