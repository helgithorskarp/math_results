"""Independent bit-mask replay of the 81-entry S(6) prefix certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


SOURCE = Path(__file__).resolve().parent.parent / "schur_s6_prefix81_obstruction"
BASELINE_HASH = "2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d"
PROOF_HASH = "0fddc52d3193648237e26bf0353331f70a86bb7c5e141c3f800b18aaeee84324"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def audit() -> None:
    baseline_data = (SOURCE / "baseline.txt").read_bytes()
    proof_data = (SOURCE / "prefix81_proof.json").read_bytes()
    require(hashlib.sha256(baseline_data).hexdigest() == BASELINE_HASH,
            "baseline hash mismatch")
    require(hashlib.sha256(proof_data).hexdigest() == PROOF_HASH,
            "proof hash mismatch")

    word = baseline_data.decode("ascii").strip()
    require(len(word) == 536 and set(word) == set("123456"),
            "invalid baseline length or alphabet")
    classes = {colour: {i for i, digit in enumerate(word, 1)
                        if digit == str(colour)} for colour in range(1, 7)}
    for colour, values in classes.items():
        sums = {a + b for a in values for b in values if a + b <= 536}
        require(not values & sums, f"baseline colour {colour} is not sum-free")

    certificate = json.loads(proof_data)
    require(certificate["format"] == "schur-domain-deletion-v1", "wrong format")
    require((certificate["N"], certificate["colours"], certificate["prefix"])
            == (537, 6, 81), "wrong theorem parameters")
    require(certificate["baseline_sha256"] == BASELINE_HASH,
            "proof refers to a different baseline")
    steps = certificate["steps"]
    require(isinstance(steps, list) and len(steps) == 351,
            "wrong number of deduction steps")

    full_mask = (1 << 6) - 1
    domain = [0] + [full_mask] * 537
    for index in range(1, 82):
        domain[index] = 1 << (int(word[index - 1]) - 1)
    doubling = 0
    for number, step in enumerate(steps, 1):
        require(isinstance(step, list) and len(step) == 4
                and all(type(v) is int for v in step),
                f"malformed step {number}")
        target, colour, x, y = step
        z = x + y
        require(1 <= x <= y and z <= 537 and target in {x, y, z},
                f"invalid Schur triple at step {number}")
        require(1 <= colour <= 6, f"invalid colour at step {number}")
        bit = 1 << (colour - 1)
        require(domain[target] & bit != 0,
                f"absent colour removed at step {number}")
        for vertex in {x, y, z} - {target}:
            require(domain[vertex] == bit,
                    f"unforced premise at step {number}")
        domain[target] &= ~bit
        doubling += x == y
        require(domain[target] != 0 or (number == len(steps) and target == 537),
                f"early or misplaced contradiction at step {number}")

    require(domain[537] == 0 and doubling == 23,
            "wrong final contradiction or doubling count")
    require(all(domain[i] for i in range(1, 537)),
            "another variable was contradicted")
    print("PASS independent_prefix81 baseline=536 certificate_steps=351 "
          "doubling_steps=23 contradiction_at=537")
    print(f"baseline_sha256={BASELINE_HASH}")
    print(f"proof_sha256={PROOF_HASH}")


if __name__ == "__main__":
    audit()
