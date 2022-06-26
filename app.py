from copy import copy, deepcopy
import inspect
from math import ceil
import os
from string import punctuation
from random import randint, choice
from time import sleep
from dungeon_delvers.utilities import print_sep, clr, get_selection
import pickle
from dungeon_delvers.base import Player
from dungeon_delvers.monsters import Goblinoid, Dragon, Orc
from colorama import Back, Fore, Style


def construct_class(klass, **kwargs):
    constructor = globals()[klass]
    return constructor(**kwargs)


class Game:
    def __init__(self):
        gob1 = Goblinoid(
            name="Goblin Elite",
            strength=10,
            agility=14,
            intellect=8,
            luck=8,
            hit_dice_type=6,
            hit_dice_num_base=2,
            cr=0.25,
            classification="elite",
        )
        gob2 = Goblinoid(
            name="Goblin Minion",
            strength=10,
            agility=14,
            intellect=8,
            luck=8,
            hit_dice_type=6,
            hit_dice_num_base=2,
            cr=0.25,
            classification="minion",
        )
        gob3 = Goblinoid(
            name="Goblin",
            strength=10,
            agility=14,
            intellect=8,
            luck=8,
            hit_dice_type=6,
            hit_dice_num_base=2,
            cr=0.25,
            classification="standard",
        )
        gob4 = Goblinoid(
            name="Goblin Minion",
            strength=10,
            agility=14,
            intellect=8,
            luck=8,
            hit_dice_type=6,
            hit_dice_num_base=2,
            cr=0.25,
            classification="minion",
        )
        gob5 = Goblinoid(
            name="Goblin Minion",
            strength=10,
            agility=14,
            intellect=8,
            luck=8,
            hit_dice_type=6,
            hit_dice_num_base=2,
            cr=0.25,
            classification="minion",
        )

        # orc1 = Orc(
        #     name="Orc",
        #     strength=16,
        #     agility=12,
        #     intellect=7,
        #     luck=10,
        #     hit_dice_type=8,
        #     hit_dice_num_base=2,
        #     cr=0.5,
        #     classification="champion",
        # )

        # orc2 = Orc(
        #     name="Orc",
        #     strength=16,
        #     agility=12,
        #     intellect=7,
        #     luck=10,
        #     hit_dice_type=8,
        #     hit_dice_num_base=2,
        #     cr=0.5,
        #     classification="boss",
        # )

        valid_selection = ["1", "2", "3", "4", "5"]
        self.playing = True
        self.party = Party([], "None")

        while self.playing:
            if self.party.size == 0:
                has_party = False
            else:
                has_party = True
            self.main_menu()
            selection = get_selection(
                valid_selection, "That is an invalid selection. Please Try Again..."
            )
            if selection == "1":
                self.party = self.party_generation()
            if not selection == "1" and not has_party:
                print("Error: You need to have a party before doing that.")
                sleep(2)
            if selection == "2" and has_party:
                print("Welcome to the battle simulator!")
                self.enemy_list = [gob1, gob2, gob3, gob4, gob5]
                new_battle = Battle(self.enemy_list, self.party.members)

            if selection == "3" and has_party:
                print("This feature has not been implemented yet.")
                sleep(1)
            if selection == "4" and has_party:
                self.campaign_menu()
                print("\nThis feature has not been implemented yet.")
                sleep(1)
            if selection == "5" and has_party:
                print("Saving Party....")
                self.save_all()
                self.playing = False
                break

    def campaign_menu(self):
        clr()
        print(
            f"""{print_sep('-', 100)}
            \rWelcome Brave Adventurer,
            \r
            \rYou have been tasked with leading a party into the many dungeons and crypts that surround the city.
            \r
            \rIn those dungeons you will find creatures of all shapes and sizes ready to cut, burn, or
            \reven eat you.
            \r
            \rDefeat them in combat and keep the city safe.
            \r{print_sep('-', 100)}
            """
        )
        input("Press Enter To Play...")

    def main_menu(self):
        clr()
        plural = ""
        if not self.party.size == 1:
            plural = "s"
        print(
            f"""{print_sep('-', 45)}Main Menu{print_sep('-', 46)}
            \r1.) Generate or Load your party.
            \r2.) Battle Simulator (Not Fully Implemented)
            \r3.) Dungeon Delving (Not Implemented)
            \r4.) Campaign (Not Implemented)
            \r5.) Save Party and Exit.
            \r{print_sep('-', 100)}
            \rCurrent Party: {self.party.display_party()}
            \rParty Size: {self.party.size} Member{plural}"""
        )

    def party_generation(self):
        clr()
        ready = False
        party_num_fmt = ""
        valid_options = ["1", "2"]
        party = []
        while True:
            try:
                print(
                    f"""Do you want to load an entire saved party?
                    \r1.) - Yes
                    \r2.) - No"""
                )
                load_party_choice = input("Selection: ")
                if not load_party_choice in valid_options:
                    raise TypeError(
                        "That is not a valid choice, please try again. 1 for yes or 2 for no."
                    )
            except TypeError as e:
                print(e)
            else:
                if load_party_choice == "1":
                    while True:
                        try:
                            clr()
                            party_name = input("Enter the party's name: ")
                            party = self.load_party(party_name)
                            input("Press Enter To Continue...")
                            return party
                        except FileNotFoundError:
                            print(
                                f"\nNo Party Found With Name: {party_name}. Please Try Again."
                            )
                            input("Press Enter To Continue...")
                else:
                    while len(party) < 4 and not ready:
                        while True:
                            try:
                                clr()
                                print(
                                    "\nIt is the time to either load a previously saved Hero, or to create a new Hero to join your party."
                                )
                                print(
                                    """Please make your selection:
                                    \r1.) - Load
                                    \r2.) - Create a New Character"""
                                )
                                load = input("Selection: ")
                                if not load in valid_options:
                                    raise TypeError(
                                        "\nNot a valid option. Please choose 1 for Load or 2 to Create a New Character."
                                    )
                            except TypeError as e:
                                print(e)
                                input("Press Enter To Continue...")
                            else:
                                if load == "1":
                                    while True:
                                        try:
                                            clr()
                                            character_name = input(
                                                "Enter the character's name: "
                                            )
                                            character = self.load_character(
                                                character_name
                                            )
                                            input("Press Enter To Continue...")
                                            break
                                        except FileNotFoundError:
                                            print(
                                                f"No Character Found With Name: {character_name}. Please Try Again."
                                            )
                                            input("Press Enter To Continue...")
                                else:
                                    clr()
                                    character = self.generate_character()
                                    self.save_character(character, character.name)

                                party.append(character)
                                if len(party) == 1:
                                    party_num_fmt = "first"
                                if len(party) == 2:
                                    party_num_fmt = "second"
                                if len(party) == 3:
                                    party_num_fmt = "third"
                                if len(party) == 4:
                                    party_num_fmt = "final"

                                print(
                                    f"\nYou have choosen {character.name.title()}, {character.race.display_name.title()} {character.job.name.title()} as your {party_num_fmt} character!"
                                )
                                if len(party) == 1:
                                    print(
                                        f"You now have {len(party)} member in your party:"
                                    )
                                else:
                                    print(
                                        f"You now have {len(party)} members in your party:"
                                    )
                                for i, member in enumerate(party, 1):
                                    print(
                                        f"{i}.) - {member.name} - Level {member.job.level} {member.race.display_name.title()} {member.job.name.title()}"
                                    )

                                if len(party) < 4:
                                    while True:
                                        try:
                                            print(
                                                f"""\nWould you like to load/generate another character or are you finished with your party?
                                                \r1.) - Load/Create a New Character
                                                \r2.) - Finished Generating Party"""
                                            )
                                            new_char_choice = input("Selection: ")
                                            if not new_char_choice in valid_options:
                                                raise TypeError(
                                                    "\nNot a valid option. Please choose 1 to Load or to Create a New Character, or 2 to finish with generating your party."
                                                )
                                        except TypeError as e:
                                            print(e)
                                        else:
                                            if new_char_choice == "2":
                                                ready = True
                                                break
                                            else:
                                                break
                                elif len(party) == 4:
                                    ready = True
                                if ready:
                                    break
                    print(f"Your party is now complete.")
                    party_name = self.get_name("party")
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
        print(
            f"""
            \rWelcome to the character generator.
            \nIn this part, you will generate your character from scratch by answering the following prompts.
            \rThis includes, naming the character, selecting their race, selecting their job, as well as generating
            \ryour characters attributes.
            """
        )
        name = self.get_name("character").title()
        race = self.get_race().title()
        job = self.get_job().title()
        attributes = self.assign_stat_pool(self.build_stat_pool())
        return construct_class(
            "Player",
            name=name,
            race=race,
            job=job,
            strength=attributes["strength"],
            agility=attributes["agility"],
            intellect=attributes["intellect"],
            luck=attributes["luck"],
        )

    def get_name(self, type_of_get):
        while True:
            try:
                invalid_characters = set(punctuation)
                invalid_characters.remove("-")
                name = input(f"What is the name of your {type_of_get}?\n")
                if len(name) == 0:
                    raise ValueError(
                        f"Your {type_of_get} name cannot be blank. Please try again.\n"
                    )
                for char in name:
                    if char.isdigit():
                        raise ValueError(
                            f"\nInvalid Character: Do not use any numbers in your {type_of_get} name. Valid characters are a-z, A-Z, spaces, and '-'.\n"
                        )
                    elif char in invalid_characters:
                        raise ValueError(
                            f"\nInvalid Character: Do not use any special characters in your {type_of_get} name. Valid characters are a-z, A-Z, spaces, and '-'.\n"
                        )
            except ValueError as e:
                print(e)
            else:
                return name

    def get_race(self):
        valid_options = ["1", "2", "3", "4", "5", "6", "7"]
        while True:
            try:
                print(
                    f"""\nWhat is your character's race?
                    \r1 - Human - +1 Str, +1 Agi, +1 Int, +1 Luck
                    \r2 - Dwarf - +2 Str, +1 Luck
                    \r3 - Elf - +2 Agi, +1 Int
                    \r4 - Gnome - +2 Int, +1 Luck
                    \r5 - Halfling - +2 Luck, +1 Agi, +1 Int
                    \r6 - Half-Orc - +2 Str, +1 Agi
                    \r7 - Half-Elf - +2 Luck, +1 Agi, +1 Str
                    """
                )
                race = input("Selection: ")
                if race not in valid_options:
                    raise ValueError("That is not a correct option, please try again.")
            except ValueError as e:
                print(e)
            else:
                if race == "1":
                    return "human"
                elif race == "2":
                    return "dwarf"
                elif race == "3":
                    return "elf"
                elif race == "4":
                    return "gnome"
                elif race == "5":
                    return "halfling"
                elif race == "6":
                    return "halforc"
                elif race == "7":
                    return "halfelf"

    def get_job(self):
        valid_options = ["1", "2", "4", "5"]
        while True:
            try:
                print(
                    f"""\nWhat is your character's job?
                    \r1 - Fighter - Melee, Heavy Armorored
                    \r2 - Paladin - Divine, Faith and Heavy Armor - Not Implemented
                    \r3 - Wizard - Magic, Shield and Pew Pew - Not Implemented
                    \r4 - Monk - Melee and Discipline - Not Implemented
                    \r5 - Rogue - Sneak Attacks, Evasion - Not Implemented
                    \r6 - Barbarian - Rage and Smash - Not Implemented
                    """
                )
                race = input("Selection: ")
                if race not in valid_options:
                    raise ValueError("That is not a correct option, please try again.")
            except ValueError as e:
                print(e)
            else:
                if race == "1":
                    return "fighter"
                elif race == "2":
                    return "paladin"
                elif race == "3":
                    return "wizard"
                elif race == "4":
                    return "monk"
                elif race == "5":
                    return "rogue"
                elif race == "6":
                    return "barbarian"

    def assign_stat_pool(self, stat_pool):
        attributes = {}
        stats = ["strength", "agility", "intellect", "luck"]
        for stat in stats:
            print(f"Assigning {stat.title()}:")
            for i, item in enumerate(stat_pool, 1):
                print(f"{i} - {item}")
            print(f"Which option do you want to assign to {stat.title()}: ")
            choice = get_selection(
                stat_pool, "That is not a valid option. Please try again."
            )
            attributes[stat] = choice
            print(f"{stat.title()} now has the value {attributes[stat]}")
            stat_pool.remove(choice)
        print(
            f"""
            \rFinal Stat Distribution:
            \rStrength - {attributes['strength']}
            \rAgility - {attributes['agility']}
            \rIntellect - {attributes['intellect']}
            \rLuck - {attributes['luck']}
            """
        )
        return attributes

    def build_stat_pool(self):
        stat_pool = []
        clr()
        print(
            "Let's create your stat pool. You'll have two options per roll to choose from."
        )
        for i in range(4):
            print(f"Your stat pool is currently: {*stat_pool,}\n")
            roll = self.build_stat_roll()
            stat_pool.append(roll)
        clr()
        print(f"Your stat pool is: {*stat_pool,}")
        return stat_pool

    def build_stat_roll(self):
        valid_options = ["1", "2"]
        roll_one = self.roll_4_drop_lowest(6)
        roll_two = self.roll_4_drop_lowest(6)
        while True:
            try:
                print("For this roll your options are:")
                print(f"1 - {roll_one}")
                print(f"2 - {roll_two}")
                choice = input("Selection: ")
                if choice not in valid_options:
                    raise ValueError(
                        "\nThat is not a valid choice. Please choose 1 or 2.\n"
                    )
            except ValueError as e:
                print(e)
            else:
                if choice == "1":
                    return roll_one
                elif choice == "2":
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
        with open(f"dungeon_delvers/saves/hero/{character_name}_save.pkl", "wb") as f:
            pickle.dump(character, f, -1)

    def load_character(self, character_name):
        character_name = self.fmt_save_load(character_name)
        for atr in self.pkl_loader(
            f"dungeon_delvers/saves/hero/{character_name}_save.pkl"
        ):
            return atr

    def load_party(self, party_name):
        party_name = self.fmt_save_load(party_name)
        for atr in self.pkl_loader(
            f"dungeon_delvers/saves/party/{party_name}_save.pkl"
        ):
            # print(f"Object = {atr}")
            print(f"Party Name: {atr.name}")
            print("Members:")
            for member in atr.members:
                print(f"  {member}")
            atr.size = len(atr.members)
            return atr

    def save_party(self, party, party_name):
        party_name = self.fmt_save_load(party_name)
        with open(f"dungeon_delvers/saves/party/{party_name}_save.pkl", "wb") as f:
            pickle.dump(party, f, -1)

    def pkl_loader(self, file):
        with open(file, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    def fmt_save_load(self, name):
        if " " in name:
            name = name.lower().split(" ")
            name = "_".join(name)
        if "-" in name:
            name = name.lower().replace("-", "_")
        else:
            name = name.lower()
        return name

    def save_all(self):
        party_name = self.fmt_save_load(self.party.name)
        for member in self.party.members:
            self.save_character(member, member.name)
            print(f"Saved {member.name} successfully!")
            sleep(0.5)
        self.save_party(self.party, party_name)
        print(f"Saved {self.party.name} successfully!")
        sleep(0.5)
        input("Thank you for playing!")


class Battle:
    def __init__(self, enemy_pool, party_pool):
        self.enemy_pool = enemy_pool
        self.character_pool = party_pool
        self.enemy_dead_pool = []
        self.character_dead_pool = []
        self.order = []
        self.round = 1
        self.initiative_order()

        while not self.enemies_lost() and not self.characters_lost():
            self.battle_turn()
            self.round += 1
            if self.enemies_lost():
                print("Congratulations! All of the enemies have been defeated!")
                sleep(1)
                self.assign_exp(self.enemy_dead_pool, self.character_pool)
                # self.tally_monster_type_killed(self.character_pool) TODO
            if self.characters_lost():
                print("Your party has been wiped out! Game Over.")
                sleep(1)

    def initiative_order(self):
        for entity in self.character_pool:
            entity_initiative = (
                randint(1, 20) + entity.attributes["agility"]["modifier"]
            )
            self.order.append(
                {
                    "entity": entity,
                    "initiative": entity_initiative,
                    "has_gone": False,
                    "is_active": False,
                    "multi_attack_hide": False,
                    "is_character": True,
                }
            )
        for entity in self.enemy_pool:
            entity_initiative = (
                randint(1, 20) + entity.attributes["agility"]["modifier"]
            )
            self.order.append(
                {
                    "entity": entity,
                    "initiative": entity_initiative,
                    "has_gone": False,
                    "is_active": False,
                    "multi_attack_hide": False,
                    "is_character": False,
                }
            )
        self.order = sorted(self.order, key=lambda x: x["initiative"], reverse=True)

    def enemies_lost(self):
        if len(self.enemy_pool) == len(self.enemy_dead_pool):
            return True
        else:
            return False

    def characters_lost(self):
        if len(self.character_pool) == len(self.character_dead_pool):
            return True
        else:
            return False

    def print_menu(self):
        print(
            f"""{print_sep('-')}
            \r|     1.Attack      |      3.Magic      |     5.Inspect     |      7.Flee      |
            \r{print_sep('-')}
            \r|    2.Abilities    |      4.Items      |      6.Pass       |                  |
            \r{print_sep('-')}"""
        )

    def print_player_turn(self, player: Player):
        print(f"\nActive Character: {player.display_name}")
        self.print_menu()

    def print_turn_order(self):
        longest_name = 0
        for combatent in self.order:
            if combatent["entity"].name_length > longest_name:
                longest_name = combatent["entity"].name_length
        print(f"Turn {self.round}")
        print("Turn Order:")
        for i, combatent in enumerate(self.order, 1):
            if not longest_name % 2 == 0:
                longest_name += 1
            padding = longest_name - combatent["entity"].name_length
            front_padding = padding // 2
            back_padding = ceil(padding / 2)
            if combatent["has_gone"] == True:
                status_indicator = "-"
            elif combatent["is_active"]:
                status_indicator = "*"
            else:
                status_indicator = " "
            if combatent["entity"] in self.character_pool:
                print(
                    f"{i}:({status_indicator}) Name: {' ' * front_padding}{combatent['entity'].display_name}{' ' * back_padding} - {combatent['entity'].current_hp} HP out of {combatent['entity'].max_hp} HP"
                )
            else:
                print(
                    f"{i}:({status_indicator}) Name: {' ' * front_padding}{combatent['entity'].name}{' ' * back_padding} - {combatent['entity'].current_hp} HP out of {combatent['entity'].max_hp} HP"
                )

    def display_attacks(self, combatent):
        valid_selection = []
        print(f"\n{combatent['entity'].name}'s Attacks:\n")
        for i, attack in enumerate(combatent["entity"].job.attacks, 1):
            print(f"{i}.) {attack['name']} - {attack['description']}")
            valid_selection.append(str(i))
        selection = int(
            get_selection(
                valid_selection,
                "That is not a valid attack selection. Please try again.",
            )
        )
        selected_attack: str = (
            combatent["entity"].job.attacks[selection - 1]["name"].lower()
        )
        if " " in selected_attack:
            selected_attack = selected_attack.replace(" ", "_")
        return selected_attack

    def get_active_abilities(self, combatent):
        active_abilities = []
        for ability in combatent["entity"].job.abilities:
            if ability["type"] == "active":
                active_abilities.append(ability)
        return active_abilities

    def display_abilities(self, combatent):
        valid_selection = []
        print(f"\n{combatent['entity'].display_name}'s Abilities:\n")
        for i, ability in enumerate(self.get_active_abilities(combatent), 1):
            print(f"{i}.) {ability['name']} - {ability['description']}")
            valid_selection.append(str(i))
        selection = int(
            get_selection(
                valid_selection,
                "That is not a valid abilities selection. Please try again.",
            )
        )
        selected_ability: str = (
            combatent["entity"].job.abilities[selection - 1]["name"].lower()
        )
        if " " in selected_ability:
            selected_ability = selected_ability.replace(" ", "_")
        return selected_ability

    def party_member_attacks(self, combatent):

        for attack in range(combatent["entity"].job.num_attacks):
            selected_attack = self.display_attacks(combatent)

            attack = getattr(combatent["entity"].job, selected_attack)
            target_selection = inspect.getcomments(attack)
            if "target" in target_selection:
                num_targets = target_selection[-2]
                if num_targets == "0":
                    target_list = []
                    for enemy in self.enemy_pool:
                        if enemy.is_alive():
                            target_list.append(enemy)
                    attack(combatent["entity"].equipped_items["weapon"], target_list)
                elif num_targets == "1":
                    num_targets = int(num_targets)
                    if (
                        len(self.enemy_pool) - len(self.enemy_dead_pool)
                    ) <= num_targets:
                        for enemy in self.enemy_pool:
                            if enemy.is_alive():
                                target = enemy
                    else:
                        valid_selection = []
                        for i, enemy in enumerate(self.enemy_pool, 1):
                            if enemy.is_alive():
                                print(
                                    f"{i}: {enemy.name} - Current HP: {enemy.current_hp} of {enemy.max_hp}"
                                )
                                valid_selection.append(str(i))
                        selection = int(
                            get_selection(
                                valid_selection,
                                "Error: Not a valid enemy selection. Please try again.",
                            )
                        )
                        target = self.enemy_pool[selection - 1]
                        print(target.name + " is being attacked.")
                    attack(combatent["entity"].equipped_items["weapon"], target)
                else:
                    num_targets = int(num_targets)
                    target_list = []
                    if (
                        len(self.enemy_pool) - len(self.enemy_dead_pool)
                    ) <= num_targets:
                        for enemy in self.enemy_pool:
                            if enemy.is_alive():
                                target_list.append(enemy)
                    else:
                        for target in range(num_targets):
                            for i, enemy in enumerate(self.enemy_pool, 1):
                                if enemy.is_alive():
                                    if not enemy in target_list:
                                        print(
                                            f"{i}: {enemy.name}  - Current HP: {enemy.current_hp} of {enemy.max_hp}"
                                        )
                            selection = int(input("Choose a target: "))
                            target = self.enemy_pool[selection - 1]
                            target_list.append(target)
                    attack(
                        combatent["entity"].equipped_items["weapon"],
                        target_list,
                    )

    def party_member_abilities(self, combatent):
        selected_abilities = self.display_abilities(combatent)
        ability = getattr(combatent["entity"].job, selected_abilities)
        target_selection = inspect.getcomments(ability)
        if "self" in target_selection:
            ability()
        elif "friendly" in target_selection:
            target_list = []
            num_targets = target_selection[-2]
            num_targets = int(num_targets)
            for target in range(num_targets):
                for i, character in enumerate(self.character_pool, 1):
                    print(
                        f"{i}: {character.display_name}  - Current HP: {character.current_hp} of {character.max_hp}"
                    )
                selection = int(input("Choose a target: "))
                if num_targets == 1:
                    target = self.character_pool[selection - 1]
                    ability(target)
                else:
                    target_list.append(self.character_pool[selection - 1])
            if num_targets != 1:
                ability(target_list)

    def clean_up_dead(self):
        for combatent in self.order:
            if not combatent["entity"].is_alive():
                if combatent["entity"] in self.character_pool:
                    self.character_dead_pool.append(combatent["entity"])
                    self.order.remove(combatent)
                    sleep(1)
                else:
                    self.enemy_dead_pool.append(combatent["entity"])
                    self.order.remove(combatent)
                    sleep(1)

    def reset_turn_statuses(self):
        for combatent in self.order:
            combatent["has_gone"] = False
            combatent["is_active"] = False

    def print_dead_pools(self):
        print("Character Dead Pool:")
        [print(f"  {char.display_name}") for char in self.character_dead_pool]
        print("Enemy Dead Pool:")
        [print(f"  {enemy.name}") for enemy in self.enemy_dead_pool]

    def battle_turn(self):
        self.reset_turn_statuses()
        valid_selection = ["1", "2", "3", "4", "5", "6", "7"]
        for combatent in self.order:
            clr()
            self.print_dead_pools()
            combatent["is_active"] = True
            self.print_turn_order()
            if combatent["entity"] in self.character_pool:
                combatent["entity"].job.level_up = combatent["entity"].job.level_up
                self.print_player_turn(combatent["entity"])
                selection = get_selection(
                    valid_selection,
                    "That is not a valid selection. Please enter a single number between 1 and 7 that corresponds with the above options.",
                )

                if selection == "1":  # Attacks
                    self.party_member_attacks(combatent)
                elif selection == "2":  # Abilities
                    self.party_member_abilities(combatent)
                elif selection == "3":  # Magic
                    pass
                elif selection == "4":  # Items
                    pass
                elif selection == "5":  # Inspect
                    pass
                elif selection == "6":  # Pass
                    pass
                elif selection == "7":  # Flee
                    pass
            else:
                print(f"\n{combatent['entity'].name}'s Turn.")
                target_list = []
                for character in self.character_pool:
                    if character.is_alive():
                        target_list.append(character)
                target = choice(target_list)
                combatent["entity"].basic_attack(target)
            self.clean_up_dead()

            combatent["has_gone"] = True
            combatent["is_active"] = False

    def assign_exp(self, enemy_pool, character_pool) -> None:
        clr()
        print("Calculating experience gained by the party...")
        xp_pool = 0
        for enemy in enemy_pool:
            xp_pool += enemy.exp_value
        sleep(1)
        print(f"\nTotal experience from slain enemies is {xp_pool} exp.")
        sleep(1)
        xp_per_character = xp_pool // len(character_pool)
        print(f"\nEach party member will receive {xp_per_character} exp.")
        input(f"\nPress Enter To Calculate {character_pool[0]}'s experience gain...")
        for i, character in enumerate(character_pool, 1):
            print(f"\n{character.display_name} currently has {character.exp} exp.")
            character.exp += xp_per_character
            print(f"\n{character.display_name} now has {character.exp} exp.")
            if character.gained_enough_exp_to_level(xp_per_character):
                character.job.level_up_job()
            if not i == len(character_pool):
                input(
                    f"\nPress Enter to calculate {character_pool[i].display_name}'s experience gain..."
                )
            else:
                print(
                    f"\nFinished calculating experience gain. Press Enter to Continue."
                )
                sleep(1)

    # def tally_monster_type_killed(self, party):
    #     monster_types_killed = copy(party.monsters_killed)
    #     for monster in self.enemy_dead_pool:
    #         monster_type = monster.__class__.__name__.lower()
    #         monster_types_killed[monster_type] += 1
    #     for monster in monster_types_killed:
    #         difference = monster - party.monsters_killed[monster]
    #         if difference > 0:
    #             print(f"{party.name} has killed {difference} {monster.keys()}")

    #     print(monster_types_killed)
    #     input("Enter...")


class GenerateEnemy:
    def generate_enemy(self):
        classification_options = ["minion", "standard", "elite", "champion", "boss"]
        name = input("Input the name of your enemy: ")
        type = input("What kind of monster is it: ")
        str_ = int(input("What is the strength of the monster: "))
        agi = int(input("What is the agility of the monster: "))
        int_ = int(input("What is the intellect of the monster: "))
        luck = int(input("What is the luck of the monster: "))
        hit_dice_type = int(
            input("What is the hit dice of the monster (Max HP of the dice): ")
        )
        hit_dice_num_base = int(input("How many hit dice does the monster have: "))
        challenge_rating = float(input("What is the challenge rating of the monster: "))
        for classification in classification_options:
            name_monster = construct_class(
                type.title(),
                name=name.title(),
                strength=str_,
                agility=agi,
                intellect=int_,
                luck=luck,
                hit_dice_type=hit_dice_type,
                hit_dice_num_base=hit_dice_num_base,
                classification=classification,
                cr=challenge_rating,
            )
            self.save_enemy(name_monster, name)
            print(name_monster)

    def fmt_save_load(self, name):
        if " " in name:
            name = name.lower().split(" ")
            name = "_".join(name)
        if "-" in name:
            name = name.lower().replace("-", "_")
        else:
            name = name.lower()
        return name

    def save_enemy(self, enemy, enemy_name):
        enemy_name = self.fmt_save_load(enemy_name)
        with open(
            f"dungeon_delvers/enemies/{enemy_name}_{enemy.classification['display_name']}.pkl",
            "wb",
        ) as f:
            pickle.dump(enemy, f, -1)


class Party:
    def __init__(self, party, name) -> None:
        self.members = party
        self.name = name
        self.size = len(self.members)
        self.party_items = []
        self.monsters_killed = {
            "abberation": 0,
            "beast": 0,
            "celestial": 0,
            "construct": 0,
            "dragon": 0,
            "elemental": 0,
            "fey": 0,
            "fiend": 0,
            "giant": 0,
            "goblinoid": 0,
            "humanoid": 0,
            "monstrosity": 0,
            "ooze": 0,
            "plant": 0,
            "undead": 0,
        }
        self.cr = 0
        party_levels = 0
        for member in self.members:
            party_levels += member.job.level
        # self.cr = party_levels // self.size

    def display_party(self):
        party_obj = f"{self.name}"
        for member in self.members:
            party_obj += f"\n  {member}"
        return party_obj

    def __str__(self) -> str:
        return f"""
            \r{self.name.title()}
            \r{*self.members,}"""


class EnemyParty:
    def __init__(self, party_cr) -> None:
        self.members = []
        # TODO Create a way to load a party based on a CR rating.
        # Load all pkl files in the enemies folder into memory
        # Get their challenge ratings and build a party that is +/- the party CR.
        directory_ = "dungeon_delvers/enemies"
        for filename in os.scandir(directory_):
            if filename.is_file():
                self.pkl_loader(filename)

    def pkl_loader(self, file):
        with open(file, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break


if __name__ == "__main__":
    game = Game()
    # enemy_generator = GenerateEnemy()
    # enemy_generator.generate_enemy()

    # new_mon = Goblinoid(
    #     name="Murzod",
    #     strength=14,
    #     agility=12,
    #     intellect=8,
    #     luck=10,
    #     hp=21,
    #     cr=0.25,
    #     unique=True,
    #     unique_cr_mod=2,
    #     unique_hp_mod=1.5,
    #     unique_stat_mod=6,
    #     unique_exp_mod=1.75,
    #     classification="unique",
    # )
    # new_mon2 = Goblinoid(
    #     name="Goblin",
    #     strength=10,
    #     agility=14,
    #     intellect=10,
    #     luck=8,
    #     hit_dice_type=6,
    #     hit_dice_num_base=2,
    #     cr=0.25,
    #     classification="champion",
    # )
    # new_mon3 = Goblinoid(
    #     name="Goblin Minion",
    #     strength=14,
    #     agility=12,
    #     intellect=8,
    #     luck=0,
    #     hp=21,
    #     cr=1,
    #     classification="minion",
    # )

    # jonah = Player(
    #     name="Jonah",
    #     race="human",
    #     job="fighter",
    #     strength=18,
    #     agility=15,
    #     intellect=10,
    #     luck=16,
    # )

    # horus = Player(
    #     name="Horus",
    #     race="halfling",
    #     job="paladin",
    #     strength=14,
    #     agility=12,
    #     intellect=18,
    #     luck=16,
    # )

    # new_battle = Battle([new_mon2], [horus])

    # new_battle = Battle([new_mon], [jonah])
    # print(new_mon2.print_stats())
    # new_mon2.basic_attack(jonah)

    # while True:
    #     new_mon.basic_attack(jonah)
    # new_mon.basic_attack(jonah)
    # jonah.job.basic_attack(jonah.equipped_items["weapon"], new_mon, jonah)
    # game = Game()
    # party_list = [jonah]
    # enemy_list = [new_mon, new_mon2, new_mon3]
    # new_battle = Battle(enemy_list, party_list)
    # while not len(new_battle.enemy_dead_pool) == len(new_battle.enemy_pool):
    #     new_battle.battle_turn()
    # new_battle.assign_exp(new_battle.enemy_dead_pool, new_battle.character_pool)

    # for i in range(1, 20):
    #     jonah.job.level_up_job()
