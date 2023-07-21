from src.troop import Troop
import src.globals as macros
import math
# define the barbarian class
# inherit from the troop class
# set the troop type to barbarian


class Barabarian(Troop):

    def __init__(self, x, y, health=macros.BARBARIAN_HEALTH_POINTS, damage=macros.BARBARIAN_DAMAGE, speed=macros.BARBARIAN_MOVEMENT_SPEED):

        super().__init__(x, y, health, damage, speed)
        self.troop_type = macros.BARBARIAN
        self.texture = macros.BARBARIAN_TILE
        self.tile = macros.BARB

    def set_position(self, x, y):
        self.position = (x, y)

    def get_position(self):
        return self.position

    def distance(self, coord):
        x = coord[0]
        y = coord[1]
        # using manhatten distance for finding up the nearest building !
        return abs(self.position[0] - x) + abs(self.position[1] - y)

    def move_barbarian(self, village):
        # set the game boundary variables
        # print(self.position)
        # print(village.tiles[self.position[0]][self.position[1]-1])
        if self.health <= 0:
            self.alive = False
            return
        top = 1
        left = 1
        right = village.width - 1
        bottom = village.height - 1

        # look for the building to move to move
        # to the building

        minDist = 100000
        building = (-1, -1)

        for coordinate in village.activeBuildings:
            dist = self.distance(coordinate)
            if dist < minDist:
                if village.tiles[coordinate[0]][coordinate[1]] == macros.EMPTY:
                    continue
                minDist = dist
                building = coordinate
        # just add the barbarian to the screen , meaning game won
        if building == (-1, -1):
            return True
        # got the building make the barbarian move towards it

        direction = (building[0],
                     building[1])

        for i in range(0, 3):
            for j in range(0, 3):
                dist = self.distance((building[0]-1 + i, building[1]-1 + j))
                if dist < minDist:
                    minDist = dist
                    direction = (building[0]-1 + i, building[1]-1 + j)

        direction = (direction[0] - self.position[0],
                     direction[1] - self.position[1])
        if direction[1] == 0:
            # print("1")
            # it is in same vertical level
            if direction[0] > 0:
                # move down
                steps = 0
                attack = False
                for i in range(1, self.movement_speed + 1):
                    if self.position[0] + i < bottom and (village.tiles[self.position[0] + i][self.position[1]] == macros.EMPTY or village.tiles[self.position[0] + i][self.position[1]] == macros.BARB):
                        steps += 1
                    else:
                        attack = True
                        break
                if self.position[0] + steps > bottom:
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.EMPTY
                    self.set_position(bottom, self.position[1])
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.BARB
                    return False

                if self.position[0]+steps > building[0]:
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.EMPTY
                    self.set_position(building[0], self.position[1])
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.BARB

                else:
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.EMPTY
                    self.set_position(
                        self.position[0] + steps, self.position[1])
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.BARB

                prev = self.position[0]
                if attack == True:
                    # print(building)

                    self.attackBarbarian(
                        village, (prev + 1, self.position[1]))
            elif direction[0] < 0:
                # move up
                steps = 0
                attack = False
                for i in range(1, self.movement_speed + 1):

                    if self.position[0]-i > 1 and (village.tiles[self.position[0] - i][self.position[1]] == macros.EMPTY or village.tiles[self.position[0] - i][self.position[1]] == macros.BARB):
                        steps += 1
                    else:
                        attack = True
                        break
                if self.position[0] - steps < top:
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.EMPTY

                    self.set_position(top, self.position[1])
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.BARB

                    return False

                if self.position[0]-steps < building[0]:
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.EMPTY
                    self.set_position(building[0], self.position[1])
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.BARB
                else:
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.EMPTY
                    self.set_position(
                        self.position[0] - steps, self.position[1])
                    village.tiles[self.position[0]
                                  ][self.position[1]] = macros.BARB
                prev = self.position[0]
                if attack == True:
                    # print(building)
                    self.attackBarbarian(
                        village, (prev - 1, self.position[1]))
            elif direction[0] == 0:
                self.attackBarbarian(village, building)
        elif direction[1] > 0:
            # move right
            # print("2    ")
            steps = 0
            attack = False
            for i in range(1, self.movement_speed + 1):
                if self.position[1] + i < right and (village.tiles[self.position[0]][self.position[1] + i] == macros.EMPTY or village.tiles[self.position[0]][self.position[1] + i] == macros.BARB):
                    steps += 1
                else:
                    attack = True
                    break
            if self.position[1] + steps > right:
                self.set_position(
                    self.position[0], right)
                steps = 0
                return False
            if self.position[1]+steps > building[1]:
                self.set_position(
                    self.position[0], building[1])

            else:
                self.set_position(
                    self.position[0], self.position[1]+steps)
            prev = self.position[1]

            if attack == True:
                # print(building)
                self.attackBarbarian(
                    village, (self.position[0], prev+1))
        else:
          # move left
            # print("3")
            steps = 0
            attack = False
            for i in range(1, self.movement_speed + 1):
                if self.position[1] - i > left and (village.tiles[self.position[0]][self.position[1] - i] == macros.EMPTY or village.tiles[self.position[0]][self.position[1] - i] == macros.BARB):
                    steps += 1
                else:
                    attack = True
                    break
            # print(steps)
            if self.position[1] - steps < left:
                self.set_position(self.position[0], left)
                return False
            if self.position[1]-steps < building[1]:
                self.set_position(
                    self.position[0], building[1])
            else:
                self.set_position(
                    self.position[0], self.position[1]-steps)
            prev = self.position[1]

            if attack == True:
                self.attackBarbarian(
                    village, (self.position[0], prev-1))

            return False

    def attackBarbarian(self, village, coord):
        # print("HI")
        # print(coord)
        if self.health <= 0:
            self.alive = False
            return
        # print(coord)
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
