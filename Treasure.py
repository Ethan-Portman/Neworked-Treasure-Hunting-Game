
class Treasure:
    def __init__(self, value: int, description: str = '$'):
        if value < 1:
            raise ValueError("Treasure must have a value greater than 0.")
        if len(description) < 1:
            raise ValueError("Description of treasure must be at least one character.")

        self.description = description
        self.value = value

    def get_value(self):
        return self.value

    def get_description(self):
        return self.description

    def set_value(self, value: int):
        if value < 1:
            raise ValueError("Treasure must have a value greater than 0.")
        self.value = value

    def set_description(self, description: str):
        if len(description) < 1:
            raise ValueError("Description of treasure must be at least one character.")
        self.description = description

