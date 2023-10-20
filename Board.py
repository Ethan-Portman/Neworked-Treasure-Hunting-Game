import random
import sys

from Tile import Tile
from Player import Player
from Treasure import Treasure


class Board:
    def __init__(self, length: int, num_treasures: int, min_treasure: int, max_treasure: int):
        self.length = length
        self.num_treasures = num_treasures
        self.min_treasure = min_treasure
        self.max_treasure = max_treasure
        self.validate_board()
        self.game_board = self.create_game_board()
        self.populate_board_with_treasure()
        self.players = []

    def validate_board(self):
        """
        Validates the initial parameters for the game_board, ensuring they meet Requirements.
        Throws a ValueError if requirements are not met.
        """
        if self.length < 2 or self.length > 50:
            raise ValueError("Length of board must be between 2 and 50")
        if self.num_treasures < 0 or self.num_treasures > (self.length * self.length):
            raise ValueError("Number of treasures must be between 0 and length x length")
        if self.min_treasure < 1 or self.min_treasure > 100:
            raise ValueError("Minimum Treasure must be between 1 and 100")
        if self.max_treasure < self.min_treasure or self.max_treasure > 1000:
            raise ValueError("Maximum Treasure must be between minimum Treasure and a 1000")

    # -------------------------------- CREATE/ SETUP GAME-BOARD AND BASIC METHODS  -------------------------------------
    def create_game_board(self) -> list[list[Tile]]:
        """
        Creates a 2D List of Tiles to be used as the game-board
        :return: A 2D List of Tiles representing the game-board
        """
        return [[Tile(y_pos, x_pos) for x_pos in range(self.length)] for y_pos in range(self.length)]

    def populate_board_with_treasure(self) -> None:
        """
        Inserts num_treasures amount of treasure randomly across the board.
        Treasure Value is between min_treasure and max_treasure (inclusive)
        """
        for _ in range(self.num_treasures):
            tile = self.find_empty_tile()
            tile.add_treasure(Treasure(random.randint(self.min_treasure, self.max_treasure)))

    def find_empty_tile(self) -> Tile:
        """
        Retrieves a Tile that is free of both treasure and player
        :return: The Tile Object
        """
        while True:
            y_pos, x_pos = random.randint(0, self.length - 1), random.randint(0, self.length - 1)
            tile = self.game_board[y_pos][x_pos]
            if tile.get_treasure() is None and tile.get_player() is None:
                return tile

    def add_player_to_game_board(self, player_name: str) -> None:
        """
        Adds a player to a random empty tile on the board
        :param player_name: Name of the player to be added to the board
        """
        tile = self.find_empty_tile()
        new_player = Player(tile.get_coordinates(), player_name)

        self.players.append(new_player)
        tile.add_player(new_player)

    def find_player_by_name(self, player_name: str) -> Player:
        """
        Fetches a player on the board
        :param player_name: The name of the player to be fetched
        :return: The Player Object
        """
        for player in self.players:
            if player.name == player_name:
                return player
        raise ValueError("Error: Player not Found")

    # ---------------------------------- MOVEMENT & COLLECTING TREASURE ------------------------------------------------
    def move_player_on_board(self, player_name: str, direction: str) -> None:
        """
        Moves a player to a new Tile and collects Treasure
        :param player_name: Name of the player to be moved
        :param direction: The direction that the player will move
        """
        if self.is_valid_movement(player_name, direction):
            dst_tile = self.get_tile_after_player_move(player_name, direction)
            self.move_player_to_tile(player_name, dst_tile)
            self.collect_treasure_from_tile(player_name, dst_tile)

    def is_valid_movement(self, player_name: str, direction: str) -> bool:
        """
        Validates whether the direction for the player is executable
        :param player_name: The player to be moved
        :param direction: The direction the player is trying to move
        :return: If the direction is valid or not
        """
        curr_y, curr_x = self.find_player_by_name(player_name).get_coordinates()
        try:
            match direction:
                case 'U' if curr_y > 0 and self.game_board[curr_y - 1][curr_x].get_player() is None:
                    return True
                case 'D' if curr_y < self.length - 1 and self.game_board[curr_y + 1][curr_x].player is None:
                    return True
                case 'L' if curr_x > 0 and self.game_board[curr_y][curr_x - 1].player is None:
                    return True
                case 'R' if curr_x < self.length - 1 and self.game_board[curr_y][curr_x + 1].player is None:
                    return True
                case 'Q':
                    self.get_results()
                    self.quit_application()
                case _:
                    raise ValueError("Invalid input")
        except ValueError as details:
            print(details)
            return False

    def get_tile_after_player_move(self, player_name: str, direction: str) -> Tile:
        """
        Retrieves the tile that the player will move to.
        :param player_name: The name of the player to be moved
        :param direction: The direction of movement
        :return: The Tile Object
        """
        y_pos, x_pos = self.find_player_by_name(player_name).get_coordinates()
        match direction:
            case 'U': y_pos -= 1
            case 'D': y_pos += 1
            case 'L': x_pos -= 1
            case 'R': x_pos += 1
        return self.game_board[y_pos][x_pos]

    def move_player_to_tile(self, player_name: str, tile: Tile) -> None:
        """
        Moves a player onto a different tile
        :param player_name: The name of the player to be moved
        :param tile: The Tile the player will be moved to
        """
        player = self.find_player_by_name(player_name)
        old_y, old_x = player.get_coordinates()

        player.set_coordinates(tile.get_coordinates())  # Change player coordinates
        tile.add_player(player)  # Copy player to tile
        self.game_board[old_y][old_x].remove_player()  # Remove player from old tile

    def collect_treasure_from_tile(self, player_name: str, tile: Tile) -> None:
        """
        Searches tile for treasure and adds the treasure's value to the players score. It then removes the treasure.
        :param player_name: The name of the player searching for treasure
        :param tile: The Tile that is being searched
        """
        treasure = tile.get_treasure()
        if treasure is not None:
            player = self.find_player_by_name(player_name)
            player.add_points(treasure.get_value())
            print(f"{player_name} has collected {treasure.get_value()} points\nTheir new score is {player.get_score()}")
            tile.remove_treasure()
            self.num_treasures -= 1

    # --------------------------------------------- END THE GAME -------------------------------------------------------
    @staticmethod
    def quit_application() -> None:
        """
        Exits the program
        """
        print("Goodbye")
        sys.exit()

    def get_results(self) -> str:
        if len(self.players) == 0:
            return "Nobody was playing."

        top_score = max([p.get_score() for p in self.players])
        winners = [p for p in self.players if p.get_score == top_score]

        results = "\n".join(f"{p.get_name()} final score: {p.get_score()}" for p in self.players)
        results += f"\n{winners[0].get_name()} wins!\n" if len(winners) == 1 else "\nTie game!\n"

        print(results)
        return results
