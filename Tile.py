from Player import Player
from Treasure import Treasure

TILE_DESCRIPTION = "."


class Tile:
    """
    The Tile class represents a tile on the game board. A tile can contain a player or a treasure.
    """
    def __init__(self, y_pos, x_pos, description=TILE_DESCRIPTION):
        if len(description) < 1:
            raise ValueError("Tile description must have at least one character")
        if y_pos < 0 or x_pos < 0:
            raise ValueError("Coordinates must be above 0.")
        self.description = description
        self.coordinates = (y_pos, x_pos)
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
        """Add the specified treasure to the tile."""
        self.treasure = treasure

    def remove_treasure(self) -> None:
        """Remove a treasure on the tile, if any."""
        self.treasure = None

    def get_treasure(self) -> Treasure:
        """Retrieve the treasure on the tile, if any."""
        return self.treasure

    def add_player(self, player: Player) -> None:
        """Add the specified player to the tile."""
        self.player = player

    def remove_player(self) -> None:
        """Remove a player on the tile, if any."""
        self.player = None

    def get_player(self) -> Player:
        """Retrieve the player on the tile, if any."""
        return self.player

    def get_coordinates(self) -> tuple[int, int]:
        """Retrieve the coordinates of the tile."""
        return self.coordinates
