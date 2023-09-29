import pytest
from Treasure import Treasure
from Tile import Tile
from Player import Player
from Board import Board


# ---------------------------------------- TESTS FOR TREASURE CLASS ----------------------------------------------------
def test_treasure_constructor():
    treasure = Treasure(10)
    assert treasure.get_value() == 10
    assert treasure.get_description() == '$'
    treasure = Treasure(20, '%')
    assert treasure.get_value() == 20
    assert treasure.get_description() == '%'
    with pytest.raises(ValueError, match="Treasure must have a value greater than 0."):
        treasure = Treasure(0)
    with pytest.raises(ValueError, match="Description of treasure must be at least one character."):
        treasure = Treasure(10, '')
    assert 0 == 1


def test_treasure_setters():
    treasure = Treasure(20)
    treasure.set_value(50)
    treasure.set_description('&')
    assert treasure.get_value() == 50
    assert treasure.get_description() == '&'
    with pytest.raises(ValueError, match="Treasure must have a value greater than 0."):
        treasure.set_value(0)
    with pytest.raises(ValueError, match="Description of treasure must be at least one character."):
        treasure.set_description('')


# ------------------------------------------ TESTS FOR TILE CLASS ------------------------------------------------------
def test_tile_constructor():
    tile = Tile()
    assert tile.get_description() == "."
    assert tile.get_treasure() is None
    assert tile.get_player() is None
    tile = Tile("%")
    assert tile.get_description() == "%"
    with pytest.raises(ValueError, match="Tile description must have at least one character"):
        tile = Tile('')


def test_tile_description():
    tile = Tile()
    tile.set_description("#")
    assert tile.get_description() == "#"
    with pytest.raises(ValueError, match="Tile description must have at least one character"):
        tile.set_description("")


def test_tile_treasure():
    tile = Tile()
    treasure = Treasure(10)
    tile.add_treasure(treasure)
    assert tile.get_treasure() == treasure
    tile.remove_treasure()
    assert tile.get_treasure() is None


def test_tile_player():
    tile = Tile()
    player = Player(1, 1, '1')
    tile.add_player(player)
    assert tile.get_player() == player
    tile.remove_player()
    assert tile.get_player() is None


def test_tile_string():
    tile = Tile()
    player = Player(1, 1, "1")
    treasure = Treasure(10)
    tile.add_player(player)
    tile.add_treasure(treasure)
    assert str(tile) == "1"
    tile.remove_player()
    assert str(tile) == "$"
    tile.remove_treasure()
    assert str(tile) == "."


# ------------------------------------------ TESTS FOR PLAYER CLASS ----------------------------------------------------
# def test_player_constructor():  # TO_DO - update for new paramaters
#     player = Player()
#     assert player.get_name() == "unknown"
#     assert player.get_score() == 0
#     assert player.get_coordinates() == (None, None)
#     player = Player("#")
#     assert player.get_name() == "#"
#     assert player.get_score() == 0
#     assert player.get_coordinates() == (None, None)
#     player = Player("@", 10)
#     assert player.get_name() == "@"
#     assert player.get_score() == 10
#     assert player.get_coordinates() == (None, None)
#     with pytest.raises(ValueError, match="Player cannot have a negative score"):
#         player = Player("#", -1)
#     with pytest.raises(ValueError, match="Player name must be at least one character"):
#         player = Player("")
#     with pytest.raises(ValueError, match="Player name must be at least one character"):
#         player = Player("", 10)


def test_player_name():
    player = Player(1, 1)
    player.set_name("#")
    assert player.get_name() == "#"
    with pytest.raises(ValueError, match="Player name must be at least one character"):
        player.set_name("")


def test_player_scoring():
    player = Player(1, 1)
    player.add_points(5)
    assert player.get_score() == 5
    with pytest.raises(ValueError, match="Value for points must be a positive number"):
        player.add_points(-1)


def test_player_coordinates():
    player = Player(1, 2)
    player.set_coordinates(2, 5)
    assert player.get_coordinates() == (2, 5)
    player.set_coordinates(3, 0)
    assert player.get_coordinates() == (3, 0)
    with pytest.raises(ValueError, match="Coordinates must be 0 or higher"):
        player.set_coordinates(-1, 2)
    with pytest.raises(ValueError, match="Coordinates must be 0 or higher"):
        player.set_coordinates(5, -3)
    with pytest.raises(ValueError, match="Coordinates must be 0 or higher"):
        player.set_coordinates(-4, -4)


# ------------------------------------------- TESTS FOR BOARD CLASS ----------------------------------------------------
def test_board_constructor():
    board = Board(10, 20, 1, 10)
    assert board.length == 10
    assert board.num_treasures == 20
    assert board.min_treasure == 1
    assert board.max_treasure == 10
    # Test for invalid length of board
    with pytest.raises(ValueError, match="Length of board must be between 2 and 50"):
        board = Board(0, 0, 1, 2)
    with pytest.raises(ValueError, match="Length of board must be between 2 and 50"):
        board = Board(51, 0, 1, 2)
    # Test for invalid number of treasures
    with pytest.raises(ValueError, match="Number of treasures must be between 0 and length x length"):
        board = Board(10, -1, 1, 2)
    with pytest.raises(ValueError, match="Number of treasures must be between 0 and length x length"):
        board = Board(5, 26, 1, 2)
    # Test for invalid minimum Treasure
    with pytest.raises(ValueError, match="Minimum Treasure must be between 1 and 100"):
        board = Board(10, 1, 0, 2)
    with pytest.raises(ValueError, match="Minimum Treasure must be between 1 and 100"):
        board = Board(10, 1, 101, 110)
    # Test for invalid maximum Treasure
    with pytest.raises(ValueError, match="Maximum Treasure must be between minimum Treasure and a 1000"):
        board = Board(10, 1, 10, 9)
    with pytest.raises(ValueError, match="Maximum Treasure must be between minimum Treasure and a 1000"):
        board = Board(10, 1, 10, 1001)


# ---------- Tests for Generating Treasure and placing on Board ----------
def test_create_board():
    board = Board(5, 0, 1, 10)
    assert len(board.game_board) == 5
    assert len(board.game_board[0]) == 5
    assert str(board.game_board[0][0]) == "."


def test_generate_treasure():
    min_treasure = 1
    max_treasure = 5
    board = Board(5, 5, min_treasure, max_treasure)
    for _ in range(100):
        treasure = board.generate_treasure()
        value = treasure.get_value()
        assert min_treasure <= value <= max_treasure


def test_get_square_free_of_treasure():
    board = Board(5, 20, 1, 5)
    for _ in range(100):
        y_pos, x_pos = board.get_square_free_of_treasure()
        assert board.game_board[y_pos][x_pos].get_treasure() is None


def test_get_square_free_of_treasure_and_player():
    board = Board(5, 20, 1, 5)
    board.add_player("1")
    board.add_player("2")
    for _ in range(100):
        y_pos, x_pos = board.get_square_free_of_treasure_and_player()
        assert board.game_board[y_pos][x_pos].get_treasure() is None
        assert board.game_board[y_pos][x_pos].get_player() is None


def test_populate_board_with_treasure():
    treasure_board_1 = 20
    treasure_board_2 = 16
    treasure_board_3 = 0
    board_1 = Board(5, treasure_board_1, 1, 5)
    board_2 = Board(4, treasure_board_2, 1, 5)
    board_3 = Board(5, treasure_board_3, 1, 5)
    treasure_in_board_1 = 0
    for row in board_1.game_board:
        for square in row:
            if square.get_treasure() is not None:
                treasure_in_board_1 += 1
    treasure_in_board_2 = 0
    for row in board_2.game_board:
        for square in row:
            if square.get_treasure() is not None:
                treasure_in_board_2 += 1
    treasure_in_board_3 = 0
    for row in board_3.game_board:
        for square in row:
            if square.get_treasure() is not None:
                treasure_in_board_3 += 1
    assert treasure_in_board_1 == treasure_board_1
    assert treasure_in_board_2 == treasure_board_2
    assert treasure_in_board_3 == treasure_board_3



# ---------- Tests for Adding player onto the Board ----------
def test_add_player():
    player_1 = "1"
    player_2 = "2"
    for _ in range(10):
        player_1_added = False
        player_2_added = False
        board = Board(2, 2, 1, 5)
        board.add_player(player_1)
        board.add_player(player_2)
        for row in board.game_board:
            for square in row:
                if square.get_player() is not None and square.get_player().get_name() == "1":
                    player_1_added = True
                if square.get_player() is not None and square.get_player().get_name() == "2":
                    player_2_added = True
        assert player_1_added is True
        assert player_2_added is True


def test_find_player():
    player_1 = "1"
    player_2 = "2"
    for _ in range(10):
        board = Board(20, 10, 1, 5);
        board.add_player(player_1)
        board.add_player(player_2)
        player_1_player = board.find_player(player_1)
        player_2_player = board.find_player(player_2)
        assert player_1_player.get_name() == player_1
        assert player_2_player.get_name() == player_2







