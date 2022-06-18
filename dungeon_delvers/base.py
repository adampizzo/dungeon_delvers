import pprint
from random import randint, random, choice
from time import sleep
from typing import Type

from dungeon_delvers.utilities import construct_class, print_sep, clr



class Entity():
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']
        self.attributes = {
            'strength': {
                'score': kwargs['strength'],
                'base': kwargs['strength'],
                'modifier': 0
            },
            'agility': {
                'score': kwargs['agility'],
                'base': kwargs['agility'],
                'modifier': 0
            },
            'intellect': {
                'score': kwargs['intellect'],
                'base': kwargs['intellect'],
                'modifier': 0
            },
            'luck': {
                'score': kwargs['luck'],
                'base': kwargs['luck'],
                'modifier': 0
            },
        }
        self.equipped_items = {
            'armor': {},
            'weapon': {},
            'shield': {},
        }
        self.other_items = []
        self.update_stat_modifiers()

    def print_stats(self):
        print(f"""Name - {self.name}
            \rStrength - {self.attributes['strength']['score']} - {self.attributes['strength']['modifier']}
            \rAgility - {self.attributes['agility']['score']} - {self.attributes['agility']['modifier']}
            \rIntellect - {self.attributes['intellect']['score']} - {self.attributes['intellect']['modifier']}
            """)

    def update_stat_modifiers(self):
        for stat in self.attributes:
            self.attributes[stat]['modifier'] = (
                self.attributes[stat]['score'] - 10) // 2

    def is_slot_empty(self, slot):
        if self.equipped_items[slot] == {}:
            return True
        else:
            return False

    def update_stats(self):
        for item in self.equipped_items:
            # print(
            #     f'{__class__} - {self.name} - {item} slot empty? - {self.is_slot_empty(item)}')
            if not self.is_slot_empty(item):
                if item == 'armor':
                    if 'no_agi' in self.equipped_items[item]['abilities']:
                        self.armor_class = self.equipped_items[item]['armor_class']
                    else:
                        self.armor_class = self.equipped_items[item]['armor_class'] + \
                            self.attributes['agility']['modifier']
                if item == 'shield':
                    self.armor_class += self.equipped_items[item]['armor_class']
                if item == 'weapon':
                    self.weapon_max_damage_die = self.equipped_items[item]['max_damage_die']
                    self.weapon_num_dice = self.equipped_items[item]['num_dice']


class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.race = construct_class(kwargs['race'].title())
        self.job = construct_class(kwargs['job'].title())
        self.equipped_items['armor'] = self.job.starting_armor
        self.equipped_items['weapon'] = self.job.starting_weapon
        self.exp = 0
        self.add_race_attributes()
        self.add_job_attributes()
        self.update_ability_scores()
        self.assign_starting_hp()
        self.update_stats()
        

    def update_ability_scores(self):
        for stat in self.attributes:
            self.attributes[stat]['racial_modifier'] = self.race.attributes[stat]
            self.attributes[stat]['job_modifier'] = self.job.attributes[stat]
            self.attributes[stat]['score'] = self.attributes[stat]['base'] + \
                self.race.attributes[stat] + self.job.attributes[stat]
            self.attributes[stat]['modifier'] = (
                self.attributes[stat]['score'] - 10) // 2

    def print_stats(self):
        print(f"""Name - {self.name}  |  Race - {self.race.name.title()}  |  Job -  {self.job.name.title()}
            \rStrength - {self.attributes['strength']['score']} - {self.attributes['strength']['modifier']} -
            \rAgility - {self.attributes['agility']['score']} - {self.attributes['agility']['modifier']}
            \rIntellect - {self.attributes['intellect']['score']} - {self.attributes['intellect']['modifier']}
            """)

    def add_race_attributes(self):
        for stat in self.attributes:
            self.attributes[stat]['racial_modifier'] = self.race.attributes[stat]

    def add_job_attributes(self):
        for stat in self.attributes:
            self.attributes[stat]['job_modifier'] = self.job.attributes[stat]

    def assign_starting_hp(self):
        self.max_hp = (
            self.job.hp_dice_max + self.attributes['strength']['modifier'])
        self.current_hp = self.max_hp

    def take_damage(self, damage, source):
        self.current_hp -= damage
        print(f"{self.name} took {damage} damage from {source.name}.")
        if self.is_alive():
            print(f"{self.name} has {self.current_hp} reamining.")
        else:
            print(f"{self.name} has been slain!\n")

    def is_alive(self):
        if self.current_hp > 0:
            return True
    
    def assign_exp(self, enemy_pool, character_pool) -> None:  #TODO should be in the battle/game class
        xp_pool = 0
        for enemy in enemy_pool:
            xp_pool += enemy.exp_value
        
        xp_per_character = xp_pool // len(character_pool)
        for character in character_pool:
            character.exp += xp_per_character
            if character.gained_enough_exp_to_level(xp_per_character):
                character.level_up()

    def gained_enough_exp_to_level(self, gained_xp: float) -> bool:
        experience_level_requirements = {
            2: 300,
            3: 900,
            4: 2700,
            5: 6500,
            6: 14000,
            7: 23000,
            8: 34000,
            9: 48000,
            10: 64000,
            11: 85000,
            12: 100000,
            13: 120000,
            14: 140000,
            15: 165000,
            16: 195000,
            17: 225000,
            18: 265000,
            19: 305000,
            20: 35500,
        }
        exp_to_level = experience_level_requirements[self.job.level+1]
        current_exp = self.exp
        print(f'{self.name} has gained {gained_xp} experience.')
        if current_exp > exp_to_level:
            print("Congratulations! You have leveled up!")
            return True
        else:
            print("You have not leveled up.")
            return False

    def level_up(self):
        self.job.level += 1
        self.job.set_attribute_bonuses()
        self.update_ability_scores()



def initiative_order(combatent_list):
    order = []
    for entity in combatent_list:
        entity_initiative = randint(
            1, 20) + entity.attributes['agility']['modifier']
        order.append({'entity': entity, 'initiative': entity_initiative})
    order = sorted(order, key=lambda x: x['initiative'], reverse=True)
    return order


if __name__ == "__main__":
    pass
    # jonah = Player(name='Jonah', race="human", job="fighter", strength=18,
    #                agility=15, intellect=10, luck=16)

    # new_mon = monsters.Goblinoid(
    #     name='Goblin Boss', strength=14, agility=12, intellect=8, luck=0, hp=21, cr=2)

    # new_mon3 = monsters.Goblinoid(
    #     name='Goblin Spearman', strength=12, agility=14, intellect=8, luck=0, hp=8, cr=.25)
