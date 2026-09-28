"""Replay a finite deduction from 15 fixed colours to a Schur contradiction.

No SAT solver or source colouring is needed. Run with Python 3.8 or later.
Each trace row is: target forbidden_colour x y z, with x+y=z.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
N, COLOURS = 537, set(range(1, 7))


def rows(name, width):
    result = []
    for line in (HERE / name).read_text(encoding="ascii").splitlines():
        numbers = tuple(map(int, line.split()))
        assert len(numbers) == width, (name, line)
        result.append(numbers)
    return result


def main():
    anchors = rows("anchors.txt", 2)
    trace = rows("trace.txt", 5)
    assert len(anchors) == 15 and len(trace) == 16

    possible = [set(COLOURS) for _ in range(N + 1)]
    seen = set()
    for position, colour in anchors:
        assert 1 <= position <= N and colour in COLOURS
        assert position not in seen
        seen.add(position)
        possible[position] = {colour}

    assert all(possible[position] for position in range(1, N + 1))
    for index, (target, colour, x, y, z) in enumerate(trace, 1):
        assert 1 <= x <= y and x + y == z <= N
        assert 1 <= target <= N and colour in COLOURS
        involved = {x, y, z}
        assert target in involved
        premises = involved - {target}
        assert premises and all(possible[position] == {colour} for position in premises), (
            index, premises, colour
        )
        assert colour in possible[target], (index, target, colour)
        possible[target].remove(colour)
        if not possible[target]:
            assert index == len(trace) and target == 5 and colour == 2
            print("PASS anchors=15 deductions=16 contradiction_at=5 final_triple=5+41=46")
            return
    raise AssertionError("Certificate did not produce a contradiction")


if __name__ == "__main__":
    main()
