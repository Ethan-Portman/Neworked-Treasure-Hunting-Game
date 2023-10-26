from Board import Board


def display(board: Board) -> str:
    """
    Generates, prints, and returns the  String representation of the game-board.
    :param board: The Board object
    :return: The String representation of the game-board.
    """
    output_str = ""
    for row in board.game_board:
        for square in row:
            output_str += str(square) + " "
        output_str += '\n'
    print(output_str)
    return output_str
