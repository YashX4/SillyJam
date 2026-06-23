# type cell which contains an x and y coordinate in the grid and a color value:
from dataclasses import dataclass, field
from enum import IntEnum


class PipeSprite(IntEnum):
    """Which pipe frame to draw in a cell.

    Named by the directions a pipe connects to / can be entered from.
    Values line up with the frame order in assets/images/Pipes.png and are
    used as the index when we eventually render. 15 options total:
      - 6 two-way pieces (straights + corners)
      - 4 three-way pieces (T-junctions)
      - 1 four-way piece (cross)
      - 4 one-way pieces (dead-end caps)
    """

    # two-way: straights
    NORTH_SOUTH = 0
    EAST_WEST = 1
    # two-way: corners
    NORTH_EAST = 2
    NORTH_WEST = 3
    SOUTH_EAST = 4
    SOUTH_WEST = 5
    # three-way: T-junctions
    NORTH_SOUTH_EAST = 6
    NORTH_SOUTH_WEST = 7
    NORTH_EAST_WEST = 8
    SOUTH_EAST_WEST = 9
    # four-way: cross
    NORTH_SOUTH_EAST_WEST = 10
    # one-way: dead-end caps
    NORTH = 11
    SOUTH = 12
    EAST = 13
    WEST = 14

    def next(self) -> "PipeSprite":
        """Return the next sprite in the cycle, wrapping back to the start."""
        members = list(PipeSprite)
        return members[(self.value + 1) % len(members)]


@dataclass
class Cell:
    x: int
    y: int
    color: tuple[int, int, int]
    pipe_sprite: PipeSprite = PipeSprite.NORTH_SOUTH
