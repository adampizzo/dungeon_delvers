from math import ceil
from random import randint
from colorama import init, Fore, Back, Style
import dungeon_delvers.base as ddb
import dungeon_delvers.items as ddi
from time import sleep

init()


class Monster(ddb.Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        classification = {
            "minion": {
                "name": f"{Fore.BLACK}{Back.WHITE}{Style.BRIGHT}Minion{Style.RESET_ALL}",
                "display_name": "minion",
                "cr_mod": -1,
                "max_hp": 1,
                "stat_mod": -4,
                "exp_mod": 0.5,
                "text_color": {
                    "fore": Fore.BLACK,
                    "back": Back.WHITE,
                    "style": Style.BRIGHT,
                },
            },
            "standard": {
                "name": f"{Fore.BLACK}{Back.GREEN}{Style.BRIGHT}Standard{Style.RESET_ALL}",
                "display_name": "standard",
                "cr_mod": 0,
                "max_hp": 1,
                "stat_mod": 0,
                "exp_mod": 1,
                "text_color": {
                    "fore": Fore.GREEN,
                    "back": Back.BLACK,
                    "style": Style.BRIGHT,
                },
            },
            "elite": {
                "name": f"{Fore.BLACK}{Back.BLUE}{Style.BRIGHT}Elite{Style.RESET_ALL}",
                "display_name": "elite",
                "cr_mod": 1,
                "max_hp": 2,
                "stat_mod": 2,
                "exp_mod": 1.5,
                "text_color": {
                    "fore": Fore.BLUE,
                    "back": Back.BLACK,
                    "style": Style.BRIGHT,
                },
            },
            "champion": {
                "name": f"{Fore.BLACK}{Back.YELLOW}{Style.BRIGHT}Champion{Style.RESET_ALL}",
                "display_name": "champion",
                "cr_mod": 2,
                "max_hp": 3,
                "stat_mod": 4,
                "exp_mod": 2,
                "text_color": {
                    "fore": Fore.YELLOW,
                    "back": Back.BLACK,
                    "style": Style.BRIGHT,
                },
            },
            "boss": {
                "name": f"{Fore.BLACK}{Back.RED}{Style.BRIGHT}Boss{Style.RESET_ALL}",
                "display_name": "boss",
                "cr_mod": 3,
                "max_hp": 4,
                "stat_mod": 6,
                "exp_mod": 3,
                "text_color": {
                    "fore": Fore.RED,
                    "back": Back.BLACK,
                    "style": Style.BRIGHT,
                },
            },
        }

        if "unique" in kwargs:
            classification.update(
                {
                    "unique": {
                        "name": f"{Fore.BLACK}{Back.MAGENTA}Unique{Style.RESET_ALL}",
                        "display_name": "unique",
                        "cr_mod": kwargs["unique_cr_mod"],
                        "max_hp": kwargs["unique_hp_mod"],
                        "stat_mod": kwargs["unique_stat_mod"],
                        "exp_mod": kwargs["unique_exp_mod"],
                        "text_color": {
                            "fore": Fore.BLACK,
                            "back": Back.MAGENTA,
                            "style": Style.BRIGHT,
                        },
                    },
                }
            )
        self.monster_race_name = "monster"
        self.name = (
            classification[kwargs["classification"]]["text_color"]["style"]
            + classification[kwargs["classification"]]["text_color"]["fore"]
            + classification[kwargs["classification"]]["text_color"]["back"]
            + self.name
            + Style.RESET_ALL
        )
        self.classification = classification[kwargs["classification"]]
        self.treasure_types = {}
        self.hit_dice_type = kwargs["hit_dice_type"]
        self.hit_dice_num_base = kwargs["hit_dice_num_base"]
        self.hit_dice_num = self.hit_dice_num_base * self.classification["max_hp"]
        for atr in self.attributes:
            self.attributes[atr]["score"] += self.classification["stat_mod"]
        self.update_stat_modifiers()
        hp = []
        for dice in range(self.hit_dice_num):
            dice_roll = randint(1, self.hit_dice_type)
            hp.append(dice_roll + self.attributes["strength"]["modifier"])
        hp = sum(hp)
        # if self.classification == "minion":
        if hp < 1:
            hp = 1
        self.max_hp = hp
        self.current_hp = self.max_hp
        self.armor_class = 10 + self.attributes["agility"]["modifier"]
        self.challenge_rating = kwargs["cr"]
        monster_cr_list = [
            0,
            0.125,
            0.25,
            0.5,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
        ]
        cr_index = monster_cr_list.index(self.challenge_rating)
        cr_mod = self.classification["cr_mod"]
        new_index = cr_index + cr_mod
        self.challenge_rating = monster_cr_list[new_index]
        monster_proficiency = {
            0: {"proficiency": 2, "exp_value": 10},
            0.125: {"proficiency": 2, "exp_value": 25},
            0.25: {"proficiency": 2, "exp_value": 50},
            0.5: {"proficiency": 2, "exp_value": 100},
            1: {"proficiency": 2, "exp_value": 200},
            2: {"proficiency": 2, "exp_value": 450},
            3: {"proficiency": 2, "exp_value": 700},
            4: {"proficiency": 2, "exp_value": 1100},
            5: {"proficiency": 3, "exp_value": 1800},
            6: {"proficiency": 3, "exp_value": 2300},
            7: {"proficiency": 3, "exp_value": 2900},
            8: {"proficiency": 3, "exp_value": 3900},
            9: {"proficiency": 4, "exp_value": 5000},
            10: {"proficiency": 4, "exp_value": 5900},
            11: {"proficiency": 4, "exp_value": 7200},
            12: {"proficiency": 4, "exp_value": 8400},
            13: {"proficiency": 5, "exp_value": 10000},
            14: {"proficiency": 5, "exp_value": 11500},
            15: {"proficiency": 5, "exp_value": 13000},
            16: {"proficiency": 5, "exp_value": 15000},
            17: {"proficiency": 6, "exp_value": 18000},
            18: {"proficiency": 6, "exp_value": 20000},
            19: {"proficiency": 6, "exp_value": 22000},
            20: {"proficiency": 6, "exp_value": 25000},
            21: {"proficiency": 7, "exp_value": 33000},
            22: {"proficiency": 7, "exp_value": 41000},
            23: {"proficiency": 7, "exp_value": 50000},
            24: {"proficiency": 7, "exp_value": 62000},
            25: {"proficiency": 8, "exp_value": 75000},
            26: {"proficiency": 8, "exp_value": 90000},
            27: {"proficiency": 8, "exp_value": 105000},
            28: {"proficiency": 8, "exp_value": 12000},
            29: {"proficiency": 9, "exp_value": 135000},
            30: {"proficiency": 9, "exp_value": 155000},
        }
        self.proficiency = monster_proficiency[kwargs["cr"]]["proficiency"]
        self.exp_value = monster_proficiency[self.challenge_rating]["exp_value"]
        starting_armor = None
        starting_weapon = None
        starting_shield = None
        self.equipped_items["armor"] = starting_armor
        self.equipped_items["weapon"] = starting_weapon
        self.equipped_items["shield"] = starting_shield
        self.update_equipment_stats()

    def take_damage(self, damage, source):
        self.current_hp -= damage
        print(f"\n{self.name} took {damage} damage from {source.name}.\n")
        if self.is_alive():
            print(f"{self.name} has {self.current_hp} reamining.")
        else:
            print(f"{self.name} has been slain!\n")

    def is_alive(self):
        if self.current_hp > 0:
            return True

    def basic_attack(self, target: ddb.Entity):
        roll = randint(1, 20)
        attack_attribute_modifier = self.attack_attribute_modifier()
        luck_roll: int = self.luck_roll()
        bonuses = attack_attribute_modifier["stat"] + self.proficiency + luck_roll
        # if not self.is_slot_empty("weapon"):
        #     if 'finesse' in self.equipped_items["weapon"].abilities:
        #         bonus_breakdown = f"Agility(Finesse Weapon): {self.attributes['agility']['modifier']}, Proficiency Modifier: {self.proficiency}"
        #         bonuses = self.attributes["agility"]["modifier"] + self.proficiency
        #     else:
        #         bonuses = self.attributes["strength"]["modifier"] + self.proficiency
        # else:
        #     bonuses = self.attributes["strength"]["modifier"] + self.proficiency
        total_roll = roll + bonuses

        print(f"\n{self.name} is attacking {target.display_name}.")
        sleep(1)
        # print(f"\n{self.name} rolled a {total_roll}")
        if total_roll >= target.armor_class:
            print(f"{total_roll} - Hit!")
            damage_roll = (
                randint(1, self.weapon_max_damage_die)
                + attack_attribute_modifier["stat"]
            )
            if damage_roll <= 0:
                print(f"\n{self.display_name} did no damage to {target.display_name}!")
            else:
                target.take_damage(damage_roll, self)
        else:
            print(f"\n{self.name} missed {target.display_name} with their attack!")
        input("Press Enter To Continue...")

    def print_stats(self) -> str:
        return f"""
            \r{self.name} [{self.classification['name']}] - {self.monster_race_name} - CR {self.challenge_rating}
            \r{Fore.RED}{Style.BRIGHT}Strength Score{Style.RESET_ALL}: {self.attributes['strength']['score']} - Modifier: {self.attributes['strength']['modifier']}
            \r{Fore.GREEN}{Style.BRIGHT}Agility Score{Style.RESET_ALL}: {self.attributes['agility']['score']} - Modifier: {self.attributes['agility']['modifier']}
            \r{Fore.BLUE}{Style.BRIGHT}Intellect Score{Style.RESET_ALL}: {self.attributes['intellect']['score']} - Modifier: {self.attributes['intellect']['modifier']}
            \r{Fore.YELLOW}{Style.BRIGHT}Luck Score{Style.RESET_ALL}: {self.attributes['luck']['score']} - Modifier: {self.attributes['luck']['modifier']}
            \r{Fore.RED}Max HP{Style.RESET_ALL}: {self.max_hp} - {Fore.RED}Current HP{Style.RESET_ALL}: {self.current_hp}
            \r{Fore.YELLOW}Armor Class{Style.RESET_ALL}: {self.armor_class}
                """

    # def __repr__(self) -> str:
    #     return f"\r{self.name} - {self.monster_race_name} [{self.classification['name']}] - CR {self.challenge_rating}"


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


class Monstrosity(Monster):
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
        self.size = "small"

        self.monster_race_name = f"{Fore.GREEN}Goblinoid{Style.RESET_ALL}"
        self.treasure_types = ["weapon", "armor", "shield", "trade_good", "potion"]
        starting_armor = ddi.Armor(
            name="leather armor",
            description="",
            proficiency_required="light",
            rarity="common",
            weight=10,
            armor_class=1,
            abilities=[],
        )
        starting_weapon = ddi.Weapon(
            name="scimitar",
            description="",
            proficiency_required="martial",
            rarity="common",
            weight=3,
            abilities=["finesse", "light"],
            damage_max_die=6,
        )
        starting_shield = ddi.Shield(
            name="shield",
            description="",
            proficiency_required="shield",
            rarity="common",
            weight=6,
            armor_class=2,
            abilities=[],
        )

        self.equipped_items["armor"] = starting_armor
        self.equipped_items["weapon"] = starting_weapon
        self.equipped_items["shield"] = starting_shield
        self.update_equipment_stats()


class Dragonborn(Humanoid):
    pass


class Elvish(Humanoid):
    pass


class Dwarven(Humanoid):
    pass


class Human_(Humanoid):
    pass


class Gnomish(Humanoid):
    pass


class HalfElven(Humanoid):
    pass


class HalfOrc(Humanoid):
    pass


class Orc(Humanoid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monster_race_name = f"{Style.BRIGHT}{Fore.GREEN}Orc{Style.RESET_ALL}"
        starting_armor = ddi.Armor(
            name="hide armor",
            description="",
            proficiency_required="medium",
            rarity="common",
            weight=12,
            armor_class=2,
            abilities=["max_dex_bonus_2"],
        )
        starting_weapon = ddi.Weapon(
            name="Great Axe",
            description="",
            proficiency_required="martial",
            rarity="common",
            weight=7,
            abilities=["two_handed"],
            damage_max_die=12,
        )

        self.equipped_items["armor"] = starting_armor
        self.equipped_items["weapon"] = starting_weapon

        self.update_equipment_stats()


if __name__ == "__main__":
    pass
