from src.troop import Troop
import src.globals as macros


class Balloon(Troop):

    def __init___(self, x, y, health=macros.BALLOON_HEALTH, damage=macros.BALLOON_DAMAGE, speed=macros.BALLOON_MOVEMENT_SPEED):
        super().__init__(x, y, health, damage, speed)
        self.position = (x, y)
        # self.alive = True
        self.troop_type = 'BALLOON'
        self.texture = macros.BALLOON_TEXTURE
        self.tile = macros.BALLOON

    def set_position(self, x, y):
        self.position = (x, y)

    def get_position(self):
        return super().get_position()

    def distance(self, coord):
        x = coord[0]
        y = coord[1]
        # using manhatten distance for finding up the nearest building !
        return abs(self.position[0] - x) + abs(self.position[1] - y)

    def find_target(self, village):
        minDist = 100000
        building = (-1, - 1)
        idx = -1
        defense = False

        itr = 0

        for coordinate in village.coordCannon:
            if village.cannons[itr].health > 0:
                defense = True
                dist = self.distance(coordinate)
                if dist < minDist:
                    minDist = dist
                    building = coordinate
                    idx = itr

            itr += 1

        itr = 0

        for coordinate in village.coordWizard:
            if village.wizardTower[itr].health > 0:
                dist = self.distance(coordinate)
                defense = True
                if dist < minDist:
                    minDist = dist
                    building = coordinate
                    idx = itr
            itr += 1

        if defense == False:

            itr = 0

            for coordinate in village.coordHut:
                if village.huts[itr].health > 0:
                    dist = self.distance(coordinate)
                    if dist < minDist:
                        minDist = dist
                        building = coordinate
                        idx = itr
                itr += 1

            itr = 0

            if village.townhall.health > 0:
                for i in range(macros.COORD_TOWN_HALL[0], macros.COORD_TOWN_HALL[0] + len(village.townhall.drawing)):
                    for j in range(macros.COORD_TOWN_HALL[1], macros.COORD_TOWN_HALL[1] + len(village.townhall.drawing[0])):
                        dist = self.distance((i, j))
                        if dist < minDist:
                            minDist = dist
                            building = (i, j)
                            idx = -2

        # got the nearest building to attack

        return building

    def move_balloon(self, village):
        if self.health <= 0:
            return
        target = self.find_target(village)
        # print("TARGET IS ", target)
        if target == (-1, -1):
            return True
        direction = (target[0], target[1])
        direction = (direction[0]-self.position[0],
                     direction[1]-self.position[1])
        if direction[0] > 0:
            # target niche hoga ig
            # niche move kro
            # print("1")
            new_position = self.position[0]+self.movement_speed
            if new_position > target[0]:
                new_position = target[0]
            self.set_position(new_position, self.position[1])
        elif direction[0] < 0:
            # print("2")
            new_position = self.position[0]-self.movement_speed
            if new_position < target[0]:
                new_position = target[0]
            self.set_position(new_position, self.position[1])
        elif direction[0] == 0:
            # print("3")
            new_position = self.position[1]
            if direction[1] > 0:
                # move right
                # print("3.1")
                new_position = self.position[1]+self.movement_speed
                if new_position > target[1]:
                    new_position = target[1]
                self.set_position(self.position[0], new_position)
            elif direction[1] < 0:
                # move left
                # print("3.2")
                new_position = self.position[1]-self.movement_speed
                if new_position < target[1]:
                    new_position = target[1]
                self.set_position(self.position[0], new_position)

            else:
                self.set_position(self.position[0], self.position[1])
                # print("3.3")
                # reached the target ab attack kro !
                building_type = village.tiles[target[0]][target[1]]
                if building_type == macros.CANNON_TILE:
                    idx = village.coordCannon.index(target)
                    if idx >= 0 and village.cannons[idx].active == True and village.cannons[idx].health > 0:
                        village.cannons[idx].health -= self.damage
                        if village.cannons[idx].health <= 0:
                            village.cannons[idx].texture = macros.BACKGROUND_PIXEL
                            village.cannons[idx].tile = macros.EMPTY
                            village.cannons[idx].active = False
                            # village.activeBuildings.remove(coord)
                            village.village[target[0]][target[1]
                                                       ] = macros.BACKGROUND_PIXEL
                            village.tiles[target[0]][target[1]] = macros.EMPTY

                elif building_type == macros.WIZARD_TILE:
                    idx = village.coordWizard.index(target)
                    if idx >= 0 and village.wizardTower[idx].active == True and village.wizardTower[idx].health > 0:
                        village.wizardTower[idx].health -= self.damage
                        if village.wizardTower[idx].health <= 0:
                            village.wizardTower[idx].texture = macros.BACKGROUND_PIXEL
                            village.wizardTower[idx].tile = macros.EMPTY
                            village.wizardTower[idx].active = False
                            # village.activeBuildings.remove(coord)
                            village.village[target[0]][target[1]
                                                       ] = macros.BACKGROUND_PIXEL
                            village.tiles[target[0]][target[1]] = macros.EMPTY

                elif building_type == macros.HUT_TILE:
                    idx = village.coordHut.index(target)
                    if idx >= 0 and village.huts[idx].active == True and village.huts[idx].health > 0:
                        village.huts[idx].health -= self.damage
                        if village.huts[idx].health <= 0:
                            village.huts[idx].texture = macros.BACKGROUND_PIXEL
                            village.huts[idx].tile = macros.EMPTY
                            village.huts[idx].active = False
                            # village.activeBuildings.remove(coord)
                            village.village[target[0]][target[1]
                                                       ] = macros.BACKGROUND_PIXEL
                            village.tiles[target[0]][target[1]] = macros.EMPTY

                elif building_type == macros.TOWN_HALL:
                    if village.townhall.health > 0 and village.townhall.active == True:
                        village.townhall.health -= self.damage
                        if village.townhall.health <= 0:
                            village.townhall.active = False
                            for i in range(macros.COORD_TOWN_HALL[0], macros.COORD_TOWN_HALL[0] + len(village.townhall.drawing)):
                                for j in range(macros.COORD_TOWN_HALL[1], macros.COORD_TOWN_HALL[1] + len(village.townhall.drawing[0])):
                                    # village.activeBuildings.remove((i, j))
                                    village.tiles[i][j] = macros.EMPTY
                                    village.village[i][j] = macros.BACKGROUND_PIXEL
