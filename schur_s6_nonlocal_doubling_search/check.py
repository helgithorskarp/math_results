"""Definition-level check of a bounded nonlocal search checkpoint."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_BEST = [(2, 281, 283), (4, 146, 150),
                 (4, 260, 264), (4, 391, 395)]


def read_word(name: str) -> str:
    word = (HERE / name).read_text(encoding="ascii").strip()
    if len(word) != 537 or set(word) != set("123456"):
        raise ValueError(f"{name} is not a 537-entry six-colour word")
    return word


def violations(word: str) -> tuple[int, list[tuple[int, int, int]]]:
    colour = [0] + [int(d) for d in word]
    count = 0
    bad = []
    for x in range(1, 538):
        for y in range(x, 538 - x):  # x=y is included
            count += 1
            if colour[x] == colour[y] == colour[x + y]:
                bad.append((x, y, x + y))
    return count, bad


def main() -> None:
    source = read_word("seed_359.txt")
    candidate = read_word("best4.txt")
    source_count, source_bad = violations(source)
    candidate_count, candidate_bad = violations(candidate)
    if source_count != candidate_count or source_count != 72092:
        raise ValueError("incomplete Schur-triple enumeration")
    if source_bad != [(2, 2, 4)]:
        raise ValueError(f"unexpected source defects: {source_bad}")
    if candidate_bad != EXPECTED_BEST:
        raise ValueError(f"unexpected candidate defects: {candidate_bad}")
    distance = sum(a != b for a, b in zip(source, candidate))
    if distance != 80:
        raise ValueError(f"unexpected distance: {distance}")
    print(f"PASS triples={source_count} seed_defects=1 "
          f"candidate_defects={len(candidate_bad)} doubling_defects=0 "
          f"distance_from_seed={distance}")


if __name__ == "__main__":
    main()
