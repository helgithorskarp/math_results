"""Independent four-C support relaxation by all exact edge-subset flow cuts."""
import argparse,hashlib,json,time
from pathlib import Path
CANON=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def require(p,message):
    if not p:raise ValueError(message)
def compositions(total,width):
    if width==1:return [(total,)]
    out=[]
    for first in range(total+1):
        for tail in compositions(total-first,width-1):out.append((first,)+tail)
    return out
def data(short):
    pairs=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    lam={p:4 for p in pairs};lam[short]=3
    degree=[sum(lam[p] for p in pairs if a in p)-(2 if a==0 else 6) for a in range(4)]
    capacity=[14-3*lam[p] for p in pairs]
    return pairs,lam,degree,capacity
def passes(N,m,short,clock,columns=True):
    pairs,lam,D,L=data(short)
    # Direct total-degree upper bound for all four shortened hub stars.
    for a in range(4):
        total=17*16-12*(18 if a==0 else 19)
        high=total-(14-N[a])
        if high>(N[a]+3)*(N[a]+2)+(14-N[a]):return False
        if m[a] and (N[a]<5 or m[a]>N[a] or m[a]>D[a]-N[a]):return False
    permitted=[];demand=[]
    for a in range(4):
        ids=[]
        for i,p in enumerate(pairs):
            if a not in p:continue
            other=p[1] if p[0]==a else p[0]
            if columns and other!=0 and N[other]==2 and lam[p]==4:continue
            ids.append(i)
        permitted.append(ids);demand.append(max(0,8-N[a]))
        if m[a] and demand[a]>len(ids):return False
    for mask in range(64):
        clock()
        capacity=sum(L[i] for i in range(6) if mask&(1<<i))
        required=0
        for a in range(4):
            outside=sum(not(mask&(1<<i)) for i in permitted[a])
            required+=m[a]*max(0,demand[a]-outside)
        if required>capacity:return False
    return True
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    require(not a.output.exists(),'fresh independent dual four-C output')
    begin=time.monotonic();states=0
    def clock():
        nonlocal states
        states+=1
        require(states<=500000 and time.monotonic()-begin<20,'INCOMPLETE original finite-auditor guard; no absence')
    ms=compositions(4,4);require(len(ms)==35 and ms==sorted(set(ms)),'entire independent composition recursion')
    out=[];records=[];total=0
    for short in [(0,1),(1,2)]:
        pairs,lam,D,L=data(short);mask_bytes=bytearray();offset=0
        for n0 in range(D[0]+1):
            for n1 in range(D[1]+1):
                for n2 in range(D[2]+1):
                    for n3 in range(D[3]+1):
                        N=(n0,n1,n2,n3)
                        for m in ms:
                            clock();ok=passes(N,m,short,clock)
                            if offset%8==0:mask_bytes.append(0)
                            if ok:
                                mask_bytes[-1]|=1<<(offset%8)
                                require(sum(N)>16,'entire independent K<=16 infeasibility')
                                records.append([list(short),list(N),list(m)])
                            offset+=1
        out.append(dict(short=list(short),D=D,L=L,cases=offset,feasible_mask_hex=mask_bytes.hex()));total+=offset
    require(total==199920,'complete independent N/composition domain')
    m=(3,0,1,0);low=(6,2,5,2);high=(6,3,5,3)
    require(passes(high,m,(0,1),clock) and not passes(low,m,(0,1),clock) and passes(low,m,(0,1),clock,columns=False),'independent actual column-rule discrimination')
    control=dict(K17_relaxation_feasible=True,K15_with_column_rule_feasible=False,K15_without_only_column_rule_feasible=True,
        proper_low_N=list(low),positive_N=list(high),m=list(m),short=[0,1],no_code_attainment=True)
    math=dict(carriers=out,feasible_cases=records,total_cases=total,minimum_relaxation_K=min(sum(r[1]) for r in records),controls=control)
    result=dict(agent='six-code-3',role='researcher',status='COMPLETE_FOUR_C_INDEPENDENT_ALL_SUBSET_DUAL_RELAXATION',math=math,
        ordinary_bridges_formalized=False,independent_person_review=False,no_code_exclusion=True)
    a.output.write_bytes(CANON(result)+b'\n')
    print(json.dumps(dict(cases=total,feasible_cases=len(records),minimum_K=math['minimum_relaxation_K'],guard_states=states,
        full_output_sha256=hashlib.sha256(a.output.read_bytes()).hexdigest()),sort_keys=True),flush=True)
if __name__=='__main__':main()
