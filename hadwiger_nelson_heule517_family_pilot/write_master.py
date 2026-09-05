#!/usr/bin/env python3
"""Regenerate the final necessary master; this does not run a solver."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import engine

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--out',type=Path,required=True)
args=ap.parse_args()
rows=json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())['rows']
variables,clauses=engine.master(rows)
raw=engine.dimacs(variables,clauses)
args.out.write_bytes(raw)
print(json.dumps({'variables':variables,'clauses':len(clauses),'sha256':sha256(raw).hexdigest()}))
