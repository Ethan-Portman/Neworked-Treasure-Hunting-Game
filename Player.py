class Player:
    def __init__(self, name=None, score=0):
        self.name = name
        self.score = score

    def add_points(self, points):
        self.score += points

    def get_score(self):
        return self.score

    def get_name(self):
        return self.name
