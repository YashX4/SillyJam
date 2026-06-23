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
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]

    @property
    def opposite(self) -> "Direction":
        return Direction((-self.dx, -self.dy))

    @classmethod
    def from_delta(cls, dx: int, dy: int) -> "Direction | None":
        """The direction matching this step, or None if it isn't one cell
        orthogonally (diagonals, zero, or jumps > 1 all return None)."""
        try:
            return cls((dx, dy))
        except ValueError:
            return None


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

    @property
    def openings(self) -> frozenset[Direction]:
        """The directions this pipe connects to, derived from its name.

        e.g. NORTH_WEST -> {NORTH, WEST}; AIR -> {} (no openings).
        """
        if self is PipeSprite.AIR:
            return frozenset()
        return frozenset(Direction[token] for token in self.name.split("_"))


@dataclass
class Cell:
    x: int
    y: int
    color: tuple[int, int, int]
    pipe_sprite: PipeSprite = PipeSprite.AIR
