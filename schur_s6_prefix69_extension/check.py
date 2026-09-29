"""Directly check the saved 338-word, including doubling x=x."""

from pathlib import Path

root = Path(__file__).parent
prefix = (root / "prefix69.txt").read_text(encoding="ascii").strip()
word = (root / "witness338.txt").read_text(encoding="ascii").strip()
assert len(prefix) == 69 and set(prefix) == set("123456")
assert len(word) == 338 and set(word) == set("123456")
assert word.startswith(prefix)
triples = 0
for x in range(1, len(word) + 1):
    for y in range(x, len(word) - x + 1):
        triples += 1
        assert not (word[x-1] == word[y-1] == word[x+y-1]), (x, y, x+y)
assert triples == len(word) ** 2 // 4
print(f"PASS n={len(word)} prefix={len(prefix)} triples={triples} defects=0")
