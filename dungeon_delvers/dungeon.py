class Dungeon:
    def __init__(self) -> None:
        self.x_size = 0
        self.y_size = 0
        self.dungeon_size = self.x_size * self.y_size
        self.starting_room = (0, 0)
        self.ending_room = (0, 0)


class Room:
    def __init__(self, *args, **kwargs) -> None:
        self.num_doors = kwargs["num_doors"]
