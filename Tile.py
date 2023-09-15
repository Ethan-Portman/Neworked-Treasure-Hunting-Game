from Treasure import Treasure

class Tile:
    def __init__(self, description: str='.', treasure: Treasure=None):
        self.description = description
        self.treasure = treasure
