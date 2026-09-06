#!/usr/bin/env python3
"""Regenerate the optional fixed master proof instance without search."""
import argparse
import json
from pathlib import Path
import engine as E

ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
sep=json.loads((E.J.HERE/'separator.json').read_text())
rows=json.loads((E.HERE/'certificate.json').read_text())['rows']
n,cs=E.master(rows,sep['small']);args.out.write_bytes(E.J.dimacs(n,cs))
print(json.dumps({'variables':n,'clauses':len(cs),'solver_calls':0}))
