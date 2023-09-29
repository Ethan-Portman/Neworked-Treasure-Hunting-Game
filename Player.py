class Player:
    def __init__(self, y_coordinate, x_coordinate, name="unknown", score=0):
        if score < 0:
            raise ValueError("Player cannot have a negative score")
        if len(name) < 1:
            raise ValueError("Player name must be at least one character")
        self.name = name
        self.score = score
        self.y_coordinate = y_coordinate
        self.x_coordinate = x_coordinate

    def get_name(self):
        return self.name

    def set_name(self, name: str):
        if len(name) < 1:
            raise ValueError("Player name must be at least one character")
        self.name = name

    def get_score(self):
        return self.score

    def add_points(self, points):
        if points < 0:
            raise ValueError("Value for points must be a positive number")
        self.score += points

    def set_coordinates(self, y_coordinate: int, x_coordinate: int):
        if y_coordinate < 0 or x_coordinate < 0:
            raise ValueError("Coordinates must be 0 or higher")
        self.y_coordinate = y_coordinate
        self.x_coordinate = x_coordinate

    def get_coordinates(self) -> tuple[int, int]:
        return self.y_coordinate, self.x_coordinate
