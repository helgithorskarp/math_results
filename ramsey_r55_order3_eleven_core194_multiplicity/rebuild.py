#!/usr/bin/env python3
"""Freshly rebuild the entire guarded Core194 base in an isolated namespace."""
from pathlib import Path
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'ramsey_r55_order3_eleven_core194_full'))
import run
import cube


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    prep=run.prepare(a.work);old=json.loads((cube.ROOT/'result.json').read_text())
    cube.require(prep==old['preparation'],'entire preceding preparation differs')
    rebuilt=run.make_case(a.work,cube.cases()[0])
    cube.require(all(old['cases'][0][k]==rebuilt[k] for k in rebuilt),'complete guarded base differs')
    run.atomic(a.work/'reconstruction.json',dict(matches_published_preparation=True,source_result=cube.info(cube.ROOT/'result.json'),preparation=prep,guarded=rebuilt))
    print('PASS entire guarded Core194 base rebuilt')
