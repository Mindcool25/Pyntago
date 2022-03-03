#!/usr/bin/env python

class pentago:
    # Initial board state
    matrix = [
        [0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0],

        [0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0]
    ]

    coords = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    p1 = "X"
    p2 = "O"
    empty = "*"

    currPlayer = 1

    def __init__(self):
        return

    # Main game loop, prints everything
    def main_loop(self):
        return

    # Main game loop, doesn't print anything
    def headless_loop(self):
        return

    # Rotate given matrix
    def rotate(self, quad):
        # If there is a "-", rotate counterclockwise, otherwise clockwise
        if quad[0] == "-":
            self.counterclockwise(int(quad[1]))
        else:
            self.clockwise(int(quad[0]))

    # Places marker according to current player input
    def place(self, playerIn):
        # Grab quadrant and position from input (example: a1, b3, c9)
        quad = playerIn[0].lower()
        pos = int(playerIn[1])

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
        pos = self.coords[pos-1]

        # Placing marker according to current player if spot is empty
        if self.matrix[pos[0] + mody][pos[1] + modx] == 0:
            self.matrix[pos[0] + mody][pos[1] + modx] = self.currPlayer
            return True
        return False

    # Rotates matrix clockwise
    def clockwise(self, matrix_num):
        temp = self.matrix

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
        temp = self.matrix

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

    def ai_in(self, ai_in):
        self.place(ai_in[0])
        self.rotate(ai_in[1])

    # Prints out board
    def printBoard(self):
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
