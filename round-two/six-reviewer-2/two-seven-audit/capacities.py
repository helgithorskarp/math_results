"""Reviewer-owned original inventory audit of 10162; target code unopened.

Model/partition ideas reuse this reviewer's six-three first_stage.py and the
exposed written target proof. New original allocations and role bounds are
reconstructed here. Standard library exact arithmetic, no stored census input.
"""
import functools,itertools,json,math,sys
from pathlib import Path

P=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
D=(3,5,7,9,15,21,35,45,63,105,315)

def need(ok,why):
    if not ok:raise ValueError(why)

def residual(mode):
    if mode=='sets':return tuple(sorted(set(range(2520))-set().union(*(set(range(a,2520,m))for m,a in P))))
    return tuple(x for x in range(2520)if all(x%m!=a for m,a in P))

def bits(mask):return tuple(i for i in range(11)if mask>>i&1)

def submasks(mask):
    sub=mask
    while True:
        yield sub
        if not sub:break
        sub=(sub-1)&mask

def data(mode):
    R=residual(mode);parents={p:tuple(x for x in R if x%8==p)for p in (2,6)}
    if mode=='sets':
        columns={d:[frozenset(x for x in parents[6]if x%d==a)for a in range(d)]for d in D};count=len
    else:
        columns={d:[sum(1<<j for j,x in enumerate(parents[6])if x%d==a)for a in range(d)]for d in D};count=int.bit_count
    C={d:max(map(count,v))for d,v in columns.items()}
    pair={};phase_pairs=[]
    for i,j in itertools.combinations(range(11),2):
        vals=[count(a|b)for a in columns[D[i]]for b in columns[D[j]]]
        pair[i,j]=max(vals);phase_pairs.append({'cofactors':[D[i],D[j]],'unions':vals})
    @functools.cache
    def savings(mask):
        if not mask:return 0
        i=(mask&-mask).bit_length()-1;rest=mask^(1<<i);best=savings(rest)
        for j in bits(rest):best=max(best,C[D[i]]+C[D[j]]-pair[min(i,j),max(i,j)]+savings(rest^(1<<j)))
        return best
    @functools.cache
    def unioncap(mask):
        if mode=='sets':return min(150,sum(C[D[i]]for i in bits(mask))-savings(mask))
        if not mask:return 0
        i=(mask&-mask).bit_length()-1;rest=mask^(1<<i);best=C[D[i]]+unioncap(rest)
        for j in bits(rest):best=min(best,pair[min(i,j),max(i,j)]+unioncap(rest^(1<<j)))
        return min(best,150)
    U=[unioncap(mask)for mask in range(2048)]
    @functools.cache
    def intersection(a,b):
        return min(U[a],U[b],sum(C[math.lcm(D[i],D[j])]for i in bits(a)for j in bits(b)))
    @functools.cache
    def armmax(mask):
        return max(intersection(a,mask^a)for a in submasks(mask))
    A=[armmax(mask)for mask in range(2048)]
    return R,parents,C,phase_pairs,U,A,intersection

def inventory(mode,lo,hi):
    R,parents,C,pairs,U,A,inter=data(mode)
    masks={k:[sum(1<<i for i in v)for v in itertools.combinations(range(11),k)]for k in range(7)}
    Hmasks={k:[m for m in masks[k]if not m&1]for k in range(7)}
    out=[];summary=[];survivors=[];cuts=0
    for h in range(lo,hi):
        q=6-h;rows=[];localcuts=0
        for H in Hmasks[h]:
            for Q in masks[q]:
                best=0;rowcuts=0
                if Q:
                    for HA in submasks(H):
                        HB=H^HA
                        for QB in submasks(Q):
                            if not QB:continue
                            val=min(U[HA]+A[Q^QB],U[HB]+U[QB],150)
                            best=max(best,val);rowcuts+=1
                row={'H':[D[i]for i in bits(H)],'Q':[D[i]for i in bits(Q)],'bound':best,'cut_count':rowcuts,'H_mask':H,'Q_mask':Q}
                rows.append(row);localcuts+=rowcuts
                if best>=87:survivors.append(row)
        out.extend(rows);cuts+=localcuts
        summary.append({'h':h,'q':q,'inventories':len(rows),'maximum':max(r['bound']for r in rows),'reaching87':sum(r['bound']>=87 for r in rows),'cuts':localcuts})
    return {'mode_independent_domain':{'P':P,'D':D,'H_spent_original48':True,'Q96_available':True,'cross_type_equal_cofactors_allowed':True,'essential16_32_required':True,'selected_unproductive_tails_allowed':True,'actual_LCM_proper_divisor_allowed':True},'h_interval':[lo,hi],'R':R,'parents':parents,'single_maxima':C,'all_phase_pair_unions':pairs,'all_group_upper_bounds':U,'all_Q_arm_upper_bounds':A,'inventories':out,'summary':summary,'survivors':survivors,'cuts':cuts}

def shadows(mode):
    R=residual(mode);Rset=set(R);parents={p:tuple(x for x in R if x%8==p)for p in (2,6)}
    base=tuple(m for m in range(8,2521)if 2520%m==0 and m not in{m for m,a in P})
    rows=[]
    for d in (5,9):
        for a in range(d):
            S=set(parents[6])|{x for x in parents[2]if x%d==a};budget=len(S)-177
            footprints=[];bound=0
            for m in base:
                if mode=='sets':
                    values=[]
                    for b in range(m):
                        f=set(range(b,2520,m))&Rset;values.append([len(f&S),len(f-S)])
                else:
                    inside=[0]*m;outside=[0]*m
                    for x in R:
                        (inside if x in S else outside)[x%m]+=1
                    values=[[i,o]for i,o in zip(inside,outside)]
                bound+=max([0]+[o for i,o in values if i<=budget]);footprints.append({'original':m,'all_phases':values})
            rows.append({'d':d,'a':a,'S':sorted(S),'size':len(S),'budget':budget,'need':len(R)-len(S),'outside_bound':bound,'deficit':len(R)-len(S)-bound,'all_original_phases':footprints})
    return {'R':R,'parents':parents,'unused_originals':base,'rows':rows,'original48_parent2_rows':[{'phase':a,'repair':[x for x in parents[2]if all(n%16==2 or n%48==a for n in (x+2520*k for k in range(4)))]}for a in (10,26,42)]}

if __name__=='__main__':
    need(len(sys.argv)>=4,'kind mode output [lo hi]');kind,mode,output=sys.argv[1:4];need(mode in ('sets','literal'),'mode')
    result=shadows(mode)if kind=='shadows'else inventory(mode,int(sys.argv[4]),int(sys.argv[5]))
    raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode()+b'\n';Path(output).write_bytes(raw)
    print(json.dumps({'bytes':len(raw),'summary':result.get('summary'),'cuts':result.get('cuts'),'survivors':len(result.get('survivors',[])),'shadows':[[r['d'],r['a'],r['size'],r['outside_bound'],r['deficit']]for r in result.get('rows',[])]}))
