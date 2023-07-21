from colorama import Fore, Style, Back


class Building():

    def __init__(self, x, y, size=(1, 1), health=10):
        # define the building's position
        self.position = (x, y)
        # define the size of the building
        self.size = size
        # set the health for the building
        self.health = health
        # gib points upon destroying the building
        self.points = 1
        # define boolean expression
        self.active = True
        self.high_health = 0.5*health
        self.medium_health = 0.2*health
       

    def deal_damage(self, damage):
        self.health -= damage

    def get_position(self):
        return self.position
