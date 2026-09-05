#!/usr/bin/env python3
"""Reconstruct all25 inherited full bases in an isolated module namespace."""
from pathlib import Path
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'ramsey_r55_order3_eleven_empty_propagation'))
import run
import cube


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    prep=run.prepare(a.work);old=json.loads((cube.ROOT/'result.json').read_text())
    cube.require(prep==old['preparation'],'full inherited preparation differs')
    saved={c['index']:c for c in old['cases'] if c['status']=='open'};rows=[]
    for case in cube.cases():
        if case['index'] not in saved:continue
        rebuilt=run.make_case(a.work,case)
        cube.require(all(rebuilt[k]==saved[case['index']][k] for k in rebuilt),'changed inherited complete base')
        rows.append(dict(index=case['index'],**rebuilt))
    cube.require(len(rows)==25,'complete25 bases')
    run.atomic(a.work/'reconstruction.json',dict(matches_published_preparation=True,preparation_file=cube.info(a.work/'preparation.json'),source_result=cube.info(cube.ROOT/'result.json'),cores=rows))
    print('PASS complete parent and all25 inherited complete bases')


if __name__=='__main__':main()
