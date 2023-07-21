from src.building import Building
import src.globals as macros


class Wall(Building):
    def __init__(self, x, y, size=(1, 1), health=10, level=1):
        super().__init__(x, y, size, health)
        self.points = 1
        self.type = "WALL"
        self.drawing = "#"
        self.level = level
        self.texture = macros.WALL_LEVEL_1
        if level == 2:
            self.texture = macros.WALL_LEVEL_2
        elif level == 3:
            self.texture = macros.WALL_LEVEL_3
        self.tile = macros.TILE_WALL_LEVEL_1
        if level == 2:
            self.tile = macros.TILE_WALL_LEVEL_2
        elif level == 3:
            self.tile = macros.TILE_WALL_LEVEL_3
        self.health = macros.HWALL_LEVEL_1
        if level == 2:
            self.health = macros.HWALL_LEVEL_2
        elif level == 3:
            self.health = macros.HWALL_LEVEL_3
