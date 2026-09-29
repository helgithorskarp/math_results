#!/usr/bin/env python3
"""Regenerate bounded DRAT proofs, then run the independent literal audit."""
import argparse
import json
import resource
import subprocess
from pathlib import Path

import audit
import encode


def proof_limit():
    resource.setrlimit(resource.RLIMIT_FSIZE, (128*1024*1024, 128*1024*1024))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=120)
    parser.add_argument("--ratios", nargs="+", type=int, choices=encode.RATIOS, default=encode.RATIOS)
    args = parser.parse_args()
    audit.require(args.seconds > 0, "positive per-stage time limit required")
    audit.require(len(set(args.ratios)) == len(args.ratios), "duplicate ratio")
    output = args.output.resolve()
    data = json.loads(Path(__file__).with_name("data.json").read_text())
    encode.write_formulas(output, args.ratios)
    # Check the semantics before spending time generating a certificate.
    audit.audit(data, cnf_dir=output, ratios=args.ratios)
    for ratio in args.ratios:
        with (output / f"ratio{ratio}.solver.log").open("wb") as log:
            proc = subprocess.run([str(args.cadical.resolve()), "-t", str(args.seconds),
                                   str(output / f"ratio{ratio}.cnf"),
                                   str(output / f"ratio{ratio}.drat")],
                                  stdout=log, stderr=subprocess.STDOUT,
                                  timeout=args.seconds+10, preexec_fn=proof_limit)
        lines = (output / f"ratio{ratio}.solver.log").read_text().splitlines()
        audit.require(proc.returncode == 20 and "s UNSATISFIABLE" in lines,
                      f"ratio {ratio}: solver did not finish UNSAT; no exclusion claimed")
    result = audit.audit(data, output, output, args.drat_trim.resolve(), args.ratios, args.seconds)
    (output / "audit.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
