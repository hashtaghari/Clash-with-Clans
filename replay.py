from matplotlib.pyplot import table
from src.village import Village
import src.globals as macros
from src.globals import *
import time
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


f = open('src/numreplay.txt', 'r')
num = int(f.read())
if num == 0:
    print("No replays !!!")
    exit()
# print(num)
# sys.path.insert(0, './src')

timeout = 0.9
for replay in range(1, num+1):
    print("Replaying " + str(replay))
    village = Village()
    village.render()
    file_name = "replay/" + str(replay) + ".txt"
    file = open(file_name, 'r')
    data = file.readlines()
    troop_type = data[0][0]
    # print(troop_type)
    # print(type(troop_type))

    itr = 0
    for input in data:
        if itr == 0:
            itr += 1
            continue
        if input == "None":
            time.sleep(timeout)
        else:
            ret = input[0]
            if ret == 'q':
                break
            if troop_type == '1':
                village.king.moveKing(ret, village)
            else:
                village.queen.moveQueen(ret, village)

            village.render()
            village.moveBarbs()
            village.moveArcher()
            village.moveBall()
            village.shootCannon()
            village.shootWizard()
            handle_input(ret, village)
            r = village.isActive()
            if r == False:
                if village.level == 1:
                    village = Village(2, int(troop_type))
                elif village.level == 2:
                    village = Village(3, int(troop_type))
                else:
                    break
            else:
                flag = False
                for barbs in village.barbarians:
                    flag = barbs.alive
                for archs in village.archers:
                    flag = archs.alive
                for ball in village.balloons:
                    flag = ball.alive
                troopFlag = False
                if troop_type == '1':
                    troopFlag = village.king.alive
                else:
                    troopFlag = village.queen.alive
                if flag == False and village.barbs == 0 and village.archs == 0 and village.ball == 0 and troopFlag == False:
                    break
            time.sleep(0.1)
    # print("Replay " + str(replay) + " completed")
    time.sleep(timeout+1)
