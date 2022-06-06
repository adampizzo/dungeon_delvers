from dungeon_delvers.utilities import construct_class, print_sep, clr


class Entity():
    def __init__(self, *args, **kwargs):
        self.stats = {
            'name': kwargs['name'],
            'attributes': {
                'power': {
                    'score': kwargs['power'],
                    'base': kwargs['power'],
                    'modifier': 0
                },
                'agility': {
                    'score': kwargs['agility'],
                    'base': kwargs['agility'],
                    'modifier': 0
                },
                'toughness': {
                    'score': kwargs['toughness'],
                    'base': kwargs['toughness'],
                    'modifier': 0
                },
                'guile': {
                    'score': kwargs['guile'],
                    'base': kwargs['guile'],
                    'modifier': 0
                },
                'luck': {
                    'score': kwargs['luck'],
                    'base': kwargs['luck'],
                    'modifier': 0
                }

            }
        }

        self.update_stat_modifiers()

    def print_stats(self):
        print(f"""Name - {self.stats['name']}
            \rPower - {self.stats['attributes']['power']['score']} - {self.stats['attributes']['power']['modifier']}
            \rAgility - {self.stats['attributes']['agility']['score']} - {self.stats['attributes']['agility']['modifier']}
            \rToughness - {self.stats['attributes']['toughness']['score']} - {self.stats['attributes']['toughness']['modifier']}
            \rGuile - {self.stats['attributes']['guile']['score']} - {self.stats['attributes']['guile']['modifier']}
            \rLuck - {self.stats['attributes']['luck']['score']} - {self.stats['attributes']['luck']['modifier']}
            """)

    def update_stat_modifiers(self):
        for stat in self.stats['attributes']:
            self.stats['attributes'][stat]['modifier'] = (
                self.stats['attributes'][stat]['score'] - 10) // 2


class Monster(Entity):
    pass


class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.race = construct_class(kwargs['race'].title())
        self.job = construct_class(kwargs['job'].title())
        self.stats['race'] = {}
        self.stats['race']['name'] = self.race.name
        self.stats['job'] = {}
        self.stats['job'][self.job.name] = {}
        self.stats['job'][self.job.name]['name'] = self.job.name
        self.stats['job'][self.job.name]['level'] = 1
        self.stats['exp'] = 0
        self.add_race_attributes()
        self.update_ability_scores()

    def update_ability_scores(self):
        for stat in self.stats['attributes']:
            self.stats['attributes'][stat]['score'] = self.stats['attributes'][stat]['base'] + \
                self.race.attributes[stat]
            self.stats['attributes'][stat]['modifier'] = (
                self.stats['attributes'][stat]['score'] - 10) // 2

    def print_stats(self):
        print(f"""Name - {self.stats['name']}  |  Race - {self.stats['race'].name.title()}  |  Job -  {self.stats['job'].name.title()}
            \rPower - {self.stats['attributes']['power']['score']} - {self.stats['attributes']['power']['modifier']}
            \rAgility - {self.stats['attributes']['agility']['score']} - {self.stats['attributes']['agility']['modifier']}
            \rToughness - {self.stats['attributes']['toughness']['score']} - {self.stats['attributes']['toughness']['modifier']}
            \rGuile - {self.stats['attributes']['guile']['score']} - {self.stats['attributes']['guile']['modifier']}
            \rLuck - {self.stats['attributes']['luck']['score']} - {self.stats['attributes']['luck']['modifier']}
            """)

    def add_race_attributes(self):
        for stat in self.stats['attributes']:
            self.stats['attributes'][stat]['racial_modifier'] = self.race.attributes[stat]


if __name__ == "__main__":
    jonah = Player(name='Jonah', race="human", job="fighter", power=14,
                   agility=12, toughness=10, guile=18, luck=18)
    jonah.print_stats()
