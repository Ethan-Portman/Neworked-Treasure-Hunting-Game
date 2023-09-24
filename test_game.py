import pytest
from Treasure import Treasure
from Tile import Tile
from Player import Player


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
    assert tile.get_treasure() is  None
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
    player = Player('1')
    tile.add_player(player)
    assert tile.get_player() == player
    tile.remove_player()
    assert tile.get_player() is None


def test_tile_string():
    tile = Tile()
    player = Player("1")
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
    player = Player()
    assert player.get_name() == "unknown"
    assert player.get_score() == 0
    assert player.get_coordinates() == (None, None)
    player = Player("#")
    assert player.get_name() == "#"
    assert player.get_score() == 0
    assert player.get_coordinates() == (None, None)
    player = Player("@", 10)
    assert player.get_name() == "@"
    assert player.get_score() == 10
    assert player.get_coordinates() == (None, None)
    with pytest.raises(ValueError, match="Player cannot have a negative score"):
        player = Player("#", -1)
    with pytest.raises(ValueError, match="Player name must be at least one character"):
        player = Player("")
    with pytest.raises(ValueError, match="Player name must be at least one character"):
        player = Player("", 10)


def test_player_name():
    player = Player()
    player.set_name("#")
    assert player.get_name() == "#"
    with pytest.raises(ValueError, match="Player name must be at least one character"):
        player.set_name("")


def test_player_scoring():
    player = Player()
    player.add_points(5)
    assert player.get_score() == 5
    with pytest.raises(ValueError, match="Value for points must be a positive number"):
        player.add_points(-1)


def test_player_coordinates():
    player = Player()
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

























    
    


