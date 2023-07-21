# A king is a type of troop
from src.troop import Troop
import src.globals as macros
from src.input import *
from src.barbarians import Barabarian
from src.balloon import Balloon

# define king as Troop , but control the king's position by the user
# control king using wasd keys
# space bar for using power up
# f for attack
attackRadius = 5


class King(Troop):

    def __init__(self, x, y):
        super().__init__(x, y, macros.KING_HEALTH_POINTS,
                         macros.KING_DAMAGE, macros.KING_MOVEMENT_SPEED)
        self.troop_type = macros.KING

    def moveKing(self, char, village):
        #  just to check health bar
        if char == 'w':
            # is present at the top edge of the game
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
                self.attackKing(village)

    def attackKing(self, village):
        # axe vala attack , in radius of 5 tiles
        x = int(self.position[0])
        # print(x)

        y = int(self.position[1])
        # print(y)
        attackTh = False

        for i in range(x-attackRadius, x+attackRadius+1):
            for j in range(y-attackRadius, y+attackRadius+1):
                # check if it lies inside the box frame
                if i >= 0 and i < village.height and j >= 0 and j < village.width:
                    # it can be a cannon object , or hut , or townhall , or walls , loop over them
                    if (i, j) in village.coordHut:
                        idx = village.coordHut.index((i, j))
                        if village.huts[idx].health > 0 and village.huts[idx].active == True:
                            village.huts[idx].health -= self.damage
                            if village.huts[idx].health <= 0:
                                village.village[village.huts[idx].position[0]
                                                ][village.huts[idx].position[1]] = macros.EMPTY
                                village.huts[idx].texture = macros.BACKGROUND_PIXEL
                                village.huts[idx].tile = macros.EMPTY
                                if (village.huts[idx].position[0], village.huts[idx].position[1]) in village.activeBuildings:
                                    village.huts[idx].active = False
                    # check for townhall
                    if attackTh == False and i >= macros.COORD_TOWN_HALL[0] and i < macros.COORD_TOWN_HALL[0] + len(village.townhall.drawing) and j >= macros.COORD_TOWN_HALL[1] and j < macros.COORD_TOWN_HALL[1] + len(village.townhall.drawing[0]):
                        if village.townhall.health > 0 and village.townhall.active == True:
                            village.townhall.health -= self.damage
                        # attack the townhall
                            if village.townhall.health <= 0:
                                village.townhall.active = False
                            attackTh = True

                    # check for cannons

                    if(i, j) in village.coordCannon:
                        idx = village.coordCannon.index((i, j))
                        if village.cannons[idx].health > 0 and village.cannons[idx].active == True:
                            village.cannons[idx].health -= self.damage
                            if village.cannons[idx].health <= 0:
                                village.cannons[idx].texture = macros.BACKGROUND_PIXEL
                                village.cannons[idx].tile = macros.EMPTY
                                if (village.cannons[idx].position[0], village.cannons[idx].position[1]) in village.activeBuildings:
                                    village.cannons[idx].active = False

                    if (i, j) in village.coordWizard:
                        idx = village.coordWizard.index((i, j))
                        if village.wizardTower[idx].health > 0 and village.wizardTower[idx].active == True:
                            village.wizardTower[idx].health -= self.damage
                            if village.wizardTower[idx].health <= 0:
                                village.wizardTower[idx].texture = macros.BACKGROUND_PIXEL
                                village.wizardTower[idx].tile = macros.EMPTY
                                if (village.wizardTower[idx].position[0], village.wizardTower[idx].position[1]) in village.activeBuildings:
                                    village.wizardTower[idx].active = False
                    # check for walls
                    for itr in range(0, len(village.coordWall)):
                        if i == village.coordWall[itr][0] and j == village.coordWall[itr][1]:
                            # print(itr)
                            # print(len(village.walls))
                            village.walls[itr].health -= self.damage
                            # remove the wall
                            if village.walls[itr].health <= 0:
                                village.walls[itr].texture = macros.BACKGROUND_PIXEL
                                village.walls[itr].tile = macros.EMPTY
                                village.walls[itr].active = False
