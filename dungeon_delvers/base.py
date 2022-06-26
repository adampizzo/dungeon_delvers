from colorama import Fore, Style
from random import randint, random, choice
from time import sleep

from dungeon_delvers.utilities import print_sep, clr
from dungeon_delvers.job import Fighter, Paladin
from dungeon_delvers.race import Human, Halfelf, Halfling, Halforc, Elf, Dwarf, Gnome


def construct_class(klass, *args, **kwargs):
    constructor = globals()[klass]
    return constructor(*args, **kwargs)


class Entity:
    def __init__(self, *args, **kwargs):
        self.name = kwargs["name"]
        self.display_name = self.name
        self.name_length = len(self.name)
        self.attributes = {
            "strength": {
                "score": kwargs["strength"],
                "base": kwargs["strength"],
                "modifier": 0,
            },
            "agility": {
                "score": kwargs["agility"],
                "base": kwargs["agility"],
                "modifier": 0,
            },
            "intellect": {
                "score": kwargs["intellect"],
                "base": kwargs["intellect"],
                "modifier": 0,
            },
            "luck": {"score": kwargs["luck"], "base": kwargs["luck"], "modifier": 0},
        }
        self.equipped_items = {
            "armor": None,
            "weapon": None,
            "shield": None,
        }
        self.damage_reduction = 0
        self.items = []
        self.abilities = []
        self.attacks = []
        self.magic = []
        self.update_stat_modifiers()

    def print_stats(self):
        print(
            f"""Name - {self.name}
            \rStrength - {self.attributes['strength']['score']} - {self.attributes['strength']['modifier']}
            \rAgility - {self.attributes['agility']['score']} - {self.attributes['agility']['modifier']}
            \rIntellect - {self.attributes['intellect']['score']} - {self.attributes['intellect']['modifier']}
            """
        )

    def update_stat_modifiers(self):
        for stat in self.attributes:
            self.attributes[stat]["modifier"] = (
                self.attributes[stat]["score"] - 10
            ) // 2

    def luck_roll(self):
        if self.attributes["luck"]["modifier"] > 0:
            return randint(0, self.attributes["luck"]["modifier"])
        elif self.attributes["luck"]["modifier"] < 0:
            return randint(self.attributes["luck"]["modifier"], 0)
        else:
            return 0

    def is_slot_empty(self, slot):
        if self.equipped_items[slot] is None:
            return True
        else:
            return False

    def is_weapon_finesse(self):
        if (
            not self.is_slot_empty("weapon")
            and "finesse" in self.equipped_items["weapon"].abilities
        ):
            return True
        else:
            return False

    def attack_attribute_modifier(self):
        if self.is_weapon_finesse():
            return {"name": "agility", "stat": self.attributes["agility"]["modifier"]}
        else:
            return {"name": "strength", "stat": self.attributes["strength"]["modifier"]}

    def update_equipment_stats(self):
        for item in self.equipped_items:
            if not self.is_slot_empty(item):
                # if item == "shield":
                #     print("shield")
                # print(
                #     f"{__class__} - {self.name} - {item} slot empty? - {self.is_slot_empty(item)} - item name: {self.equipped_items[item].display_name}"
                # )
                if item == "armor":
                    if "no_agi" in self.equipped_items[item].abilities:
                        self.armor_class = 10 + self.equipped_items[item].armor_class
                    if "max_dex_bonus_2" in self.equipped_items[item].abilities:
                        if self.attributes["agility"]["modifier"] > 2:
                            max_bonus = 2
                        else:
                            max_bonus = self.attributes["agility"]["modifier"]
                        self.armor_class = (
                            10 + self.equipped_items[item].armor_class + max_bonus
                        )
                        # print(
                        #     f"{self.display_name} - AC = 10 + Armor(+{self.equipped_items[item].armor_class}) + Agi(+{max_bonus})"
                        # )
                        # print(self.armor_class)
                        # input(...)
                    else:
                        self.armor_class = (
                            10
                            + self.equipped_items[item].armor_class
                            + self.attributes["agility"]["modifier"]
                        )
                if item == "shield":
                    self.armor_class += self.equipped_items[item].armor_class
                if item == "weapon":
                    self.weapon_max_damage_die = self.equipped_items[
                        item
                    ].damage_max_die
                    self.weapon_num_dice = self.equipped_items[item].num_dice


class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display_name = self.name
        self.race = construct_class(kwargs["race"].title())
        self.job = construct_class(kwargs["job"].title(), step_parent=self)
        self.equipped_items["armor"] = self.job.starting_armor
        self.equipped_items["weapon"] = self.job.starting_weapon
        self.exp = 0
        self.hp_roll_amounts = {}

        self.update_ability_scores()
        self.assign_starting_hp()
        self.update_equipment_stats()

    def update_ability_scores(self):
        for stat in self.attributes:
            self.attributes[stat]["racial_modifier"] = self.race.attributes[stat]
            self.attributes[stat]["job_modifier"] = self.job.attributes[stat]
            self.attributes[stat]["score"] = (
                self.attributes[stat]["base"]
                + self.race.attributes[stat]
                + self.job.attributes[stat]
            )
            self.attributes[stat]["modifier"] = (
                self.attributes[stat]["score"] - 10
            ) // 2

    def print_stats(self):
        print(
            f"""Name - {self.name}  |  Race - {self.race.name.title()}  |  Job -  {self.job.name.title()}
            \rStrength - {self.attributes['strength']['score']} - {self.attributes['strength']['modifier']} -
            \rAgility - {self.attributes['agility']['score']} - {self.attributes['agility']['modifier']}
            \rIntellect - {self.attributes['intellect']['score']} - {self.attributes['intellect']['modifier']}
            """
        )

    def print_abilities(self):
        print(f"{self.name}'s Abilities:")
        for ability in self.abilities:
            print(f"{ability}")
        for j_ability in self.job.abilities:
            print(f"{j_ability['name']}")

    def assign_starting_hp(self):
        self.max_hp = self.job.hp_dice_max + self.attributes["strength"]["modifier"]
        self.current_hp = self.max_hp
        self.hp_roll_amounts["1"] = self.job.hp_dice_max

    def update_hp(self) -> int:
        hp_pool = []
        for hp_level_values in self.hp_roll_amounts.values():
            hp_with_modifiers = (
                hp_level_values + self.attributes["strength"]["modifier"]
            )
            hp_pool.append(hp_with_modifiers)
        self.max_hp = sum(hp_pool)
        self.current_hp = self.max_hp

    def take_damage(self, damage, source):
        if not hasattr(self, "damage_reduction"):
            setattr(self, "damage_reduction", 0)

        if self.damage_reduction > 0:
            damage_minus_reduction = damage - self.damage_reduction
            self.current_hp -= damage_minus_reduction
            print(
                f"{self.name} took {damage_minus_reduction} damage from {source.name}. {self.damage_reduction} damage negated by damage reduction."
            )
        else:
            self.current_hp -= damage
            print(f"{self.name} took {damage} damage from {source.name}.")
        if self.is_alive():
            print(f"{self.name} has {self.current_hp} reamining.")
        else:
            print(f"{self.name} has been slain!\n")

    def heal_damage(self, heal, source, ability_name):
        self.current_hp += heal
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
        print(f"{self.name} healed {heal} from {source.name}'s {ability_name}.")
        print(f"{self.name} is now at {self.current_hp} hp out of {self.max_hp} hp.")

    def is_alive(self):
        if self.current_hp > 0:
            return True

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
        exp_to_level = experience_level_requirements[self.job.level + 1]
        current_exp = self.exp

        print(f"{self.display_name} levels up at {exp_to_level} exp.")
        if current_exp > exp_to_level:
            print(f"Congratulations! {self.display_name} have leveled up!")
            return True
        else:
            print(f"{self.display_name} has not leveled up.")
            return False

    def level_up(self):
        self.job.level += 1
        self.job.set_attribute_bonuses()
        self.update_ability_scores()

    def display_attacks(self):
        pass

    def print_player_stats(self) -> str:
        return f"""
            \r{self.name} - Level {self.job.level} {self.race.name.title()} {self.job.name.title()}
            \r{Fore.RED}Strength Score{Style.RESET_ALL}: {self.attributes['strength']['score']} - Modifier: {self.attributes['strength']['modifier']}
            \r{Fore.GREEN}Agility Score{Style.RESET_ALL}: {self.attributes['agility']['score']} - Modifier: {self.attributes['agility']['modifier']}
            \r{Fore.BLUE}Intellect Score{Style.RESET_ALL}: {self.attributes['intellect']['score']} - Modifier: {self.attributes['intellect']['modifier']}
            \r{Fore.YELLOW}Luck Score{Style.RESET_ALL}: {self.attributes['luck']['score']} - Modifier: {self.attributes['luck']['modifier']}
            \rMax HP: {self.max_hp} - Current HP: {self.current_hp}
            \rArmor Class: {self.armor_class} - Armor: {self.equipped_items['armor'].name.title()}
            \rWeapon: {self.equipped_items['weapon'].name.title()}
                """

    def __str__(self) -> str:
        return f"{self.display_name} - Level {self.job.level} {self.race.name.title()} {self.job.name}"


if __name__ == "__main__":
    pass
    # jonah = Player(name='Jonah', race="human", job="fighter", strength=18,
    #                agility=15, intellect=10, luck=16)

    # new_mon = monsters.Goblinoid(
    #     name='Goblin Boss', strength=14, agility=12, intellect=8, luck=0, hp=21, cr=2)

    # new_mon3 = monsters.Goblinoid(
    #     name='Goblin Spearman', strength=12, agility=14, intellect=8, luck=0, hp=8, cr=.25)
