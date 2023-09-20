from Board import Board


def display(board: Board):
    output_str = ""
    for row in board.game_board:
        for square in row:
            output_str += str(square)
        output_str += '\n'

    print(output_str)

