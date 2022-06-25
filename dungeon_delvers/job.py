from abc import abstractmethod
import itertools
from operator import indexOf
from random import randint
from time import sleep
from colorama import Back, Fore, Style


# import dungeon_delvers.attacks as dda
import dungeon_delvers.items as ddi
from dungeon_delvers.utilities import print_sep, clr

# import dungeon_delvers.base as ddb


class Job:
    def __init__(self, *args, **kwargs):
        self.step_parent = kwargs["step_parent"]
        self.name = "job"
        self.hp_dice_min = 1
        self.hp_dice_max = 20
        self.abilities = []
        self.attacks = []
        self.attributes = {
            "strength": 0,
            "agility": 0,
            "intellect": 0,
            "luck": 0,
        }
        self.num_attacks = 1
        self.primary_attribute = "luck"
        self.primary_stat = ""
        self.job_proficiency_values = {
            1: {"proficiency": 2},
            2: {"proficiency": 2},
            3: {"proficiency": 2},
            4: {"proficiency": 2},
            5: {"proficiency": 3},
            6: {"proficiency": 3},
            7: {"proficiency": 3},
            8: {"proficiency": 3},
            9: {"proficiency": 4},
            10: {"proficiency": 4},
            11: {"proficiency": 4},
            12: {"proficiency": 4},
            13: {"proficiency": 5},
            14: {"proficiency": 5},
            15: {"proficiency": 5},
            16: {"proficiency": 5},
            17: {"proficiency": 6},
            18: {"proficiency": 6},
            19: {"proficiency": 6},
            20: {"proficiency": 6},
        }
        self.level = 1
        self.proficiency: int = self.job_proficiency_values[self.level]["proficiency"]
        self.level_up = {
            2: {"new_abilities": [{}], "new_attacks": [{}]},
            3: {"new_abilities": [{}], "new_attacks": [{}]},
            4: {"new_abilities": [{}], "new_attacks": [{}]},
            5: {"new_abilities": [{}], "new_attacks": [{}]},
            6: {"new_abilities": [{}], "new_attacks": [{}]},
            7: {"new_abilities": [{}], "new_attacks": [{}]},
            8: {"new_abilities": [{}], "new_attacks": [{}]},
            9: {"new_abilities": [{}], "new_attacks": [{}]},
            10: {"new_abilities": [{}], "new_attacks": [{}]},
            11: {"new_abilities": [{}], "new_attacks": [{}]},
            12: {"new_abilities": [{}], "new_attacks": [{}]},
            13: {"new_abilities": [{}], "new_attacks": [{}]},
            14: {"new_abilities": [{}], "new_attacks": [{}]},
            15: {"new_abilities": [{}], "new_attacks": [{}]},
            16: {"new_abilities": [{}], "new_attacks": [{}]},
            17: {"new_abilities": [{}], "new_attacks": [{}]},
            18: {"new_abilities": [{}], "new_attacks": [{}]},
            19: {"new_abilities": [{}], "new_attacks": [{}]},
            20: {"new_abilities": [{}], "new_attacks": [{}]},
        }
        self.critical_hit_roll = 20
        self.critical_hit_roll_mod = 0

    def set_attribute_bonuses(self):
        if self.level == 4:
            self.attributes[self.primary_attribute] = 2
        elif self.level == 8:
            self.attributes[self.primary_attribute] = 4
        elif self.level == 12:
            self.attributes[self.primary_attribute] = 6
        elif self.level == 16:
            self.attributes[self.primary_attribute] = 8
        elif self.level == 20:
            self.attributes[self.primary_attribute] = 10

    def ability_in_abilities(self, ability_to_check: str):
        in_abilities = False
        for ability in self.abilities:
            if ability_to_check in ability["name"]:
                in_abilities = True
        return in_abilities

    def level_up_job(self):
        clr()
        self.level += 1
        previous_str = self.step_parent.attributes["strength"]["modifier"]
        self.set_attribute_bonuses()
        self.step_parent.update_ability_scores()
        strength_mod_difference = (
            self.step_parent.attributes["strength"]["modifier"] - previous_str
        )
        print(f"\n{print_sep('-', 100)}")
        print(
            f"\n{self.step_parent.display_name} is now a level {self.level} {self.name.title()}."
        )
        sleep(1)
        if not self.level_up[self.level]["new_abilities"] == [{}]:
            print(
                f"\n{self.step_parent.display_name} has gained the following abilities: "
            )
            for abilities in self.level_up[self.level]["new_abilities"]:
                print(f"\n{abilities['name']} - {abilities['description']}")
                if abilities["cooldown"] == -1:
                    print(
                        f"Type: {abilities['type'].title()} - Uses per battle: {abilities['uses_per_battle']}"
                    )
                elif abilities["cooldown"] == 1:
                    print(
                        f"Type: {abilities['type'].title()} - Cooldown {abilities['cooldown']} turn"
                    )
                else:
                    print(
                        f"Type: {abilities['type'].title()} - Cooldown {abilities['cooldown']} turns"
                    )
                if abilities["name"] not in self.abilities:
                    self.abilities.append(abilities)
        else:
            print("\nNo Abilities Gained This Level.")
        sleep(1)
        if not self.level_up[self.level]["new_attacks"] == [{}]:
            print(
                f"\n{self.step_parent.display_name} has gained the following attacks: "
            )
            for attacks in self.level_up[self.level]["new_attacks"]:
                print(f"\n{attacks['name']} - {attacks['description']}")
                print(
                    f"Type: {attacks['type'].title()} - Cooldown {attacks['cooldown']} turns"
                )
                self.attacks.append(attacks)
        else:
            print("\nNo Attacks Gained This Level.")
        sleep(1)
        self.proficiency = self.job_proficiency_values[self.level]["proficiency"]
        if (
            self.job_proficiency_values[self.level - 1]["proficiency"]
            < self.proficiency
        ):
            print(
                f"\n{self.step_parent.display_name}'s proficiency modifier is now +{self.proficiency}."
            )
        else:
            print("\nNo Proficiency Change.")
        sleep(1)
        if strength_mod_difference > 0:
            print(
                f"\n{self.step_parent.display_name}'s strength modifier has increased by {strength_mod_difference}. This provides {self.step_parent.display_name} with +{strength_mod_difference} hp per level."
            )
            sleep(1)
            print(
                f"\n{self.step_parent.display_name}'s strength is now {self.step_parent.attributes['strength']['score']} | Modifier: {self.step_parent.attributes['strength']['modifier']}"
            )
            sleep(1)
        print(
            f"\n{self.step_parent.display_name}'s previous maximum hp was {self.step_parent.max_hp} hp."
        )
        sleep(1)
        self.step_parent.hp_roll_amounts[self.level] = randint(1, self.hp_dice_max)
        print(
            f"\nNew HP rolled for {self.step_parent.display_name}: {self.step_parent.hp_roll_amounts[self.level] + self.step_parent.attributes['strength']['modifier']} hp."
        )
        sleep(1)
        self.step_parent.update_hp()
        print(
            f"\n{self.step_parent.display_name}'s new maximum hp is {self.step_parent.max_hp} hp."
        )
        print(f"\n{print_sep('-', 100)}")
        sleep(1)
        input("Press Enter To Continue...")


class Fighter(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step_parent.display_name = (
            f"{Fore.YELLOW}{self.step_parent.name}{Style.RESET_ALL}"
        )
        self.primary_attribute = "strength"
        self.name = "fighter"
        self.primary_stat = "strength"
        self.hp_dice_max = 10
        self.attacks = [
            {
                "name": "Smash",
                "description": "A devastating overhand melee strike. Weapon Damage + Strength + (Random Luck)",
                "source": self.name,
                "type": "active",
                "cooldown": 0,
            }
        ]
        self.abilities = [
            {
                "name": "Second Wind",
                "description": """Pulling from deep within, for each level of fighter, heal yourself 1d10 + Strength Modifier + 1 per level of fighter. For Example: A 3rd level fighter with 16 Strength will heal for 3d10 + 9 (Str Mod +3 * 3) + 9 (Fighter Level 3 * 3""",
                "source": self.name,
                "type": "active",
                "cooldown": -1,
                "uses_per_battle": 1,
            }
        ]

        self.starting_armor = ddi.Armor(
            name="chain mail",
            description="",
            proficiency_required="heavy",
            rarity="common",
            weight=55,
            armor_class=6,
            abilities=["stealth_disadvantage", "str_req_13", "no_agi"],
        )
        self.starting_weapon = ddi.Weapon(
            name="great axe",
            description="",
            proficiency_required="martial",
            rarity="common",
            weight=7,
            abilities=["two_handed"],
            damage_max_die=12,
        )
        self.level_up = {
            2: {
                "new_abilities": [
                    {
                        "name": "Brutal Attack",
                        "description": "When damaging an enemy, any result of 1 or 2 will be rerolled.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            3: {
                "new_abilities": [
                    {
                        "name": "Action Surge",
                        "description": f"{self.step_parent.display_name} uses their extreme battle focus to take an additional action this turn.",
                        "source": self.name,
                        "type": "active",
                        "cooldown": -1,
                        "uses_per_battle": 1,
                    }
                ],
                "new_attacks": [
                    {
                        "name": "Cleave",
                        "description": "An attack that hits 2 enemies. Weapon Damage + Strength + (Random Luck)",
                        "source": self.name,
                        "type": "active",
                        "cooldown": 1,
                    }
                ],
            },
            4: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()}",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            5: {
                "new_abilities": [
                    {
                        "name": "Extra Attack",
                        "description": f"{self.step_parent.display_name} gains an additional attack.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            6: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()}",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    },
                    {
                        "name": "Vicious Criticals",
                        "description": f"{self.step_parent.display_name} becomes better at targeting vital areas of enemies. Critical strikes come more frequently.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    },
                ],
                "new_attacks": [{}],
            },
            7: {
                "new_abilities": [
                    {
                        "name": "Iron Skin",
                        "description": f"{self.step_parent.display_name} becomes tough as nails. If they were to take damage, reduce it by their strength modifier.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            8: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()}",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            9: {
                "new_abilities": [
                    {
                        "name": "Extra Attack",
                        "description": f"{self.step_parent.display_name} gains an additional attack.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            10: {
                "new_abilities": [
                    {
                        "name": "Action Surge",
                        "description": f"{self.step_parent.display_name} uses their extreme battle focus to take an additional action this turn.",
                        "source": self.name,
                        "type": "active",
                        "cooldown": -1,
                        "uses_per_battle": 2,
                    }
                ],
                "new_attacks": [
                    {
                        "name": "Whirlwind",
                        "description": "An attack that hits all enemies. Weapon Damage + Strength + (Random Luck)",
                        "source": self.name,
                        "type": "active",
                        "cooldown": 3,
                    }
                ],
            },
            11: {
                "new_abilities": [
                    {
                        "name": "Vicious Criticals",
                        "description": f"{self.step_parent.display_name} becomes better at targeting vital areas of enemies. Critical strikes come more frequently.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    },
                ],
                "new_attacks": [{}],
            },
            12: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()}",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            13: {
                "new_abilities": [
                    {
                        "name": "Extra Attack",
                        "description": f"{self.step_parent.display_name} gains an additional attack.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            14: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()}",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            15: {
                "new_abilities": [{}],
                "new_attacks": [
                    {
                        "name": "Thunderclap",
                        "description": "An attack that hits all enemies stunning them for 1 round. Strength + (Random Luck)",
                        "source": self.name,
                        "type": "active",
                        "cooldown": 5,
                    }
                ],
            },
            16: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()}",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            17: {
                "new_abilities": [
                    {
                        "name": "Extra Attack",
                        "description": f"{self.step_parent.display_name} gains an additional attack.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    },
                    {
                        "name": "Vicious Criticals",
                        "description": f"{self.step_parent.display_name} becomes better at targeting vital areas of enemies. Critical strikes come more frequently.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    },
                ],
                "new_attacks": [{}],
            },
            18: {
                "new_abilities": [
                    {
                        "name": "Action Surge",
                        "description": f"{self.step_parent.display_name} uses their extreme battle focus to take an additional action this turn.",
                        "source": self.name,
                        "type": "active",
                        "cooldown": -1,
                        "uses_per_battle": 3,
                    }
                ],
                "new_attacks": [{}],
            },
            19: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()} ",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            20: {
                "new_abilities": [
                    {
                        "name": "Godlike Physique",
                        "description": f"{self.step_parent.display_name} taps into the power of the gods. They regenerate 5 + Strength Modifier HP Per turn. They also ignore their Strength Modifier in damage from non-magical sources. ",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [
                    {
                        "name": "Blade Storm",
                        "description": "An attack that hits all enemies an amount of times equal to the amount of attacks you have. (Weapon Damage + Strength + (Random Luck)) * Number of Attacks",
                        "source": self.name,
                        "type": "active",
                        "cooldown": 5,
                    }
                ],
            },
        }

    def set_attribute_bonuses(self):
        if self.level == 4:
            self.attributes[self.primary_attribute] = 2
        elif self.level == 6:
            self.attributes[self.primary_attribute] = 4
        elif self.level == 8:
            self.attributes[self.primary_attribute] = 6
        elif self.level == 12:
            self.attributes[self.primary_attribute] = 8
        elif self.level == 14:
            self.attributes[self.primary_attribute] = 10
        elif self.level == 16:
            self.attributes[self.primary_attribute] = 12
        elif self.level == 19:
            self.attributes[self.primary_attribute] = 14

    def set_num_attacks(self):
        if self.level == 5:
            self.num_attacks += 1
            print(
                f"{self.step_parent.display_name} has gained an attack! They have {self.num_attacks} attacks now."
            )
        elif self.level == 9:
            self.num_attacks += 1
            print(
                f"{self.step_parent.display_name} has gained an attack! They have {self.num_attacks} attacks now."
            )
        elif self.level == 13:
            self.num_attacks += 1
            print(
                f"{self.step_parent.display_name} has gained an attack! They have {self.num_attacks} attacks now."
            )
        elif self.level == 17:
            self.num_attacks += 1
            print(
                f"{self.step_parent.display_name} has gained an attack! They have {self.num_attacks} attacks now."
            )

    def level_up_job(self):
        super().level_up_job()
        self.set_num_attacks()

    # target 1
    def smash(self, weapon: ddi.Weapon, target):
        print(f"\n{self.step_parent.display_name} is smashing {target.name}.")
        damage_rolls = []
        base_roll: int = randint(1, 20)
        luck_roll: int = self.step_parent.luck_roll()
        attack_attribute_modifier: int = self.step_parent.attack_attribute_modifier()
        total_roll = (
            base_roll + attack_attribute_modifier["stat"] + self.proficiency + luck_roll
        )
        if total_roll >= target.armor_class:
            if base_roll >= (self.critical_hit_roll - self.critical_hit_roll_mod):
                crit = True
                print(
                    f"\n{Back.RED}{self.step_parent.display_name} critically smashed {target.name}!{Style.RESET_ALL}"
                )
            else:
                crit = False
                print(f"\nHit! {self.step_parent.display_name} smashed {target.name}!")
            sleep(0.5)
            for _ in itertools.repeat(None, weapon.num_dice):
                damage_roll: int = randint(1, weapon.damage_max_die)
                if self.ability_in_abilities("Brutal Attack"):
                    damage_roll = self.brutal_attack_reroll(damage_roll)
                damage_rolls.append(
                    damage_roll
                    + attack_attribute_modifier["stat"]
                    + self.step_parent.luck_roll()
                )
            total_damage = sum(damage_rolls)
            if crit:
                total_damage = total_damage * 2
            target.take_damage(total_damage, self.step_parent)
        else:
            print(f"{self.step_parent.display_name} missed {target.name} with smash!")
        input(
            f"\n{self.step_parent.display_name} finished smashing. Press enter to continue..."
        )

    # self
    def second_wind(self):
        total_heal = 0

        for i in range(self.level):
            roll = randint(1, 10)
            str_mod = self.step_parent.attributes["strength"]["modifier"]
            level = self.level
            total_heal += sum([roll, str_mod, level])
        self.step_parent.heal_damage(total_heal, self.step_parent, "Second Wind")
        input("Press Enter To Continue...")

    # target 2
    def cleave(self, weapon: ddi.Weapon, targets):
        # TODO Debating removing parameter for weapon and just using self.step_parent.equipped_items['weapon']
        if len(targets) == 2:
            tar1, tar2 = targets
            print(
                f"\n{self.step_parent.display_name} is cleaving {tar1.name} and {tar2.name}."
            )
        elif len(targets) == 1:
            print(f"\n{self.step_parent.display_name} is cleaving {targets[0].name}.")

        for i, target in enumerate(targets, 1):
            damage_rolls = []
            base_roll: int = randint(1, 20)
            luck_roll: int = self.step_parent.luck_roll()
            attack_attribute_modifier: int = (
                self.step_parent.attack_attribute_modifier()
            )
            total_roll = (
                base_roll
                + attack_attribute_modifier["stat"]
                + self.proficiency
                + luck_roll
            )

            print(f"\n{self.step_parent.display_name} is cleaving {target.name}!")
            sleep(0.5)

            if total_roll >= target.armor_class:
                if base_roll >= (self.critical_hit_roll - self.critical_hit_roll_mod):
                    crit = True
                    print(
                        f"\n{Back.RED}{self.step_parent.display_name} critically cleaved {target.name}!{Style.RESET_ALL}"
                    )
                else:
                    crit = False
                    print(
                        f"\nHit! {self.step_parent.display_name} cleaved {target.name}!"
                    )
                sleep(0.5)
                for _ in itertools.repeat(None, weapon.num_dice):
                    damage_roll: int = randint(1, weapon.damage_max_die)
                    if self.ability_in_abilities("Brutal Attack"):
                        damage_roll = self.brutal_attack_reroll(damage_roll)
                    damage_rolls.append(
                        damage_roll
                        + attack_attribute_modifier["stat"]
                        + self.step_parent.luck_roll()
                    )
                total_damage = sum(damage_rolls)
                if crit:
                    total_damage = total_damage * 2
                target.take_damage(total_damage, self.step_parent)
            else:
                print(
                    f"{self.step_parent.display_name} missed {target.name} with cleave!"
                )
            sleep(0.5)
            if not i == len(targets):
                input(f"\nPress Enter to cleave the next target, {targets[i].name}.")
            else:
                input(
                    f"\n{self.step_parent.display_name} finished cleaving. Press enter to continue..."
                )

    def brutal_attack_reroll(self, roll):
        if roll == 1 or roll == 2:
            print("Brutal Reroll!")
            print(f"Old Roll: {roll}")
            new_damage = randint(
                1, self.step_parent.equipped_items["weapon"].damage_max_die
            )
            print(f"New Roll: {new_damage}")
            return new_damage
        else:
            return roll


class Barbarian(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "barbarian"
        self.hp_dice_max = 12


class Paladin(Job):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "paladin"
        self.step_parent.display_name = (
            f"{Fore.BLUE}{self.step_parent.name}{Style.RESET_ALL}"
        )
        self.primary_attribute = "intellect"
        self.secondary_attribute = "strength"
        self.hp_dice_max = 10

        self.starting_armor = ddi.Armor(
            name="chain mail",
            description="",
            proficiency_required="heavy",
            rarity="common",
            weight=55,
            armor_class=6,
            abilities=["stealth_disadvantage", "str_req_13", "no_agi"],
        )
        self.starting_weapon = ddi.Weapon(
            name="Long Sword",
            description="",
            proficiency_required="martial",
            rarity="common",
            weight=3,
            abilities=[],
            damage_max_die=8,
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

        self.attacks = [
            {
                "name": "Smite",
                "description": "Holy weapon attack that burns your foes with radiant energy. Weapon Damage + Strength + (Random Luck) + (1d8 per Int Modifier)",
                "source": self.name,
                "type": "active",
                "cooldown": 0,
            }
        ]
        self.abilities = [
            {
                "name": "Heal",
                "description": "Calling on the power of your deity, you heal a friendly target 1d8 plus your intelligence modifier per Paladin level you have.",
                "source": self.name,
                "type": "active",
                "cooldown": 3,
            }
        ]

        self.level_up = {
            2: {"new_abilities": [{}], "new_attacks": [{}]},
            3: {"new_abilities": [{}], "new_attacks": [{}]},
            4: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()} and +1 to {self.secondary_attribute.title()}  ",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            5: {
                "new_abilities": [
                    {
                        "name": "Extra Attack",
                        "description": f"{self.step_parent.display_name} gains an additional attack.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            6: {"new_abilities": [{}], "new_attacks": [{}]},
            7: {"new_abilities": [{}], "new_attacks": [{}]},
            8: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()} and +1 to {self.secondary_attribute.title()}  ",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            9: {"new_abilities": [{}], "new_attacks": [{}]},
            10: {"new_abilities": [{}], "new_attacks": [{}]},
            11: {
                "new_abilities": [
                    {
                        "name": "Extra Attack",
                        "description": f"{self.step_parent.display_name} gains an additional attack.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            12: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()} and +1 to {self.secondary_attribute.title()}  ",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            13: {"new_abilities": [{}], "new_attacks": [{}]},
            14: {"new_abilities": [{}], "new_attacks": [{}]},
            15: {"new_abilities": [{}], "new_attacks": [{}]},
            16: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()} and +1 to {self.secondary_attribute.title()}  ",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            17: {"new_abilities": [{}], "new_attacks": [{}]},
            18: {
                "new_abilities": [
                    {
                        "name": "Extra Attack",
                        "description": f"{self.step_parent.display_name} gains an additional attack.",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            19: {
                "new_abilities": [
                    {
                        "name": "Job Stat Increase",
                        "description": f"{self.step_parent.display_name} is becoming more adept at being a {self.name.title()}. You have gained +2 to {self.primary_attribute.title()} and +1 to {self.secondary_attribute.title()}  ",
                        "source": self.name,
                        "type": "passive",
                        "cooldown": 0,
                    }
                ],
                "new_attacks": [{}],
            },
            20: {"new_abilities": [{}], "new_attacks": [{}]},
        }

    def set_attribute_bonuses(self):
        if self.level == 4:
            self.attributes[self.primary_attribute] = 1
            self.attributes[self.secondary_attribute] = 2
        elif self.level == 8:
            self.attributes[self.primary_attribute] = 2
            self.attributes[self.secondary_attribute] = 4
        elif self.level == 12:
            self.attributes[self.primary_attribute] = 3
            self.attributes[self.secondary_attribute] = 6
        elif self.level == 16:
            self.attributes[self.primary_attribute] = 4
            self.attributes[self.secondary_attribute] = 8
        elif self.level == 19:
            self.attributes[self.primary_attribute] = 5
            self.attributes[self.secondary_attribute] = 10

    # target 1
    def smite(self, weapon, target):
        print(f"\n{self.step_parent.display_name} is smiting {target.name}.")
        damage_rolls = []
        base_roll: int = randint(1, 20)
        luck_roll: int = self.step_parent.luck_roll()
        attack_attribute_modifier: int = self.step_parent.attack_attribute_modifier()
        total_roll = (
            base_roll + attack_attribute_modifier["stat"] + self.proficiency + luck_roll
        )
        if total_roll >= target.armor_class:
            if base_roll >= (self.critical_hit_roll - self.critical_hit_roll_mod):
                crit = True
                print(
                    f"\n{Back.RED}{self.step_parent.display_name} critically smited {target.name}!{Style.RESET_ALL}"
                )
            else:
                crit = False
                print(
                    f"\nHit! {self.step_parent.display_name} smited {target.name} with holy fire!"
                )
            sleep(0.5)
            for _ in itertools.repeat(None, weapon.num_dice):
                damage_roll: int = randint(1, weapon.damage_max_die)
                smite_damage = []
                smite_num_rolls = self.step_parent.attributes["intellect"]["modifier"]
                for roll in range(smite_num_rolls):
                    smite_roll_damage = randint(1, 8)
                    smite_damage.append(smite_roll_damage)
                smite_damage = sum(smite_damage)
                damage_rolls.append(
                    damage_roll
                    + attack_attribute_modifier["stat"]
                    + self.step_parent.luck_roll()
                    + smite_damage
                )
            total_damage = sum(damage_rolls)
            if crit:
                total_damage = total_damage * 2
            target.take_damage(total_damage, self.step_parent)
        else:
            print(f"{self.step_parent.display_name} missed {target.name} with smite!")
        input(
            f"\n{self.step_parent.display_name} finished smiting. Press enter to continue..."
        )

    # friendly 1
    def heal(self, target):
        total_heal = 0

        for i in range(self.level):
            roll = randint(1, 8)
            int_mod = self.step_parent.attributes["intellect"]["modifier"]
            total_heal += sum([roll, int_mod])
        target.heal_damage(total_heal, self.step_parent, "Heal")
        input("Press Enter To Continue...")


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
