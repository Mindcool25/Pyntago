#!/usr/bin/env python

import game

g = game.pentago()
g.print_board()
g.place("d1")
g.print_board()
g.rotate("4")
g.print_board()
print(g.check_win())
