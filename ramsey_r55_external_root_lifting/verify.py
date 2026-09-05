#!/usr/bin/env python3
"""Solver-free exact certification of all degree-20 triple signature patterns."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import permutations
from math import comb
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import model,literal_model,controls

HERE=Path(__file__).resolve().parent
DENSITY=HERE.parent/'ramsey_r55_rooted15_density_bound'
DENSITY_MANIFEST='7be303890c0053fd1252a6d4d5787d69f7ffd16aee0dfcad91d59c583d6c6ac0'
require=literal_model.require


def check_primal(z,rows):
    require(type(z) is list and len(z)==len(rows[0][0]) and all(type(v) is int for v in z),'primal format')
    require(all(sum(a*v for a,v in zip(row,z))<=b for row,b in rows),'exact primal inequality')


def check_dual(cert,rows):
    require(set(cert)=={'multipliers','rhs'},'dual schema')
    pairs=cert['multipliers']
    require(type(pairs) is list and all(type(p) is list and len(p)==2 for p in pairs),'dual pair format')
    require(pairs==sorted(pairs) and len({i for i,v in pairs})==len(pairs),'dual unique order')
    require(all(type(i) is int and 0<=i<len(rows) and type(v) is int and v>0 for i,v in pairs),'dual index/domain')
    require(all(sum(v*rows[i][0][j] for i,v in pairs)==0 for j in range(len(rows[0][0]))),'dual zero vector')
    rhs=sum(v*rows[i][1] for i,v in pairs)
    require(type(cert['rhs']) is int and rhs==cert['rhs'] and rhs<0,'strict integer Farkas contradiction')


def replay_density():
    require(sha256((DENSITY/'SHA256SUMS').read_bytes()).hexdigest()==DENSITY_MANIFEST,'density manifest pin')
    for line in (DENSITY/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split()
        require(sha256((DENSITY/name).read_bytes()).hexdigest()==digest,'density source/input pin: '+name)
    with tempfile.TemporaryDirectory(prefix='r55-root-lifting-') as work:
        target=Path(work)/'report.json'
        r=subprocess.run([sys.executable,str(DENSITY/'verify.py'),'--report',str(target)],
                         check=True,capture_output=True,text=True)
        require(r.stdout==(DENSITY/'EXPECTED_OUTPUT.txt').read_text(),'density replay stdout')
        require(target.read_bytes()==(DENSITY/'report.json').read_bytes(),'density replay report')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--report',type=Path)
    ap.add_argument('--certificate',type=Path,default=HERE/'CERTIFICATE.json')
    ap.add_argument('--skip-density-replay',action='store_true',help='Check new certificates conditional on imported density lemma')
    args=ap.parse_args()
    if not args.skip_density_replay:replay_density()
    require(3*20+40*21==2*450 and 450==231+219,'profile edge count and M')
    require(comb(22,2)-450+21*20==comb(21,2)-450+21*21==201,'two local identity constants')
    require(100-7==93 and 114-7==107 and 107-7==100,'explicit hard-branch local caps')
    require({x for x in range(8) if 201-x.bit_count()<=200}==set(range(1,8)),
            'nonempty central signature condition')
    universe=set()
    for mask in range(8):
        independent=literal_model.vectors(mask)
        if independent:
            require(independent==set(model.vectors(mask)),'entry-level independent vector coordinates')
            universe|={(mask,y) for y in independent}
    require(len(universe)==731 and {m for m,y in universe}=={3,5,6,7},'complete labeled universe')
    records=json.loads(args.certificate.read_text());seen=set();counts=Counter();orbit_counts=Counter()
    matrices=0;transports=0;separations=0;examples={};hist=Counter()
    for record in records:
        mask=record['mask'];y=tuple(record['y']);key=(mask,y)
        require(type(mask) is int and len(y)==8 and all(type(v) is int and v>=0 for v in y),'profile record format')
        orb=model.orbit(mask,y)
        require(min(orb)==key and orb<=universe and not seen&orb,'unique complete labeling orbit')
        require(type(record['orbit_size']) is int and record['orbit_size']==len(orb),'orbit size')
        seen|=orb;failed=record['first_failed_stage']
        require(failed is None or type(failed) is int and 0<=failed<=2,'failure stage')
        systems=[]
        for stage in range(3):
            pairs,rows=literal_model.system(mask,y,stage)
            require(rows==model.system(mask,y,stage),'independent literal 43-vertex row expansion')
            systems.append(rows);matrices+=1
            # Verify equivariance of the ENTIRE consolidated inequality set.
            for perm in permutations(range(3)):
                image_mask=model.core_image(mask,perm);image_y=model.move(y,perm)
                image_pairs=model.model(image_mask,image_y,stage>=1,stage>=2)[0]
                lookup={p:i for i,p in enumerate(image_pairs)}
                def moved(x):return sum(1<<perm[i] for i in range(3) if x>>i&1)
                pmap=[lookup[tuple(sorted((moved(a),moved(b))))] for a,b in pairs]
                moved_rows=[]
                for row,b in rows:
                    out=[0]*len(row)
                    for i,j in enumerate(pmap):out[j]=row[i]
                    moved_rows.append((tuple(out),b))
                require(sorted(moved_rows)==model.system(image_mask,image_y,stage),'full row-set relabeling')
                transports+=1
        last=2 if failed is None else failed-1
        expected={'mask','y','orbit_size','first_failed_stage'}
        if failed is not None:
            expected.add('dual');check_dual(record['dual'],systems[failed]);examples.setdefault('dual',(record['dual'],systems[failed]))
        if last>=0:
            expected.add('primal')
            for stage in range(last+1):check_primal(record['primal'],systems[stage])
            examples.setdefault('primal',(record['primal'],systems[last]))
            if failed is not None:
                try:check_primal(record['primal'],systems[failed])
                except ValueError:separations+=1
                else:raise ValueError('claimed strict strengthening lacks separation')
        require(set(record)==expected,'certificate schema')
        code=3 if failed is None else failed
        counts[mask,code]+=len(orb);orbit_counts[mask,code]+=1
        if failed is None:hist[mask,y[7]]+=len(orb)
    require(seen==universe and len(records)==141,'complete exact certificate coverage')
    z,rows=examples['primal'];bad=z.copy();bad[0]+=1
    negative=0
    for action in (lambda:check_primal(bad,rows),
                   lambda:check_dual({'multipliers':[],'rhs':-1},examples['dual'][1]),
                   lambda:check_dual({'multipliers':[[len(examples['dual'][1]),1]],'rhs':-1},examples['dual'][1])):
        try:action()
        except ValueError:negative+=1
        else:raise ValueError('mutated certificate accepted')
    summary=[]
    for mask in (3,7):
        buckets=[counts[mask,j] for j in range(4)]
        summary.append({'core_mask':mask,'input_labeled_pairs':sum(buckets),'first_failures':buckets[:3],
                        'surviving_labeled_pairs':buckets[3],'orbit_stages':[orbit_counts[mask,j] for j in range(4)]})
    require([r['first_failures']+[r['surviving_labeled_pairs']] for r in summary]==[[18,6,81,387],[27,60,69,83]],'exact stage census')
    report={'profile':'20^3 21^40','M':219,'input_labeled_core_cell_pairs':731,'certificate_orbits':141,
            'summary':summary,'survivors_after_stages':[686,620,470],
            'independent_matrix_reconstructions':matrices,'full_matrix_transports':transports,
            'strict_stage_separation_orbits':separations,'negative_certificate_controls':negative,
            'literal_lifting_controls':controls.run(),
            'surviving_triple_cell_histogram':[[m,t,count] for (m,t),count in sorted(hist.items())],
            'certificate_sha256':sha256(args.certificate.read_bytes()).hexdigest(),
            'whole_profile_excluded':False,'target_graph_found':False}
    if args.report:args.report.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print('PASS independently enumerate all 731 labeled core/signature pairs in 141 relabeling orbits')
    print('PASS 423 literal 43-vertex matrix reconstructions and 2538 full inequality-set transports')
    print('PASS exact integer primals and Farkas duals; surviving stages 686,620,470')
    print('PASS strict stage separations, certificate mutations, and literal external-root controls')
    print('SCOPE complete aggregate integer-edge relaxation; 20^3 21^40 remains open; no target graph')


if __name__=='__main__':main()
