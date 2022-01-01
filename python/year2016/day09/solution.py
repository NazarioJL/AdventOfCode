from typing import cast

import pytest

from support import get_input_data

Ans = int | str
Solution = tuple[Ans, Ans]


def decompress_v1(s: str) -> int:
    it = iter(s)
    num_1 = ""
    num_2 = ""
    length = 0

    try:
        while True:
            c = next(it)
            if c == "(":
                while (c := next(it)) != "x":
                    num_1 += c

                while (c := next(it)) != ")":
                    num_2 += c

                c_count, rep = int(num_1), int(num_2)
                for _ in range(c_count):
                    next(it)
                length += c_count * rep
                num_1, num_2 = "", ""
            else:
                length += 1
    except StopIteration:
        pass

    return length


def decompress_v2(s: str) -> int:
    def decompress_rec(start: int, end: int) -> int:
        idx = start
        length = 0
        num_1 = ""
        num_2 = ""

        while idx < end:
            c = s[idx]
            if c == "(":
                idx += 1
                while (c := s[idx]) != "x":
                    num_1 += c
                    idx += 1

                idx += 1

                while (c := s[idx]) != ")":
                    num_2 += c
                    idx += 1

                idx += 1

                c_count, rep = int(num_1), int(num_2)
                length += decompress_rec(idx, idx + c_count) * rep
                idx = idx + c_count
                num_1 = ""
                num_2 = ""
            else:
                length += 1
                idx += 1

        return length

    return decompress_rec(0, len(s))


def solve(s: str) -> tuple[Ans, Ans]:
    lines = s.splitlines()
    fs = decompress_v1, decompress_v2

    return cast(Solution, tuple(list(sum(f(line) for line in lines) for f in fs)))


TEST_INPUT = """\
ADVENT
A(1x5)BC
(3x3)XYZ
A(2x2)BCD(2x2)EFG
(6x1)(1x3)A
X(8x2)(3x3)ABCY
"""

TEST_INPUT_2 = """\
(3x3)XYZ
X(8x2)(3x3)ABCY
(27x12)(20x12)(13x14)(7x10)(1x12)A
(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (TEST_INPUT, (57, 56)),
        (TEST_INPUT_2, (589, 242394)),
    ),
)
def test_solve(input_s: str, expected: Solution) -> None:
    result = solve(input_s)
    assert result == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("(3x3)XYZ", 9),
        ("X(8x2)(3x3)ABCY", 20),
        ("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920),
        ("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", 445),
    ),
)
def test_decompress(input_s: str, expected: int) -> None:
    assert decompress_v2(input_s) == expected


if __name__ == "__main__":
    part_1, part_2 = solve(get_input_data(2016, 9))
    print(f"Solution part1: {part_1}")
    print(f"Solution part2:{part_2}")
