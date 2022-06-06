import json
from string import punctuation
from random import randint
from dungeon_delvers.utilities import print_sep, clr, get_selection
from dungeon_delvers.base import Player


def construct_class(klass, **kwargs):
    constructor = globals()[klass]
    return constructor(**kwargs)


class Game():
    def __init__(self):
        
        self.player = self.generate_character()
        self.save_character(self.player)

    def generate_character(self):
        """
            generate_character:
            Gets the following information and returns it to a constructor:

                name,
                race, (Human, Dwarf, Elf, Gnome, Halfling)
                job, (Fighter, Cleric, Sorcerer, Rogue, Barbarian)
                TODO gender, (Male, Female, Non-Binary)
                TODO age,
                TODO height,
                TODO weight,
                power,
                agility,
                toughness,
                guile,
                luck

        """
        print(f"""
            \rWelcome to the character generator.
            \n\nIn this part, you will generate your character from scratch by answering the following prompts.
            \rThis includes, naming the character, selecting their race, selecting their job, as well as generating
            \ryour characters attributes.
            """)
        self.name = self.get_name().title()
        self.race = self.get_race().title()
        self.job = self.get_job().title()
        attributes = self.assign_stat_pool(self.build_stat_pool())
        return construct_class('Player', name=self.name, race=self.race, job=self.job, power=attributes['power'], agility=attributes['agility'], toughness=attributes['toughness'], guile=attributes['guile'], luck=attributes['luck'])

    def get_name(self):
        while True:
            try:
                invalid_characters = set(punctuation)
                invalid_characters.remove('-')
                name = input("What is the name of your character?\n")
                if len(name) == 0:
                    raise ValueError("Your character name cannot be blank. Please try again.\n")
                for char in name:
                    if char.isdigit():
                        raise ValueError("\nInvalid Character: Do not use any numbers in your name. Valid characters are a-z, A-Z, spaces, and '-'.\n")
                    elif char in invalid_characters:
                        raise ValueError("\nInvalid Character: Do not use any special characters. Valid characters are a-z, A-Z, spaces, and '-'.\n")
                    
            except ValueError as e:
                print(e)
            else:
                return name
    
    
    def get_race(self):
        valid_options = ['1', '2', '3', '4', '5', '6', '7']
        while True:
            try:
                print(f"""\nWhat is your character's race?
                    \r1 - Human
                    \r2 - Dwarf
                    \r3 - Elf
                    \r4 - Gnome
                    \r5 - Halfling
                    \r6 - Half-Orc
                    \r7 - Half-Elf
                    """)
                race = input("Selection: ")
                if race not in valid_options:
                    raise ValueError(
                        "That is not a correct option, please try again.")
            except ValueError as e:
                print(e)
            else:
                if race == '1':
                    return 'human'
                elif race == '2':
                    return 'dwarf'
                elif race == '3':
                    return 'elf'
                elif race == '4':
                    return 'gnome'
                elif race == '5':
                    return 'halfling'
                elif race == '6':
                    return 'halforc'
                elif race == '7':
                    return 'halfelf'

    def get_job(self):
        valid_options = ['1', '2', '3', '4', '5']
        while True:
            try:
                print(f"""\nWhat is your character's job?
                    \r1 - Fighter
                    \r2 - Cleric
                    \r3 - Sorcerer
                    \r4 - Rogue
                    \r5 - Barbarian
                    """)
                race = input('Selection: ')
                if race not in valid_options:
                    raise ValueError(
                        'That is not a correct option, please try again.')
            except ValueError as e:
                print(e)
            else:
                if race == '1':
                    return 'fighter'
                elif race == '2':
                    return 'cleric'
                elif race == '3':
                    return 'sorcerer'
                elif race == '4':
                    return 'rogue'
                elif race == '5':
                    return 'barbarian'

    def assign_stat_pool(self, stat_pool):
        attributes = {}
        stats = ['power', 'agility', 'toughness', 'guile', 'luck']
        for stat in stats:
            print(f'Assigning {stat.title()}:')
            for i, item in enumerate(stat_pool, 1):
                print(f'{i} - {item}')
            print(f'Which option do you want to assign to {stat.title()}: ')
            choice = get_selection(
                stat_pool, "That is not a valid option. Please try again.")
            attributes[stat] = choice
            print(
                f'{stat.title()} now has the value {attributes[stat]}')
            stat_pool.remove(choice)
        print(f"""
            \rFinal Stat Distribution:
            \rPower - {attributes['power']}
            \rAgility - {attributes['agility']}
            \rToughness - {attributes['toughness']}
            \rGuile - {attributes['guile']}
            \rLuck - {attributes['luck']}
            """)
        return attributes

    def build_stat_pool(self):
        stat_pool = []
        clr()
        print(
            "Let's create your stat pool. You'll have two options per roll to choose from.")
        for i in range(5):
            print(f'Your stat pool is currently: {*stat_pool,}\n')
            roll = self.build_stat_roll()
            stat_pool.append(roll)
        clr()
        print(f'Your stat pool is: {*stat_pool,}')
        return stat_pool

    def build_stat_roll(self):
        valid_options = ['1', '2']
        roll_one = self.roll_4_drop_lowest(6)
        roll_two = self.roll_4_drop_lowest(6)
        while True:
            try:
                print("For this roll your options are:")
                print(f'1 - {roll_one}')
                print(f'2 - {roll_two}')
                choice = input("Selection: ")
                if choice not in valid_options:
                    raise ValueError(
                        "\nThat is not a valid choice. Please choose 1 or 2.\n")
            except ValueError as e:
                print(e)
            else:
                if choice == '1':
                    return roll_one
                elif choice == '2':
                    return roll_two

    def roll_4_drop_lowest(self, max_side):
        stat_pool = []
        for i in range(4):
            stat_pool.append(randint(1, max_side))
        minimum = min(stat_pool)
        stat_pool.remove(minimum)
        return sum(stat_pool)

    def save_character(self, player):
        if ' ' in player.stats['name']:
            player_name = player.stats['name'].lower().split(' ')
            print(player_name)
            player_name = '_'.join(player_name)
        if '-' in player.stats['name']:
            player_name = player.stats['name'].lower.replace('-', '_')
            print(player_name)
            
        else:
            player_name = player.stats['name'].lower()
        with open(f"dungeon_delvers/saves/{player_name}_save.json", 'w') as f:
            json_object = json.dumps(player.stats, indent = 4)
            f.write(json_object)


if __name__ == "__main__":
    player = Game()
    
