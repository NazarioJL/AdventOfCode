from __future__ import annotations

import re
from collections import Counter
from typing import Hashable
from typing import NamedTuple

from support import get_input_data

regex = re.compile(r"(?P<name>(([a-z]+)\-)+)(?P<sector_id>\d+)\[(?P<checksum>[a-z]+)\]")


def invert_counter(c: Counter[Hashable]) -> dict[int, set[Hashable]]:
    result: dict[int, set[Hashable]] = {}
    for key, count in c.items():
        if count not in result:
            result[count] = set()
        result[count].add(key)

    return result


class Room(NamedTuple):
    name: str
    sector_id: int
    checksum: str


def parse_room(s: str) -> Room:
    match = regex.search(s)
    assert match
    return Room(
        name=match.group("name"),
        sector_id=int(match.group("sector_id")),
        checksum=match.group("checksum"),
    )


def is_room_decoy(room: Room) -> bool:
    freq = Counter(room.name.replace("-", ""))
    ordered_chars = list(
        char for cnt, char in sorted((-cnt, char) for char, cnt in freq.items())
    )
    return any(a != b for a, b in zip(room.checksum, ordered_chars))


def decrypt(name: str, sector_id: int) -> str:
    base = ord("a")
    decrypted = []
    for c in name:
        val = ord(c) - base
        val += sector_id
        val %= 26
        val += base
        decrypted.append(chr(val))

    return "".join(decrypted)


INPUT_S = """\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
"""


def part1(s: str) -> str | int:
    return sum(
        r.sector_id
        for line in s.splitlines()
        if not is_room_decoy(r := parse_room(line))
    )


def part2(s: str) -> str | int:
    room_with_objects = [
        r
        for line in s.splitlines()
        if decrypt((r := parse_room(line)).name, r.sector_id).find("object") > 0
    ]

    return room_with_objects[0].sector_id


def test_part1():
    assert part1(INPUT_S) == 1514


def test_decrypt():
    assert decrypt("qzmtzixmtkozyivhz", 343) == "veryencryptedname"


if __name__ == "__main__":
    print(part1(get_input_data(2016, 4)))
    print(part2(get_input_data(2016, 4)))
