from random import randint
from colorama import init, Fore, Style

init(autoreset=True)


class Item:
    def __init__(self, *args, **kwargs):
        rarity_range = {
            "common": 0,
            "uncommon": 1,
            "rare": 2,
            "epic": 3,
            "legendary": 4,
            "artifact": 5,
        }
        rarity_colors = {
            "common": "",
            "uncommon": Fore.GREEN,
            "rare": Fore.BLUE,
            "epic": Fore.MAGENTA,
            "legendary": Fore.YELLOW,
            "artifact": Fore.RED,
            "divine": Fore.CYAN,
        }
        item_type = [
            "potion",
            "scroll",
            "art",
            "gem",
            "weapon",
            "armor",
            "shield",
            "trade good",
            "ring",
            "amulet",
        ]

        # self.name = kwargs["name"]
        self.description = kwargs["description"]
        self.abilities = kwargs["abilities"]
        
        # self.value = kwargs["value"]
        self.type = ""
        self.rarity = kwargs["rarity"]
        self.name = rarity_colors[self.rarity] + kwargs["name"]
        self.display_name = rarity_colors[self.rarity] + kwargs["name"].title()
        # self.item_level = kwargs["item_level"]
        self.weight = kwargs["weight"]

        # Magic Section
        if self.rarity == "common":
            self.is_magic = False

        else:
            self.is_magic = True

        self.magic_level = rarity_range[self.rarity]
        self.attribute_increase = {}

        self.magic_prefixes = {

            "regenerating": {
                "prepended_name": "Regenerating",
                "attributes_to_modify": [
                    self.abilities.append(("regenerating_item", {self.magic_level}))
                ],
            },
        }

        def __repr__(self) -> None:
            return f"""{self.name}
                \r{self.description}"""

        def __str__(self) -> None:
            return f"""{self.name}
                \r{self.description}"""


class Equipment(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.magic_suffixes = {
            "of_the_gorilla": {
                "appended_name": "of the Gorilla",
                "attributes_to_modify": ["strength"],
                "amount": self.magic_level * 2,
            },
            "of_the_cheetah": {
                "appended_name": "of the Cheetah",
                "attributes_to_modify": [["agility"]],
                "amount": self.magic_level * 2,
            },
            "of_the_orangutan": {
                "appended_name": "of the Orangutan",
                "attributes_to_modify": [["intellect"]],
                "amount": self.magic_level * 2,
            },
            "of_the_rat": {
                "appended_name": "of the Rat",
                "attributes_to_modify": [["luck"]],
                "amount": self.magic_level * 2,
            },
            "of_the_elephant": {
                "appended_name": "of the Elephant",
                "attributes_to_modify": [
                    ["intellect"],
                    ["strength"],
                ],
                "amount": self.magic_level,
            },
            "of_the_dolphin": {
                "appended_name": "of the Dolphin",
                "attributes_to_modify": [
                    ["agility"],
                    ["intellect"],
                ],
                "amount": self.magic_level,
            },
            "of_the_lion": {
                "appended_name": "of the Lion",
                "attributes_to_modify": [
                    ["agility"],
                    ["strength"],
                ],
                "amount": self.magic_level,
            },
            "of_the_rabbit": {
                "appended_name": "of the Rabbit",
                "attributes_to_modify": [
                    ["agility"],
                    ["luck"],
                ],
                "amount": self.magic_level,
            },
            "of_the_ox": {
                "appended_name": "of the Ox",
                "attributes_to_modify": [
                    ["luck"],
                    ["strength"],
                ],
                "amount": self.magic_level,
            },
            "of_the_pig": {
                "appended_name": "of the Pig",
                "attributes_to_modify": [
                    ["intellect"],
                    ["luck"],
                ],
                "amount": self.magic_level,
            },
            "of_the_dragon": {
                "appended_name": "of the Pig",
                "attributes_to_modify": [
                    ["intellect"],
                    ["luck"],
                    ["strength"],
                    ["agility"],
                ],
                "amount": self.magic_level,
            },
        }


class Weapon(Equipment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "weapon"
        self.damage_min_die = 1
        self.damage_max_die = kwargs["damage_max_die"]
        
        self.proficiency_required = kwargs["proficiency_required"]
        
        if 'num_dice' in kwargs:
            self.num_dice = kwargs['num_dice']
        else:
            self.num_dice = 1

        self.magic_prefixes.update(
            {
                "frigid": {
                    "prepended_name": "Frigid",
                    "attributes_to_modify": [
                        self.abilities.append(("frigid_item", {self.magic_level}))
                    ],
                },
                "fiery": {
                    "prepended_name": "Fiery",
                    "attributes_to_modify": [
                        self.abilities.append(("fiery_item", {self.magic_level}))
                    ],
                },
                "shocking": {
                    "prepended_name": "Shocking",
                    "attributes_to_modify": [
                        self.abilities.append(("shocking_item", {self.magic_level}))
                    ],
                },
                "toxic": {
                    "prepended_name": "Toxic",
                    "attributes_to_modify": [
                        self.abilities.append(("toxic_item", {self.magic_level}))
                    ],
                },
                "holy": {
                    "prepended_name": "Holy",
                    "attributes_to_modify": [
                        self.abilities.append(("holy_item", {self.magic_level}))
                    ],
                },
                "unholy": {
                    "prepended_name": "Unholy",
                    "attributes_to_modify": [
                        self.abilities.append(("unholy_item", {self.magic_level}))
                    ],
                },
            }
        )

        # Mithral, Adamantite, Silver, Gold
        if "material" in kwargs:
            self.material = kwargs["material"]
        else:
            self.material = "steel"

        if self.material == "mithril":
            self.weight = self.weight // 2
            self.abilities.append("mithril_weapon")
        elif self.material == "adamantite":
            self.abilities.append("adamantite_weapon")
        elif self.material == "silver":
            self.abilities.append("silver_weapon")
        elif self.material == "gold":
            self.abilities.append("gold_weapon")


class Armor(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "armor"
        self.material = ""
        self.armor_class = kwargs['armor_class']
        self.magic_prefixes.update(
            {
                "shielding": {
                    "prepended_name": "Shielding",
                    "attributes_to_modify": [self.armor_class],
                    "amount": self.magic_level,
                }
            }
        )

        if self.material == "wood":
            self.abilities.append("wood_armor")
        elif self.material == "mithril":
            self.weight = self.weight // 2
            self.abilities.append("mithril_armor")
        elif self.material == "adamantite":
            self.abilities.append("adamantite_armor")
        elif self.material == "silver":
            self.abilities.append("silver_armor")
        elif self.material == "gold":
            self.abilities.append("gold_armor")


class Ring(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "ring"

        if self.is_magic:
            pass


class Amulet(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "amulet"


class Potion(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "potion"


class Scroll(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "scroll"


class Art(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "art"


class Gem(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "gem"


class TradeGood(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "trade_good"


class Shield(Armor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "shield"


def generate_item(cr):
    rarity_range = ["common", "uncommon", "rare", "epic", "legendary", "artifact"]
    item_type = [
        "potion",
        "scroll",
        "art",
        "gem",
        "weapon",
        "armor",
        "shield",
        "trade good",
        "ring",
        "amulet",
    ]

    return


def generate_loot_type(cr):
    cr_dict = {
        1: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
        ],
        2: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
        ],
        3: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
        ],
        4: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
        ],
        5: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"wonderous": cr},
        ],
        6: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
        ],
        7: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
        ],
        8: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
        ],
        9: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
        ],
        10: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        11: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        12: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        13: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        14: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        15: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        16: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        17: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        18: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        19: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        20: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        21: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        22: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        23: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        24: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        25: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        26: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        27: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        28: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        29: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
        30: [
            {"scroll": cr},
            {"art": cr},
            {"gem": cr},
            {"weapon": cr},
            {"armor": cr},
            {"shield": cr},
            {"trade_good": cr},
            {"ring": cr},
            {"amulet": cr},
            {"wonderous": cr},
        ],
    }


# spread = []
# for x in range(1, 100001):
#     item_rolled = generate_item(1)
#     spread.append(item_rolled)

# masterwork = spread.count('masterwork')
# superior = spread.count('superior')
# fine = spread.count('fine')
# normal = spread.count('normal')
# subpar = spread.count('subpar')
# damaged = spread.count('damaged')
# dilapidated = spread.count('dilapidated')
# total_items = sum([masterwork, superior, fine, normal, subpar, damaged, dilapidated])


# print(f"Dialpidated Count: {dilapidated} - {dilapidated/total_items:.2f}%")
# print(f"Damaged Count: {damaged} - {damaged/total_items:.2f}%")
# print(f"Subpar Count: {subpar} - {subpar/total_items:.2f}%")
# print(f"Normal Count: {normal} - {normal/total_items:.2f}%")
# print(f"Fine Count: {fine} - {fine/total_items:.2f}%")
# print(f"Superior Count: {superior} - {superior/total_items:.2f}%")
# print(f"Masterwork Count: {masterwork} - {masterwork/total_items:.2f}%")
# print(f"Total Items = {total_items}")


# print(f'{Fore.GREEN}Test Color{Style.RESET_ALL}')
# print(f'{Fore.BLACK}Test Color{Style.RESET_ALL}')
# print(f'{Fore.BLUE}Test Color{Style.RESET_ALL}')
# print(f'{Fore.CYAN}Test Color{Style.RESET_ALL}')
# print(f'{Fore.RED}Test Color{Style.RESET_ALL}')
# print(f'{Fore.MAGENTA}Test Color{Style.RESET_ALL}')
# print(f'{Fore.WHITE}Test Color{Style.RESET_ALL}')

if __name__ == '__main__':

    item = Item(
        name="Crystal Sword of the Elephant",
        description="",
        weight=4,
        abilities=[],
        rarity="artifact",
    )
    print(item.name)
    print(item.display_name)
