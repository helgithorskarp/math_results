#!/usr/bin/env python3
"""Rebuild the complete multiple-empty Core194 formula without old solver runs."""
from pathlib import Path
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'ramsey_r55_order3_eleven_core194_multiplicity'))
import run
import cube


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    prep=run.prepare(a.work);old=json.loads((cube.ROOT/'result.json').read_text())
    cube.require(prep==old['preparation'],'entire preceding preparation differs')
    case=next(c for c in cube.cases() if c['id']=='multiple');rebuilt=run.make_case(a.work,case)
    saved=next(c for c in old['cases'] if c['id']=='multiple')
    cube.require(all(saved[k]==rebuilt[k] for k in rebuilt),'complete multiple base differs')
    run.atomic(a.work/'reconstruction.json',dict(matches_published_preparation=True,source_result=cube.info(cube.ROOT/'result.json'),preparation=prep,multiple=rebuilt))
    print('PASS entire multiple-empty Core194 base rebuilt')
