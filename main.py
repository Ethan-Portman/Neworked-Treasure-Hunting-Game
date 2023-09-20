#!/usr/bin/python3
from Board import Board
import View


# Create the Game Board
game_board = Board(5, 10, 1, 5)

# Add the players to the Game Board
game_board.add_player('1')
# game_board.add_player('2')

# View the Game Board
View.display(game_board)


while game_board.num_treasures > 0:
    one_move = input('Player 1 Move:\n(U)p (L)eft (R)ight (D)own (Q)uit? ').upper()
    game_board.move_player('1', one_move)
    View.display(game_board)

    # two_move = input('2\n(U)p (L)eft (R)ight (D)own (Q)uit? ')
    # game_board.move_player('2', one_move)
    # View.display(game_board)

