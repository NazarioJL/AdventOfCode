from collections import deque
from enum import auto
from enum import Enum
from functools import reduce
from typing import Any
from typing import Iterable
from typing import NamedTuple
from typing import Protocol

import pytest
from mypy_extensions import Arg

from support import get_input_data

Ans = int | str
Solution = tuple[Ans, Ans]

Chip = int
Id = int


class SupportsLessThan(Protocol):
    def __lt__(self, __other: Any) -> bool:
        ...


def nonemin(*args: Arg(SupportsLessThan | None)) -> SupportsLessThan:
    filtered = [arg for arg in args if arg is not None]
    if not filtered:
        raise ValueError("All values cannot be None")

    return min(filtered)


def nonemax(*args: Arg(SupportsLessThan | None)) -> SupportsLessThan:
    filtered = [arg for arg in args if arg is not None]
    if not filtered:
        raise ValueError("All values cannot be None")

    return max(filtered)


class ControlRoomError(Exception):
    pass


class Recipient(Protocol):
    def accept(self, chip: Chip) -> None:
        ...


class Provider(Protocol):
    def give(self, recipient: Recipient, chip: Chip) -> None:
        ...


class HasId(Protocol):
    @property
    def id(self) -> Id:
        ...

    def __hash__(self):
        return self.id


class RecipientType(Enum):
    Output = "output"
    Bot = "bot"


class ChipType(Enum):
    High = "high"
    Low = "low"


class InstructionType(Enum):
    Give = auto()
    Assign = auto()


class AssignInstruction(NamedTuple):
    recipient_type: RecipientType
    recipient_id: Id
    chip: Chip
    instruction_type: InstructionType = InstructionType.Assign


class GiveDirective(NamedTuple):
    recipient_id: Id
    recipient_type: RecipientType


class GiveInstruction(NamedTuple):
    giver_id: Id
    high: GiveDirective
    low: GiveDirective
    instruction_type: InstructionType = InstructionType.Give


TInstruction = AssignInstruction | GiveInstruction


class ActionType(Enum):
    Compare = auto()
    Give = auto()


class Action(NamedTuple):
    sender: Id
    action_type: ActionType
    args: tuple[int | None, int | None] | tuple[...]


class ControlRoom:
    def __init__(self, comparison_of_interest: tuple[Chip, Chip]):
        self._bots: dict[Id, Bot] = {}
        self._outputs: dict[Id, Output] = {}
        self._comparison_of_interest = comparison_of_interest
        self._action_of_interest: Action | None = None

    def process(self, instructions: Iterable[TInstruction]) -> None:
        for instruction in instructions:
            match instruction.instruction_type:
                case InstructionType.Assign:
                    self.assign_internal(instruction)
                case InstructionType.Give:
                    bot_id = instruction.giver_id
                    if bot_id not in self._bots:
                        self._bots[bot_id] = Bot(id_=bot_id, ctrl_room=self)
                    self._bots[bot_id].add_command(instruction)
                case _:
                    raise ValueError(f"Unexpected instruction: {instruction}")

    def notify(self, action: Action) -> None:
        if action.action_type == ActionType.Compare:
            a, b = self._comparison_of_interest
            if action.args == (a, b) or action.args == (b, a):
                self._action_of_interest = action

    def assign_internal(self, instruction: AssignInstruction) -> None:
        r_id = instruction.recipient_id
        r_type = instruction.recipient_type
        chip = instruction.chip

        t: Recipient
        d: dict[Id, Recipient]
        if r_type == RecipientType.Bot:
            t = Bot
            args = dict(id_=r_id, ctrl_room=self)
            d = self._bots
        elif r_type == RecipientType.Output:
            t = Output
            args = dict(id_=r_id)
            d = self._outputs
        else:
            raise ValueError(f"Cannot recognize type: {r_type}")

        if r_id not in d:
            d[r_id] = t(**args)
        d[r_id].accept(chip)

    @property
    def action_of_interest(self) -> Action | None:
        return self._action_of_interest

    @property
    def outputs(self) -> dict[Id, "Output"]:
        return self._outputs


class Bot(Recipient, HasId):
    def __init__(self, id_: Id, ctrl_room: ControlRoom):
        self._id = id_
        self._low_chip: Chip | None = None
        self._high_chip: Chip | None = None
        self._queue = deque()
        self._ctrl_room = ctrl_room

    def accept(self, chip: Chip) -> None:
        if self._low_chip is not None and self._high_chip is not None:
            raise ControlRoomError("Bot cannot accept more chips")

        if self._low_chip is None and self._high_chip is None:
            self._low_chip = chip
        else:
            min_ = nonemin(self._low_chip, self._high_chip, chip)
            max_ = nonemax(self._low_chip, self._high_chip, chip)
            self._low_chip = min_
            self._high_chip = max_
            if self._queue:
                self._execute_command()

    def add_command(self, command: GiveInstruction) -> None:
        self._queue.appendleft(command)
        if self._low_chip and self._high_chip:
            self._execute_command()

    def _execute_command(self) -> None:
        if not self._queue:
            raise ControlRoomError(f"No commands to execute for: {self}")
        command: GiveInstruction = self._queue.pop()
        action = Action(
            action_type=ActionType.Compare,
            sender=self.id,
            args=(self._low_chip, self._high_chip),
        )
        self._ctrl_room.notify(action)
        low = AssignInstruction(
            recipient_type=command.low.recipient_type,
            recipient_id=command.low.recipient_id,
            chip=self._low_chip,
        )
        high = AssignInstruction(
            recipient_type=command.high.recipient_type,
            recipient_id=command.high.recipient_id,
            chip=self._high_chip,
        )
        self._low_chip = None
        self._high_chip = None
        self._ctrl_room.assign_internal(low)
        self._ctrl_room.assign_internal(high)

    def __str__(self) -> str:
        empty = "Empty"
        return (
            f"Bot(id={self.id}, low={self._low_chip or empty}, "
            f"high={self._high_chip or empty}, cmd_count={len(self._queue)})"
        )

    @property
    def id(self) -> Id:
        return self._id


class Output(Recipient, HasId):
    def __init__(self, id_: Id):
        self._id = id_
        self._chips: set[Chip] = set()

    def accept(self, chip: Chip) -> None:
        if chip in self._chips:
            raise ValueError(f"Chip: {chip} already exists")
        self._chips.add(chip)

    @property
    def id(self) -> Id:
        return self._id

    @property
    def chips(self) -> set[Chip]:
        return self._chips


def parse_input(s: str) -> Iterable[AssignInstruction | GiveInstruction]:
    for command in s.splitlines():
        match command.split():
            case ["value", chip, *_, bot_id]:  # rect 1x3
                yield AssignInstruction(
                    recipient_type=RecipientType.Bot,
                    chip=int(chip),
                    recipient_id=int(bot_id),
                )

            case [
                "bot",
                bot_id,
                "gives",
                "low",
                "to",
                low_rt,
                low_id,
                "and",
                "high",
                "to",
                high_rt,
                high_id,
            ]:
                low = GiveDirective(
                    recipient_type=RecipientType(low_rt), recipient_id=int(low_id)
                )
                high = GiveDirective(
                    recipient_type=RecipientType(high_rt), recipient_id=int(high_id)
                )
                yield GiveInstruction(giver_id=int(bot_id), low=low, high=high)
            case _:
                raise ValueError(f"Unexpected command: {command}")


def solve(s: str, comparison: tuple[int, int] = (61, 17)) -> Solution:
    instructions = parse_input(s)
    control = ControlRoom(comparison_of_interest=comparison)
    control.process(instructions)

    if not control.action_of_interest:
        raise ValueError("Not found")

    m = reduce(
        lambda acc, e: acc * e, [control.outputs[i].chips.pop() for i in (0, 1, 2)]
    )

    return control.action_of_interest.sender, m


TEST_INPUT = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, (2, 30)),),
)
def test_solve(input_s: str, expected: Solution) -> None:
    solve(input_s, (2, 5))


if __name__ == "__main__":
    part_1, part_2 = solve(get_input_data(2016, 10))
    print(f"Solution part1: {part_1}")
    print(f"Solution part2: {part_2}")
