#!/usr/bin/python3
from Game import Game

"""
COMMANDS
Get Board: echo -n 'F0' | xxd -r -p | nc 127.0.0.1 12345
Quit Game: echo -n '00' | xxd -r -p | nc 127.0.0.1 12345

Player 1:
  UP: echo -n '24' | xxd -r -p | nc 127.0.0.1 12345 | xxd
  DOWN: echo -n '34' | xxd -r -p | nc 127.0.0.1 12345 | xxd
  LEFT: echo -n '44' | xxd -r -p | nc 127.0.0.1 12345 | xxd
  RIGHT: echo -n '64' | xxd -r -p | nc 127.0.0.1 12345 | xxd

Player 2: 
  UP: echo -n '28' | xxd -r -p | nc 127.0.0.1 12345 | xxd
  DOWN: echo -n '38' | xxd -r -p | nc 127.0.0.1 12345 | xxd
  LEFT: echo -n '48' | xxd -r -p | nc 127.0.0.1 12345 | xxd
  RIGHT: echo -n '68' | xxd -r -p | nc 127.0.0.1 12345 | xxd
"""

g = Game()
g.start()
