#!/usr/bin/env python

import game

# Testing placements
def testPlace():
    p = game.pentago()
    goal = [[0, 1, 0,  0, 0, 0],
            [0, 0, 0,  0, 1, 0],
            [0, 0, 0,  0, 0, 0],

            [1, 0, 0,  0, 0, 0],
            [0, 0, 0,  0, 0, 0],
            [0, 0, 0,  0, 0, 1]]
    p.place("a2")
    p.place("b5")
    p.place("c1")
    p.place("d9")
    if goal == p.matrix:
        del p
        return "Passed"
    else:
        del p
        return "Failed"

# Testing for rotation issues, clockwise and counterclockwise
def testRotation():
    r = game.pentago()
    goal = [[0, 0, 1,  0, 0, 1],
            [0, 0, 0,  0, 0, 0],
            [0, 0, 0,  0, 0, 0],

            [0, 0, 0,  0, 0, 0],
            [0, 0, 0,  0, 0, 0],
            [1, 0, 0,  1, 0, 0]]
    r.place("a1")
    r.place("b1")
    r.place("c1")
    r.place("d1")
    r.rotate("1")
    r.rotate("2")
    r.rotate("-3")
    r.rotate("-4")
    if goal == r.matrix:
        del r
        return "Passed"
    else:
        print(r.matrix)
        r.print_board()
        del r
        return "Failed"

# Testing win condition
def testWin():
    results = ""
    w = game.pentago()
    m = [[1, 1, 1,  1, 1, 0],
         [0, 0, 0,  0, 0, 0],
         [0, 0, 0,  0, 0, 0],
         [0, 0, 0,  0, 0, 0],
         [0, 0, 0,  0, 0, 0],
         [0, 0, 0,  0, 0, 0]]
    w.matrix = m
    white_win, black_win = w.check_win()
    if white_win == True:
        results += "Testing p1 Win: Passed\n"
    else:
        results += "Testing p1 Win: Failed\n"
    m = [[2, 2, 2,  2, 2, 0],
         [0, 0, 0,  0, 0, 0],
         [0, 0, 0,  0, 0, 0],
         [0, 0, 0,  0, 0, 0],
         [0, 0, 0,  0, 0, 0],
         [0, 0, 0,  0, 0, 0]]
    w.matrix = m
    white_win, black_win = w.check_win()
    if black_win == True:
        results += "Testing p2 Win: Passed\n"
    else:
        results += "Testing p2 Win: Failed\n"
    m = [[1, 2, 2,  2, 2, 0],
         [0, 1, 0,  0, 0, 0],
         [0, 0, 1,  0, 0, 0],
         [0, 0, 0,  1, 0, 0],
         [0, 0, 0,  0, 1, 0],
         [0, 0, 0,  0, 0, 0]]
    w.matrix = m
    white_win, black_win = w.check_win()
    if white_win == True:
        results += "Testing Diagonal Win: Passed\n"
    else:
        results += "Testing Diagonal Win: Failed\n"



    return results


def main():
    print("Testing Placements: " + testPlace())
    print("Testing Rotations: " + testRotation())
    print(testWin())
    return

if __name__ == "__main__":
    main()
