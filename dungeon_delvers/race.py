class Race():
    def __init__(self, *args, **kwargs):
        self.name = "race"
        self.size = "medium"
        self.speed = 30
        self.attributes = {
            'power': 0,
            'agility': 0,
            'toughness': 0,
            'guile': 0,
            'luck': 0
        }


class Human(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "human"
        self.display_name = "Human"
        self.attributes['power'] = 1
        self.attributes['agility'] = 1
        self.attributes['toughness'] = 1
        self.attributes['guile'] = 1
        self.attributes['luck'] = 1

class Dwarf(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "dwarf"
        self.display_name = "Dwarf"
        self.speed = 25
        self.attributes['toughness'] = 2
        self.attributes['power'] = 1

class Elf(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "elf"
        self.display_name = "Elf"
        self.attributes['agility'] = 2
        self.attributes['guile'] = 1

class Gnome(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "gnome"
        self.display_name = "Gnome"
        self.size = "small"
        self.speed = 25
        self.attributes['guile'] = 2
        self.attributes['toughness'] = 1

class Halfling(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "halfling"
        self.display_name = "Halfling"
        self.size = "small"
        self.speed = 25
        self.attributes['luck'] = 2
        self.attributes['agility'] = 2

class Halforc(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "halforc"
        self.display_name = "Half-Orc"
        self.attributes['toughness'] = 1
        self.attributes['power'] = 2

class Halfelf(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "halfelf"
        self.display_name = "Half-Elf"
        self.speed = 25
        self.attributes['toughness'] = 1
        self.attributes['luck'] = 2
        self.attributes['guile'] = 1