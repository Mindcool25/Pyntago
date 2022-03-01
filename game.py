#!/usr/bin/env python

class pentago:
    # Initial board state
    matrix = [
        [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ],
        [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ],
        [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ],
        [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]
    ]

    p1 = "X"
    p2 = "O"
    empty = "*"
    def __init__(self):
        return

    # Main game loop, prints everything
    def main_loop(self):
        return

    # Main game loop, doesn't print anything
    def headless_loop(self):
        return

    # Rotate given matrix
    def rotate(quad):
        # If there is a "-", rotate counterclockwise, otherwise clockwise
        if quad[0] == "-":
            counterclockwise(int(quad[1]))
        else:
            clockwise(int(quad[0]))

    # Rotates matrix clockwise
    def clockwise(self, matrix_num):
        temp = self.matrix[matrix_num]
        self.matrix[matrix_num][0][2] = temp[0][0]
        self.matrix[matrix_num][1][2] = temp[0][1]
        self.matrix[matrix_num][2][2] = temp[0][2]
        self.matrix[matrix_num][0][1] = temp[1][0]
        self.matrix[matrix_num][2][1] = temp[1][2]
        self.matrix[matrix_num][0][0] = temp[2][0]
        self.matrix[matrix_num][1][0] = temp[2][1]
        self.matrix[matrix_num][2][0] = temp[2][2]

    # Rotates matrix counterclockwise
    def counterclockwise(self, matrix_num):
        temp = self.matrix[matrix_num]
        self.matrix[matrix_num][0][0] = temp[0][2]
        self.matrix[matrix_num][0][1] = temp[1][2]
        self.matrix[matrix_num][0][2] = temp[2][2]
        self.matrix[matrix_num][1][0] = temp[0][1]
        self.matrix[matrix_num][1][2] = temp[2][1]
        self.matrix[matrix_num][2][0] = temp[0][0]
        self.matrix[matrix_num][2][1] = temp[1][0]
        self.matrix[matrix_num][2][2] = temp[2][0]

    def ai_in(ai_in):
        place(ai_in[0])
        rotate(ai_in[1])

    def printBoard(self):
        string = ""
        # Iterating through top two matricies, row by row.
        for row in range(0,2):
            for matrix in range(0,1):
                for column in range(0,2):
                    curr = self.matrix[matrix][row][column]
                    if curr == 0:
                        string += self.empty + " "
                    elif curr == 1:
                        string += self.p1 + " "
                    elif curr == 2:
                        string += self.p2 + " "

        print(string)
