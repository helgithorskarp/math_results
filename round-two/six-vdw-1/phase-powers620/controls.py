"""Complete tiny winding inputs with genuine cross-field positives; certificate damages."""
import argparse
import copy
import csv
import importlib.util
import json
from math import gcd
from pathlib import Path

# Resolve the intended checker explicitly, including under Python's -I mode.
_spec = importlib.util.spec_from_file_location('phase_power_checker', Path(__file__).resolve().parent / 'check.py')
_checker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_checker)
check = _checker.check


def require(ok,message):
    if not ok:raise ValueError(message)


def tiny(q,m,k,root):
    n=q*2*m;logs={pow(root,i,q):i for i in range(q-1)}
    require(set(logs)==set(range(1,q)),'tiny primitive field')
    inputs=closed=positive=negative=regular=Hchecks=0
    for base in range(2**m):
        bits=[((base>>s)%2) for s in range(m)]+[1-((base>>s)%2) for s in range(m)]
        for u in range(2*m):
            if gcd(u,2*m)!=1:continue
            for t in range(2*m):
                inputs+=1;permutation=[(u*s+t)%(2*m) for s in range(2*m)];powers=[list(range(2*m))]
                for _ in range(q-1):powers.append([permutation[s] for s in powers[-1]])
                closure=all(bits[powers[-1][s]]==bits[s] for s in range(2*m))
                closed+=closure
                word=[None]*n
                for r in range(1,q):
                    for s in range(2*m):
                        x=next(x for x in range(r,n,q) if x%(2*m)==s)
                        word[x]=bits[powers[logs[r]][s]]
                full=True
                for a in range(n):
                    for b in range(n):
                        if a==b:continue
                        positions=[(a+j*(b-a))%n for j in range(k)]
                        if any(x%q==0 for x in positions):continue
                        regular+=1
                        if len({word[x] for x in positions})==1:full=False
                local=all(len({bits[(s+j*h)%(2*m)] for j in range(k)})>1 for s in range(2*m) for h in range(1,2*m))
                normalized=local
                for a in range(q):
                    if any((a+j)%q==0 for j in range(k)):continue
                    for s in range(2*m):
                        for h in range(2*m):
                            start=next(x for x in range(n) if x%q==a and x%(2*m)==s)
                            d=next(x for x in range(1,n) if x%q==1 and x%(2*m)==h)
                            if len({word[(start+j*d)%n] for j in range(k)})==1:normalized=False
                if closure:require(full==normalized,'tiny conditional complete physical/normalized equivalence')
                group_order=sum(gcd(x,2*m)==1 for x in range(2*m))*(2*m)
                e=gcd(q-1,group_order);multiplier=pow(root,e,q)
                if closure:
                    require(all(bits[powers[e][s]]==bits[s] for s in range(2*m)),'tiny Lagrange row-period bridge')
                    for r in range(1,q):
                        for s in range(2*m):
                            require(bits[powers[logs[r]][s]]==bits[powers[logs[r*multiplier%q]][s]],'tiny original subgroup colors')
                            Hchecks+=1
                positive+=full;negative+=not full
    return {'q':q,'half':m,'AP_length':k,'all_base_generator_inputs':inputs,'closed_transport_pairs':closed,'actual_regular_positives':positive,
            'actual_regular_negatives':negative,'all_actual_regular_APs_examined':regular,'original_subgroup_color_identities':Hchecks}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('catalogue',type=Path);a=p.parse_args()
    with a.catalogue.open(newline='') as f:
        r=csv.reader(f);next(r);records=[[int(v) if j!=4 else v for j,v in enumerate(row)] for row in r]
    antipodal_truth=0
    for phase in range(20):
        start=next(x for x in range(620) if x%31==1 and x%20==phase)
        positions=[(start+310*j)%620 for j in range(7)]
        require(all(x%31==1 for x in positions) and [x%20 for x in positions]==[(phase+10*j)%20 for j in range(7)],'actual first-field antipodal necessity')
        for a,b in [(0,0),(0,1),(1,0),(1,1)]:
            colors=[a if x%20==phase else b for x in positions]
            require((len(set(colors))>1)==(a!=b),'ALL arbitrary first-field color pairs')
            antipodal_truth+=1
    specs=[tiny(3,2,3,2),tiny(5,1,3,2),tiny(7,2,7,3)]
    require(specs[1]['actual_regular_positives']==2 and specs[1]['actual_regular_negatives']==2,'genuine cross-field positive/negative calibration')
    require(specs[0]['actual_regular_positives']==32 and specs[2]['actual_regular_positives']==32,'complete tiny subgroup positives')
    damages=[]
    x=copy.deepcopy(records);x.pop();damages.append(x)
    x=copy.deepcopy(records);x[1]=copy.deepcopy(x[0]);damages.append(x)
    for column,value in [(0,16),(1,2),(2,False)]:
        x=copy.deepcopy(records);x[0][column]=value;damages.append(x)
    bad_index=next(i for i,r in enumerate(records) if r[4]=='BAD_AP')
    for column,value in [(4,'CLOSURE'),(4,'UNVERIFIED'),(5,0),(6,0),(6,311),(7,1-records[bad_index][7])]:
        x=copy.deepcopy(records);x[bad_index][column]=value;damages.append(x)
    x=copy.deepcopy(records);x[bad_index][4]='CORE';x[bad_index][5:]=[-1,-1,-1];damages.append(x)
    x=copy.deepcopy(records);x[bad_index][3]=1-x[bad_index][3];damages.append(x)
    x=copy.deepcopy(records);x[bad_index][3]=bool(x[bad_index][3]);damages.append(x)
    for damaged in damages:
        try:check(damaged,False)
        except (ValueError,KeyError,TypeError,StopIteration):pass
        else:raise ValueError('damaged winding certificate accepted')
    print(json.dumps({'author':'six-vdw-1','role':'researcher','status':'COMPLETE_CANONICAL_PHASE_POWER_TINY_CONTROLS',
                      'arbitrary_first_field_antipodal_truth_inputs':antipodal_truth,'all_tiny_inputs':sum(r['all_base_generator_inputs'] for r in specs),'closed_tiny_transport_pairs':sum(r['closed_transport_pairs'] for r in specs),
                      'actual_regular_positive_profiles':sum(r['actual_regular_positives'] for r in specs),'actual_regular_negative_profiles':sum(r['actual_regular_negatives'] for r in specs),
                      'actual_tiny_regular_AP_checks':sum(r['all_actual_regular_APs_examined'] for r in specs),'actual_tiny_subgroup_identities':sum(r['original_subgroup_color_identities'] for r in specs),
                      'damaged_catalogue_rejections':len(damages),'case_results':specs,
                      'scope':'Tiny full physical positives/negatives and diagnostic certificate damages; full production bridges checked separately.'},sort_keys=True),flush=True)
