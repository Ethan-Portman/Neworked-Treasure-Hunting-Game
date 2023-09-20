import random
from Tile import Tile
from Player import Player
from Treasure import Treasure


class Board:

    # ---------------------------------------------- CONSTRUCTORS ------------------------------------------------------
    def __init__(self, length, num_treasures, min_treasure, max_treasure):
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
            x, y = self.get_square_free_of_treasure()
            self.game_board[x][y].treasure = treasure

    def get_square_free_of_treasure(self) -> tuple[int, int]:
        """
        Retrieves the coordinates of a Tile with no treasure
        :return: The coordinates of a Tile with no treasure
        """
        while True:
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.length - 1)
            if self.game_board[x][y].treasure is None:
                return x, y

    def generate_treasure(self) -> Treasure:
        """
        Creates a treasure object with a random value between min_treasure
        and max_treasure (inclusive)
        :return: The newly generated treasure
        """
        value = random.randint(self.min_treasure, self.max_treasure)
        return Treasure(value)

    # ------------------------------------------ LOGIC FOR ADDING PLAYER -----------------------------------------------
    def add_player(self, name):
        x_coordinate, y_coordinate = self.get_square_free_of_treasure_and_player()
        new_player = Player(name)
        self.game_board[x_coordinate][y_coordinate].player = new_player

    def get_square_free_of_treasure_and_player(self) -> tuple[int, int]:
        while True:
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.length - 1)
            if self.game_board[x][y].treasure is None and self.game_board[x][y].player is None:
                return x, y

    # -------------------------------------- LOGIC FOR MOVING  PLAYER --------------------------------------------------
    def move_player(self, name, direction):
        # Find and retrieve the position of the player that will be moved
        curr_row, curr_col = self.find_player(name)

        # Get a valid direction for the player to be moved
        direction = self.get_valid_movement_direction(name, curr_row, curr_col, direction)

        # Get the position of the new coordinate
        new_row, new_col = self.get_new_coordinates(curr_row, curr_col, direction)

        # Update the player to the new position on the board
        self.update_player_position(name, curr_row, curr_col, new_row, new_col)

        # Check and collect treasure on the new position
        self.collect_treasure(name, new_row, new_col)

    def find_player(self, name) -> tuple[int, int]:
        row_num = 0
        for row in self.game_board:
            col_num = 0
            for square in row:
                if square.player is not None and square.player.name is name:
                    return row_num, col_num
                col_num += 1
            row_num += 1

    def get_valid_movement_direction(self, name, curr_row, curr_col, direction) -> str:
        while True:
            valid_direction = self.is_valid_movement(name, curr_row, curr_col, direction)
            if valid_direction:
                return direction
            else:
                print("player cannot move that way!")
                direction = input("Try again: ").upper()

    def is_valid_movement(self, name, row, col, direction) -> bool:
        match direction:
            case 'U' if row > 0:
                return True
            case 'D' if row < self.length - 1:
                return True
            case 'L' if col > 0:
                return True
            case 'R' if col < self.length - 1:
                return True
            case _:
                return False

    def get_new_coordinates(self, curr_row, curr_col, direction) -> tuple[int, int]:
        # Get the new coordinate after the move
        match direction:
            case 'U':
                curr_row -= 1
            case 'D':
                curr_row += 1
            case 'L':
                curr_col -= 1
            case 'R':
                curr_col += 1
        return curr_row, curr_col

    def update_player_position(self, name, curr_row, curr_col, new_row, new_col):
        # Copy the player to the new coordinate
        self.game_board[new_row][new_col].player = self.game_board[curr_row][curr_col].player

        # Remove the player from the old coordinate
        self.game_board[curr_row][curr_col].player = None

    def collect_treasure(self, name, row, col):
        player = self.game_board[row][col].player
        treasure = self.game_board[row][col].treasure
        if treasure is not None:
            value = treasure.value
            player.add_points(value)
            print(f"{name} has just collected {value}\nTheir new score is {player.get_score()}")

            self.game_board[row][col].treasure = None
            self.num_treasures -= 1

    # ---------------------------------------- LOGIC FOR ENDING GAME  --------------------------------------------------







