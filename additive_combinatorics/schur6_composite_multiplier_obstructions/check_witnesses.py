"""Definition-level witness checker; does not import the construction rules."""
import hashlib
import json
import math
from pathlib import Path


def check(row):
    n, k = row["modulus"], row["colours"]
    word, pi = row["word"], row["permutation"]
    if n < 2 or not 1 <= k <= 10 or math.gcd(row["multiplier"], n) != 1:
        raise ValueError("invalid modulus, palette or multiplier")
    if len(word) != n-1 or any(ch not in "0123456789" for ch in word):
        raise ValueError("malformed colour word")
    colours = [int(ch) for ch in word]
    if set(colours) != set(range(k)) or sorted(pi) != list(range(k)):
        raise ValueError("wrong palette")
    modular = integer = 0
    for x in range(1, n):
        if colours[x-1] != colours[n-x-1]:
            raise ValueError("reflection failure")
        if colours[row["multiplier"]*x % n-1] != pi[colours[x-1]]:
            raise ValueError("multiplier failure")
        for y in range(x, n):
            z = (x+y) % n
            if z:
                modular += 1
                if colours[x-1] == colours[y-1] == colours[z-1]:
                    raise ValueError(f"modular Schur triple {(x,y,z)}")
            if x+y < n:
                integer += 1
                if colours[x-1] == colours[y-1] == colours[x+y-1]:
                    raise ValueError(f"integer Schur triple {(x,y,x+y)}")
    return {"name":row["name"], "modulus":n, "colours":k,
            "modular_pairs":modular, "integer_triples":integer,
            "word_sha256":hashlib.sha256(word.encode("ascii")).hexdigest()}


if __name__ == "__main__":
    rows = json.loads(Path(__file__).with_name("witnesses.json").read_text())
    print(json.dumps([check(row) for row in rows], indent=2, sort_keys=True))
