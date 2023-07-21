from distutils.command.build import build
from src.troop import Troop
import src.globals as macros


class Archer(Troop):

    def __init__(self, x, y, health=macros.BARBARIAN_HEALTH_POINTS/2, damage=macros.BARBARIAN_DAMAGE/2, speed=macros.BARBARIAN_MOVEMENT_SPEED*2):

        super().__init__(x, y, health, damage, speed)
        self.troop_type = 'A'
        self.texture = macros.ARCHER_TILE
        self.tile = macros.ARCH
        self.attack_range = macros.ARCHER_ATTACK_RANGE

    def set_position(self, x, y):
        self.position = (x, y)

    def get_position(self):
        return self.position

    def distance(self, coord):
        x = coord[0]
        y = coord[1]
        # using manhatten distance for finding up the nearest building !
        return abs(self.position[0] - x) + abs(self.position[1] - y)

    def get_nearest_building(self, village):
        minDist = 100000
        building = (-1, -1)
        # iterate over the coordinates of the active buildings
        # iterate over the huts
        itr = 0
        for coordinate in village.coordHut:
            dist = self.distance(coordinate)
            if dist < minDist and village.huts[itr].health > 0:
                minDist = dist
                building = coordinate
            itr += 1
        #  iterate over the cannons
        itr = 0
        for coordinate in village.coordCannon:
            dist = self.distance(coordinate)
            if dist < minDist and village.cannons[itr].health > 0:
                minDist = dist
                building = coordinate
            itr += 1
        #  iterate over the town hall
        if village.townhall.health > 0:
            for i in range(macros.COORD_TOWN_HALL[0], macros.COORD_TOWN_HALL[0] + len(village.townhall.drawing)):
                for j in range(macros.COORD_TOWN_HALL[1], macros.COORD_TOWN_HALL[1] + len(village.townhall.drawing[0])):
                    dist = self.distance((i, j))
                    if dist < minDist:
                        minDist = dist
                        building = (i, j)

        #  iterate over the wizard towers
        itr = 0
        for coordinate in village.coordWizard:
            dist = self.distance(coordinate)
            if dist < minDist and village.wizardTower[itr].health > 0:
                minDist = dist
                building = coordinate
            itr += 1

        return building

    def in_range(self, position, building):
        if abs(building[0]-position[0]) <= self.attack_range and abs(building[1]-position[1]) <= self.attack_range:
            return True
        return False

    def move_archer(self, village):

        building = self.get_nearest_building(village)

        if building == (-1, -1):
            return

        if self.in_range(self.position, building):
            self.attack_archer(village, building)

        else:

            direction = (building[0]-self.position[0],
                         building[1]-self.position[1])
            if direction[0] < 0:
                #  building upr h , need to move up
                # print("1")
                steps = 0
                attack = False
                battack = False

                for i in range(1, self.movement_speed+1):
                    x = self.position[0]-i
                    y = self.position[1]
                    if x < 1:
                        break
                    flag = self.in_range((x, y), building)
                    if flag == True:
                        battack = True
                        break
                    if village.tiles[x][y] == macros.ARCH or village.tiles[x][y] == macros.BARB or village.tiles[x][y] == macros.EMPTY or village.tiles[x][y] == macros.BALLOON:
                        steps += 1
                    else:
                        attack = True
                        break

                #  just check if attack is true that means the building
                #  change the position of the archer
                # print("ARCH is ", steps)
                x = self.position[0] - steps
                if self.position[0]-steps < 1:
                    x = 1
                if self.position[0] - steps < building[0]:
                    x = building[0]
                    # attack = True
                self.set_position(x, self.position[1])
                # if attack == True :

                if battack == True:
                    self.attack_archer(village, building)
                    return
                if attack == True:
                    self.attack_archer(
                        village, (self.position[0]-1, self.position[1]))
                pass
            elif direction[0] > 0:
                # print("2")
                steps = 0
                attack = False
                battack = False

                for i in range(1, self.movement_speed+1):
                    x = self.position[0]+i
                    y = self.position[1]
                    if x >= village.height-1:
                        break
                    flag = self.in_range((x, y), building)
                    if flag == True:
                        battack = True
                        break
                    if village.tiles[x][y] == macros.ARCH or village.tiles[x][y] == macros.BARB or village.tiles[x][y] == macros.EMPTY or village.tiles[x][y] == macros.BALLOON:
                        steps += 1
                    else:
                        attack = True
                        break

                #  just check if attack is true that means the building
                #  change the position of the archer
                x = self.position[0] + steps
                if self.position[0]+steps >= village.height-1:
                    x = village.height-2
                if self.position[0] + steps > building[0]:
                    x = building[0]
                    # attack = True
                self.set_position(x, self.position[1])
                # if attack == True :

                if battack == True:
                    self.attack_archer(village, building)
                    return
                if attack == True:
                    self.attack_archer(
                        village, (self.position[0]-1, self.position[1]))

            else:
                # print("3")
                #  in same vertical plane ig
                if direction[1] == 0:
                    # print("4")
                    self.attack_archer(village, building)
                elif direction[1] < 0:
                    # print("5")
                    steps = 0
                    attack = False
                    battack = False
                    for i in range(1, self.movement_speed+1):
                        x = self.position[0]
                        y = self.position[1]-i
                        if y < 1:
                            break
                        flag = self.in_range((x, y), building)
                        if flag == True:
                            battack = True
                            break
                        if village.tiles[x][y] == macros.ARCH or village.tiles[x][y] == macros.BARB or village.tiles[x][y] == macros.EMPTY or village.tiles[x][y] == macros.BALLOON:
                            steps += 1
                        else:
                            attack = True
                            break
                    y = self.position[1]-steps
                    if self.position[1]-steps < 1:
                        y = 1
                    if self.position[1]-steps < building[1]:
                        y = building[1]+1
                    self.set_position(self.position[0], y)
                    if battack == True:
                        self.attack_archer(village, building)
                        return
                    if attack == True:
                        self.attack_archer(
                            village, (self.position[0], self.position[1]-1))

                else:
                    # print("6")
                    steps = 0
                    attack = False
                    battack = False
                    for i in range(1, self.movement_speed+1):
                        x = self.position[0]
                        y = self.position[1]+i
                        if y >= village.width-1:
                            break
                        flag = self.in_range((x, y), building)
                        if flag == True:
                            battack = True
                            break
                        if village.tiles[x][y] == macros.ARCH or village.tiles[x][y] == macros.BARB or village.tiles[x][y] == macros.EMPTY or village.tiles[x][y] == macros.BALLOON:
                            steps += 1
                        else:
                            attack = True
                            break
                    y = self.position[1]+steps
                    if self.position[1]+steps >= village.width-1:
                        y = village.width-2
                    if self.position[1]+steps > building[1]:
                        y = building[1]-1
                    self.set_position(self.position[0], y)
                    if battack == True:
                        self.attack_archer(village, building)
                        return
                    if attack == True:
                        self.attack_archer(
                            village, (self.position[0], self.position[1]+1))

    def attack_archer(self, village, coord):

        if self.health <= 0:
            self.alive = False
            return
        objtype = village.tiles[coord[0]][coord[1]]

        if objtype == macros.HUT_TILE:
            idx = village.coordHut.index(coord)

            if village.huts[idx].active == True and village.huts[idx].health > 0:
                village.huts[idx].health -= self.damage
                if village.huts[idx].health <= 0:
                    village.huts[idx].texture = macros.BACKGROUND_PIXEL
                    village.huts[idx].tile = macros.EMPTY
                    village.huts[idx].active = False

        elif objtype == macros.TOWN_HALL:
            if village.townhall.health > 0 and village.townhall.active == True:
                village.townhall.health -= self.damage
                if village.townhall.health <= 0:
                    village.townhall.active = False
                    for i in range(macros.COORD_TOWN_HALL[0], macros.COORD_TOWN_HALL[0] + len(village.townhall.drawing)):
                        for j in range(macros.COORD_TOWN_HALL[1], macros.COORD_TOWN_HALL[1] + len(village.townhall.drawing[0])):
                            # village.activeBuildings.remove((i, j))
                            village.tiles[i][j] = macros.EMPTY
                            village.village[i][j] = macros.BACKGROUND_PIXEL

        elif objtype == macros.CANNON_TILE:
            idx = village.coordCannon.index(coord)
            if idx >= 0 and village.cannons[idx].active == True and village.cannons[idx].health > 0:
                village.cannons[idx].health -= self.damage
                if village.cannons[idx].health <= 0:
                    village.cannons[idx].texture = macros.BACKGROUND_PIXEL
                    village.cannons[idx].tile = macros.EMPTY
                    village.cannons[idx].active = False
                    # village.activeBuildings.remove(coord)
                    village.village[coord[0]][coord[1]
                                              ] = macros.BACKGROUND_PIXEL
                    village.tiles[coord[0]][coord[1]] = macros.EMPTY

        elif objtype == macros.WIZARD_TILE:
            idx = village.coordWizard.index(coord)
            if village.wizardTower[idx].active == True and village.wizardTower[idx].health > 0:
                village.wizardTower[idx].health -= self.damage
                if village.wizardTower[idx].health <= 0:
                    village.wizardTower[idx].texture = macros.BACKGROUND_PIXEL
                    village.wizardTower[idx].tile = macros.EMPTY
                    village.wizardTower[idx].active = False
                    # village.activeBuildings.remove(coord)
                    village.village[coord[0]][coord[1]
                                              ] = macros.BACKGROUND_PIXEL
                    village.tiles[coord[0]][coord[1]] = macros.EMPTY

        else:  # wall object perhaps
            level = 1
            if village.tiles[coord[0]][coord[1]] == macros.TILE_WALL_LEVEL_2:
                level = 2
            elif village.tiles[coord[0]][coord[1]] == macros.TILE_WALL_LEVEL_3:
                level = 3

            if ((coord[0], coord[1], level)) in village.coordWall:
                idx = village.coordWall.index((coord[0], coord[1], level))
                # print(idx)
                if village.walls[idx].active == True and village.walls[idx].health > 0:
                    village.walls[idx].health -= self.damage
                    if village.walls[idx].health <= 0:
                        village.walls[idx].texture = macros.BACKGROUND_PIXEL
                        village.walls[idx].tile = macros.EMPTY
            return
