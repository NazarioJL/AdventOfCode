import sys
import textwrap
from enum import Enum
from io import StringIO
from typing import IO, Callable
from typing import Iterable

from support import get_input_data

Ans = int | float | str


class Grid:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._pixels: set[tuple[int, int]] = set()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def pixels(self):
        return self._pixels

    def rect(self, width: int, height: int) -> None:
        for r in range(height):
            for c in range(width):
                self._pixels.add((r, c))

    def rotate_row(self, row: int, count: int) -> None:
        to_move = []
        for col in range(self.width):
            if (row, col) in self.pixels:
                self.pixels.remove((row, col))
                to_move.append((row, (col + count) % self.width))

        for move in to_move:
            self.pixels.add(move)

    def rotate_col(self, col: int, count: int) -> None:
        to_move = []
        for row in range(self.height):
            if (row, col) in self.pixels:
                self.pixels.remove((row, col))
                to_move.append(((row + count) % self.height, col))

        for move in to_move:
            self.pixels.add(move)

    def __eq__(self, other):
        if not isinstance(other, Grid):
            raise ValueError(
                f"Cannot compare this to obj of type: {type(other).__name__}"
            )
        return (self.pixels, self.width, self.height) == (
            other.pixels,
            other.width,
            other.height,
        )


def print_grid(grid: Grid, on: str = "#", off: str = " ", out: IO = sys.stdout):
    for r in range(grid.height):
        buffer = []
        for c in range(grid.width):
            if (r, c) in grid.pixels:
                buffer.append(on)
            else:
                buffer.append(off)

        out.write("".join(buffer))
        out.write("\n")


def text_to_grid(data: str) -> Grid:
    lines = data.splitlines()
    height = len(lines)
    width = len(lines[0])

    result = Grid(height=height, width=width)

    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == "#":
                result.pixels.add((row, col))

    return result


class OperationType(Enum):
    RECT = "rect"
    ROTATE_COLUMN = "rotate_column"
    ROTATE_ROW = "rotate_row"


Instruction = tuple[OperationType, int, int]  # all operations take 2 params


def parse_input(s: str) -> Iterable[Instruction]:
    for command in s.splitlines():
        match command.split():  # type: ignore
            case ["rect", *rest]:  # rect 1x3
                w, h = rest[0].split("x")
                yield OperationType.RECT, int(w), int(h)
            case ["rotate", "column", *rest]:  # rotate column x=0 by 1
                *_, x = rest[0].split("=")
                a = rest[-1]
                yield OperationType.ROTATE_COLUMN, int(x), int(a)
            case ["rotate", "row", *rest]:  # rotate row y=0 by 2
                *_, y = rest[0].split("=")
                a = rest[-1]
                yield OperationType.ROTATE_ROW, int(y), int(a)
            case _:
                raise ValueError(f"Unexpected command: {command}")


INSTRUCTION_MAP: dict[OperationType, Callable[[Grid, int, int], None]] = {
    OperationType.RECT: lambda g, w, h: g.rect(width=w, height=h),
    OperationType.ROTATE_COLUMN: lambda g, y, a: g.rotate_col(col=y, count=a),
    OperationType.ROTATE_ROW: lambda g, x, a: g.rotate_row(row=x, count=a),
}


def solve(s: str, width: int = 50, height: int = 6) -> tuple[Ans, Ans]:
    grid = Grid(width=width, height=height)
    for op, a, b in parse_input(s):
        INSTRUCTION_MAP[op](grid, a, b)

    buffer = StringIO()
    print_grid(grid, on="\u2588", off="\u0020", out=buffer)
    return len(grid.pixels), buffer.getvalue()


TEST_INPUT = """\
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""


def test_solve() -> None:
    result, _ = solve(TEST_INPUT, width=7, height=3)
    assert result == 6


def test_part1_execute() -> None:
    actual = Grid(7, 3)
    instructions = parse_input(TEST_INPUT)
    for op, a, b in instructions:
        INSTRUCTION_MAP[op](actual, a, b)

    expected = textwrap.dedent(
        """\
    .#..#.#
    #.#....
    .#.....
    """
    )

    expected_grid = text_to_grid(expected)

    assert actual == expected_grid


if __name__ == "__main__":
    part_1, part_2 = solve(get_input_data(2016, 8))
    print(f"Solution part1: {part_1}")
    print(f"Solution part2:\n{part_2}")
