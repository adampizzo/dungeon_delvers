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
        self.stats = {
            'name': kwargs['name'],
            'id': '',
            'description': kwargs['description'],
            'abilities': kwargs['abilities'],
            'cost': {
                'platinum': kwargs['pp'],
                'gold': kwargs['gp'],
                'electrum': kwargs['ep'],
                'silver': kwargs['sp'],
                'copper': kwargs['cp']
            },
            'type': '',
            'is_magic': False,
            'rarity': kwargs['rarity'],
            'quality': kwargs['quality'],
            'weight': kwargs['weight']
            
        }
        if self.stats['is_magic']:
            self.stats['magic_level'] = self.stats['rarity']

class Weapon(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats['damage_min_dice'] = 1
        self.stats['damage_max_dice'] = kwargs['damage_max_dice']
        self.stats['material'] = kwargs['material']  # Mithral, Adamantite, Silver, Gold
        
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
    pass


class Ring(Item):
    pass


class Amulet(Item):
    pass