"""Direct classical Schur-triple check of a public two-defect seed and its derivative."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 537


def load(name: str) -> list[int]:
    word = (HERE / name).read_text(encoding="ascii").strip()
    assert len(word) == N and set(word) == set("123456")
    return [0] + [int(d) for d in word]


def defects(c: list[int]) -> list[tuple[int, int, int, int]]:
    return [(x, y, x + y, c[x])
            for x in range(1, N + 1)
            for y in range(x, N + 1 - x)
            if c[x] == c[y] == c[x + y]]


def main() -> None:
    seed, result = load("external_two.txt"), load("best3.txt")
    seed_bad = defects(seed)
    result_bad = defects(result)
    assert seed_bad == [(12, 12, 24, 4), (12, 24, 36, 4)], seed_bad
    assert result_bad == [(5, 41, 46, 2), (5, 46, 51, 2),
                          (46, 51, 97, 2)], result_bad
    distance = sum(seed[v] != result[v] for v in range(1, N + 1))
    assert distance == 433, distance
    assert all(result[v] != result[2 * v] for v in range(1, 269))
    assert sum(x == y for x, y, _, _ in result_bad) == 0
    print("PASS triples=72092 seed_defects=2 result_defects=3 "
          "doubling_defects=0 distance_from_seed=433")


if __name__ == "__main__":
    main()
