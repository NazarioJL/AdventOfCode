from __future__ import annotations

from hashlib import md5
from itertools import count
from typing import Generator


def get_hashes(door_id: str) -> Generator[str, None, None]:
    num = count()
    while True:
        salted = door_id + str(next(num))
        digest = md5(salted.encode()).hexdigest()
        if digest.startswith("00000"):
            yield digest


def parts_1_2() -> tuple[str, str]:
    # Part 1 produces a subset of what Part 2 needs
    positions = {*list(range(8))}
    part1_code: list[str] = []
    part2_code: list[tuple[int, str]] = []

    generator = get_hashes("uqwqemis")

    while positions:
        hash_ = next(generator)
        if len(part1_code) < 8:
            part1_code.append(hash_[5])

        pos = int(hash_[5], 16)

        if pos in positions:
            positions.remove(pos)
            part2_code.append((pos, hash_[6]))

    return "".join(part1_code), "".join(c for _, c in sorted(part2_code))


if __name__ == "__main__":
    part1, part2 = parts_1_2()
    print(f"Solution part 1: {part1}")
    print(f"Solution part 2: {part2}")
