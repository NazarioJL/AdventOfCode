import operator
from collections import defaultdict
from collections.abc import Callable
from collections.abc import Iterable
from itertools import pairwise
from typing import DefaultDict
from typing import Literal
from typing import TypeAlias
from unittest.mock import ANY

import pytest

from support import get_input_data
from support import print_solution
from support import Solution
from support import time_solve

YEAR = 2022
DAY = 21


Operator = Literal["+", "-", "*", "/"]

OPERATOR_FUNC_MAP: dict[Operator, Callable[[int, int], int]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}

OPERATION_INVERSE_MAP: dict[Operator, Operator] = {
    "+": "-",
    "-": "+",
    "*": "/",
    "/": "*",
}

INVERSE_FUNC_MAP: dict[tuple[bool, Operator, bool], Callable[[int, int, int], int]] = {
    # Format of expression is: a OP b = c
    # We are solving for a or b depending on which is True
    (True, "+", False): lambda a, b, c: c - b,
    (False, "+", True): lambda a, b, c: c - a,
    (True, "*", False): lambda a, b, c: c // b,
    (False, "*", True): lambda a, b, c: c // a,
    (True, "-", False): lambda a, b, c: c + b,
    (False, "-", True): lambda a, b, c: a - c,
    (True, "/", False): lambda a, b, c: c * b,
    (False, "/", True): lambda a, b, c: a // c,
}

Expression: TypeAlias = int | tuple[str, Operator, str]
Children: TypeAlias = tuple[()] | tuple[str] | tuple[str, str]


def parse_input(s: str) -> Iterable[tuple[str, Expression]]:
    for line in s.splitlines():
        name, expression = line.split(":")
        exp_parts = expression.split()
        if len(exp_parts) == 1:
            yield name, int(exp_parts[0])
        else:
            yield name, tuple(exp_parts)


def calc(exp: Expression, lookup: dict[str, int]) -> int:
    if isinstance(exp, int):
        return exp
    else:
        lhs, op, rhs = exp
        return OPERATOR_FUNC_MAP[op](lookup[lhs], lookup[rhs])


@time_solve
def solve(s: str) -> Solution:
    exps = list(parse_input(s))
    # This makes various assumptions:
    #   1. All nodes have a single parent, except for root, which does not
    #   2. Any division operation does NOT result in fractions (both ways)
    #   3. All expressions := lhs <OP> rhs | <NUMBER>
    expressions: dict[str, Expression] = {}
    lookup: dict[str, int] = {}
    parent_map: dict[str, str] = {}
    children_map: DefaultDict[str, Children] = defaultdict(tuple)

    for key, exp in exps:
        expressions[key] = exp
        children_map[key] = ()
        if isinstance(exp, tuple):
            lhs, _, rhs = exp
            children_map[key] = (lhs, rhs)
            parent_map[lhs] = key
            parent_map[rhs] = key

    topo_sorted = []

    while children_map:
        childless = set()
        for parent, children in children_map.items():
            if len(children) == 0:
                childless.add(parent)

        for c in childless:
            topo_sorted.append(c)
            parent = parent_map.get(c)
            if parent:
                siblings = children_map[parent]
                if len(siblings) == 1:
                    children_map[parent] = ()
                elif len(siblings) == 2:
                    a, b = siblings
                    if a == c:
                        children_map[parent] = (b,)
                    else:
                        children_map[parent] = (a,)
                else:
                    # Should not get here ever
                    pass
            del children_map[c]

    for item in topo_sorted:
        lookup[item] = calc(expressions[item], lookup)

    node_to_solve = "humn"
    path_with_node_to_solve = [node_to_solve]

    while node_to_solve in parent_map:
        node_to_solve = parent_map[node_to_solve]
        path_with_node_to_solve.append(node_to_solve)

    path_with_node_to_solve.reverse()

    curr_value = 0

    for parent, child in pairwise(path_with_node_to_solve):
        lhs, op, rhs = expressions[parent]
        if parent == "root":
            curr_value = lookup[lhs] if rhs == child else lookup[rhs]
        else:
            curr_value = INVERSE_FUNC_MAP[(lhs == child, op, rhs == child)](
                lookup[lhs], lookup[rhs], curr_value
            )

    return lookup["root"], curr_value


TEST_INPUT = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, (152, 301)),),
)
def test_solve(input_s: str, expected: str):
    assert solve(input_s) == (*expected, ANY)


if __name__ == "__main__":
    print_solution(solve(get_input_data(YEAR, DAY)))
