"""Exact typed hub-support partitions; ordinary proofs are in PROOF.md.

All necessary D0=5..13,Dlight=1..9,total24 are retained. Each hub
support is disjoint in the two surviving T4 populations. A positive
one-deficit row needs support2, a two-deficit row support5. No HHH
word model, local frequency cap, solver or symmetry quotient is used.
"""
from collections import Counter
import itertools,json,time
from pathlib import Path
S=Path('round-two/six-code-3/scratch')

def need(c,m):
    if not c:raise ValueError(m)

def fits(D,N,U,V,min_two=5):
    units=tuple(2*n-d for n,d in zip(N,D));doubles=tuple(d-n for n,d in zip(N,D))
    if min(units+doubles)<0 or sum(units)!=U or sum(doubles)!=V:return False
    return all((not units[a] or N[a]>=2) and (not doubles[a] or N[a]>=min_two) for a in range(4))

def main():
    start=time.monotonic();data=json.loads((S/'pass18-t4-producer.json').read_text());inventory=data['inventory']
    survivors=[dict(branch=[b[k] for k in ('Q','T','X','tau')],population=t['population']) for b in inventory['branches'] for t in b['templates'] if not t['failures']]
    need(survivors==[dict(branch=[0,4,1,0],population=[[16,2],[18,12]]),dict(branch=[0,4,2,0],population=[[17,4],[18,10]])],'whole focused T4 surviving stream')
    for tid,e,k,w,q,hist in [(16,1,0,0,0,[3,1,0,0,0]),(17,1,1,1,0,[2,1,0,0,0]),(18,1,1,2,0,[3,0,0,0,0])]:
        row=inventory['types'][tid];need([row[x] for x in ['e','k','hub_weight','q','ss_hist']]==[e,k,w,q,hist],'actual typed row meaning')
    Dgrid=[(heavy,)+lights for heavy in range(5,14) for lights in itertools.product(range(1,10),repeat=3) if heavy+sum(lights)==24]
    records=[];steps=0
    for U,V in [(0,12),(4,10)]:
        rows=[];before=passing=0
        for D in Dgrid:
            counts=0;solutions=[];ranges=[range((d+1)//2,d+1) for d in D]
            for first in itertools.product(*ranges[:3]):
                N=first+(U+V-sum(first),);steps+=1
                need(steps<=500000 and time.monotonic()-start<20,'INCOMPLETE fixed typed-partition guard')
                unit=tuple(2*n-d for n,d in zip(N,D));double=tuple(d-n for n,d in zip(N,D))
                if min(unit+double)<0 or sum(unit)!=U or sum(double)!=V:continue
                counts+=1
                if fits(D,N,U,V):solutions.append(list(N))
            before+=counts;passing+=len(solutions)
            rows.append(dict(D4=list(D),typed_weight_allocations=counts,passing_support_N4=solutions))
        need(passing==0,'typed support survivor is not excluded')
        records.append(dict(unit_rows=U,double_rows=V,neutral_rows=14-U-V,degree_targets=len(Dgrid),typed_weight_allocations=before,passing_support_allocations=passing,rows=rows))
    # A positive abstract partition and a support-threshold sensitivity control.
    need(fits((8,8,2,2),(5,5,2,2),8,6),'positive abstract disjoint-support partition')
    need(not fits((6,8,8,2),(4,4,4,2),4,10),'strict two-deficit support5')
    need(fits((6,8,8,2),(4,4,4,2),4,10,min_two=4),'weakened support control should expose a typed survivor')
    result=dict(agent='six-code-3',role='researcher',status='AUTHOR_COMPLETE_T4_DISJOINT_SUPPORT_EXCLUSION',T4_scalar_branches=len(inventory['branches']),T4_raw_vectors=sum(len(b['templates']) for b in inventory['branches']),T4_surviving_vectors=survivors,degree_target_count=len(Dgrid),records=records,controls=dict(positive_partition=1,strict_support_rejection=1,weakened_support_positive=1),ordinary_bridges_formalized=False,external_review=False,new_unrestricted_code_bound=None)
    out=S/'pass18-t4-support-producer.json';need(not out.exists(),'fresh support output');out.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(status=result['status'],degree_targets=len(Dgrid),typed_partition_steps=steps,statistics=[{k:v for k,v in r.items() if k!='rows'} for r in records],elapsed_seconds=time.monotonic()-start)),flush=True)
if __name__=='__main__':main()
