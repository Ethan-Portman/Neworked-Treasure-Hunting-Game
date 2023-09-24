from Player import Player
from Treasure import Treasure


class Tile:
    def __init__(self, description="."):
        if len(description) < 1:
            raise ValueError("Tile description must have at least one character")
        self.description = description
        self.treasure = None
        self.player = None

    def __str__(self):
        if self.player is not None:
            return self.player.name
        if self.treasure is not None:
            return self.treasure.description
        return self.description

    def set_description(self, description: str):
        if len(description) < 1:
            raise ValueError("Tile description must have at least one character")
        self.description = description

    def get_description(self):
        return self.description

    def add_treasure(self, treasure: Treasure):
        self.treasure = treasure

    def get_treasure(self):
        return self.treasure

    def remove_treasure(self):
        self.treasure = None

    def add_player(self, player: Player):
        self.player = player

    def get_player(self):
        return self.player

    def remove_player(self):
        self.player = None

