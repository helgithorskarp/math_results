"""Independent parent, palette, and full CNF multiset audit."""

import argparse
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
FILENAMES = ("parent_a.txt", "parent_b.txt", "parent_c.txt", "parent_d.txt")
# Each tuple gives the old parent's label for new labels 1,...,6.
MAPS = ((1, 6, 5, 2, 3, 4), (1, 3, 2, 6, 5, 4), (5, 2, 1, 4, 6, 3))


def defects(word: str) -> tuple[list[tuple[int, int, int]], list[int]]:
    bad = []
    for z in range(2, 538):
        for x in range(1, z//2 + 1):
            y = z-x
            if word[x-1] != "0" and word[x-1] == word[y-1] == word[z-1]:
                bad.append((x, y, z))
    return bad, [i for i, digit in enumerate(word, 1) if digit == "0"]


def make_palettes() -> list[tuple[int, ...]]:
    words = [(ROOT / name).read_text(encoding="ascii").strip() for name in FILENAMES]
    for word in words:
        if len(word) != 537 or set(word) - set("0123456"):
            raise ValueError("invalid parent word")
    summaries = [defects(word) for word in words]
    expected = (
        ([(3, 3, 6), (3, 6, 9)], []),
        ([(2, 281, 283), (4, 146, 150), (4, 260, 264), (4, 391, 395)], []),
        ([], [161]),
        ([(1, 1, 2), (1, 2, 3)], []),
    )
    if tuple((sorted(bad), holes) for bad, holes in summaries) != tuple(
            (sorted(bad), holes) for bad, holes in expected):
        raise ValueError("parent defects or hole differ from advertised values")
    translated = [words[0]]
    for word, alignment in zip(words[1:], MAPS):
        if sorted(alignment) != list(range(1, 7)):
            raise ValueError("invalid alignment")
        lookup = {str(old): str(new) for new, old in enumerate(alignment, 1)}
        lookup["0"] = "0"
        translated.append("".join(lookup[digit] for digit in word))
    palettes = [()]
    for i in range(537):
        palette = tuple(c for c in range(1, 7) if any(word[i] == str(c)
                                                    for word in translated))
        if not palette:
            raise ValueError("empty palette")
        palettes.append(palette)
    sizes = Counter(map(len, palettes[1:]))
    if sizes != {1: 10, 2: 97, 3: 320, 4: 110}:
        raise ValueError(f"unexpected palette sizes: {sizes}")
    if [i for i in range(1, 538) if len(palettes[i]) == 1] != [
            104, 284, 296, 304, 343, 361, 408, 428, 512, 516]:
        raise ValueError("unexpected singleton positions")
    return palettes


def expected_clauses(palettes: list[tuple[int, ...]]) -> tuple[int, Counter]:
    number = {}
    for i in range(1, 538):
        for colour in palettes[i]:
            number[i, colour] = len(number) + 1
    clauses = Counter()
    for i in range(1, 538):
        clauses[tuple(number[i, c] for c in palettes[i])] += 1
        for left in range(len(palettes[i])):
            for right in range(left+1, len(palettes[i])):
                clauses[tuple(sorted((-number[i,palettes[i][left]],
                                      -number[i,palettes[i][right]])))] += 1
    # Endpoint-first traversal differs from the encoder's x-first order.
    for z in range(2, 538):
        for x in range(1, z//2 + 1):
            y = z-x
            for c in range(1, 7):
                if all(c in palettes[v] for v in (x, y, z)):
                    clauses[tuple(sorted({-number[x,c], -number[y,c],
                                          -number[z,c]}))] += 1
    return len(number), clauses


def audit(path: Path) -> None:
    palettes = make_palettes()
    variables, expected = expected_clauses(palettes)
    observed = Counter()
    with path.open(encoding="ascii") as source:
        header = source.readline().split()
        if header != ["p", "cnf", str(variables), str(sum(expected.values()))]:
            raise ValueError(f"header mismatch: {header}")
        for line in source:
            row = tuple(map(int, line.split()))
            if not row or row[-1] != 0 or 0 in row[:-1]:
                raise ValueError("malformed DIMACS clause")
            observed[tuple(sorted(row[:-1]))] += 1
    if observed != expected:
        missing = expected - observed
        extra = observed - expected
        raise ValueError(f"clause multiset differs: missing={len(missing)}, extra={len(extra)}")
    print(f"PASS parents=4 n=537 variables={variables} clauses={sum(expected.values())} "
          "palettes=10,97,320,110 doubling_included=yes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    audit(parser.parse_args().cnf)
