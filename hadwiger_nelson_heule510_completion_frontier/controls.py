#!/usr/bin/env python3
"""Bounded definition-level controls for the native filter and field lifting."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import subprocess
import audit
import census


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--filter',type=Path,required=True);ap.add_argument('--work',type=Path,required=True)
    args=ap.parse_args();args.work.mkdir(parents=True,exist_ok=True)
    O=[[0]*8 for _ in (0,1)]
    def point(x=0,y=0,ys=0):
        q=[r[:] for r in O];q[0][0]=x;q[1][0]=y;q[1][1]=ys;return q
    samples=[point(96),point(-48,ys=48),point(-48,ys=-48),point(),point(0,96),point(0,-96),point(96,96),point(144)]
    H,_,_,_,scaled=census.inputs()
    fixtures=[samples,[[r[:8],r[8:]] for r in scaled[:18]],[[r[:8],r[8:]] for r in scaled[::30]]]
    checks=[]
    for no,points in enumerate(fixtures):
        path=args.work/f'control{no}.txt';out=args.work/f'control{no}.tsv'
        path.write_text(f'{len(points)} 96\n'+''.join(' '.join(str(x) for axis in p for x in axis)+'\n' for p in points))
        r=subprocess.run([str(args.filter.resolve()),str(path),str(out)],capture_output=True,text=True,check=True);stats=json.loads(r.stdout)
        emitted={tuple(map(int,s.split())) for s in out.read_text().splitlines()}
        exact={t for t in combinations(range(len(points)),3) if audit.exact_unit_triple(*(points[v] for v in t),96)}
        census.require(exact==emitted,'complete small exact triple comparison')
        for triple in exact:
            Q=census.circumcentre(*(tuple(tuple(census.F(c,96) for c in axis) for axis in points[v]) for v in triple))
            census.require(Q is not None and all(census.dist(Q,tuple(tuple(census.F(c,96) for c in axis) for axis in points[v]))==census.ONE for v in triple),'exact lifting control')
        checks.append({'vertices':len(points),'triples':stats['triples'],'exact_unit_triples':len(exact)})
    basis=[tuple(int(i==j) for i in range(8)) for j in range(8)]
    for a in basis:
        for b in basis:census.require(census.mul(a,b)==audit.multiply(a,b),'field multiplication control')
    inverse_inputs=basis+[tuple(range(1,9)),(2,1,0,0,0,0,0,0)]
    for a in inverse_inputs:census.require(census.mul(a,census.inverse(a))==census.ONE,'tower inverse control')
    # Invalid input must terminate, rather than produce a partial certificate.
    bad=args.work/'bad.txt';bad.write_text('511 96\n')
    r=subprocess.run([str(args.filter.resolve()),str(bad),str(args.work/'bad.tsv')],capture_output=True,text=True)
    census.require(r.returncode!=0,'invalid header accepted')
    result={'status':'CONTROLS PASSED','fixtures':checks,'field_basis_products':64,'inverse_controls':len(inverse_inputs),'invalid_header_rejected':True}
    (args.work/'controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
