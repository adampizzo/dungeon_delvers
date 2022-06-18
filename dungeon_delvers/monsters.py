from random import randint
import dungeon_delvers.base

class Monster(dungeon_delvers.base.Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monster_race = 'monster'
        self.max_hp = kwargs['hp']
        self.current_hp = self.max_hp
        self.armor_class = 10 + self.attributes['agility']['modifier']
        self.challenge_rating = kwargs['cr']
        monster_proficiency = {
            0: {
                'proficiency': 2,
                'exp_value': 10
            },
            .125: {
                'proficiency': 2,
                'exp_value': 25
            },
            .25: {
                'proficiency': 2,
                'exp_value': 50
            },
            .5: {
                'proficiency': 2,
                'exp_value': 100
            },
            1: {
                'proficiency': 2,
                'exp_value': 200
            },
            2: {
                'proficiency': 2,
                'exp_value': 450
            },
            3: {
                'proficiency': 2,
                'exp_value': 700
            },
            4: {
                'proficiency': 2,
                'exp_value': 1100
            },
            5: {
                'proficiency': 3,
                'exp_value': 1800
            },
            6: {
                'proficiency': 3,
                'exp_value': 2300
            },
            7: {
                'proficiency': 3,
                'exp_value': 2900
            },
            8: {
                'proficiency': 3,
                'exp_value': 3900
            },
            9: {
                'proficiency': 4,
                'exp_value': 5000
            },
            10: {
                'proficiency': 4,
                'exp_value': 5900
            },
            11: {
                'proficiency': 4,
                'exp_value': 7200
            },
            12: {
                'proficiency': 4,
                'exp_value': 8400
            },
            13: {
                'proficiency': 5,
                'exp_value': 10000
            },
            14: {
                'proficiency': 5,
                'exp_value': 11500
            },
            15: {
                'proficiency': 5,
                'exp_value': 13000
            },
            16: {
                'proficiency': 5,
                'exp_value': 15000
            },
            17: {
                'proficiency': 6,
                'exp_value': 18000
            },
            18: {
                'proficiency': 6,
                'exp_value': 20000
            },
            19: {
                'proficiency': 6,
                'exp_value': 22000
            },
            20: {
                'proficiency': 6,
                'exp_value': 25000
            },
            21: {
                'proficiency': 7,
                'exp_value': 33000
            },
            22: {
                'proficiency': 7,
                'exp_value': 41000
            },
            23: {
                'proficiency': 7,
                'exp_value': 50000
            },
            24: {
                'proficiency': 7,
                'exp_value': 62000
            },
            25: {
                'proficiency': 8,
                'exp_value': 75000
            },
            26: {
                'proficiency': 8,
                'exp_value': 90000
            },
            27: {
                'proficiency': 8,
                'exp_value': 105000
            },
            28: {
                'proficiency': 8,
                'exp_value': 12000
            },
            29: {
                'proficiency': 9,
                'exp_value': 135000
            },
            30: {
                'proficiency': 9,
                'exp_value': 155000
            },
        }
        self.proficiency = monster_proficiency[kwargs['cr']]['proficiency']
        self.exp_value = monster_proficiency[kwargs['cr']]['exp_value']
        self.starting_armor = {}
        self.starting_weapon = {}
        self.starting_shield = {}
        self.equipped_items['armor'] = self.starting_armor
        self.equipped_items['weapon'] = self.starting_weapon
        self.equipped_items['shield'] = self.starting_weapon
        self.update_stats()
        
    def take_damage(self, damage, source):
        self.current_hp -= damage
        print(f"{self.name} took {damage} damage from {source.name}.\n")
        if self.is_alive():
            print(f"{self.name} has {self.current_hp} reamining.")
        else:
            print(f"{self.name} has been slain!\n")
    
    def is_alive(self):
        if self.current_hp > 0:
            return True
    
    def basic_attack(self, target: dungeon_delvers.base.Entity):
        roll = randint(1,20)
        bonuses = self.attributes['agility']['modifier'] + self.proficiency
        total_roll = roll + bonuses
        print(f'\n{self.name} - CR {self.challenge_rating} - {self.monster_race} (+{bonuses}) is attacking {target.name} (AC {target.armor_class})')
        if total_roll >= target.armor_class:
            print(f'{total_roll} - Hit!')
            damage_roll = randint(1, self.weapon_max_damage_die) + self.attributes['agility']['modifier']
            target.take_damage(damage_roll, self)
        else:
            print(f'{total_roll} - Miss!')


class Abberation(Monster):
    pass


class Beast(Monster):
    pass


class Celestial(Monster):
    pass


class Construct(Monster):
    pass


class Dragon(Monster):
    pass


class Elemental(Monster):
    pass


class Fey(Monster):
    pass


class Fiend(Monster):
    pass


class Giant(Monster):
    pass


class Humanoid(Monster):
    pass


class Monstrosities(Monster):
    pass


class Ooze(Monster):
    pass


class Plant(Monster):
    pass


class Undead(Monster):
    pass


class Goblinoid(Humanoid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = 'small'
        self.monster_race = 'goblin'
        self.starting_armor = {
            'name': 'leather armor',
            'display_name': 'Leather Armor',
            'type': 'armor',
            'proficiency_req': 'light',
            'quality': 'normal',
            'rarity': 'common',
            'is_magic': False,
            'magic_level': 0,
            'weight': 10,
            'cost': 10,
            'abilities': [],
            'armor_class': 11
        }
        self.starting_shield = {
            'name': 'shield',
            'display_name': 'Shield',
            'type': 'armor',
            'proficiency_req': 'shield',
            'quality': 'normal',
            'rarity': 'common',
            'is_magic': False,
            'magic_level': 0,
            'weight': 6,
            'cost': 10,
            'abilities': [],
            'armor_class': 2
        }
        self.starting_weapon = {
            'name': 'scimitar',
            'display_name': 'Scimitar',
            'type': 'weapon',
            'proficiency_req': 'martial',
            'quality': 'normal',
            'rarity': 'common',
            'is_magic': False,
            'magic_level': 0,
            'weight': 3,
            'cost': 25,
            'abilities': ['finesse', 'light'],
            'max_damage_die': 6,
            'num_dice': 1
        }
        self.equipped_items['armor'] = self.starting_armor
        self.equipped_items['weapon'] = self.starting_weapon
        self.equipped_items['shield'] = self.starting_shield
        self.update_stats()

if __name__ == '__main__':
        new_mon = Goblinoid(
        name='Goblin Boss', strength=14, agility=12, intellect=8, luck=0, hp=21, cr=1)
        
        print(dir(new_mon))