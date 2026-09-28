#!/usr/bin/env python3
"""Check the prefix obstruction directly from x+y=z; standard library only."""
import argparse
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_baseline(path):
    data = path.read_bytes()
    word = data.decode("ascii").strip()
    require(len(word) == 536 and set(word) <= set("123456"),
            "baseline must contain exactly 536 colour digits")
    colours = [0] + [int(x) for x in word]
    checked = 0
    for z in range(2, 537):
        for x in range(1, z // 2 + 1):
            y = z - x
            require(not (colours[x] == colours[y] == colours[z]),
                    f"monochromatic baseline triple {(x, y, z)}")
            checked += 1
    return colours, hashlib.sha256(data).hexdigest(), checked


def replay(n, k, seeds, steps):
    """Return the contradicted integer; trust no generator or solver."""
    domains = {x: set(range(1, k + 1)) for x in range(1, n + 1)}
    for x, colour in seeds.items():
        require(1 <= x <= n and 1 <= colour <= k, "invalid seed")
        domains[x] = {colour}
    require(isinstance(steps, list) and steps, "missing deduction steps")
    contradiction = None
    doubling_steps = 0
    for index, step in enumerate(steps):
        require(contradiction is None, "steps continue after contradiction")
        require(isinstance(step, list) and len(step) == 4 and
                all(type(v) is int for v in step), "malformed deduction")
        target, colour, x, y = step
        require(1 <= x <= y and x + y <= n, "invalid Schur triple")
        vertices = {x, y, x + y}
        require(target in vertices and 1 <= colour <= k, "invalid target")
        premises = vertices - {target}
        require(premises and all(domains[v] == {colour} for v in premises),
                f"unproved premises at step {index}")
        require(colour in domains[target], "deleting an absent colour")
        domains[target].remove(colour)
        doubling_steps += x == y
        if not domains[target]:
            contradiction = target
    require(contradiction is not None, "deductions did not give a contradiction")
    return contradiction, doubling_steps


def check(baseline_path, certificate_path):
    colours, digest, checked = read_baseline(baseline_path)
    proof = json.loads(certificate_path.read_text())
    require(proof.get("format") == "schur-domain-deletion-v1", "unknown format")
    require(proof.get("N") == 537 and proof.get("colours") == 6 and
            proof.get("prefix") == 81, "wrong theorem parameters")
    require(proof.get("baseline_sha256") == digest, "baseline hash mismatch")
    seeds = {x: colours[x] for x in range(1, 82)}
    contradiction, doubles = replay(537, 6, seeds, proof["steps"])
    require(contradiction == 537, "unexpected contradiction location")
    return {
        "baseline_N": 536,
        "baseline_sha256": digest,
        "baseline_triples_checked": checked,
        "claim": "No six-colouring of [1,537] agrees with the baseline on [1,81]",
        "contradiction_at": contradiction,
        "deletion_steps": len(proof["steps"]),
        "doubling_steps": doubles,
        "verified": True,
    }


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=here / "baseline.txt")
    parser.add_argument("--certificate", type=Path,
                        default=here / "prefix81_proof.json")
    args = parser.parse_args()
    print(json.dumps(check(args.baseline, args.certificate), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
