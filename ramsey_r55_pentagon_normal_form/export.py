#!/usr/bin/env python3
"""Export a physically checked normalization as an edge list and free bits."""
import argparse
import itertools as it
import json
from pathlib import Path
import frame
import verify


def export(graph, certificate, edge_output, bit_output):
    n, edges = verify.read_graph(graph)
    cert = json.loads(Path(certificate).read_text())
    report = verify.verify(n, edges, cert)
    if report["status"] != "VERIFIED_PHYSICAL_FRAME":
        raise ValueError("only a frame certificate can be exported")
    order, flip = cert["order"], cert["flip"]
    moved = {e: int(tuple(sorted((order[e[0]], order[e[1]]))) in edges) ^ flip
             for e in it.combinations(range(n), 2)}
    red = [e for e in moved if moved[e]]
    Path(edge_output).write_text(f"{n} {len(red)}\n" + ''.join(f"{i} {j}\n" for i, j in red))
    variables = frame.variables(n)
    bits = ''.join(str(moved[e]) for e in variables)
    Path(bit_output).write_text(bits + "\n")
    return {"status": "EXPORTED_FRAME_CANDIDATE", "n": n,
            "free_bits": len(bits), "ramsey_status": "not_checked_by_export"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("graph", "certificate", "edge_output", "bit_output"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    print(json.dumps(export(args.graph, args.certificate, args.edge_output, args.bit_output), sort_keys=True))
