# type cell which contains an x and y coordinate in the grid and a color value:
from dataclasses import dataclass, field
from enum import Enum, IntEnum


class Direction(Enum):
    """A cardinal direction, with its (dx, dy) step in grid coordinates.

    y grows downward, so NORTH is dy=-1 (up) and SOUTH is dy=+1 (down).
    """

    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

    @property
    def dir_x(self) -> int:
        return self.value[0]

    @property
    def dir_y(self) -> int:
        return self.value[1]

    def opposite(self) -> "Direction":
        return Direction((-self.dir_x, -self.dir_y))


class PipeSprite(IntEnum):
    """Which pipe frame to draw in a cell.

    Named by the directions a pipe connects to / can be entered from.
    AIR is empty
      - 1 empty (AIR)
      - 6 two-way pieces (straights + corners)
      - 4 three-way pieces (T-junctions)
      - 1 four-way piece (cross)
      - 4 one-way pieces (dead-end caps)
    """

    AIR = 0
    # two-way: straights
    NORTH_SOUTH = 1
    EAST_WEST = 2
    # two-way: corners
    NORTH_EAST = 3
    NORTH_WEST = 4
    SOUTH_EAST = 5
    SOUTH_WEST = 6
    # three-way: T-junctions
    NORTH_SOUTH_EAST = 7
    NORTH_SOUTH_WEST = 8
    NORTH_EAST_WEST = 9
    SOUTH_EAST_WEST = 10
    # four-way: cross
    NORTH_SOUTH_EAST_WEST = 11
    # one-way: dead-end caps
    NORTH = 12
    SOUTH = 13
    EAST = 14
    WEST = 15

    def next(self) -> "PipeSprite":
        """Return the next sprite in the cycle, wrapping back to the start."""
        members = list(PipeSprite)
        return members[(self.value + 1) % len(members)]

    def openings(self) -> frozenset[Direction]:
        """The directions this pipe connects to, derived from its name.

        e.g. NORTH_WEST -> {NORTH, WEST}; AIR -> {} (no openings).
        """
        if self is PipeSprite.AIR:
            return frozenset()
        directions = (Direction[token] for token in self.name.split("_"))
        return frozenset(directions)    

@dataclass
class Cell:
    x: int
    y: int
    pipe: PipeSprite = PipeSprite.AIR
