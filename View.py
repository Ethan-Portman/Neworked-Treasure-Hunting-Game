from Board import Board


def display(board: Board) -> str:
    """
    Prints the String representation of the game_board to the console
    :param board: The Board object
    """
    output_str = "\n    Current Board\n"
    for row in board.game_board:
        output_str += "      "
        for square in row:
            output_str += str(square) + ' '
        output_str += '\n'
    output_str += '__________________________\n'
    print(output_str)
    return output_str
