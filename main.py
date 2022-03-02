#!/usr/bin/env python

import game

g = game.pentago()
g.printBoard()
g.place("d1")
g.printBoard()
g.rotate("-4")
g.printBoard()