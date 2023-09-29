#!/usr/bin/python3
from Board import Board
import View

PLAYER_ONE_NAME = "1"
PLAYER_TWO_NAME = "2"
BOARD_LENGTH = 5
NUM_TREASURES = 10
MIN_TREASURE = 1
MAX_TREASURE = 5

game_board = Board(BOARD_LENGTH, NUM_TREASURES, MIN_TREASURE, MAX_TREASURE)
game_board.add_player(PLAYER_ONE_NAME)
game_board.add_player(PLAYER_TWO_NAME)
View.display(game_board)


while game_board.num_treasures > 0:
    player_one_move = input(f"{PLAYER_ONE_NAME} Move:\n(U)p (L)eft (R)ight (D)own (Q)uit? ").upper()
    game_board.move_player(PLAYER_ONE_NAME, player_one_move)
    View.display(game_board)

    if game_board.num_treasures > 0:
        player_two_move = input(f"{PLAYER_TWO_NAME} Move:\n(U)p (L)eft (R)ight (D)own (Q)uit? ").upper()
        game_board.move_player(PLAYER_TWO_NAME, player_two_move)
        View.display(game_board)

game_board.display_results(PLAYER_ONE_NAME, PLAYER_TWO_NAME)

