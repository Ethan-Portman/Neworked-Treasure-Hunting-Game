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
        self.invalid_board_check()
        self.game_board = self.create_board()
        self.populate_board_with_treasure()

    def invalid_board_check(self):
        if self.length < 2 or self.length > 50:
            raise ValueError("Length of board must be between 2 and 50")
        if self.num_treasures < 0 or self.num_treasures > (self.length * self.length):
            raise ValueError("Number of treasures must be between 0 and length x length")
        if self.min_treasure < 1 or self.min_treasure > 100:
            raise ValueError("Minimum Treasure must be between 1 and 100")
        if self.max_treasure < self.min_treasure or self.max_treasure > 1000:
            raise ValueError("Maximum Treasure must be between minimum Treasure and a 1000")

    # --------------------------------- CREATE GAME-BOARD AND SETTING UP GAME ------------------------------------------
    def create_board(self) -> list[list[Tile]]:
        """
        Creates a 2D List to be used as the game-board
        :return: A 2D List of Tiles representing the game-board
        """
        return [[Tile() for _ in range(self.length)] for _ in range(self.length)]

    def populate_board_with_treasure(self) -> None:
        """
        Inserts num_treasures amount of treasure randomly across the board.
        Treasure is between min_treasure and max_treasure (inclusive)
        """
        for _ in range(self.num_treasures):
            y_pos, x_pos = self.get_square_free_of_treasure()
            self.game_board[y_pos][x_pos].add_treasure(self.generate_treasure())

    def generate_treasure(self) -> Treasure:
        """
        Creates a treasure object with a random value between min_treasure
        and max_treasure (inclusive)
        :return: The newly generated treasure
        """
        return Treasure(random.randint(self.min_treasure, self.max_treasure))

    def get_square_free_of_treasure(self) -> tuple[int, int]:
        """
        Retrieves the coordinates of a Tile with no treasure
        :return: The coordinates of a Tile with no treasure
        """
        while True:
            y_pos, x_pos = random.randint(0, self.length - 1), random.randint(0, self.length - 1)
            if self.game_board[y_pos][x_pos].get_treasure() is None:
                return y_pos, x_pos

    def get_square_free_of_treasure_and_player(self) -> tuple[int, int]:
        """
        Retrieves the coordinates of a Tile that is free of both treasure and player
        :return: The coordinates of a tile with no treasure or player
        """
        while True:
            y_pos, x_pos = self.get_square_free_of_treasure()
            if self.game_board[y_pos][x_pos].get_player() is None:
                return y_pos, x_pos

    def add_player(self, name: str) -> None:
        """
        Adds a player to a random position on the board free of treasure or player
        :param name: Name of the player to be added to the board
        """
        y_pos, x_pos = self.get_square_free_of_treasure_and_player()
        self.game_board[y_pos][x_pos].add_player(Player(y_pos, x_pos, name))

    # -------------------------------------------- PLAYING THE GAME ----------------------------------------------------
    def find_player(self, name: str) -> Player:
        """
        Retrieves a player on the board
        :param name: The name of the player to be retrieved
        :return: The player
        """
        return next((square.player for row in self.game_board for square in row
                     if square.player and square.player.name == name), None)

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
            if self.is_valid_direction(name, direction):
                return direction
            direction = input("Try again: ").upper()

    def is_valid_direction(self, name: str, direction: str) -> bool:
        """
        Validates if the entered direction is a valid input
        :param name: The player to be moved
        :param direction: The direction the player will move
        :return: If the direction is valid or not
        """
        curr_y, curr_x = self.find_player(name).get_coordinates()

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
        y, x = self.find_player(name).get_coordinates()
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
        old_y, old_x = player.get_coordinates()
        player.set_coordinates(new_y, new_x)

        self.game_board[new_y][new_x].add_player(player)
        self.game_board[old_y][old_x].remove_player()

    def collect_treasure(self, name: str, y: int, x: int):
        """
        Searches tile for treasure. If there is a treasure it adds the value to the player and removes the
        treasure from the game board
        :param name: The name of the player that is searching/ collecting the treasure
        :param y: The y coordinate that the player is searching
        :param x: The x coordinate that the player is searching
        """
        treasure = self.game_board[y][x].get_treasure()

        if treasure is not None:
            player = self.find_player(name)
            player.add_points(treasure.get_value())
            print(f"Player {name} has just collected {treasure.get_value()} points\nTheir new score is {player.get_score()}")
            self.game_board[y][x].remove_treasure()
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
