"""Build the exact classical Schur CNF for four aligned parent palettes."""

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).parent
FILES = ("parent_a.txt", "parent_b.txt", "parent_c.txt", "parent_d.txt")
# Entry j of each tuple is the parent colour representing base colour j+1.
ALIGNMENTS = ((1, 6, 5, 2, 3, 4), (1, 3, 2, 6, 5, 4), (5, 2, 1, 4, 6, 3))


def domains() -> list[list[int]]:
    words = [(ROOT / name).read_text(encoding="ascii").strip() for name in FILES]
    if any(len(word) != 537 or set(word) - set("0123456") for word in words):
        raise ValueError("parent words must each have 537 entries over 0..6")
    aligned = [words[0]]
    for word, permutation in zip(words[1:], ALIGNMENTS):
        if sorted(permutation) != list(range(1, 7)):
            raise ValueError("alignment is not a permutation")
        inverse = {str(parent): str(base) for base, parent in enumerate(permutation, 1)}
        inverse["0"] = "0"
        aligned.append("".join(inverse[digit] for digit in word))
    result = [[]]
    for i in range(537):
        palette = sorted({int(word[i]) for word in aligned if word[i] != "0"})
        if not palette:
            raise ValueError(f"all parents have a hole at position {i+1}")
        result.append(palette)
    return result


def emit(output: Path) -> None:
    palette = domains()
    variable = {}
    for i in range(1, 538):
        for colour in palette[i]:
            variable[i, colour] = len(variable) + 1
    clauses = []
    for i in range(1, 538):
        choices = [variable[i, colour] for colour in palette[i]]
        clauses.append(choices)
        for colour in palette[i]:
            for earlier in palette[i]:
                if earlier < colour:
                    clauses.append([-variable[i, colour], -variable[i, earlier]])
    for x in range(1, 538):
        for y in range(x, 538-x):
            for colour in sorted(set(palette[x]) & set(palette[y]) & set(palette[x+y])):
                # x=y collapses the duplicated literal, retaining doubling.
                clauses.append(sorted({-variable[x, colour], -variable[y, colour],
                                       -variable[x+y, colour]}))
    with output.open("w", encoding="ascii") as stream:
        stream.write(f"p cnf {len(variable)} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"CNF variables={len(variable)} clauses={len(clauses)} sha256={digest}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    emit(parser.parse_args().output)
