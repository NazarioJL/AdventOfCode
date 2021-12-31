from __future__ import annotations

from functools import reduce
from typing import Generator
from typing import Iterable

import pytest
from more_itertools.more import windowed

from support import get_input_data


def is_abba(s: str) -> bool:
    if len(s) < 4:
        return False

    for i in range(2, len(s) - 1):
        # is abba iff for cabd -> a == b and c == d and a != b
        a, b = s[i - 1], s[i]  # interior pair
        if a == b:
            c, d = s[i - 2], s[i + 1]  # exterior pair
            if c == d and a != c:
                return True
    return False


def parse_ip(s: str) -> Generator[str, None, None]:
    buffer: list[str] = []
    for c in s:
        if c == "[" or c == "]":
            yield "".join(buffer)
            buffer.clear()
        buffer.append(c)
    yield "".join(buffer)


def does_supports_tls(s: str) -> bool:
    is_ip = True
    result = False
    for part in parse_ip(s):
        if is_ip:
            result |= is_abba(part)
        else:
            if is_abba(part):
                return False

        is_ip ^= True

    return result


def get_aba(s: str) -> Iterable[tuple[str, str, str]]:
    for a, b, c in windowed(s, 3):
        if a == c:
            yield a, b, c


def does_support_ssl(s: str) -> bool:
    is_ip = True
    supernet: set[tuple[str, str, str]] = set()
    hypernet: set[tuple[str, str, str]] = set()

    for part in parse_ip(s):
        if is_ip:
            for aba in get_aba(part):
                supernet.add(aba)
        else:
            for bab in get_aba(part):
                b, a, b = bab
                hypernet.add((a, b, a))
        is_ip ^= True

    return len(supernet.intersection(hypernet)) > 0


def solve(s: str) -> tuple[int, int]:
    return reduce(
        lambda acc, e: (acc[0] + does_supports_tls(e), acc[1] + does_support_ssl(e)),
        s.splitlines(),
        (0, 0),
    )


TEST_INPUT = """\
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("aaaa", False),
        ("abba", True),
        ("ioxxoj", True),
        ("abbaxsdsd", True),
        ("asdasdabba", True),
        ("asbaxsdsd", False),
        ("sds", False),
    ),
)
def test_is_abba(input_s: str, expected: str) -> None:
    assert is_abba(input_s) == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("abba[mnop]qrst", True),
        ("abcd[bddb]xyyx", False),
        ("aaaa[qwer]tyui", False),
        ("ioxxoj[asdfgh]zxcvbn", True),
    ),
)
def test_does_supports_tls(input_s: str, expected: str) -> None:
    assert does_supports_tls(input_s) == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("aba[bab]xyz", True),
        ("xyx[xyx]xyx", False),
        ("aaa[kek]eke", True),
        ("zazbz[bzb]cdb", True),
    ),
)
def test_does_supports_ssl(input_s: str, expected: str) -> None:
    assert does_support_ssl(input_s) == expected


if __name__ == "__main__":
    print(f"Solution Parts 1 and 2: {solve(get_input_data(2016, 7))}")
