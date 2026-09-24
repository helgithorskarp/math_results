"""Compare native state counts with Python and, optionally, a sanitizer build."""
from itertools import combinations
from pathlib import Path
import argparse
import json
import subprocess

import native_star
import reference_star
from controls import check

ROOT=Path(__file__).resolve().parent
PAIRS=tuple(sum(1<<p for p in t) for t in combinations(range(13),2))

def instances():
    for case in json.loads((ROOT/'NATIVE_CASES.json').read_text()):
        high=[p for p,e in case['excess']];targets=[9]*13
        for p,e in case['excess']:targets[p]+=e
        h=high[0];q=high[1] if len(high)>1 else h
        highmask=sum(1<<p for p in high)
        bounds={t:(20 if not t&~highmask else 5) for t in PAIRS}
        yield (12,case['r'],20,h,q,case['fixed'],targets,bounds,'UNSAT')
    blocks=[sum(1<<(p-1) for p in b) for b in json.loads((ROOT/'UPPER21.json').read_text())['blocks']]
    targets=[sum(b>>p&1 for b in blocks) for p in range(13)]
    bounds={t:sum(b&t==t for b in blocks) for t in PAIRS}
    check(blocks,21,targets,bounds)
    removable=[b for b in blocks if not b&((1<<12)|(1<<8))]
    for n in range(1,8):
        fixed=[b for b in blocks if b not in removable[:n]]
        yield (12,8,21,11,1,fixed,targets,bounds,'SAT')
    bad=targets.copy();x=next(p for p in range(13) if removable[0]>>p&1);bad[x]-=1
    yield (12,8,21,11,1,[b for b in blocks if b!=removable[0]],bad,bounds,'UNSAT')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--sanitizer',type=Path)
    args=parser.parse_args();lines=[];expected=[];count=0;points=bundles=0
    py_spaces={};native_spaces={}
    for p,r,total,h,q,fixed,targets,bounds,status in instances():
        if (p,r) not in py_spaces:
            py_spaces[p,r]=reference_star.Space(p,r);native_spaces[p,r]=native_star.Space(p,r)
        reference=reference_star.solve(py_spaces[p,r],fixed,h,q,total_blocks=total,target_degrees=targets,pair_bounds=bounds)
        actual=native_star.solve(native_spaces[p,r],fixed,h,q,total_blocks=total,target_degrees=targets,pair_bounds=bounds)
        if actual!=reference or actual['status']!=status:raise ValueError(('native/reference mismatch',count,actual,reference))
        if status=='SAT':check(fixed+actual['witness'],total,targets,bounds)
        encoded=[p,r,total,h,q,len(fixed),*targets,*(bounds[t] for t in PAIRS),*fixed]
        lines.append(' '.join(map(str,encoded)))
        expected.append([int(status=='SAT'),actual['point_states'],actual['bundle_states'],*actual.get('witness',[])])
        count+=1;points+=actual['point_states'];bundles+=actual['bundle_states']
    if args.sanitizer:
        binary=str(args.sanitizer.resolve())
        process=subprocess.run([binary],input='\n'.join(lines)+'\n',text=True,capture_output=True)
        if process.returncode or process.stderr:raise ValueError(('sanitizer failure',process.returncode,process.stderr))
        output=[[int(x) for x in line.split()] for line in process.stdout.splitlines()]
        if output!=expected:raise ValueError('sanitizer/reference mismatch')
    print(json.dumps(dict(status='NATIVE_REFERENCE_AND_CONTROLS_MATCH',cases=count,
                          point_states=points,bundle_states=bundles,
                          sanitizer_checked=bool(args.sanitizer)),indent=2))

if __name__=='__main__':main()
