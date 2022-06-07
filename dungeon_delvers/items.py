class Item():
    def __init__(self, *args, **kwargs):
        rarity_range = {
            'common': 0,
            'uncommon': 1,
            'rare': 2,
            'epic': 3,
            'legendary': 4,
            'artifact': 5
        }
        quality_range = {
            'dilapidated': -3,
            'damaged': -2,
            'subpar': -1,
            'normal': 0,
            'fine': 1,
            'superior': 2,
            'masterwork': 3
        }
        item_type = [
            'potion',
            'scroll',
            'art',
            'gem',
            'weapon',
            'armor',
            'shield',
            'trade good',
            'ring',
            'amulet',

        ]
        self.stats = {
            'name': kwargs['name'],
            'id': '',
            'description': kwargs['description'],
            'abilities': kwargs['abilities'],
            'value': {
                'platinum': kwargs['pp'],
                'gold': kwargs['gp'],
                'electrum': kwargs['ep'],
                'silver': kwargs['sp'],
                'copper': kwargs['cp']
            },
            'type': '',
            'is_magic': False,
            'rarity': rarity_range[kwargs['rarity']],
            'quality': quality_range[kwargs['quality']],
            'weight': kwargs['weight']

        }
        if self.stats['is_magic']:
            self.stats['magic_level'] = self.stats['rarity']


class Weapon(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats['type'] = 'weapon'
        self.stats['damage_min_dice'] = 1
        self.stats['damage_max_dice'] = kwargs['damage_max_dice']
        # Mithral, Adamantite, Silver, Gold
        self.stats['material'] = kwargs['material']

        if self.stats['material'] == 'mithril':
            self.stats['weight'] = self.stats['weight'] // 2
            self.stats['abilities'] = 'mithril_weapon'
        elif self.stats['material'] == 'adamantite':
            self.stats['abilities'] = 'adamantite_weapon'
        elif self.stats['material'] == 'silver':
            self.stats['abilities'] = 'silver_weapon'
        elif self.stats['material'] == 'gold':
            self.stats['abilities'] = 'gold_weapon'


class Armor(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats['type'] = 'armor'


class Ring(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats['type'] = 'ring'


class Amulet(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats['type'] = 'amulet'


class Potion(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats['type'] = 'potion'


class Scroll(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats['type'] = 'scroll'


class Art(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats['type'] = 'art'


class Gem(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats['type'] = 'gem'


class TradeGood(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats['type'] = 'trade_good'


class Shield(Armor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats['type'] = 'shield'


def generate_item():
    quality_range = [
        'dilapidated',
        'damaged',
        'subpar',
        'normal',
        'fine',
        'superior',
        'masterwork'
    ]
    rarity_range = [
        'common',
        'uncommon',
        'rare',
        'epic',
        'legendary',
        'artifact'
    ]
    item_type = [
        'potion',
        'scroll',
        'art',
        'gem',
        'weapon',
        'armor',
        'shield',
        'trade good',
        'ring',
        'amulet',
    ]
    dilapidated_weight = 2
    damaged_weight = 10
    subpair_weight = 20
    normal_weight_min = 21
    normal_weight_max = 79

