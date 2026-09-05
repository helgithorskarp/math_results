#!/usr/bin/env python3
"""Isolated import context: rebuild the inherited full strengthened core194."""
from pathlib import Path
import argparse
import json
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'ramsey_r55_order3_eleven_anchor_propagation'))
import run
import cube


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    prep=run.prepare(a.work)
    old=json.loads((cube.ROOT/'result.json').read_text())
    saved=next(c for c in old['cases'] if c['index']==194)
    case=next(c for c in cube.cases() if c['index']==194)
    rebuilt=run.make_case(a.work,case)
    cube.require(all(rebuilt[k]==saved[k] for k in rebuilt),'inherited complete core194 formula differs')
    run.atomic(a.work/'reconstruction.json',dict(preparation=prep,case=case,rebuilt=rebuilt))
    print('PASS independently audited parent and inherited strengthened core194',flush=True)


if __name__=='__main__':main()
