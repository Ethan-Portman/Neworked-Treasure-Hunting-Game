TREASURE_DESCRIPTION = '$'


class Treasure:
    """
    The Treasure class represents a valuable item in the game. It is how players collect points
    and win. Treasures are located on tiles. Treasures have a value and a description.
    """
    def __init__(self, value: int, description: str = TREASURE_DESCRIPTION):
        if value < 1:
            raise ValueError("Treasure must have a value greater than 0.")
        if len(description) < 1:
            raise ValueError("Description of treasure must be at least one character.")

        self.description = description
        self.value = value

    def get_value(self) -> int:
        """Retrieves the value of the treasure."""
        return self.value

    def get_description(self) -> str:
        """Retrieves the description of the treasure."""
        return self.description

    def set_value(self, value: int) -> None:
        """Sets the specified value of the treasure."""
        if value < 1:
            raise ValueError("Treasure must have a value greater than 0.")
        self.value = value

    def set_description(self, description: str):
        """Sets the specified description for the treasure."""
        if len(description) < 1:
            raise ValueError("Description of treasure must be at least one character.")
        self.description = description
