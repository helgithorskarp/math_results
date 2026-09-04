#!/usr/bin/env python3
"""Build a SAT decision instance for a hitting set of size at most 89.

Variables z_v mean that an S vertex is *not* selected.  The 30 singleton
killing sets are selected necessarily and are eliminated.  A hitting set of
total size at most 89 would therefore leave at least 46 of the remaining 105
vertices unselected.  For every residual killing set D, the clause
``OR(-z_v for v in D)`` prohibits all of D from being unselected.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF

from verify_hitting_witness import DEFAULT_CERTIFICATE, minimal_family


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    args = parser.parse_args()

    certificate = json.loads(args.certificate.read_text())
    universe = list(map(int, certificate["S"]))
    family = minimal_family(certificate["killing_sets"])
    forced = {next(iter(item)) for item in family if len(item) == 1}
    assert len(forced) == 30
    remaining = [vertex for vertex in universe if vertex not in forced]
    variable = {vertex: index + 1 for index, vertex in enumerate(remaining)}
    residual = [item for item in family if not (item & forced)]
    assert len(remaining) == 105 and len(residual) == 2822

    cnf = CNF()
    for item in residual:
        cnf.append([-variable[vertex] for vertex in item])
    cardinality = CardEnc.atleast(
        lits=list(variable.values()),
        bound=46,
        top_id=len(variable),
        encoding=EncType.seqcounter,
    )
    cnf.extend(cardinality.clauses)
    assert cnf.nv == 2819 and len(cnf.clauses) == 8237
    cnf.to_file(args.output)
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(
        f"forced={len(forced)} remaining={len(remaining)} "
        f"residual_sets={len(residual)}"
    )
    print(f"variables={cnf.nv} clauses={len(cnf.clauses)} sha256={digest}")


if __name__ == "__main__":
    main()
