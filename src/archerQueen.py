from pickle import TRUE
from src.troop import Troop
import src.globals as macros
from colorama import Fore, Style, Back

# special troop , control king's position by the user
# usig the ijkl keys similiar to wasd key combination


class Queen(Troop):

    def __init__(self, x, y):
        super().__init__(x, y, macros.QUEEN_HEALTH_POINTS,
                         macros.QUEEN_DAMAGE, macros.QUEEN_MOVEMENT_SPEED)
        self.troop_type = macros.QUEEN
        self.move_direction = ""

    def moveQueen(self, char, village, flag="FALSE"):
        if char == 'w' or char == 'a' or char == 's' or char == 'd':
            self.move_direction = char
        if char == 'w':
            if self.health > 0:
                if self.position[0] > 0:
                    steps = 0
                    for i in range(1, self.movement_speed+1):
                        if village.tiles[self.position[0]-i][self.position[1]] == macros.EMPTY and self.position[0]-i > 0:
                            steps += 1
                        else:
                            break
                    self.position = (
                        self.position[0] - steps, self.position[1])
        elif char == 's':
            if self.health > 0:
                if self.position[0] < village.height - 1:
                    steps = 0
                    for i in range(1, self.movement_speed+1):
                        if village.tiles[self.position[0]+i][self.position[1]] == macros.EMPTY and self.position[0]+i < village.height - 1:
                            steps += 1
                        else:
                            break
                    self.position = (
                        self.position[0] + steps, self.position[1])
        elif char == 'a':
            if self.health > 0:
                if self.position[1] > 0:
                    steps = 0
                    for i in range(1, self.movement_speed+1):
                        if village.tiles[self.position[0]][self.position[1]-i] == macros.EMPTY and self.position[1]-i > 0:
                            steps += 1
                        else:
                            break
                    self.position = (
                        self.position[0], self.position[1] - steps)
        elif char == 'd':
            if self.health > 0:
                if self.position[1] < village.width - 1:
                    steps = 0
                    for i in range(1, self.movement_speed+1):
                        if village.tiles[self.position[0]][self.position[1]+i] == macros.EMPTY and self.position[1]+i < village.width - 1:
                            steps += 1
                        else:
                            break
                    self.position = (
                        self.position[0], self.position[1] + steps)
        elif char == ' ':
            if self.health > 0:
                print(flag)
                if flag == "TRUE":
                    self.attackQueen(village, 9, 16)
                else:
                    self.attackQueen(village)

    def attackQueen(self, village, area_parameter=5, dist_parameter=8):
        # choose the nearest building in vicinity of attack distance
        # attack that building , and neighbouring whatever lies in area of AoE
        # find the nearest building
        # find the nearest building in the move direction4
        attack_coord = []
        print(area_parameter)
        print(dist_parameter)
        AOE = int(area_parameter/2)

        if self.move_direction == 'w':
            curr_y = self.position[0]
            if curr_y - dist_parameter < 1:
                return
            else:
                coord = curr_y - dist_parameter

                top = coord - AOE  # attack the townhall and the nearby defense area thingys
                bottom = coord + AOE+1
                left = self.position[1] - AOE
                right = self.position[1] + AOE+1

                if top < 1:
                    top = 1
                if bottom >= village.height - 1:
                    bottom = village.height - 2
                if left <= 1:
                    left = 1
                if right >= village.width - 1:
                    right = village.width - 2
                TH = False
                for i in range(top, bottom):
                    for j in range(left, right):
                        if village.tiles[i][j] == macros.TOWN_HALL and TH == False:
                            TH = True
                            attack_coord.append((i, j))
                        elif village.tiles[i][j] == macros.EMPTY or village.tiles[i][j] == macros.ARCH or village.tiles[i][j] == macros.BARB or village.tiles[i][j] == macros.BALLOON:
                            continue
                        else:
                            attack_coord.append((i, j))
        elif self.move_direction == 's':
            coord = self.position[0] + dist_parameter
            if coord >= village.height - 1:
                return
            else:
                top = coord - AOE
                bottom = coord + AOE+1
                left = self.position[1] - AOE
                right = self.position[1] + AOE+1
                if top < 1:
                    top = 1
                if bottom >= village.height - 1:
                    bottom = village.height - 2
                if left < 1:
                    left = 1
                if right >= village.width - 1:
                    right = village.width - 2
                TH = False
                for i in range(top, bottom):
                    for j in range(left, right):
                        if village.tiles[i][j] == macros.TOWN_HALL and TH == False:
                            TH = True
                            attack_coord.append((i, j))
                        elif village.tiles[i][j] == macros.EMPTY or village.tiles[i][j] == macros.ARCH or village.tiles[i][j] == macros.BARB or village.tiles[i][j] == macros.BALLOON:
                            continue
                        else:
                            attack_coord.append((i, j))
        elif self.move_direction == 'a':
            coord = self.position[1] - dist_parameter
            if coord < 1:
                return
            else:
                top = self.position[0] - AOE
                bottom = self.position[0] + AOE+1
                left = coord - AOE
                right = coord + AOE+1
                if top < 1:
                    top = 1
                if bottom >= village.height - 1:
                    bottom = village.height - 2
                if left < 1:
                    left = 1
                if right >= village.width - 1:
                    right = village.width - 2
                TH = False
                for i in range(top, bottom):
                    for j in range(left, right):
                        if village.tiles[i][j] == macros.TOWN_HALL and TH == False:
                            TH = True
                            attack_coord.append((i, j))
                        elif village.tiles[i][j] == macros.EMPTY or village.tiles[i][j] == macros.ARCH or village.tiles[i][j] == macros.BARB or village.tiles[i][j] == macros.BALLOON:
                            continue
                        else:
                            attack_coord.append((i, j))
        elif self.move_direction == 'd':
            coord = self.position[1]+dist_parameter
            if coord >= village.width - 1:
                return
            else:
                top = self.position[0] - AOE
                bottom = self.position[0] + AOE+1
                left = coord - AOE
                right = coord + AOE+1
                if top < 1:
                    top = 1
                if bottom >= village.height - 1:
                    bottom = village.height - 2
                if left < 1:
                    left = 1
                if right >= village.width - 1:
                    right = village.width - 2
                TH = False

                for i in range(top, bottom):
                    for j in range(left, right):
                        if village.tiles[i][j] == macros.TOWN_HALL and TH == False:
                            TH = True
                            attack_coord.append((i, j))
                        elif village.tiles[i][j] == macros.EMPTY or village.tiles[i][j] == macros.ARCH or village.tiles[i][j] == macros.BARB or village.tiles[i][j] == macros.BALLOON:
                            continue
                        else:
                            attack_coord.append((i, j))

        for coord in attack_coord:
            if village.tiles[coord[0]][coord[1]] == macros.TOWN_HALL:
                if village.townhall.health > 0:
                    village.townhall.health -= self.damage
                    if village.townhall.health <= 0:
                        village.townhall.active = False
                        for i in range(macros.COORD_TOWN_HALL[0], macros.COORD_TOWN_HALL[0] + 4):
                            for j in range(macros.COORD_TOWN_HALL[1], macros.COORD_TOWN_HALL[1] + 12):
                                # village.activeBuildings.remove((i, j))
                                village.tiles[i][j] = macros.EMPTY
                                village.village[i][j] = macros.BACKGROUND_PIXEL

            if village.tiles[coord[0]][coord[1]] == macros.HUT_TILE:

                itr = village.coordHut.index(coord)
                if itr >= 0 and village.huts[itr].health > 0 and village.huts[itr].active == True:
                    village.huts[itr].health -= self.damage
                    if village.huts[itr].health <= 0:
                        village.huts[itr].active = False
                        village.huts[itr].texture = macros.BACKGROUND_PIXEL
                        village.huts[itr].tile = macros.EMPTY

            if village.tiles[coord[0]][coord[1]] == macros.WIZARD_TILE:
                itr = village.coordWizard.index(coord)
                if itr >= 0 and village.wizardTower[itr].health > 0 and village.wizardTower[itr].active == True:
                    village.wizardTower[itr].health -= self.damage
                    if village.wizardTower[itr].health <= 0:
                        village.wizardTower[itr].active = False
                        village.wizardTower[itr].texture = macros.BACKGROUND_PIXEL
                        village.wizardTower[itr].tile = macros.EMPTY

            if village.tiles[coord[0]][coord[1]] == macros.CANNON_TILE:
                itr = village.coordCannon.index(coord)
                if itr >= 0 and village.cannons[itr].health > 0 and village.cannons[itr].active == True:
                    village.cannons[itr].health -= self.damage
                    if village.cannons[itr].health <= 0:
                        village.cannons[itr].active = False
                        village.cannons[itr].texture = macros.BACKGROUND_PIXEL
                        village.cannons[itr].tile = macros.EMPTY

            if village.tiles[coord[0]][coord[1]] == macros.TILE_WALL_LEVEL_1 or village.tiles[coord[0]][coord[1]] == macros.TILE_WALL_LEVEL_2 or village.tiles[coord[0]][coord[1]] == macros.TILE_WALL_LEVEL_3:
                level = 1
                if village.tiles[coord[0]][coord[1]] == macros.TILE_WALL_LEVEL_2:
                    level = 2
                if village.tiles[coord[0]][coord[1]] == macros.TILE_WALL_LEVEL_3:
                    level = 3
                idx = village.coordWall.index((coord[0], coord[1], level))
                if idx >= 0 and village.walls[idx].health > 0 and village.walls[idx].active == True:
                    village.walls[idx].health -= self.damage
                    if village.walls[idx].health <= 0:
                        village.walls[idx].active = False
                        village.walls[idx].texture = macros.BACKGROUND_PIXEL
                        village.walls[idx].tile = macros.EMPTY
