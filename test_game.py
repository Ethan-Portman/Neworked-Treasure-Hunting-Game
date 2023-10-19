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


def test_setting_treasure_value():
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
    tile = Tile(1, 2)
    assert tile.get_treasure() is None
    assert tile.get_player() is None
    assert tile.description == "."
    assert tile.get_coordinates() == (1, 2)
    tile = Tile(0,0, "%")
    assert tile.description == "%"
    with pytest.raises(ValueError, match="Tile description must have at least one character"):
        tile = Tile(0, 0, '')
    with pytest.raises(ValueError, match="Coordinates must be above 0."):
        tile = Tile(-1, 0, '$')
    with pytest.raises(ValueError, match="Coordinates must be above 0."):
        tile = Tile(0, -1, '$')


def test_add_remove_treasure_from_tile():
    tile = Tile(0, 0)
    treasure = Treasure(10)
    tile.add_treasure(treasure)
    assert tile.get_treasure() == treasure
    tile.remove_treasure()
    assert tile.get_treasure() is None


def test_add_remove_player_from_tile():
    tile = Tile(0,0)
    player = Player((0, 0), '1')
    tile.add_player(player)
    assert tile.get_player() == player
    tile.remove_player()
    assert tile.get_player() is None


def test_tile_to_string():
    tile = Tile(0,0)
    player = Player((0,0), "1")
    treasure = Treasure(10)
    tile.add_player(player)
    tile.add_treasure(treasure)
    assert str(tile) == "1"
    tile.remove_player()
    assert str(tile) == "$"
    tile.remove_treasure()
    assert str(tile) == "."


# ------------------------------------------ TESTS FOR PLAYER CLASS ----------------------------------------------------
def test_player_constructor():
    player = Player((1, 1))
    assert player.get_name() == "unknown"
    assert player.get_score() == 0
    assert player.get_coordinates() == (1, 1)
    player = Player((1, 1),"1")
    assert player.get_name() == "1"
    player = Player((1, 1),"1", 10)
    assert player.get_score() == 10
    with pytest.raises(ValueError, match="Player cannot have a negative score"):
        player = Player((1,1),"1", -1)
    with pytest.raises(ValueError, match="Player name must be at least one character"):
        player = Player((1,1),"")
    with pytest.raises(ValueError, match="Player coordinates must be greater than 0"):
        player = Player((-1, 0))
    with pytest.raises(ValueError, match="Player coordinates must be greater than 0"):
        player = Player((0, -1))


def test_player_scoring():
    player = Player((0,0))
    player.add_points(5)
    assert player.get_score() == 5
    with pytest.raises(ValueError, match="Value for points must be a positive number"):
        player.add_points(-1)


def test_player_coordinates():
    player = Player((0,0))
    player.set_coordinates((2, 5))
    assert player.get_coordinates() == (2, 5)
    player.set_coordinates((3, 0))
    assert player.get_coordinates() == (3, 0)
    with pytest.raises(ValueError, match="Player coordinates must be greater than 0"):
        player.set_coordinates((-1, 2))
    with pytest.raises(ValueError, match="Player coordinates must be greater than 0"):
        player.set_coordinates((5, -3))
    with pytest.raises(ValueError, match="Player coordinates must be greater than 0"):
        player.set_coordinates((-4, -4))


# ------------------------------------------- TESTS FOR BOARD CLASS ----------------------------------------------------
def test_board_constructor():
    board = Board(10, 20, 1, 10)
    assert board.length == 10
    assert board.num_treasures == 20
    assert board.min_treasure == 1
    assert board.max_treasure == 10
    with pytest.raises(ValueError, match="Length of board must be between 2 and 50"):
        board = Board(0, 0, 1, 2)
    with pytest.raises(ValueError, match="Length of board must be between 2 and 50"):
        board = Board(51, 0, 1, 2)
    with pytest.raises(ValueError, match="Number of treasures must be between 0 and length x length"):
        board = Board(10, -1, 1, 2)
    with pytest.raises(ValueError, match="Number of treasures must be between 0 and length x length"):
        board = Board(5, 26, 1, 2)
    with pytest.raises(ValueError, match="Minimum Treasure must be between 1 and 100"):
        board = Board(10, 1, 0, 2)
    with pytest.raises(ValueError, match="Minimum Treasure must be between 1 and 100"):
        board = Board(10, 1, 101, 110)
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
                treasure_val = square.get_treasure().get_value()
                assert 5 >= treasure_val >= 1
    assert treasure_in_board_1 == treasure_board_1

    treasure_in_board_2 = 0
    for row in board_2.game_board:
        for square in row:
            if square.get_treasure() is not None:
                treasure_in_board_2 += 1
                treasure_val = square.get_treasure().get_value()
                assert 5 >= treasure_val >= 1
    assert treasure_in_board_2 == treasure_board_2

    treasure_in_board_3 = 0
    for row in board_3.game_board:
        for square in row:
            if square.get_treasure() is not None:
                treasure_in_board_3 += 1
    assert treasure_in_board_3 == treasure_board_3


def test_find_empty_tile():
    board = Board(5, 20, 1, 5)
    board.add_player_to_game_board("1")
    board.add_player_to_game_board("2")
    for _ in range(100):
        tile = board.find_empty_tile()
        assert tile.get_treasure() is None
        assert tile.get_player() is None


# ---------- Tests for Adding player onto the Board ----------
def test_add_player():
    for i in range(10):
        player_1_added = False
        player_2_added = False
        board = Board(i + 2, 1, 1, 1)
        board.add_player_to_game_board("1")
        board.add_player_to_game_board("2")
        for row in board.game_board:
            for square in row:
                if square.get_player() is not None and square.get_player().get_name() == "1":
                    player_1_added = True
                if square.get_player() is not None and square.get_player().get_name() == "2":
                    player_2_added = True
        assert player_1_added is True
        assert player_2_added is True
        assert any(player.get_name() == "1" for player in board.players)
        assert any(player.get_name() == "2" for player in board.players)


def test_find_player_by_name():
    for _ in range(10):
        board = Board(50, 10, 1, 5)
        board.add_player_to_game_board("1")
        board.add_player_to_game_board("2")
        player_1 = board.find_player_by_name("1")
        player_2 = board.find_player_by_name("2")
        assert player_1.get_name() == "1"
        assert player_2.get_name() == "2"


def test_general_movement():
    board = Board(5, 0, 1, 1)
    player = Player((2, 2), "1")
    board.players.append(player)
    board.game_board[2][2].add_player(player)
    board.move_player_on_board("1", "U")
    assert board.find_player_by_name("1").get_coordinates() == (1, 2)
    assert board.game_board[2][2].get_player() is None
    board.move_player_on_board("1", "L")
    assert board.find_player_by_name("1").get_coordinates() == (1, 1)
    assert board.game_board[1][2].get_player() is None
    board.move_player_on_board("1", "R")
    assert board.find_player_by_name("1").get_coordinates() == (1, 2)
    assert board.game_board[1][1].get_player() is None
    board.move_player_on_board("1", "D")
    assert board.find_player_by_name("1").get_coordinates() == (2, 2)
    assert board.game_board[1][2].get_player() is None


def test_colliding_into_wall():
    board = Board(2, 1, 1, 1)
    player = Player((0, 0), "1")
    board.players.append(player)
    board.game_board[0][0].add_player(player)
    assert board.is_valid_movement("1", "U") is False
    assert board.is_valid_movement("1", "L") is False
    board.move_player_on_board("1", "D")
    board.move_player_on_board("1", "R")
    assert board.is_valid_movement("1", "D") is False
    assert board.is_valid_movement("1", "R") is False


def test_colliding_into_player():
    board = Board(5, 1, 1, 1)
    player_1 = Player((0, 0), "1")
    board.players.append(player_1)
    board.game_board[0][0].add_player(player_1)
    player_2 = Player((0, 1), "2")
    board.players.append(player_2)
    board.game_board[0][1].add_player(player_2)
    assert board.is_valid_movement("1", "R") is False
    assert board.is_valid_movement("2", "L") is False
    board.move_player_on_board("1", "D")
    board.move_player_on_board("1", "R")
    assert board.is_valid_movement("1", "U") is False
    assert board.is_valid_movement("2", "D") is False


def test_collect_treasure():
    board = Board(10, 1, 1, 3)
    player = Player((0,0), "1")
    board.players.append(player)
    board.game_board[0][0].add_player(player)
    board.game_board[0][1].add_treasure(Treasure(1))
    board.move_player_on_board('1', 'R')
    assert player.get_score() == 1
    assert board.game_board[0][1].get_treasure() is None
    board.game_board[0][2].add_treasure(Treasure(2))
    board.move_player_on_board('1', 'R')
    assert player.get_score() == 3
    board.game_board[0][3].add_treasure(Treasure(3))
    board.move_player_on_board('1', 'R')
    assert player.get_score() == 6














