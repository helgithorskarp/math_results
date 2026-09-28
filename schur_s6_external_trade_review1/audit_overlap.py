"""Independent identity check for the earlier and later near-537 inputs."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EARLIER = ROOT / "schur_s6_three_colour_trades"
LATER = ROOT / "schur_s6_external_class_trade"


def defects(word):
    found = []
    for z in range(2, 538):
        for x in range(1, z // 2 + 1):
            y = z - x
            if word[x - 1] == word[y - 1] == word[z - 1]:
                found.append((x, y, z, int(word[z - 1])))
    return found


def main():
    fixture_bytes = (EARLIER / "fixtures.json").read_bytes()
    certificate_bytes = (EARLIER / "class_splitting.json").read_bytes()
    if hashlib.sha256(fixture_bytes).hexdigest() != (
            "be1de027a09a08e6d78785a6af6ee126f7bc3f49bfa59f6061359566406d1a5a"):
        raise ValueError("earlier fixture changed")
    if hashlib.sha256(certificate_bytes).hexdigest() != (
            "027b1c25df0ed2c21cbf25f653a8abb6e13bbc8dc2e0dfb868bc6da7a4812a81"):
        raise ValueError("earlier certificate changed")
    word = json.loads(fixture_bytes)["near537"]["colours"]
    later = (LATER / "seed537.txt").read_bytes()
    if later != (word + "\n").encode("ascii"):
        raise ValueError("complete near537 words differ")
    if len(word) != 537 or set(word) != set("123456"):
        raise ValueError("invalid normalized word")
    if defects(word) != [(12, 12, 24, 4), (12, 24, 36, 4)]:
        raise ValueError("unexpected seed defects")
    print("PASS earlier_near537_equals_later_seed=yes entries=537 "
          "defects=2 prior_certificate_hash=yes")


if __name__ == "__main__":
    main()
