# type cell which contains an x and y coordinate in the grid and a color value:
from dataclasses import dataclass, field
from enum import IntEnum


class PipeSprite(IntEnum):
    """Which pipe frame to draw in a cell.

    Named by the directions a pipe connects to / can be entered from.
    AIR is empty
    `frame_index` (i.e. value - 1, since AIR has no frame). 16 options total:
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
    def frame_index(self) -> int:
        """Index of this pipe's frame in Pipes.png. Invalid for AIR."""
        return self.value - 1


@dataclass
class Cell:
    x: int
    y: int
    color: tuple[int, int, int]
    pipe_sprite: PipeSprite = PipeSprite.AIR
