#!/usr/bin/python3
from Game import Game

"""
COMMANDS
Get Board: echo -n 'F0' | xxd -r -p | nc 127.0.0.1 12345
echo -n 'F0' | xxd -r -p | nc 10.21.75.15 12345 | xxd

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



def parse_board(board_str: str) -> [[str]]:
    print("PARSING BOARD INPUT")
    print(board_str)
    rows = board_str.split('\n')
    # Remove any empty rows at the end
    while rows and not rows[-1]:
        rows.pop()
    board = []
    for row in rows:
        cells = list(row)
        board.append(cells)
    # print("PARSING BOARD OUTPUT")
    # print(board)
    # print("DONE")
    return board
