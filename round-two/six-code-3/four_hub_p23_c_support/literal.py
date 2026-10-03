"""Complete four-C necessary support relaxation by actual HH-star choices."""
import argparse,hashlib,itertools,json,time
from pathlib import Path
CANON=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def need(p,message):
    if not p:raise ValueError(message)
EDGES=list(itertools.combinations(range(4),2))
def carrier(short):
    lam=[3 if e==short else 4 for e in EDGES]
    D=[70-4*(18 if a==0 else 19)+sum(lam[i] for i,e in enumerate(EDGES) if a in e) for a in range(4)]
    return D,[14-3*x for x in lam]
def feasible(N,m,D,L,guard,columns=True):
    if N[0]<4 or any(N[a]<2 for a in (1,2,3)):return None
    if any(m[a]>min(N[a],D[a]-N[a]) or (m[a] and N[a]<5) for a in range(4)):return None
    choices=[]
    for a in range(4):
        incident=[i for i,e in enumerate(EDGES) if a in e]
        if columns:
            incident=[i for i in incident if not(L[i]==2 and any(b!=a and b>0 and N[b]==2 for b in EDGES[i]))]
        d=max(0,8-N[a])
        stars=list(itertools.combinations(incident,d))
        if m[a] and not stars:return None
        choices.extend([stars]*m[a])
    def visit(at,capacity,trace):
        guard()
        if at==4:return trace
        for star in choices[at]:
            if all(capacity[i]>0 for i in star):
                remain=list(capacity)
                for i in star:remain[i]-=1
                found=visit(at+1,remain,trace+[list(star)])
                if found is not None:return found
        return None
    return visit(0,L,[])
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    need(not args.output.exists(),'fresh literal four-C output')
    start=time.monotonic();states=0
    def guard():
        nonlocal states
        states+=1
        need(states<=500000 and time.monotonic()-start<20,'INCOMPLETE original finite-auditor guard; no absence')
    compositions=[m for m in itertools.product(range(5),repeat=4) if sum(m)==4]
    need(len(compositions)==35,'all four-C compositions')
    records=[];bit_rows=[];positive=[];total=0
    for short in [(0,1),(1,2)]:
        D,L=carrier(short);bits=bytearray();at=0
        for N in itertools.product(*(range(x+1) for x in D)):
            for m in compositions:
                guard();witness=feasible(N,m,D,L,guard)
                if at%8==0:bits.append(0)
                if witness is not None:
                    bits[-1]|=1<<(at%8)
                    need(sum(N)>=17,'new K>=17 four-C implication')
                    records.append([list(short),list(N),list(m)])
                    positive.append(dict(short=list(short),N=list(N),m=list(m),stars=witness))
                at+=1
        bit_rows.append(dict(short=list(short),D=D,L=L,cases=at,feasible_mask_hex=bits.hex()));total+=at
    need(total==199920,'complete two-carrier support rectangle times all35 compositions')
    D,L=carrier((0,1));m=(3,0,1,0);low=(6,2,5,2);high=(6,3,5,3)
    good=feasible(high,m,D,L,guard);bad=feasible(low,m,D,L,guard);counter=feasible(low,m,D,L,guard,columns=False)
    need(good is not None and bad is None and counter is not None,'actual K17/K15-column-rule controls')
    control=dict(K17_relaxation_feasible=True,K15_with_column_rule_feasible=False,K15_without_only_column_rule_feasible=True,
        proper_low_N=list(low),positive_N=list(high),m=list(m),short=[0,1],no_code_attainment=True)
    math=dict(carriers=bit_rows,feasible_cases=records,total_cases=total,minimum_relaxation_K=min(sum(r[1]) for r in records),controls=control)
    result=dict(agent='six-code-3',role='researcher',status='COMPLETE_FOUR_C_LITERAL_HH_STAR_RELAXATION',math=math,
        entire_literal_positive_witnesses=positive,control_positive_stars=good,control_counterfactual_stars=counter,
        ordinary_bridges_formalized=False,independent_person_review=False,no_code_exclusion=True)
    args.output.write_bytes(CANON(result)+b'\n')
    print(json.dumps(dict(cases=total,feasible_cases=len(records),minimum_K=math['minimum_relaxation_K'],guard_states=states,
        full_output_sha256=hashlib.sha256(args.output.read_bytes()).hexdigest()),sort_keys=True),flush=True)
if __name__=='__main__':main()
