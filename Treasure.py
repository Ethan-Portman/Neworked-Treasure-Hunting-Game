import constants


class Treasure:
    """
    The Treasure class represents a valuable item in the game. It is how players collect points
    and win. Treasures are located on tiles. Treasures have a value and a description.
    """
    def __init__(self, value: int, description: str = constants.TREASURE_DESCRIPTION):
        """
        Initialize a Treasure object with the given value and description.
        :param value: The value of the treasure.
        :param description: The description of the treasure.
        :raises ValueError: If value is less than 1 or description is an empty string.
        """
        if value < 1:
            raise ValueError("Treasure must have a value greater than 0.")
        if len(description) < 1:
            raise ValueError("Description of treasure must be at least one character.")

        self.description = description
        self.value = value

    def get_value(self) -> int:
        """
        Retrieves the value of the treasure.
        :return: Value of the treasure.
        """
        return self.value

    def get_description(self) -> str:
        """
        Retrieves the description of the treasure.
        :return: Description of the treasure.
        """
        return self.description

    def set_value(self, value: int) -> None:
        """
        Sets the specified value of the treasure.
        :param value: The new value of the treasure.
        :raises ValueError: If the new value of the treasure is less than 1.
        """
        if value < 1:
            raise ValueError("Treasure must have a value greater than 0.")
        self.value = value

    def set_description(self, description: str) -> None:
        """
        Sets the specified description for the treasure.
        :param description: The new description of the treasure.
        :raises ValueError: If the new description of the treasure is an empty string.
        """
        if len(description) < 1:
            raise ValueError("Description of treasure must be at least one character.")
        self.description = description
