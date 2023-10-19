class Player:
    """
    The player class represents a user in the game. A player can move around the game board collecting
    treasure from the tiles.
    """
    def __init__(self, coordinates: tuple[int, int], name="unknown", score=0):
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
        """Retrieves the name of the player."""
        return self.name

    def set_name(self, name: str) -> None:
        """Sets the name of the player to the specified string."""
        if len(name) < 1:
            raise ValueError("Player name must be at least one character")
        self.name = name

    def get_score(self) -> int:
        """Retrieves the score of the player."""
        return self.score

    def add_points(self, points) -> None:
        """Adds the specified amount of points to the players score."""
        if points < 0:
            raise ValueError("Value for points must be a positive number")
        self.score += points

    def set_coordinates(self, coordinates: tuple[int, int]):
        """Sets the players position to the specified coordinates."""
        if coordinates[0] < 0 or coordinates[1] < 0:
            raise ValueError("Player coordinates must be greater than 0")
        self.coordinates = coordinates

    def get_coordinates(self) -> tuple[int, int]:
        """Retrieves the position of the player."""
        return self.coordinates
