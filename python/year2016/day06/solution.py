from __future__ import annotations

from collections import Counter
from typing import Iterable

from support import get_input_data


def get_message(lines: list[str], indexes: Iterable[int]) -> Iterable[str]:
    counters: list[Counter[str]] = [Counter() for _ in range(len(lines[0]))]
    for line in lines:
        for counter, c in zip(counters, line):
            counter.update(c)

    for index in indexes:
        yield "".join(counter.most_common()[index][0] for counter in counters)


def part_1_2(s: str) -> tuple[str, ...]:
    return tuple(get_message(s.splitlines(), (0, -1)))


TEST_INPUT = """\
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
"""


def test_get_message():
    actual = get_message(TEST_INPUT.splitlines(), (0, -1))
    assert list(actual) == ["easter", "advent"]


if __name__ == "__main__":
    print(f"Solution Parts 1 and 2: {part_1_2(get_input_data(2016, 6))}")
