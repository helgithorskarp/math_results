#!/usr/bin/env python3
"""Regenerate the fixed public exhaustion instance without rediscovery."""
import argparse
import json
from pathlib import Path
import engine as E

ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
args.out.mkdir(exist_ok=False)
_,sep=E.geometry();n,cs=E.cnf(sep['large'],sep['large_edges'])
(args.out/'base.cnf').write_bytes(E.dimacs(n,cs))
raw=(E.HERE/'certificate.json').read_bytes();rows=json.loads(raw)['rows']
for row in rows:cs+=E.blocking(row['pattern'],sep['large'],sep['boundary'])
(args.out/'exhaustion.cnf').write_bytes(E.dimacs(n,cs))
(args.out/'certificate.json').write_bytes(raw)
print(json.dumps({'variables':n,'clauses':len(cs),'patterns':len(rows),'native_queries':0}))
