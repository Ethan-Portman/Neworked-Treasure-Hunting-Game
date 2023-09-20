from Board import Board
import View

# Create the Game Board
game_board = Board(5, 10, 1, 5)
game_board.add_player('😎')
# game_board.add_player('👿')
View.display(game_board)


while game_board.num_treasures > 0:
    one_move = input('😎\n(U)p (L)eft (R)ight (D)own (Q)uit? ').upper()
    game_board.move_player('😎', one_move)
    View.display(game_board)

    # two_move = input('👿\n(U)p (L)eft (R)ight (D)own (Q)uit? ')
    # game_board.move_player('👿', one_move)
    # View.display(game_board)



