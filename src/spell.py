import enum


from enum import Enum
import src.globals as macros


class SpellType(Enum):
    Rage = 1
    Heal = 2


class Spell():

    def __init__(self):
        # define the spell type
        self.type = "spell"
        # define the radius of the spell
        # effect
        self.factorSpeed = 0
        self.factorHealth = 0


class HealingSpell(Spell):

    def __init__(self, type=1):
        super().__init__()
        self.type = "heal"
        self.factorHealth = 1.5

    def doHeal(self, village):

        if village.troop == "KING":
            # heal the king first
            if village.king.health > 0:
                health = village.king.health
                health *= self.factorHealth

                if health > macros.KING_HEALTH_POINTS:
                    village.king.health = macros.KING_HEALTH_POINTS
                else:
                    village.king.health = health

        elif village.troop == "QUEEN":
            # heal the queen first
            if village.queen.health > 0:
                health = village.queen.health
                health *= self.factorHealth

                if health > macros.QUEEN_HEALTH_POINTS:
                    village.queen.health = macros.QUEEN_HEALTH_POINTS
                else:
                    village.queen.health = health

        # heal the troops

        for barbs in village.barbarians:
            if barbs.alive == True:
                health = barbs.health
                health *= 1.5
                if health > macros.BARBARIAN_HEALTH_POINTS:
                    barbs.health = macros.BARBARIAN_HEALTH_POINTS
                else:
                    barbs.health = health

        for arch in village.archers:
            if arch.health > 0:
                health = arch.health
                health *= 1.5
                if health > macros.ARCHER_HEALTH_POINTS:
                    arch.health = macros.ARCHER_HEALTH_POINTS
                else:
                    arch.health = health
        for ball in village.balloon:
            if ball.health > 0:
                health = ball.health
                health *= 1.5
                if health > macros.BALLOON_HEALTH_POINTS:
                    ball.health = macros.BALLOON_HEALTH_POINTS
                else:
                    ball.health = health


class RageSpell(Spell):

    def __init__(self, type=1):
        super().__init__()
        self.type = "rage"
        self.factorSpeed = 2

    def doRage(self, village):
        # rage king first
        if village.troop == "KING":
            if village.king.health > 0:
                speed = village.king.movement_speed
                speed *= self.factorSpeed
                village.king.movement_speed = speed
                village.king.damage *= self.factorSpeed
        elif village.troop == "QUEEN":
            if village.queen.health > 0:
                speed = village.queen.movement_speed
                speed *= self.factorSpeed
                village.queen.movement_speed = speed
                village.queen.damage *= self.factorSpeed

        # rage the troops
        for barb in village.barbarians:
            if barb.alive == True:
                speed = barb.movement_speed
                speed *= self.factorSpeed
                barb.movement_speed = speed
                barb.damage *= self.factorSpeed

        for arch in village.archers:
            if arch.health > 0:
                speed = arch.movement_speed
                speed *= self.factorSpeed
                arch.movement_speed = speed
                arch.damage *= self.factorSpeed

        for ball in village.balloon:
            if ball.health > 0:
                speed = ball.movement_speed
                speed *= self.factorSpeed
                ball.movement_speed = speed
                ball.damage *= self.factorSpeed
