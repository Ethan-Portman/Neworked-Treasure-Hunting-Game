from Board import Board


def display(board: Board) -> str:
    """
    Prints the String representation of the game_board to the console
    :param board: The Board object
    """
    output_str = ""
    for row in board.game_board:
        for square in row:
            output_str += str(square) + " "
        output_str += '\n'
    print(output_str)
    return output_str




