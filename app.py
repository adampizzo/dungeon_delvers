
from string import punctuation
from random import randint
from dungeon_delvers.utilities import print_sep, clr, get_selection
import pickle
from dungeon_delvers.base import Player


def construct_class(klass, **kwargs):
    constructor = globals()[klass]
    return constructor(**kwargs)


class Game():
    def __init__(self):
        self.party_size = 0
        self.welcome_menu()
        self.party = self.party_generation()

    def welcome_menu(self):
        clr()
        print(f"""{print_sep('-', 100)}
            \rWelcome Brave Adventurer,
            \r
            \rYou have been tasked with leading a party into the many dungeons that surround Shore Noren.
            \r
            \rIn those dungeons you will find creatures of all shapes and sizes ready to gut you.
            \r
            \rDefeat them in combat and keep the city safe.
            \r{print_sep('-', 100)}
            """)
        input("Press Enter To Play...")

    def party_generation(self):
        clr()
        ready = False
        party_num_fmt = ''
        valid_options = ['1', '2']
        party = []
        while True:
            try:
                print(f'''Do you want to load an entire saved party?
                    \r1.) - Yes
                    \r2.) - No''')
                load_party_choice = input('Selection: ')
                if not load_party_choice in valid_options:
                    raise TypeError(
                        "That is not a valid choice, please try again. 1 for yes or 2 for no.")
            except TypeError as e:
                print(e)
            else:
                if load_party_choice == '1':
                    while True:
                        try:
                            clr()
                            party_name = input('Enter the party\'s name: ')
                            party = self.load_party(party_name)
                            input('Press Enter To Continue...')
                            return party
                        except FileNotFoundError:
                            print(
                                f'\nNo Party Found With Name: {party_name}. Please Try Again.')
                            input('Press Enter To Continue...')
                else:
                    while len(party) < 4 and not ready:
                        while True:
                            try:
                                clr()
                                print(
                                    '\nIt is the time to either load previously saved Hero, or to create a new Hero to join your party.')
                                print('''Please make your selection:
                                    \r1.) - Load
                                    \r2.) - Create a New Character''')
                                load = input('Selection: ')
                                if not load in valid_options:
                                    raise TypeError(
                                        '\nNot a valid option. Please choose 1 for Load or 2 to Create a New Character.')
                            except TypeError as e:
                                print(e)
                                input('Press Enter To Continue...')
                            else:
                                if load == '1':
                                    while True:
                                        try:
                                            clr()
                                            character_name = input(
                                                'Enter the character\'s name: ')
                                            character = self.load_character(
                                                character_name)
                                            input('Press Enter To Continue...')
                                            break
                                        except FileNotFoundError:
                                            print(
                                                f'No Character Found With Name: {character_name}. Please Try Again.')
                                            input('Press Enter To Continue...')
                                else:
                                    clr()
                                    character = self.generate_character()
                                    self.save_character(
                                        character, character.name)
                                    
                                party.append(character)
                                if len(party) == 1:
                                    party_num_fmt = 'first'
                                if len(party) == 2:
                                    party_num_fmt = 'second'
                                if len(party) == 3:
                                    party_num_fmt = 'third'
                                if len(party) == 4:
                                    party_num_fmt = 'final'

                                print(
                                    f'\nYou have choosen {character.name.title()}, {character.race.display_name.title()} {character.job.name.title()} as your {party_num_fmt} character!')
                                if len(party) == 1:
                                    print(
                                        f'You now have {len(party)} member in your party:')
                                else:
                                    print(
                                        f'You now have {len(party)} members in your party:')
                                for i, member in enumerate(party, 1):
                                    print(
                                        f'{i}.) - {member.name.title()} - Level {member.job.level} {member.race.display_name.title()} {member.job.name.title()}')

                                if len(party) < 4:
                                    while True:
                                        try:
                                            print(f'''\nWould you like to load/generate another character or are you finished with your party?
                                                \r1.) - Load/Create a New Character
                                                \r2.) - Finished Generating Party''')
                                            new_char_choice = input('Selection: ')
                                            if not new_char_choice in valid_options:
                                                raise TypeError(
                                                    '\nNot a valid option. Please choose 1 to Load or to Create a New Character, or 2 to finish with generating your party.')
                                        except TypeError as e:
                                            print(e)
                                        else:
                                            if new_char_choice == '2':
                                                ready = True
                                                break
                                            else:
                                                break
                                if ready:
                                    break
                    print(f'Your party is now complete.')
                    party_name = self.get_name('party')
                    new_party = Party(party, party_name)
                    self.save_party(new_party, new_party.name)
                    return new_party

    def generate_character(self):
        """
            generate_character:
            Gets the following information and returns it to a constructor:

                name,
                race, (Human, Dwarf, Elf, Gnome, Halfling, Half-Elf, Half-Orc)
                job, (Fighter, Paladin, Wizard, Monk, Rogue, Barbarian)
                TODO gender, (Male, Female, Non-Binary)
                TODO age,
                TODO height,
                TODO weight,
                strength,
                agility,
                intellect,
                luck

        """
        print(f"""
            \rWelcome to the character generator.
            \n\nIn this part, you will generate your character from scratch by answering the following prompts.
            \rThis includes, naming the character, selecting their race, selecting their job, as well as generating
            \ryour characters attributes.
            """)
        name = self.get_name('character').title()
        race = self.get_race().title()
        job = self.get_job().title()
        attributes = self.assign_stat_pool(self.build_stat_pool())
        return construct_class('Player', name=name,
                               race=race, job=job, strength=attributes['strength'],
                               agility=attributes['agility'], intellect=attributes['intellect'],
                               luck=attributes['luck'])

    def get_name(self, type_of_get):
        while True:
            try:
                invalid_characters = set(punctuation)
                invalid_characters.remove('-')
                name = input(f'What is the name of your {type_of_get}?\n')
                if len(name) == 0:
                    raise ValueError(
                        f'Your {type_of_get} name cannot be blank. Please try again.\n')
                for char in name:
                    if char.isdigit():
                        raise ValueError(
                            f'\nInvalid Character: Do not use any numbers in your {type_of_get} name. Valid characters are a-z, A-Z, spaces, and \'-\'.\n')
                    elif char in invalid_characters:
                        raise ValueError(
                            f'\nInvalid Character: Do not use any special characters in your {type_of_get} name. Valid characters are a-z, A-Z, spaces, and \'-\'.\n')
            except ValueError as e:
                print(e)
            else:
                return name

    def get_race(self):
        valid_options = ['1', '2', '3', '4', '5', '6', '7']
        while True:
            try:
                print(f"""\nWhat is your character's race?
                    \r1 - Human - +1 Str, +1 Agi, +1 Int, +1 Luck
                    \r2 - Dwarf - +2 Str, +1 Luck
                    \r3 - Elf - +2 Agi, +1 Int
                    \r4 - Gnome - +2 Int, +1 Luck
                    \r5 - Halfling - +2 Luck, +1 Agi, +1 Int
                    \r6 - Half-Orc - +2 Str, +1 Agi
                    \r7 - Half-Elf - +2 Luck, +1 Agi, +1 Str
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
        valid_options = ['1', '2', '4', '5']
        while True:
            try:
                print(f"""\nWhat is your character's job?
                    \r1 - Fighter - Melee, Heavy Armorored
                    \r2 - Paladin - Divine, Faith and Heavy Armor - Not Implemented
                    \r3 - Wizard - Magic, Shield and Pew Pew - Not Implemented
                    \r4 - Monk - Melee and Discipline - Not Implemented
                    \r5 - Rogue - Sneak Attacks, Evasion - Not Implemented
                    \r6 - Barbarian - Rage and Smash - Not Implemented
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
                    return 'paladin'
                elif race == '3':
                    return 'wizard'
                elif race == '4':
                    return 'monk'
                elif race == '5':
                    return 'rogue'
                elif race == '6':
                    return 'barbarian'

    def assign_stat_pool(self, stat_pool):
        attributes = {}
        stats = ['strength', 'agility', 'intellect', 'luck']
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
            \rStrength - {attributes['strength']}
            \rAgility - {attributes['agility']}
            \rIntellect - {attributes['intellect']}
            \rLuck - {attributes['luck']}
            """)
        return attributes

    def build_stat_pool(self):
        stat_pool = []
        clr()
        print(
            "Let's create your stat pool. You'll have two options per roll to choose from.")
        for i in range(4):
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

    def save_character(self, character, character_name):
        character_name = self.fmt_save_load(character_name)
        with open(f"dungeon_delvers/saves/hero/{character_name}_save.pkl", 'wb') as f:
            pickle.dump(character, f, -1)

    def load_character(self, character_name):
        character_name = self.fmt_save_load(character_name)
        for atr in self.pkl_loader(f'dungeon_delvers/saves/hero/{character_name}_save.pkl'):
            print(f'Object = {atr}')
            print(f'Vars = {vars(atr)}')
            print(f'Name: {atr.name}')
            return atr

    def load_party(self, party_name):
        party_name = self.fmt_save_load(party_name)
        for atr in self.pkl_loader(f'dungeon_delvers/saves/party/{party_name}_save.pkl'):
            print(f'Object = {atr}')
            print(f'Vars = {vars(atr)}')
            print(f'Name: {atr.name}')
            return atr

    def save_party(self, party, party_name):
        party_name = self.fmt_save_load(party_name)
        with open(f"dungeon_delvers/saves/party/{party_name}_save.pkl", 'wb') as f:
            pickle.dump(party, f, -1)
    
    def pkl_loader(self, file):
        with open(file, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    def fmt_save_load(self, name):
        if ' ' in name:
            name = name.lower().split(' ')
            name = '_'.join(name)
        if '-' in name:
            name = name.lower().replace('-', '_')
        else:
            name = name.lower()
        return name


class Battle():
    def __init__(self, enemy_pool, party_pool):
        self.enemy_pool = enemy_pool
        self.character_pool = party_pool

    """
    player_characters = [jonah]
    enemies_in_combat = [new_mon, new_mon3]
    enemies_dead = []
    player_in_combat = [jonah]
    all_combatents = player_in_combat + enemies_in_combat
    init_order = initiative_order(all_combatents)
    while len(enemies_in_combat) > 0 and jonah.is_alive():
        for entity in init_order:
            if entity['entity'] in player_characters:
                print("\nChoose an enemy to attack:")
                for i, enemy in enumerate(enemies_in_combat, 1):
                    print(
                        f'{i} - {enemy.name} - {enemy.current_hp} hp out of {enemy.max_hp}')
                p_choice = input('Selection: ')
                p_choice = int(p_choice) - 1
                entity['entity'].job.basic_attack(
                    entity['entity'].weapon_num_dice, entity['entity'].weapon_max_damage_die, entity['entity'].attributes['strength']['modifier'], enemies_in_combat[p_choice], entity['entity'])
                if not enemies_in_combat[p_choice].is_alive():
                    enemies_dead.append(enemies_in_combat[p_choice])
                    del enemies_in_combat[p_choice]
                sleep(1)

            else:
                if entity['entity'].is_alive():
                    entity['entity'].basic_attack(choice(player_in_combat))
                    sleep(1)
        
    jonah.assign_exp(enemies_dead, player_characters)
    
    print('Jonah\'s Experience Total:')
    print(jonah.exp)
    print(jonah.job.level)
    """


class Party():
    def __init__(self, party, name) -> None:
        self.party_members = party
        self.name = name

    def __repr__(self) -> str:
        return (f'''
                {self.name.title()}
                {*self.party_members,}
                ''')


if __name__ == "__main__":
    game = Game()
