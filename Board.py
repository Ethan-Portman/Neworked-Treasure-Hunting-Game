import random
import sys

from Tile import Tile
from Player import Player
from Treasure import Treasure


class Board:

    # ---------------------------------------------- CONSTRUCTOR -------------------------------------------------------
    def __init__(self, length: int, num_treasures: int, min_treasure: int, max_treasure: int):
        self.length = length
        self.num_treasures = num_treasures
        self.min_treasure = min_treasure
        self.max_treasure = max_treasure
        self.game_board = self.create_board()
        self.populate_board_with_treasure()

    # ------------------------------ CREATE GAME-BOARD AND POPULATE WITH TREASURE --------------------------------------
    def create_board(self) -> list[list[Tile]]:
        """
        Creates a 2D List to be used as the game-board
        :return: A 2D List of Tiles representing the game-board
        """
        board = [[Tile() for _ in range(self.length)] for _ in range(self.length)]
        return board

    def populate_board_with_treasure(self) -> None:
        """
        Inserts num_treasures amount of treasure randomly across the board.
        Treasure is between min_treasure and max_treasure (inclusive)
        """
        for _ in range(self.num_treasures):
            treasure = self.generate_treasure()
            y, x = self.get_square_free_of_treasure()
            self.game_board[y][x].treasure = treasure

    def generate_treasure(self) -> Treasure:
        """
        Creates a treasure object with a random value between min_treasure
        and max_treasure (inclusive)
        :return: The newly generated treasure
        """
        value = random.randint(self.min_treasure, self.max_treasure)
        return Treasure(value)

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

    # --------------------------------------- ADD PLAYERS TO THE BOARD -------------------------------------------------
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

    # ------------------------------------- FIND A PLAYER ON THE BOARD -------------------------------------------------
    def find_player(self, name: str) -> Player:
        """
        Retrieves a player on the board
        :param name: The name of the player to be retrieved
        :return: The player
        """
        y, x = self.find_player_coordinates(name)
        return self.game_board[y][x].player

    def find_player_coordinates(self, name: str) -> tuple[int, int]:
        """
        Retrieves the coordinates of a player on the board
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

    # ------------------------------------ MOVE A PLAYER ON THE BOARD --------------------------------------------------
    def move_player(self, name: str, direction: str) -> None:
        """
        Moves a player on the board to a new position. If there is treasure on the new position
        the player picks it up
        :param name: Name of the player to be moved
        :param direction: The direction that the player will move
        """
        # Get a valid direction for the player to move
        direction = self.get_valid_direction(name, direction)

        # Get the new coordinates after the movement
        new_y, new_x = self.get_new_coordinates(name, direction)

        # Update the player to the new coordinates
        self.update_player_position(name, new_y, new_x)

        # Search and collect treasure on the new coordinates
        self.collect_treasure(name, new_y, new_x)

    def get_valid_direction(self, name: str, direction: str) -> str:
        """
        Gets a valid input for the movement of a player.
        :param name: The player to be moved
        :param direction: The direction the player is trying to move
        :return: A valid direction the player will move
        """
        while True:
            valid_direction = self.is_valid_direction(name, direction)
            if valid_direction:
                return direction
            else:
                direction = input("Try again: ").upper()

    def is_valid_direction(self, name: str, direction: str) -> bool:
        """
        Validates if the entered direction is a valid input
        :param name: The player to be moved
        :param direction: The direction the player will move
        :return: If the direction is valid or not
        """
        curr_y, curr_x = self.find_player_coordinates(name)
        try:
            match direction:
                case 'U':
                    if curr_y > 0:
                        if self.game_board[curr_y - 1][curr_x].player is not None:
                            raise ValueError(f"{name} cannot go up. There is a player in the way.")
                        return True
                    else:
                        raise ValueError(f"{name} cannot go up. There is a wall in the way.")
                case 'D':
                    if curr_y < self.length - 1:
                        if self.game_board[curr_y + 1][curr_x].player is not None:
                            raise ValueError(f"{name} cannot go down. There is a player in the way.")
                        return True
                    else:
                        raise ValueError(f"{name} cannot go down. There is a wall in the way.")
                case 'L':
                    if curr_x > 0:
                        if self.game_board[curr_y][curr_x - 1].player is not None:
                            raise ValueError(f"{name} cannot go left. There is a player in the way.")
                        return True
                    else:
                        raise ValueError(f"{name} cannot go left. There is a wall in the way.")
                case 'R':
                    if curr_x < self.length - 1:
                        if self.game_board[curr_y][curr_x + 1].player is not None:
                            raise ValueError(f"{name} cannot go right. There is a player in the way.")
                        return True
                    else:
                        raise ValueError(f"{name} cannot go right. There is a wall in the way.")
                case 'Q':
                    self.display_results('1', '2')
                    return True
                case _:
                    raise ValueError("Invalid input")
        except ValueError as details:
            print(str(details))

    def get_new_coordinates(self, name: str, direction: str) -> tuple[int, int]:
        """
        Retrieves the new coordinates of the player after their move or quits the program depending on
        the direction entered
        :param name: The name of the player to be moved
        :param direction: The direction of movement
        :return: The coordinates after the move
        """
        y, x = self.find_player_coordinates(name)
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

    def update_player_position(self, name: str, new_y: int, new_x: int) -> None:
        """
        Moves a player from one tile to a different tile
        :param name: The name of the player to be moved
        :param new_y: The new y coordinate of the player
        :param new_x: The new x coordinate of the player
        """
        player = self.find_player(name)
        old_y, old_x = self.find_player_coordinates(name)

        self.game_board[new_y][new_x].player = player
        self.game_board[old_y][old_x].player = None

    def collect_treasure(self, name: str, y: int, x: int):
        """
        Searches tile for treasure. If there is a treasure it adds the value to the player and removes the
        treasure from the game board
        :param name: The name of the player that is searching/ collecting the treasure
        :param y: The y coordinate that the player is searching
        :param x: The x coordinate that the player is searching
        """
        player = self.find_player(name)
        treasure = self.game_board[y][x].treasure
        if treasure is not None:
            value = treasure.get_value()
            player.add_points(value)
            print(f"Player {name} has just collected {value} points\nTheir new score is {player.get_score()}")
            self.game_board[y][x].treasure = None
            self.num_treasures -= 1

    # --------------------------------------------- END THE GAME -------------------------------------------------------
    def quit_application(self):
        """
        Exits the program early if a player has chosen 'quit' for their movement option
        """
        print("Goodbye")
        sys.exit()

    def display_results(self, name_1: str, name_2: str):
        player_1 = self.find_player(name_1)
        player_2 = self.find_player(name_2)

        print(f"{player_1.get_name()} final score: {player_1.get_score()}")
        print(f"{player_2.get_name()} final score: {player_2.get_score()}")

        if player_1.get_score() > player_2.get_score():
            print(f"{player_1.get_name()} wins!")
        elif player_2.get_score() > player_1.get_score():
            print(f"{player_2.get_name()} wins!")
        else:
            print("Tie game!")
