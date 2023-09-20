import random
import sys

from Tile import Tile
from Player import Player
from Treasure import Treasure


class Board:

    # ---------------------------------------------- CONSTRUCTORS ------------------------------------------------------
    def __init__(self, length: int, num_treasures: int, min_treasure: int, max_treasure: int):
        self.length = length
        self.num_treasures = num_treasures
        self.min_treasure = min_treasure
        self.max_treasure = max_treasure
        self.game_board = self.create_board()
        self.populate_board_with_treasure()

    def create_board(self) -> list[list[Tile]]:
        """
        Creates a 2D List to be used as the game-board
        :return: A 2D List of Tiles representing the game-board
        """
        board = [[Tile() for _ in range(self.length)] for _ in range(self.length)]
        return board

    # ------------------------------------------ LOGIC FOR ADDING TREASURE ---------------------------------------------
    def populate_board_with_treasure(self) -> None:
        """
        Inserts num_treasures amount of treasure randomly across the board.
        Treasure is between min_treasure and max_treasure (inclusive)
        """
        for _ in range(self.num_treasures):
            treasure = self.generate_treasure()
            y, x = self.get_square_free_of_treasure()
            self.game_board[y][x].treasure = treasure

    def get_square_free_of_treasure(self) -> tuple[int, int]:
        """
        Retrieves the coordinates of a Tile with no treasure
        :return: The coordinates of a Tile with no treasure
        """
        while True:
            y = random.randint(0, self.length - 1)
            x = random.randint(0, self.length - 1)
            if self.game_board[y][x].treasure is None:
                return y, x

    def generate_treasure(self) -> Treasure:
        """
        Creates a treasure object with a random value between min_treasure
        and max_treasure (inclusive)
        :return: The newly generated treasure
        """
        value = random.randint(self.min_treasure, self.max_treasure)
        return Treasure(value)

    # ------------------------------------------ LOGIC FOR ADDING PLAYER -----------------------------------------------
    def add_player(self, name: str) -> None:
        """
        Adds a player to a random position on the board free of treasure or player
        :param name: Name of the player to be added to the board
        """
        y, x = self.get_square_free_of_treasure_and_player()
        new_player = Player(name)
        self.game_board[y][x].player = new_player

    def get_square_free_of_treasure_and_player(self) -> tuple[int, int]:
        """
        Retrieves the coordinates of a Tile that is free of both treasure and player
        :return: The coordinates of a tile with no treasure or player
        """
        while True:
            y, x = self.get_square_free_of_treasure()
            if self.game_board[y][x].player is None:
                return y, x

    # -------------------------------------- LOGIC FOR MOVING  PLAYER --------------------------------------------------
    def move_player(self, name: str, direction: str) -> None:
        """
        Moves a player on the board to a new position. If there is treasure on the new position
        the player picks it up
        :param name: Name of the player to be moved
        :param direction: The direction that the player will move
        """
        # Find and retrieve the position of the player that will be moved
        old_y, old_x = self.find_player(name)

        # Get a valid direction for the player to be moved
        direction = self.get_valid_movement_direction(name, old_y, old_x, direction)

        # Get the position of the new coordinate
        new_y, new_x = self.get_new_coordinates(old_y, old_x, direction)

        # Update the player to the new position on the board
        self.update_player_position(name, old_y, old_x, new_y, new_x)

        # Check and collect treasure on the new position
        self.collect_treasure(name, new_y, new_x)

    def find_player(self, name: str) -> tuple[int, int]:
        """
        Retrieves the coordinates of a player
        :param name: The name of the player to be retrieved
        :return: The coordinates of the player
        """
        y = 0
        for row in self.game_board:
            x = 0
            for square in row:
                if square.player is not None and square.player.name is name:
                    return y, x
                x += 1
            y += 1

    def get_valid_movement_direction(self, name: str, y: int, x: int, direction: str) -> str:
        """
        Gets a valid input for the movement of a player.
        :param name: The player to be moved
        :param y: The current y coordinate of the player
        :param x: The current x coordinate of the player
        :param direction: The direction the player is trying to move
        :return: A valid direction the player will move
        """
        while True:
            valid_direction = self.is_valid_movement(name, y, x, direction)
            if valid_direction:
                return direction
            else:
                print("Invalid Input.")
                direction = input("Try again: ").upper()

    def is_valid_movement(self, name: str, y: int, x: int, direction: str) -> bool:
        """
        Validates if the entered direction is a valid input
        :param name: The player to be moved
        :param y: The current y coordinate of the player
        :param x: The current x coordinate of the player
        :param direction: The direction the player will move
        :return: If the direction is valid or not
        """
        match direction:
            case 'U' if y > 0:
                return True
            case 'D' if y < self.length - 1:
                return True
            case 'L' if x > 0:
                return True
            case 'R' if x < self.length - 1:
                return True
            case 'Q':
                return True
            case _:
                return False

    def get_new_coordinates(self, y: int, x: int, direction: str) -> tuple[int, int]:
        """
        Gets the coordinates of the player after the movement or quits the program depending on
        the direction
        :param y: The current y coordinate before the move
        :param x: The current x coordinate before the move
        :param direction: The direction of movement
        :return: The coordinates after the move
        """
        match direction:
            case 'U':
                y -= 1
            case 'D':
                y += 1
            case 'L':
                x -= 1
            case 'R':
                x += 1
            case 'Q':
                self.quit_application()
        return y, x

    def update_player_position(self, name: str, old_y: int, old_x: int, new_y: int, new_x: int) -> None:
        """
        Moves a player from one tile to a different tile
        :param name: The name of the player to be moved
        :param old_y: The old y coordinate of the player
        :param old_x: The old x coordinate of the player
        :param new_y: The new y coordinate of the player
        :param new_x: The new x coordinate of the player
        """
        self.game_board[new_y][new_x].player = self.game_board[old_y][old_x].player
        self.game_board[old_y][old_x].player = None

    def collect_treasure(self, name: str, y: int, x: int):
        """
        Searches tile for treasure. If there is a treasure it adds the value to the player and removes the
        treasure from the game board
        :param name: The name of the player that is searching/ collecting the treasure
        :param y: The y coordinate that the player is searching
        :param x: The x coordinate that the player is searching
        """
        player = self.game_board[y][x].player
        treasure = self.game_board[y][x].treasure
        if treasure is not None:
            value = treasure.value
            player.add_points(value)
            print(f"Player {name} has just collected {value} points\nTheir new score is {player.get_score()}")
            self.game_board[y][x].treasure = None
            self.num_treasures -= 1

    # ---------------------------------------- LOGIC FOR ENDING GAME  --------------------------------------------------

    def quit_application(self):
        """
        Exits the program early if a player has chosen 'quit' for their movement option
        """
        print("Goodbye")
        sys.exit()

    def display_results(self, name_1: str, name_2: str):
        player_1_y, player_1_x = self.find_player(name_1)
        player_2_y, player_2_x = self.find_player(name_2)

        player_1_score = self.game_board[player_1_y][player_1_x].player.get_score()
        player_2_score = self.game_board[player_2_y][player_2_x].player.get_score()

        print('Player 1 Score: ' + player_1_score)

