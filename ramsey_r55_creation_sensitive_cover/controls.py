#!/usr/bin/env python3
"""Corruption controls and exhaustive literal truth tables for creation rows."""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import verify as v

HERE=Path(__file__).resolve().parent

def reject(fn,fragment):
    try:fn()
    except ValueError as error:
        v.require(fragment in str(error),'unexpected rejection: '+str(error))
        return str(error)
    raise ValueError('bad certificate accepted: '+fragment)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    ap.add_argument('--discovery',type=Path,default=HERE/'discovery.json')
    ap.add_argument('--report',type=Path,required=True);args=ap.parse_args()
    base=v.parent();seed=base.decode(json.loads(base.SEED.read_text()));old=base.check_seed(seed)
    cert=json.loads(args.certificate.read_text());discovery=json.loads(args.discovery.read_text())
    passed=v.verify_certificate(seed,cert,base)
    failures={}
    bad=deepcopy(cert);bad['denominator']=0
    failures['zero_denominator']=reject(lambda:v.verify_certificate(seed,bad,base),'denominator')
    bad=deepcopy(cert);bad['mixed_cliques'][0][2]=-1
    failures['negative_creation_weight']=reject(lambda:v.verify_certificate(seed,bad,base),'five-set weight')
    bad=deepcopy(cert);bad['mixed_cliques'].append(bad['mixed_cliques'][0])
    failures['duplicate_creation_row']=reject(lambda:v.verify_certificate(seed,bad,base),'duplicate five-set')
    bad=deepcopy(cert);bad['mixed_cliques'][0][0]=1-bad['mixed_cliques'][0][0]
    failures['wrong_creation_color']=reject(lambda:v.verify_certificate(seed,bad,base),'fixed edge already blocks')
    bad=deepcopy(cert);bad['mixed_cliques'][0][1]=[3,4,5,6,7]
    failures['unanchored_creation_row']=reject(lambda:v.verify_certificate(seed,bad,base),'old/mixed five-set category')
    bad=deepcopy(cert);bad['old_cliques'][0][0]=1-bad['old_cliques'][0][0]
    failures['wrong_old_color']=reject(lambda:v.verify_certificate(seed,bad,base),'old row is not an original')
    bad=deepcopy(cert);bad['upper_penalties']=[]
    failures['missing_exact_box_correction']=reject(lambda:v.verify_certificate(seed,bad,base),'overloaded edge')
    bad=deepcopy(cert);bad['degrees']=[];bad['profiles']=[]
    failures['omitted_conservation']=reject(lambda:v.verify_certificate(seed,bad,base),'overloaded edge')
    bad=deepcopy(discovery);bad['mixed_rows_sha256']='0'*64
    failures['altered_encoding_digest']=reject(lambda:v.encoding_audit(seed,old,bad,base),'encoding mismatch')
    # Check the row formula on every assignment of the free edges for both
    # possible original colors and every possible original coloring.
    # Use an actual five-set with 1 or 2 exceptional roots and fixed red
    # edges. Its blue analogue is obtained by complementing every color.
    tested=0
    for five in ((0,3,4,5,6),(0,1,3,4,5)):
        free=[e for e in combinations(five,2) if min(e)>=3]
        for target in (0,1):
            for original in range(1<<len(free)):
                adj=[set() for _ in range(43)]
                for u,w in combinations(five,2):
                    red=target if u<3 else bool(original>>free.index((u,w))&1)
                    if red:adj[u].add(w);adj[w].add(u)
                row,b=v.color_row(adj,target,five)
                for flips in range(1<<len(free)):
                    final=[bool(original>>i&1)^bool(flips>>i&1) for i in range(len(free))]
                    mono=all(c==bool(target) for c in final)
                    value=sum(row[e] for i,e in enumerate(free) if flips>>i&1)
                    v.require((value>=b)==(not mono),'colored-five-set truth table')
                    tested+=1
    missing=[];visible=base.visible_edges(seed)
    for red,five,w in cert['mixed_cliques']:
        holes=[e for e in combinations(five,2) if (e[1] in seed[e[0]])!=bool(red)]
        v.require(len(holes)==1 and holes[0] in base.EDGES,'selected creation row is not one-hole')
        missing.extend(holes)
    report={'status':'PASS','corruption_controls':failures,'literal_truth_table_cases':tested,
            'selected_creation_rows_one_hole':len(missing),'distinct_missing_edges':len(set(missing)),
            'distinct_visible_missing_edges':len(set(missing)&visible),
            'verified_integer_bound':passed['integer_lower_bound'],
            'scope_control':'No graph above the lower bound is asserted feasible; old cover witness remains mixed-K5 invalid.'}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':main()
