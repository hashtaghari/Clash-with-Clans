
from src.building import Building
import src.globals as macros


class Cannon(Building):

    def __init__(self, x, y, size=10, health=10):
        # create an instance of the cannon object
        super().__init__(x, y, size, macros.CANNON_HEALTH_POINTS)
        # define damage attribute for the cannon
        self.damage = macros.CANNON_DAMAGE
        # define the last shot time
        self.last_shot = 0
        self.texture = macros.CANNON
        self.tile = macros.CANNON_TILE

    def distance(self, coord):
        # using manhatten distance for finding up the nearest building !
        return abs(self.position[0] - coord[0]) + abs(self.position[1] - coord[1])

    def find_target(self, village):
        if self.health <= 0:
            self.active = False
            return
        # define a radius of tiles around the cannon ]
        # look for barbarian or the king object , choose the one which is nearest
        shoot = False
        dist = 100000
        idx = -2
        itr = 0
        troop = "barb"
        for barb in village.barbarians:
            if barb.health > 0:
                if abs(self.position[0]-barb.position[0]) <= macros.CANNON_RADIUS and abs(self.position[1]-barb.position[1]) <= macros.CANNON_RADIUS:
                    shoot = True
                    mindist = self.distance(barb.position)
                    if mindist < dist:
                        troop = "barb"
                        dist = mindist
                        idx = itr
            itr += 1
        itr = 0

        for arch in village.archers:
            if arch.health > 0:
                if abs(self.position[0]-arch.position[0]) <= macros.CANNON_RADIUS and abs(self.position[1]-arch.position[1]) <= macros.CANNON_RADIUS:
                    shoot = True
                    mindist = self.distance(arch.position)
                    if mindist < dist:
                        troop = "arch"
                        dist = mindist
                        idx = itr
            itr += 1
        # look for king
        if village.troop == "KING":
            if village.king.health > 0:
                # check if in shooting range
                if abs(self.position[0]-village.king.position[0]) <= macros.CANNON_RADIUS and abs(self.position[1]-village.king.position[1]) <= macros.CANNON_RADIUS:
                    shoot = True
                    mindist = self.distance(village.king.position)
                    if mindist < dist:
                        dist = mindist
                        troop = "king"
                        idx = -1
        else:
            #  look for the archer
            if village.queen.health > 0:
                # check if in shooting range
                if abs(self.position[0]-village.queen.position[0]) <= macros.CANNON_RADIUS and abs(self.position[1]-village.queen.position[1]) <= macros.CANNON_RADIUS:
                    shoot = True
                    mindist = self.distance(village.queen.position)
                    if mindist < dist:
                        troop = "queen"
                        dist = mindist
                        idx = -1

        if shoot == True:
            self.texture = macros.CANNON_SHOT
        else:
            health = float(self.health/macros.CANNON_HEALTH_POINTS)
            if health > 0.5:
                self.texture = macros.CANNON
            elif health > 0.2:
                self.texture = macros.midCannon
            else:
                self.texture = macros.CannonDead
        if self.health <= 0:
            self.texture = macros.BACKGROUND_PIXEL
            self.tile = macros.EMPTY
            self.active = False
            return

        if shoot == True:
            self.shoot(village, idx, troop)
        return shoot

    def shoot(self, village, idx, troop):

        if self.health <= 0:
            self.active = False
            return

        if idx == -1:
            # shoot the king
            # print("SHOOTING THE KING", village.king.health)
            if troop == "king":
                if village.king.health > 0:
                    village.king.health -= self.damage
                    if village.king.health <= 0:
                        village.king.texture = macros.GRAVE_TILE
                        village.tiles[village.king.position[0]
                                      ][village.king.position[1]] = macros.EMPTY
                        village.king.alive = False
            elif troop == "queen":
                if village.queen.health > 0:
                    village.queen.health -= self.damage
                    if village.queen.health <= 0:
                        village.queen.texture = macros.GRAVE_TILE
                        village.tiles[village.queen.position[0]
                                      ][village.queen.position[1]] = macros.EMPTY
                        village.queen.alive = False
        else:
            if troop == "barb":
                # shoot barb
                if idx >= 0:
                    # check
                    if village.barbarians[idx].health > 0:
                        village.barbarians[idx].health -= self.damage
                        if village.barbarians[idx].health <= 0:
                            village.barbarians[idx].texture = macros.GRAVE_TILE
                            village.barbarians[idx].alive = False
                            village.tiles[village.barbarians[idx].position[0]
                                          ][village.barbarians[idx].position[1]] = macros.EMPTY

            elif troop == "arch":
                # shoot arch
                if idx >= 0:
                    # check
                    if village.archers[idx].health > 0:
                        village.archers[idx].health -= self.damage
                        if village.archers[idx].health <= 0:
                            village.archers[idx].texture = macros.GRAVE_TILE
                            village.archers[idx].alive = False
                            village.tiles[village.archers[idx].position[0]
                                          ][village.archers[idx].position[1]] = macros.EMPTY
