from random import randint
import dungeon_delvers.items as ddi


class Job():
    def __init__(self, *args, **kwargs):
        self.name = "job"
        self.hp_dice_min = 1
        self.hp_dice_max = 20
        self.abilities = []
        self.attributes = {
            'strength': 0,
            'agility': 0,
            'intellect': 0,
            'luck': 0,
        }
        self.primary_stat = ''
        job_proficiency = {
            1: {
                'proficiency': 2
            },
            2: {
                'proficiency': 2
            },
            3: {
                'proficiency': 2
            },
            4: {
                'proficiency': 2
            },
            5: {
                'proficiency': 3
            },
            6: {
                'proficiency': 3
            },
            7: {
                'proficiency': 3
            },
            8: {
                'proficiency': 3
            },
            9: {
                'proficiency': 4
            },
            10: {
                'proficiency': 4
            },
            11: {
                'proficiency': 4
            },
            12: {
                'proficiency': 4
            },
            13: {
                'proficiency': 5
            },
            14: {
                'proficiency': 5
            },
            15: {
                'proficiency': 5
            },
            16: {
                'proficiency': 5
            },
            17: {
                'proficiency': 6
            },
            18: {
                'proficiency': 6
            },
            19: {
                'proficiency': 6
            },
            20: {
                'proficiency': 6
            }
        }
        self.level = 1
        self.proficiency = job_proficiency[self.level]['proficiency']
        self.level_up_description = {
            '2': '',
            '3': '',
            '4': '',
            '5': '',
            '6': '',
            '7': '',
            '8': '',
            '9': '',
            '10': '',
            '11': '',
            '12': '',
            '13': '',
            '14': '',
            '15': '',
            '16': '',
            '17': '',
            '18': '',
            '19': '',
            '20': '',
        }
        
        

class Fighter(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "fighter"
        self.primary_stat = 'strength'
        self.hp_dice_max = 10
        self.abilities.append('basic_attack')
        self.starting_armor = ddi.Armor()
        self.starting_armor = {
                'name': 'chain mail',
                'display_name': 'Chain Mail',
                'type': 'armor',
                'proficiency_req': 'heavy',
                'quality': 'normal',
                'rarity': 'common',
                'is_magic': False,
                'magic_level': 0,
                'weight': 55,
                'cost': 75,
                'abilities': ['stealth_disadvantage', 'str_req_13', 'no_agi'],
                'armor_class': 16
            }
        self.starting_weapon = {
                'name': 'great axe',
                'display_name': 'Great Axe',
                'type': 'weapon',
                'proficiency_req': 'martial',
                'quality': 'normal',
                'rarity': 'common',
                'is_magic': False,
                'magic_level': 0,
                'weight': 7,
                'cost': 30,
                'abilities': ['two_handed'],
                'max_damage_die': 12,
                'num_dice': 1
            }
        self.level_up_description = {
            '2': 'Fighter - Level 2: Brutal Attack. Reroll 1\'s and 2\'s when calculating damage to enemies.',
            '3': '',
            '4': '',
            '5': '',
            '6': '',
            '7': '',
            '8': '',
            '9': '',
            '10': '',
            '11': '',
            '12': '',
            '13': '',
            '14': '',
            '15': '',
            '16': '',
            '17': '',
            '18': '',
            '19': '',
            '20': '',
        }
        
    
    def set_attribute_bonuses(self):
        if self.level == 4:
            self.attributes['strength'] = 2
        elif self.level == 8:
            self.attributes['strength'] = 4
        elif self.level == 12:
            self.attributes['strength'] = 6
        elif self.level == 16:
            self.attributes['strength'] = 8
        elif self.level == 20:
            self.attributes['strength'] = 10
    
    def basic_attack(self,weapon_dice, weapon_top_end_damage, bonus, target, source):
        base_roll = randint(1,20)
        luck_roll = randint(0, source.attributes['luck']['modifier'])
        total_roll = base_roll + bonus + self.proficiency + luck_roll
        damage_roll = []
        target_hit = False
        print(f'\n{source.name} - Level {source.job.level} {source.job.name.title()} (+{bonus}) is attacking {target.name} (AC {target.armor_class})')
        print(f'Base Roll - {base_roll}')
        print(f'Total Roll - {total_roll} - (Base {base_roll}) + (Strength Modifier {bonus}) + (Proficiency Modifier {self.proficiency}) + (Luck {luck_roll})')
        if base_roll == 1:
            print(f'{base_roll} - Critical Miss')
        elif base_roll == 20 or (self.level >= 10 and base_roll >= 19):
            for dice in range(weapon_dice):
                roll = randint(1, weapon_top_end_damage)
                if source.job.level >= 2:
                    if roll == 1 or roll == 2:
                        print(f'Brutal Attack, rerolling damage roll of {roll}!')
                        roll = randint(1, weapon_top_end_damage)
                        print(f'Brutal Attack, new damage roll is {roll}!')
                        damage_roll.append(roll + bonus)
                else:
                    damage_roll.append(roll + bonus)
                print(f"Damaged Roll - {damage_roll}")
            damage_roll = sum(damage_roll) * 2
            print(f'{total_roll} - Critical Hit!')
            target_hit = True
        elif total_roll > target.armor_class:
            roll = randint(1, weapon_top_end_damage)
            if source.job.level >= 2:
                if roll == 1 or roll == 2:
                    print(f'Brutal Attack, rerolling {roll} damage rolled!')
                    roll = randint(1, weapon_top_end_damage)
                    print(f'Brutal Attack, new damage roll is {roll}!')
                damage_roll.append(roll)
            else:
                damage_roll.append(roll)
                print(f"Damaged Roll - {damage_roll}")
            damage_roll = sum(damage_roll) + bonus
            target_hit = True
        else:
            print(f"{total_roll} - Miss!")

        if target_hit:
            target.take_damage(damage_roll, source)
        
        
        
                

class Barbarian(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "barbarian"
        self.hp_dice_max = 12

class Paladin(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "paladin"
        self.hp_dice_max = 10

class Wizard(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "wizard"
        self.hp_dice_max = 6

class Rogue(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "rogue"
        self.hp_dice_max = 8

class Monk(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "monk"
        self.hp_dice_max = 8