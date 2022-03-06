#!/usr/bin/env python

import game


matrix = [
    [0, 0, 0,  0, 0, 0],
    [0, 0, 0,  0, 0, 0],
    [0, 0, 0,  0, 0, 0],

    [0, 0, 0,  0, 0, 0],
    [0, 0, 0,  0, 0, 0],
    [0, 0, 0,  0, 0, 0]
    ]

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

def testRotation():
    r = game.pentago()
    goal = [[0, 0, 1,  0, 0, 1],
            [0, 0, 0,  0, 0, 0],
            [0, 0, 0,  0, 0, 0],

            [0, 0, 1,  0, 0, 1],
            [0, 0, 0,  0, 0, 0],
            [0, 0, 0,  0, 0, 0]]
    r.place("a1")
    r.place("b1")
    r.place("c1")
    r.place("d1")
    r.rotate("1")
    r.rotate("2")
    r.rotate("3")
    r.rotate("4")
    if goal == r.matrix:
        del r
        return "Passed"
    else:
        print(r.matrix)
        r.print_board()
        del r
        return "Failed"


def main():
    print("Testing Placements: " + testPlace())
    print("Testing Rotations: " + testRotation())
    return

if __name__ == "__main__":
    main()
