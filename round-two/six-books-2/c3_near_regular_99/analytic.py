"""Exact scalar bridge for the nonsymmetric low-neighborhood obstruction."""
from pathlib import Path
from argparse import ArgumentParser
import json,time,resource

def balanced(total,columns=12):
    q,r=divmod(total,columns)
    return columns*q*(q-1)//2+r*q

def main():
    parser=ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    work=parser.parse_args().work;work.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    # Independent finite minimization over twelve column loads on nine A points.
    dp={0:0}
    for _ in range(12):
        new={}
        for total,cost in dp.items():
            for load in range(10):
                key=total+load;value=cost+load*(load-1)//2
                new[key]=min(new.get(key,10**9),value)
        dp=new
    if any(dp[total]!=balanced(total) for total in range(109)):
        raise ValueError('Complete balancing formula/DP mismatch')
    cases=[]
    for h_edges in range(9,14):
        cut=69-2*h_edges
        upper=120-5*h_edges
        lower=balanced(cut)
        if not upper<lower:raise ValueError('Five-case contradiction incomplete')
        cases.append(dict(H_edges=h_edges,K_edges=21+h_edges,cut=cut,
                          A_pair_capacity_upper=upper,incidence_overlap_lower=lower,gap=lower-upper))
    record=dict(schema=1,agent='six-books-2',role='researcher',
                statement='No ordinary valid E99 graph22 has a degree9 vertex whose red-neighbor degree multiset is8^3,9^6. No symmetry or outside degree condition.',
                cases=cases,balanced_DP_all_109_totals_equal=True,
                BB_exact_overlap_total=3*(3+6+6+10),BB_A_pair_capacity_total=75,
                trust='Exact finite scalar check; ordinary counting bridge written in PROOF.md, unformalized; no peer review.')
    if record['BB_exact_overlap_total']!=record['BB_A_pair_capacity_total']:
        raise ValueError('BB overlap saturation identity')
    (work/'analytic.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(status='COMPLETE_ANALYTIC_SCALAR_AUDIT',seconds=time.monotonic()-start,
                         peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,record=record),indent=2))

if __name__=='__main__':main()
