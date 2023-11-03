import constants
from Player import Player
from Treasure import Treasure


class Tile:
    """
    The Tile class represents a tile on the game board. A tile can contain a player or a treasure.
    """
    def __init__(self, row, col, description=constants.TILE_DESCRIPTION):
        """
        Initialize a Tile object with the given coordinates and description.
        A Tile is initialized with no treasure and no player.
        :param row: The Y-coordinate of the Tile.
        :param col: The X-coordinate of the Tile.
        :param description: The Description of the Tile.
        :raises ValueError: If either row or col are less than 0 of the description is an empty string.
        """
        if len(description) < 1:
            raise ValueError("Tile description must have at least one character")
        if row < 0 or col < 0:
            raise ValueError("Coordinates must be above 0.")
        self.description = description
        self.coordinates = (row, col)
        self.treasure = None
        self.player = None

    def __str__(self) -> str:
        """
        The tile prints out one property in the following priority:
          - Player, Treasure, Description
        :return The string representation of the tile.
        """
        if self.player is not None:
            return self.player.get_name()
        if self.treasure is not None:
            return self.treasure.get_description()
        return self.description

    def add_treasure(self, treasure: Treasure) -> None:
        """
        Add the specified treasure to the tile.
        :param treasure: The Treasure Object to be added onto the Tile.
        """
        self.treasure = treasure

    def remove_treasure(self) -> None:
        """Remove a treasure on the tile, if any."""
        self.treasure = None

    def get_treasure(self) -> Treasure:
        """
        Retrieve the treasure on the tile, if any.
        :return: The treasure on the Tile.
        """
        return self.treasure

    def add_player(self, player: Player) -> None:
        """
        Add the specified player to the tile.
        :param player: A Player object ot be added onto the Tile.
        """
        self.player = player

    def remove_player(self) -> None:
        """Remove a player on the tile, if any."""
        self.player = None

    def get_player(self) -> Player:
        """
        Retrieve the player on the tile, if any.
        :return: The PLayer object on the Tile.
        """
        return self.player

    def get_coordinates(self) -> tuple[int, int]:
        """
        Retrieve the coordinates of the tile.
        :return: A tuple in the format (row, col)
        """
        return self.coordinates
