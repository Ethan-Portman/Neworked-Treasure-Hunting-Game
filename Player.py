class Player:
    """
    The player class represents a user in the game. A player can move around the game board collecting
    treasure from the tiles.
    """
    def __init__(self, coordinates: tuple[int, int], name="unknown", score=0):
        """
        Initialize a player with a given name, score, and starting coordinates on the board.
        :param coordinates: (row, col) A tuple containing Y(row) and X(col) coordinates of the player on the board.
        :param name: The name of the player.
        :param score: The score of the player
        :raises ValueError: If name is an empty string, score is negative, or either row or col are negative.
        """
        if score < 0:
            raise ValueError("Player cannot have a negative score")
        if len(name) < 1:
            raise ValueError("Player name must be at least one character")
        if coordinates[0] < 0 or coordinates[1] < 0:
            raise ValueError("Player coordinates must be greater than 0.")
        self.name = name
        self.score = score
        self.coordinates = coordinates

    def get_name(self) -> str:
        """
        Retrieves the name of the player.
        :return: Name of the player.
        """
        return self.name

    def set_name(self, name: str) -> None:
        """
        Sets the name of the player to the specified string.
        :param name: The new name of the player
        :raises ValueError: If the new name of the player is an empty string.
        """
        if len(name) < 1:
            raise ValueError("Player name must be at least one character")
        self.name = name

    def get_score(self) -> int:
        """
        Retrieves the score of the player.
        :return: Score of the player.
        """
        return self.score

    def add_points(self, points) -> None:
        """
        Adds the specified amount of points to the players score.
        :param points: The points to be added to the player's score.
        :raises ValueError: If the points to add are below 0.
        """
        if points < 0:
            raise ValueError("Value for points must be a positive number")
        self.score += points

    def set_coordinates(self, coordinates: tuple[int, int]) -> None:
        """
        Sets the players position to the specified coordinates.
        :param coordinates: Tuple in the format (row, col)
        :raises ValueError: If either row or col are below 0.
        """
        if coordinates[0] < 0 or coordinates[1] < 0:
            raise ValueError("Player coordinates must be greater than 0")
        self.coordinates = coordinates

    def get_coordinates(self) -> tuple[int, int]:
        """
        Retrieves the coordinates of the player.
        :return: Coordinates: A tuple in the format (row, col)
        """
        return self.coordinates
