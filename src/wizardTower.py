from src.building import Building
import src.globals as macros


class WizardTower(Building):

    def __init__(self, x, y, size=10, health=macros.WIZARD_HEALTH):

        super().__init__(x, y, size, health)
        self.damage = macros.WIZARD_DAMAGE
        self.last_shot = 0
        self.texture = macros.WIZARD
        self.tile = macros.WIZARD_TILE
        self.attack_range = macros.CANNON_RADIUS

    def distance(self, coord):
        return abs(self.position[0] - coord[0]) + abs(self.position[1] - coord[1])

    def enemy_distance(coord1, coord2):
        return abs(coord1[0]-coord2[0]) + abs(coord1[1]-coord2[1])

    def find_target(self, village):
        position = (-1, -1)
        if self.health <= 0:
            self.active = False
            return
        shoot = False
        mindist = 100000
        idx = -2
        itr = 0
        #  idx = 0 -> barb , 1 -> archer , 2 -> balloon , -2 none , -1 -> king or queen
        #  check over the king and queen
        if village.troop == "KING":
            if village.king.health > 0:
                if abs(self.position[0]-village.king.position[0]) <= self.attack_range and abs(self.position[1]-village.king.position[1]) <= self.attack_range:
                    shoot = True
                    position = village.king.position
                    mindist = self.distance(village.king.position)
                    idx = -1
        else:
            if village.queen.health > 0:
                if abs(self.position[0]-village.queen.position[0]) <= self.attack_range and abs(self.position[1]-village.queen.position[1]) <= self.attack_range:
                    shoot = True
                    position = village.queen.position
                    mindist = self.distance(village.queen.position)
                    idx = -1

        # check over the barbarians

        for barb in village.barbarians:
            if barb.health > 0:
                if abs(self.position[0]-barb.position[0]) <= self.attack_range and abs(self.position[1]-barb.position[1]) <= self.attack_range:
                    shoot = True
                    dist = self.distance(barb.position)
                    if dist < mindist:
                        mindist = dist
                        position = barb.position
                        idx = 0
        # check over the archers
        for archer in village.archers:
            if archer.health > 0:
                if abs(self.position[0]-archer.position[0]) <= self.attack_range and abs(self.position[1]-archer.position[1]) <= self.attack_range:
                    shoot = True
                    dist = self.distance(archer.position)
                    if dist < mindist:
                        mindist = dist
                        position = archer.position
                        idx = 1

        # check over the balloons
        for balloon in village.balloons:
            if balloon.health > 0:
                if abs(self.position[0]-balloon.position[0]) <= self.attack_range and abs(self.position[1]-balloon.position[1]) <= self.attack_range:
                    shoot = True
                    dist = self.distance(balloon.position)
                    if dist < mindist:
                        position = balloon.position
                        mindist = dist
                        idx = 2

        if shoot == True:
            self.texture = macros.WIZARD_SHOT
        else:
            health = float(self.health/macros.WIZARD_HEALTH)
            if health > 0.5:
                self.texture = macros.WIZARD_HEALTH
            elif health > 0.25:
                self.texture = macros.WIZARD_HEALTH_25
            else:
                self.texture = macros.WIZARD_HEALTH_50

        if shoot == True:
            self.shoot(village, position)
        return shoot

    def shoot(self, village, position):
        if self.health <= 0:
            self.active = False
            return
        # look over the barbarians
        for barb in village.barbarians:
            if barb.health > 0:
                if abs(position[0]-barb.position[0])+abs(position[1]-barb.position[1]) <= 2:
                    barb.health -= self.damage
                    if barb.health <= 0:
                        barb.alive = False
                        barb.texture = macros.GRAVE_TILE
                        village.tiles[barb.position[0]
                                      ][barb.position[1]] = macros.EMPTY
        #  look over the archers
        for archer in village.archers:
            if archer.health > 0:
                if abs(position[0]-archer.position[0])+abs(position[1]-archer.position[1]) <= 2:
                    archer.health -= self.damage
                    if archer.health <= 0:
                        archer.alive = False
                        archer.texture = macros.GRAVE_TILE
                        village.tiles[archer.position[0]
                                      ][archer.position[1]] = macros.EMPTY
        for balloon in village.balloons:
            if balloon.health > 0:
                if abs(position[0]-balloon.position[0])+abs(position[1]-balloon.position[1]) <= 2:
                    balloon.health -= self.damage
                    if balloon.health <= 0:
                        balloon.alive = False
                        balloon.texture = macros.GRAVE_TILE
                        village.tiles[balloon.position[0]
                                      ][balloon.position[1]] = macros.EMPTY
        if village.troop == "KING":
            if village.king.health > 0:
                if abs(position[0]-village.king.position[0])+abs(position[1]-village.king.position[1]) <= 2:
                    village.king.health -= self.damage
                    if village.king.health <= 0:
                        village.king.alive = False
                        village.king.texture = macros.GRAVE_TILE
                        village.tiles[village.king.position[0]
                                      ][village.king.position[1]] = macros.EMPTY
        else:
            if village.queen.health > 0:
                if abs(position[0]-village.queen.position[0])+abs(position[1]-village.queen.position[1]) <= 2:
                    village.queen.health -= self.damage
                    if village.queen.health <= 0:
                        village.queen.alive = False
                        village.queen.texture = macros.GRAVE_TILE
                        village.tiles[village.queen.position[0]
                                      ][village.queen.position[1]] = macros.EMPTY
