from Player import Player


class Tile:
    def __init__(self, description='.', treasure=None):
        self.description = description
        self.player = None
        self.treasure = treasure

    def __str__(self):
        if self.player is not None:
            return self.player.name
        if self.treasure is not None:
            return self.treasure.description
        return self.description
