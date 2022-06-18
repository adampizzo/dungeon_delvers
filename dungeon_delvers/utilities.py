import os
# from dungeon_delvers import race
# from dungeon_delvers import job
from dungeon_delvers.race import Human, Dwarf, Elf, Gnome, Halfling, Halfelf, Halforc
from dungeon_delvers.job import Fighter, Rogue, Monk, Paladin
# from job import Fighter, Barbarian, Paladin, Rogue, Wizard, Monk
# from dungeon_delvers.base import Player


def get_selection(choices, e):
    while True:
        try:
            selection = input('\nSelection: ')
            selection = int(selection) - 1
            if not choices[selection]:
                raise ValueError(e)
        except ValueError:
            print(e)
        except IndexError:
            print(e)
        else:
            return choices[selection]


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def construct_class(klass, *args):
    constructor = globals()[klass]
    return constructor(*args)


def print_sep(seperator, length=80):
    """
        Prints a character an amount of times equal to length in one row.
        Default value of length is 80, for most regular terminal default widths.

        will check to make sure the separator is one character or will throw an
        error.
    """
    try:
        if len(seperator) != 1:
            raise ValueError(f'Error - {seperator} is not 1 character.')
    except ValueError as e:
        print(e)
    else:
        return(f'{seperator*length}')


if __name__ == "__main__":
    pass
