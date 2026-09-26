"""Independent graph/matching checks and an optional Boolean cover audit.

Run after verify.py has created its output directory. The optional solver
audit is validation, not a premise of the exhaustive classification.
"""
import argparse
from collections import deque
import json
from pathlib import Path
import random
import subprocess
import time

HERE=Path(__file__).resolve().parent
POINTS=[(y,z) for y in range(5) for z in range(5)]


def graph(small,a,b):
    rows=[0]*25
    for i,(y,z) in enumerate(POINTS):
        for j,(u,v) in enumerate(POINTS):
            # Interpolation from the points at x=2 and x=3.
            c=5*((3*(y+u))%5)+(3*(z+v))%5
            first=5*((2*y-u)%5)+(2*z-v)%5
            last=5*((2*u-y)%5)+(2*v-z)%5
            if small>>c&1 and a>>first&1 and b>>last&1:
                rows[i]|=1<<j
    return rows


def maximum_matching(rows):
    left=[-1]*25;right=[-1]*25
    for start in range(25):
        previous={start:None};via={};queue=deque([start]);end=None
        while queue and end is None:
            i=queue.popleft()
            for j in range(25):
                if not rows[i]>>j&1 or j in via:
                    continue
                via[j]=i
                if right[j]<0:
                    end=j;break
                if right[j] not in previous:
                    previous[right[j]]=j;queue.append(right[j])
        if end is not None:
            j=end
            while j is not None:
                i=via[j];old=left[i];left[i]=j;right[j]=i;j=old if old>=0 else None
    return sum(j>=0 for j in left)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--domain',type=Path,required=True)
    ap.add_argument('--solver-audit',action='store_true')
    args=ap.parse_args();out=args.domain.resolve();binary=out/'section_matching'
    menu=list(map(int,(out/'planar16.txt').read_text().splitlines()))
    caps=json.loads((HERE/'CAPS.json').read_text())['classes']
    centers=[m for m in menu if all(sum(POINTS[i][j] for i in range(25) if m>>i&1)%5==0 for j in range(2))]
    rng=random.Random(202609260703)
    triples=[(rng.choice(caps)['mask'],rng.choice(centers),rng.choice(menu)) for _ in range(2000)]
    models=json.loads((HERE/'models.json').read_text())
    triples += [(m['sections'][0],m['sections'][1],m['sections'][4]) for m in models]
    inputs=out/'validation_triples.txt'
    inputs.write_text(''.join(' '.join(map(str,t))+'\n' for t in triples))
    raw=subprocess.check_output([str(binary),'audit',str(inputs)],text=True)
    results=[json.loads(line) for line in raw.splitlines()]
    if len(results)!=len(triples):raise ValueError('audit coverage')
    for r,(small,a,b) in zip(results,triples):
        rows=graph(small,a,b);edges=r['matching'];n=r['matching_size_capped19']
        if rows!=r['rows'] or n!=min(19,maximum_matching(rows)):
            raise ValueError('independent graph or matching disagreement')
        if len(edges)!=n or len({i for i,j in edges})!=n or len({j for i,j in edges})!=n:
            raise ValueError('matching repeats endpoint')
        if any(not rows[i]>>j&1 for i,j in edges):raise ValueError('matching uses absent edge')
    summary={'status':'MATCHING_REFERENCE_AUDIT_PASSED','cases':len(triples),
             'seed':202609260703,'solver_audit':None}
    if args.solver_audit:
        from pysat.solvers import Minicard
        counts={'balanced':0,'unbalanced':0,'lower_matching_skipped':0};began=time.monotonic()
        for case in (0,18):
            scan=out/f'validation_case{case}.jsonl'
            subprocess.run([str(binary),'scan',str(out/'planar16.txt'),str(out/'caps6.txt'),
                            str(case),'0','1135',str(scan)],check=True,stdout=subprocess.DEVNULL)
            rows=[json.loads(line) for line in scan.read_text().splitlines()]
            inputs.write_text(''.join(f"{r['small']} {r['a']} {r['b']}\n" for r in rows))
            flags=[json.loads(line) for line in subprocess.check_output(
                [str(binary),'audit-balanced',str(inputs)],text=True).splitlines()]
            if len(rows)!=len(flags):raise ValueError('balanced audit coverage')
            for r,flag in zip(rows,flags):
                if flag[:3]!=[r['small'],r['a'],r['b']]:raise ValueError('balanced audit alignment')
                if flag[3]!=18:
                    counts['lower_matching_skipped']+=1;continue
                edges=[[i+1,j+26] for i in range(25) for j in range(25) if r['rows'][i]>>j&1]
                with Minicard(bootstrap_with=edges) as solver:
                    solver.add_atmost(list(range(1,26)),9);solver.add_atmost(list(range(26,51)),9)
                    answer=solver.solve()
                    if answer!=bool(flag[4]):raise ValueError('Boolean cover disagreement')
                    if answer:
                        truth={v for v in solver.get_model() if v>0}
                        if len(truth&set(range(1,26)))>9 or len(truth&set(range(26,51)))>9 or not all(set(e)&truth for e in edges):
                            raise ValueError('invalid cover witness')
                    counts['balanced' if answer else 'unbalanced']+=1
        summary['solver_audit']=counts
        summary['solver_audit_seconds']=time.monotonic()-began
    (out/'REFERENCE_AUDIT.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


if __name__=='__main__':
    main()
