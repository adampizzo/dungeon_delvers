class Race():
    def __init__(self, *args, **kwargs):
        self.name = "race"
        self.size = "medium"
        self.speed = 30
        self.attributes = {
            'strength': 0,
            'agility': 0,
            'intellect': 0,
            'luck': 0
        }


class Human(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "human"
        self.display_name = "Human"
        self.attributes['strength'] = 1
        self.attributes['agility'] = 1
        self.attributes['intellect'] = 1
        self.attributes['luck'] = 1


class Dwarf(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "dwarf"
        self.display_name = "Dwarf"
        self.speed = 25
        self.attributes['strength'] = 2
        self.attributes['luck'] = 1


class Elf(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "elf"
        self.display_name = "Elf"
        self.attributes['agility'] = 2
        self.attributes['intellect'] = 1


class Gnome(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "gnome"
        self.display_name = "Gnome"
        self.size = "small"
        self.speed = 25
        self.attributes['intellect'] = 2
        self.attributes['luck'] = 1


class Halfling(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "halfling"
        self.display_name = "Halfling"
        self.size = "small"
        self.speed = 25
        self.attributes['luck'] = 2
        self.attributes['agility'] = 1
        self.attributes['intellect'] = 1


class Halforc(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "halforc"
        self.display_name = "Half-Orc"
        self.attributes['strength'] = 2
        self.attributes['agility'] = 1


class Halfelf(Race):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "halfelf"
        self.display_name = "Half-Elf"
        self.attributes['agility'] = 1
        self.attributes['luck'] = 2
        self.attributes['strength'] = 1
