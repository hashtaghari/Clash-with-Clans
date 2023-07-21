from colorama import Fore, Style, Back
from os import system as sys

import math
from time import *
import src.globals as macros
from src.king import King
from src.townhall import TownHall
from src.hut import Hut
from src.cannon import Cannon
from src.wall import Wall
from src.barbarians import Barabarian
from src.spell import RageSpell, HealingSpell
from src.archerQueen import Queen
import src.levels as LEVELS
from src.wizardTower import WizardTower


class Village():

    def __init__(self, level=1, choice=1):

        self.troop = "KING"
        if choice == 2:
            self.troop = "QUEEN"
        self.level = level

        # specify the village ka dimension
        self.width = macros.VILLAGE_WIDTH
        self.height = macros.VILLAGE_HEIGHT
        self.village = [[macros.BACKGROUND_PIXEL for i in range(macros.DISPLAY_WIDTH)]
                        for j in range(macros.DISPLAY_HEIGHT)]
        # initialize the village tiles
        self.tiles = [[0 for i in range(macros.DISPLAY_WIDTH)]
                      for j in range(macros.DISPLAY_HEIGHT)]

        if self.troop == "KING":
            self.king = King(10, 1)
        else:
            self.queen = Queen(10, 1)

        self.townhall = TownHall(3, 24)
        self.coordCannon = LEVELS.Level1["coord_cannon"]
        self.spawningPoints = [
            (int(macros.VILLAGE_HEIGHT)-2, int(macros.VILLAGE_WIDTH/2)), (int(macros.VILLAGE_HEIGHT/2), int(macros.VILLAGE_WIDTH)-2), (int(macros.VILLAGE_HEIGHT/2), 1)]
        self.coordWall = []
        self.coordWizard = LEVELS.Level1["coord_wizard"]
        self.barbs = 6
        self.archs = 6
        self.ball = 3
        if level == 2:
            self.coordCannon = LEVELS.Level2["coord_cannon"]
            self.coordWizard = LEVELS.Level2["coord_wizard"]
        elif level == 3:
            self.coordCannon = LEVELS.Level3["coord_cannon"]
            self.coordWizard = LEVELS.Level3["coord_wizard"]

        self.cannons = [Cannon(x, y) for (x, y) in self.coordCannon]
        self.wizardTower = [WizardTower(x, y) for (x, y) in self.coordWizard]

        left = int((macros.VILLAGE_WIDTH/2) - 10) - 3
        right = int(macros.VILLAGE_WIDTH/2 - 10 +
                    len(self.townhall.drawing[0])-1)+3
        top = int(macros.VILLAGE_HEIGHT/2)-3
        bottom = int(macros.VILLAGE_HEIGHT/2 + len(self.townhall.drawing)-1)+3
        self.walls = []
        self.rage = RageSpell()
        self.heal = HealingSpell()
        self.healSpell = 0
        self.rageSpell = 0
        self.campsize = 0

        self.coordHut = [(top + 1, left + 1), (top+1, left + 2),
                         (top + 1, left+3), (bottom-1, right-2), (bottom-1, right-3), (bottom-1, right-1)]
        self.huts = [Hut(x, y) for (x, y) in self.coordHut]

        for i in range(top, bottom+1):
            if self.coordWall.count((i, left, 1)) == 0:
                self.coordWall.append((i, left, 1))
            if self.coordWall.count((i, right, 2)) == 0:
                self.coordWall.append((i, right, 2))

        for j in range(left, right):
            if self.coordWall.count((top, j, 1)) == 0:
                self.coordWall.append((top, j, 2))
            if self.coordWall.count((bottom, j, 3)) == 0:
                self.coordWall.append((bottom, j, 3))

        left -= 4
        right += 4
        top -= 5
        bottom += 5
        for i in range(top, bottom+1):
            if self.coordWall.count((i, left, 1)) == 0:
                self.coordWall.append((i, left, 1))
            if self.coordWall.count((i, right, 2)) == 0:
                self.coordWall.append((i, right, 2))

        for j in range(left, right):
            if self.coordWall.count((top, j, 1)) == 0:
                self.coordWall.append((top, j, 2))
            if self.coordWall.count((bottom, j, 3)) == 0:
                self.coordWall.append((bottom, j, 3))

        for (x, y, level) in self.coordWall:
            self.walls.append(Wall(x=x, y=y, level=level))

        self.activeBuildings = []

        # add all the cannons to the list

        for coord in self.coordCannon:
            self.activeBuildings.append(coord)

        for coord in self.coordWizard:
            self.activeBuildings.append(coord)
        # add all the huts to the list

        for coord in self.coordHut:
            self.activeBuildings.append(coord)

        # add all the townhall tiles to the list

        # render the barbarians
        for i in range(macros.COORD_TOWN_HALL[0], macros.COORD_TOWN_HALL[0] + len(self.townhall.drawing)):
            for j in range(macros.COORD_TOWN_HALL[1], macros.COORD_TOWN_HALL[1] + len(self.townhall.drawing[0])):
                self.activeBuildings.append((i, j))

        self.barbarians = []
        self.archers = []
        self.balloons = []
        f = open('src/logo.txt', 'r')
        self.logo = (''.join([line for line in f])).split('\n')

    def isActive(self):

        for hut in self.huts:
            if hut.health > 0:
                return True
        if self.townhall.health > 0:
            return True
        for can in self.cannons:
            if can.health > 0:
                return True
        for wiz in self.wizardTower:
            if wiz.health > 0:
                return True

        return False

    def gameWon(self):
        sys('clear')
        for i in range(macros.DISPLAY_HEIGHT):
            for j in range(macros.DISPLAY_WIDTH):
                # render the game border
                if i == 0 or (j == 0 or j == macros.DISPLAY_WIDTH-1 or i == 0 or i == macros.DISPLAY_HEIGHT-1):
                    self.village[i][j] = macros.BORDER_PIXEL
                else:
                    self.village[i][j] = Back.BLACK + \
                        Fore.WHITE + ' ' + Style.RESET_ALL
        f = open('src/gamewon.txt', 'r')
        list = (''.join([line for line in f])).split('\n')
        for line in list:
            print(line)

    def gameLost(self):
        sys('clear')
        for i in range(macros.DISPLAY_HEIGHT):
            for j in range(macros.DISPLAY_WIDTH):
                # render the game border
                if i == 0 or (j == 0 or j == macros.DISPLAY_WIDTH-1 or i == 0 or i == macros.DISPLAY_HEIGHT-1):
                    self.village[i][j] = macros.BORDER_PIXEL
                else:
                    self.village[i][j] = Back.BLACK + \
                        Fore.WHITE + ' ' + Style.RESET_ALL
        f = open('src/gamelost.txt', 'r')
        list = (''.join([line for line in f])).split('\n')
        r = 10
        c = macros.VILLAGE_WIDTH-20
        for line in list:
            print(line)

    def renderScoreBoard(self):

        if self.troop == "KING":
            king_health = self.king.health
            max_health = macros.KING_HEALTH_POINTS
            display_health = math.ceil(float((king_health/max_health) *
                                             macros.DISPLAY_WIDTH))

            for i in range(display_health):
                self.village[0][i] = Back.RED + " " + Style.RESET_ALL

        else:
            queen_health = self.queen.health
            max_health = macros.QUEEN_HEALTH_POINTS
            display_health = math.ceil(float((queen_health/max_health) *
                                             macros.DISPLAY_WIDTH))

            for i in range(display_health):
                self.village[0][i] = Back.RED + " " + Style.RESET_ALL

        # for i in range(macros.VILLAGE_WIDTH+2, macros.DISPLAY_WIDTH):
        r = 5

        for row in range(len(self.logo)):
            for col in range(len(self.logo[row])):
                self.village[row+r][col+macros.VILLAGE_WIDTH +
                                    2] = Back.BLUE + self.logo[row][col] + Style.RESET_ALL
            r += 1

    def drawWalls(self):
        for i in self.walls:
            if i.health > 0:
                max_health = macros.HWALL_LEVEL_1
                if i.level == 2:
                    max_health = macros.HWALL_LEVEL_2
                elif i.level == 3:
                    max_health = macros.HWALL_LEVEL_3
                health = float(i.health/max_health)
                if i.level == 1:
                    if health > 0.5:
                        i.texture = macros.WALL_LEVEL_1
                    elif health > 0.2:
                        i.texture = Back.LIGHTYELLOW_EX+'*'+Style.RESET_ALL
                    else:
                        i.texture = Back.LIGHTRED_EX+'*'+Style.RESET_ALL
                elif i.level == 2:
                    if health > 0.5:
                        i.texture = macros.WALL_LEVEL_2
                    elif health > 0.2:
                        i.texture = Back.LIGHTMAGENTA_EX+'*'+Style.RESET_ALL
                    else:
                        i.texture = Back.LIGHTRED_EX+'*'+Style.RESET_ALL

                elif i.level == 3:
                    if health > 0.5:
                        i.texture = macros.WALL_LEVEL_3
                    elif health > 0.2:
                        i.texture = Back.LIGHTCYAN_EX+'*'+Style.RESET_ALL
                    else:
                        i.texture = Back.LIGHTRED_EX+'*'+Style.RESET_ALL

            self.village[i.position[0]][i.position[1]] = i.texture
            self.tiles[i.position[0]][i.position[1]] = i.tile

    def render(self, choice=1):
        # initialize the village
        # sys('clear')
        print("\033[%d;%dH" % (0, 0))

        for i in range(macros.DISPLAY_HEIGHT):
            for j in range(macros.DISPLAY_WIDTH):
                # render the game border
                if j < self.width and (j == 0 or j == self.width-1 or i == 0 or i == self.height-1):
                    self.village[i][j] = macros.BORDER_PIXEL
                    self.tiles[i][j] = -1
                else:
                    # the main score card area
                    if j >= self.width:
                        self.village[i][j] = macros.SCORECARD_PIXEL
                    else:
                        # background pixel
                        self.village[i][j] = macros.BACKGROUND_PIXEL

        # render the main town hall
        for row in range(0, len(self.townhall.drawing)):
            for col in range(0, len(self.townhall.drawing[row])):
                if self.townhall.health > 0:
                    back = Back.GREEN
                    health = float(self.townhall.health /
                                   macros.TOWN_HALL_HEALTH)
                    if health > 0.5:
                        back = Back.GREEN
                    elif health > 0.2:
                        back = Back.YELLOW
                    else:
                        back = Back.LIGHTRED_EX

                    self.tiles[macros.COORD_TOWN_HALL[0] +
                               row][macros.COORD_TOWN_HALL[1] + col] = macros.TOWN_HALL
                    self.village[macros.COORD_TOWN_HALL[0]+row][macros.COORD_TOWN_HALL[1] +
                                                                col] = back + Fore.RED + self.townhall.drawing[row][col] + Style.RESET_ALL
                else:
                    self.tiles[macros.COORD_TOWN_HALL[0] +
                               row][macros.COORD_TOWN_HALL[1] + col] = macros.EMPTY
                    self.village[macros.COORD_TOWN_HALL[0]+row][macros.COORD_TOWN_HALL[1] +
                                                                col] = macros.BACKGROUND_PIXEL
                    # render walls around the townhall
        self.drawWalls()

        # render the village
        self.renderScoreBoard()

        # render the huts
        itr = 0
        for (x, y) in self.coordHut:
            if self.huts[itr].health > 0:
                self.tiles[x][y] = self.huts[itr].tile
                health = float(self.huts[itr].health/100)
                texture = macros.HUT
                if health > 0.5:
                    texture = macros.HUT
                elif health > 0.2:
                    texture = Back.LIGHTMAGENTA_EX+Fore.BLACK+"H" + Style.RESET_ALL
                else:
                    texture = Back.LIGHTRED_EX + Fore.BLACK+"H" + Style.RESET_ALL
                self.village[x][y] = texture

            else:
                self.village[x][y] = self.huts[itr].texture
                self.tiles[x][y] = self.huts[itr].tile
            itr += 1
        itr = 0
        # render the cannons
        for (x, y) in self.coordCannon:
            if self.cannons[itr].health > 0:
                # print(str(self.cannons[itr].texture))
                self.tiles[x][y] = self.cannons[itr].tile
                health = float(
                    self.cannons[itr].health/macros.CANNON_HEALTH_POINTS)
                texture = macros.CANNON
                if self.cannons[itr].texture == macros.CANNON_SHOT:
                    # print("CANNNON", self.cannons[itr].health)
                    self.village[x][y] = self.cannons[itr].texture
                    self.tiles[x][y] = self.cannons[itr].tile
                else:
                    if health > 0.5:
                        texture = macros.CANNON
                    elif health > 0.2:
                        texture = macros.midCannon
                    else:
                        texture = macros.CannonDead
                    self.village[x][y] = texture
            else:
                self.village[x][y] = self.cannons[itr].texture
                self.tiles[x][y] = self.cannons[itr].tile
            itr += 1
        # render the spawning points
        itr = 0
        for (x, y) in self.coordWizard:
            if self.wizardTower[itr].health > 0:
                self.tiles[x][y] = self.wizardTower[itr].tile
                health = float(
                    self.wizardTower[itr].health/macros.WIZARD_HEALTH)
                texture = macros.WIZARD
                if self.wizardTower[itr].texture == macros.WIZARD_SHOT:
                    self.village[x][y] = self.wizardTower[itr].texture
                    self.tiles[x][y] = self.wizardTower[itr].tile
                else:
                    if health > 0.5:
                        texture = macros.WIZARD
                    elif health > 0.2:
                        texture = Back.LIGHTMAGENTA_EX+Fore.BLACK+"W" + Style.RESET_ALL
                    else:
                        texture = Back.LIGHTRED_EX + Fore.BLACK+"W" + Style.RESET_ALL
                    self.village[x][y] = texture
            else:
                self.village[x][y] = self.wizardTower[itr].texture
                self.tiles[x][y] = self.wizardTower[itr].tile
            itr += 1

        for (x, y) in self.spawningPoints:
            self.village[x][y] = macros.RED_PIXEL

        # render the king
        if self.troop == "KING":
            self.village[self.king.position[0]
                         ][self.king.position[1]] = macros.KING_TILE if self.king.health > 0 else macros.GRAVE_TILE
        elif self.troop == "QUEEN":
            self.village[self.queen.position[0]][self.queen.position[1]
                                                 ] = macros.QUEEN_TILE if self.queen.health > 0 else macros.GRAVE_TILE
        # render barbarians
        for barbarians in self.barbarians:
            if barbarians.alive == True:
                #   /  print(barbarians.health)
                health = float(barbarians.health /
                               macros.BARBARIAN_HEALTH_POINTS)
                if health > 0.5:
                    barbarians.texture = macros.BARBARIAN_TILE
                elif health > 0.2:
                    barbarians.texture = Back.LIGHTCYAN_EX + Fore.BLACK + "B" + Style.RESET_ALL
                elif health > 0:
                    barbarians.texture = Back.LIGHTYELLOW_EX + Fore.BLACK + "B" + Style.RESET_ALL
                else:
                    barbarians.texture = macros.GRAVE_TILE

            self.village[barbarians.position[0]
                         ][barbarians.position[1]] = barbarians.texture

        for archers in self.archers:
            if archers.alive == True:
                # print(archers.movement_speed)
                health = float((2*archers.health) /
                               macros.BARBARIAN_HEALTH_POINTS)
                if health > 0.5:
                    archers.texture = macros.ARCHER_TILE
                elif health > 0.2:
                    archers.texture = Back.LIGHTCYAN_EX + Fore.BLACK + "A" + Style.RESET_ALL
                elif health > 0:
                    archers.texture = Back.LIGHTYELLOW_EX + Fore.BLACK + "A" + Style.RESET_ALL
                else:
                    archers.texture = macros.GRAVE_TILE

            self.village[archers.position[0]
                         ][archers.position[1]] = archers.texture
        for balloons in self.balloons:
            if balloons.alive == True:
                health = float(balloons.health / macros.BALLOON_HEALTH)
                # print(balloons.texture)
                # if balloons.texture != macros.BALLOON_SHOT:
                if health > 0.5:
                    # print("ok")
                    balloons.texture = macros.BALLOON_TEXTURE
                elif health > 0.2:
                    print("notok1")
                    balloons.texture = Back.LIGHTCYAN_EX + Fore.BLACK + "O" + Style.RESET_ALL
                elif health > 0:
                    # print("notok2")
                    balloons.texture = Back.LIGHTYELLOW_EX + Fore.BLACK + "O" + Style.RESET_ALL
                else:
                    balloons.texture = macros.GRAVE_TILE

            self.village[balloons.position[0]
                         ][balloons.position[1]] = balloons.texture

        # self.village[self.queen.position[0]
        #              ][self.queen.position[1]+16] = Fore.BLACK+Back.BLACK+"Q"+ Style.RESET_ALL
        # self.village[self.queen.position[0]
        #              ][self.queen.position[1]+20] = Fore.BLACK+Back.RED+"Q"+ Style.RESET_ALL
       
        for row in range(macros.DISPLAY_HEIGHT):
            for col in range(macros.DISPLAY_WIDTH):
                print(self.village[row][col],
                      end='\n' if col == macros.DISPLAY_WIDTH-1 else '')

    def shootCannon(self):
        for cannon in self.cannons:
            cannon.find_target(self)

    def shootWizard(self):
        for wizard in self.wizardTower:
            wizard.find_target(self)

    def moveBarbs(self):
        for barbs in self.barbarians:
            ret = barbs.move_barbarian(self)
            if ret == True:
                return True

    def moveBall(self):
        for ball in self.balloons:
            ball.move_balloon(self)

    def moveArcher(self):
        for archer in self.archers:
            archer.move_archer(self)
