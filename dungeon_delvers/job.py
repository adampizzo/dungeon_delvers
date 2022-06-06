class Job():
    def __init__(self, *args, **kwargs):
        self.name = "job"
        self.hp_dice_min = 1
        self.hp_dice_max = 20

class Fighter(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "fighter"
        self.hp_dice_max = 10

class Barbarian(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "barbarian"
        self.hp_dice_max = 12

class Cleric(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "cleric"
        self.hp_dice_max = 8

class Sorcerer(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "sorcerer"
        self.hp_dice_max = 6

class Rogue(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "rogue"
        self.hp_dice_max = 8