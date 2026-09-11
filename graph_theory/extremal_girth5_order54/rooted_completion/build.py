"""Regenerate the complete 15-formula cover in a new external directory."""

import argparse, hashlib, json, time
from pathlib import Path
from model import target, root_defect_bound


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    expected = json.loads(
        Path(__file__).with_name("formulas_expected.json").read_text()
    )
    records = []
    start = time.perf_counter()
    for z in (9, 10, 11):
        for a in range(root_defect_bound(z) + 1):
            for c in range((5 - a) // 2 + 1):
                cnf, data = target(z, a, c)
                path = args.output / f"z{z}_a{a}_c{c}.cnf"
                cnf.to_file(str(path))
                r = dict(
                    z=z,
                    a=a,
                    c=c,
                    counts={str(d): n for d, n in data["counts"].items()},
                    branch_sizes=data["sizes"],
                    outside=a,
                    edge_variables=len(data["E"]),
                    variables=cnf.nv,
                    clauses=len(cnf.clauses),
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                )
                if r != expected[len(records)]:
                    raise ValueError("Formula differs from archived cover")
                records.append(r)
                (args.output / "manifest.json").write_text(
                    json.dumps(records, indent=2) + "\n"
                )
                print(f"verified z={z}, a={a}, c={c}", flush=True)
    print(
        json.dumps(
            dict(verified_formulas=len(records), seconds=time.perf_counter() - start)
        )
    )


if __name__ == "__main__":
    main()
