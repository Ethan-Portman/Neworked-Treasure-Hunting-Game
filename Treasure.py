
class Treasure:
    def __init__(self, value: int, description: str = '$'):
        self.description = description
        self.value = value

    def get_value(self):
        return self.value
