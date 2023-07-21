from pickle import TRUE
from src.village import Village
from src.input import *
import src.globals as macros
import src.levels as levels
from src.barbarians import Barabarian
from src.balloon import Balloon
from src.archer import Archer
import threading


def handle_input(char, village):
    # defining 1 , 2, 3 as spawning points
    if char == 'z':
        # if village.campsize < macros.CAMP_SIZE:
        if village.barbs > 0:
            village.barbs -= 1
            village.barbarians.append(Barabarian(
                village.spawningPoints[0][0], village.spawningPoints[0][1]))
    elif char == 'x':
        if village.barbs > 0:
            village.barbs -= 1

            village.barbarians.append(Barabarian(
                village.spawningPoints[1][0], village.spawningPoints[1][1]))
    elif char == 'c':
        if village.barbs > 0:
            village.barbs -= 1
            village.barbarians.append(Barabarian(
                village.spawningPoints[2][0], village.spawningPoints[2][1]))
    elif char == 'r':
        if village.rageSpell < macros.RAGE_SPELL:
            village.rageSpell += 1
            village.rage.doRage(village)
    elif char == 'h':
        if village.healSpell < macros.HEAL_SPELL:
            village.healSpell += 1
            village.heal.doHeal(village)
    elif char == '1':
        #  spawn balloon
        if village.ball > 0:
            village.ball -= 1
            village.balloons.append(Balloon(village.spawningPoints[0][0], village.spawningPoints[0]
                                    [1], macros.BALLOON_HEALTH, macros.BALLOON_DAMAGE, macros.BALLOON_MOVEMENT_SPEED))
    elif char == '2':
        #  spawn balloon
        if village.ball > 0:
            village.ball -= 1
            village.balloons.append(Balloon(
                village.spawningPoints[1][0], village.spawningPoints[1][1], macros.BALLOON_HEALTH, macros.BALLOON_DAMAGE, macros.BALLOON_MOVEMENT_SPEED))

    elif char == '3':

        #  spawn balloon
        if village.ball > 0:
            village.ball -= 1
            village.balloons.append(Balloon(village.spawningPoints[2][0], village.spawningPoints[2]
                                    [1], macros.BALLOON_HEALTH, macros.BALLOON_DAMAGE, macros.BALLOON_MOVEMENT_SPEED))

    elif char == '4':
        if village.archs > 0:
            village.archs -= 1
            village.archers.append(
                Archer(village.spawningPoints[0][0], village.spawningPoints[0][1]))

    elif char == '5':
        if village.archs > 0:
            village.archs -= 1
            village.archers.append(
                Archer(village.spawningPoints[1][0], village.spawningPoints[1][1]))
    elif char == '6':
        if village.archs > 0:
            village.archs -= 1
            village.archers.append(
                Archer(village.spawningPoints[2][0], village.spawningPoints[2][1]))

    elif char == 'f':
        if village.troop == "QUEEN":
            #  queen special move
            #  queen showing her moves
            thread = threading.Timer(
                1, village.queen.moveQueen, [' ', village, "TRUE"])
            thread.start()


def Run(choice):
    # choice refers to king or queen chosen by the player
    # choice = 1 for king
    # choice = 2 for queen
    village = Village(1, choice)
    village.render()
    inputArr = []
    inputArr.append(choice)
    f = open('src/numreplay.txt', 'r+')
    data = f.readlines()
    n = int(data[0])
    f.close()
    while(True):

        ch = input_to(Get().__call__)
        inputArr.append(ch)
        handle_input(ch, village)
        if choice == 1:
            village.king.moveKing(ch, village)
        else:
            village.queen.moveQueen(ch, village)
        if ch == 'q':
            f = open('src/numreplay.txt', 'w')
            f.write(str(n+1))
            f.close()
            file_name = "replay/" + str(n+1)+".txt"
            file = open(file_name, 'w')
            for i in inputArr:
                file.write(str(i)+'\n')
            file.close()
            village.gameLost()
            break
        else:
            village.render()
            village.moveBarbs()
            village.shootCannon()
            village.shootWizard()
            village.moveBall()
            village.moveArcher()
            ret = village.isActive()
            # print(ret)
            if ret == False:
                if village.level == 1:
                    village = Village(2, choice)
                elif village.level == 2:
                    village = Village(3, choice)
                else:
                    file_name = "replay/" + str(n+1)+".txt"
                    file = open(file_name, 'w')
                    for i in inputArr:
                        file.write(str(i)+'\n')
                    file.close()
                    f = open('src/numreplay.txt', 'w')
                    f.write(str(n+1))
                    f.close()
                    village.gameWon()
                    break
                    # set the new variables ig
                # village.campsize = 20
            else:
                # game lost
                flag = False

                for barbs in village.barbarians:
                    flag = barbs.alive
                for archs in village.archers:
                    flag = archs.alive
                for ball in village.balloons:
                    flag = ball.alive

                troopFlag = False
                if choice == 1:
                    troopFlag = village.king.alive
                else:
                    troopFlag = village.queen.alive
                if flag == False and village.barbs == 0 and village.archs == 0 and village.ball == 0 and troopFlag == False:
                    village.gameLost()
                    break
