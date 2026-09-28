"""Independent literal check of the public two-defect seed and derived word."""
import hashlib
import sys
from pathlib import Path

N = 537
RAW_SHA256 = "ece0ce91784aca0199ffe24e36104c666c036a6c735181385fd2fabcc7627f25"


def read_upstream(path: Path) -> str:
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != RAW_SHA256:
        raise ValueError("upstream byte hash differs")
    classes = data.decode("ascii").splitlines()
    if len(classes) != 6:
        raise ValueError("expected six class lines")
    result = [""] * N
    for colour, line in enumerate(classes, 1):
        values = [int(token) for token in line.split()]
        if not values:
            raise ValueError("empty class")
        for v in values:
            if not (1 <= v <= N) or result[v - 1]:
                raise ValueError("overlap or out-of-range value")
            result[v - 1] = str(colour)
    if not all(result):
        raise ValueError("uncovered value")
    return "".join(result)


def load_word(path: Path) -> str:
    data = path.read_bytes()
    if len(data) != N + 1 or data[-1:] != b"\n" or set(data[:-1]) != set(b"123456"):
        raise ValueError(f"malformed word: {path}")
    return data[:-1].decode("ascii")


def defects(word: str) -> list[tuple[int, int, int, int]]:
    bad = []
    edge_count = 0
    for z in range(2, N + 1):
        for x in range(1, z // 2 + 1):
            y = z - x
            edge_count += 1
            if word[x - 1] == word[y - 1] == word[z - 1]:
                bad.append((x, y, z, int(word[z - 1])))
    if edge_count != 72092:
        raise ValueError("wrong edge enumeration")
    return bad


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: audit_words.py upstream.col external_two.txt best3.txt")
    upstream = read_upstream(Path(sys.argv[1]))
    seed = load_word(Path(sys.argv[2]))
    result = load_word(Path(sys.argv[3]))
    if upstream != seed:
        raise ValueError("normalization mismatch")
    seed_bad = defects(seed)
    result_bad = defects(result)
    if seed_bad != [(12, 12, 24, 4), (12, 24, 36, 4)]:
        raise ValueError(f"seed defects: {seed_bad}")
    if result_bad != [(5, 41, 46, 2), (5, 46, 51, 2), (46, 51, 97, 2)]:
        raise ValueError(f"result defects: {result_bad}")
    distance = sum(a != b for a, b in zip(seed, result))
    if distance != 433:
        raise ValueError(f"distance: {distance}")
    if any(result[v - 1] == result[2 * v - 1] for v in range(1, N // 2 + 1)):
        raise ValueError("doubling defect")
    print("PASS source_sha256_match=yes words=537 edges=72092 "
          "seed_defects=2 result_defects=3 doubling_defects=0 distance=433")


if __name__ == "__main__":
    main()
