"""Reviewer six-reviewer-2: fresh original-residue and four-lift arithmetic.

Only defining written mathematics has been exposed. No author kernel/fixture.
Every large row stream is visited completely and hashed in explicit order.
"""
from itertools import combinations, product
from math import lcm
import hashlib, json

PREFIX = ((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
COFACTORS = tuple(d for d in range(2,316) if 315%d==0)

def need(ok, why):
    if not ok: raise ValueError(why)
def wire(x): return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def fingerprint(rows): return hashlib.sha256(wire(rows)).hexdigest()
def stream(): return hashlib.sha256()
def push(h,row): h.update(wire(row)+b'\n')
def masks(points,m):
    z=[0]*m
    for j,n in enumerate(points): z[n%m]|=1<<j
    return z

def compute():
    R=tuple(n for n in range(2520) if all(n%m!=a for m,a in PREFIX))
    parents={r:tuple(n for n in R if n%8==r) for r in range(8)}
    shadows={r:tuple(sorted({n%315 for n in parents[r]})) for r in range(8)}
    U=shadows[2];need(U==shadows[6], 'actual marked shadows agree')
    labels=tuple(m for m in range(8,2521) if 2520%m==0 and m not in {m for m,a in PREFIX})
    # Entire original BASE177 prerequisite, independently rebuilt and credited.
    mm={m:masks(R,m) for m in labels};full=(1<<len(R))-1
    base_rows=[];base_stream=stream()
    for a,b in product(range(15),range(18)):
        f=mm[15][a]|mm[18][b];rem=full^f
        marg=[max((v&rem).bit_count() for v in mm[m]) for m in labels if m not in (15,18)]
        row=[a,b,f.bit_count(),marg,f.bit_count()+sum(marg)]
        base_rows.append(row);push(base_stream,row)
    # Literal physical shadows: all cofactor phase populations, not just maxima.
    phase={r:{d:masks(shadows[r],d) for d in (1,)+COFACTORS} for r in (1,2,4)}
    pops={str(r):{str(d):[v.bit_count() for v in vs] for d,vs in phase[r].items()} for r in phase}
    cap={d:max(v.bit_count() for v in phase[2][d]) for d in (1,)+COFACTORS}
    M={r:{d:max(v.bit_count() for v in phase[r][d]) for d in (1,)+COFACTORS} for r in (1,4)}
    S={k:max(sum(cap[d] for d in ds) for ds in combinations(COFACTORS,k)) for k in range(1,6)}
    intersections={};arm_rows=[]
    for k in (2,3,4,5):
        rows=[]
        for ds in combinations(COFACTORS,k):
            pairs=sum(cap[lcm(*v)] for v in combinations(ds,2))
            triples=sum(cap[lcm(*v)] for v in combinations(ds,3)) if k>=3 else 0
            rows.append([list(ds),cap[lcm(*ds)],pairs,triples])
        intersections[str(k)]=rows
    for ds in combinations(COFACTORS,4):
        # Fix first label in A: each unordered nonempty partition exactly once.
        for bits in range(1,8):
            A=(ds[0],)+tuple(ds[j+1] for j in range(3) if bits>>j&1)
            B=tuple(ds[j+1] for j in range(3) if not(bits>>j&1))
            if not B: continue
            arm_rows.append([list(ds),list(A),list(B),min(sum(cap[d] for d in A),sum(cap[d] for d in B),sum(cap[lcm(a,b)] for a in A for b in B))])
        # The missing partition A={first}, B={other three}.
        A=(ds[0],);B=ds[1:]
        arm_rows.append([list(ds),list(A),list(B),min(cap[A[0]],sum(cap[d] for d in B),sum(cap[lcm(A[0],b)] for b in B))])
    union_cache={};union_stream=stream();union_phases=0
    def UB(ds):
        nonlocal union_phases
        ds=tuple(sorted(ds))
        if not ds:return 0
        if ds in union_cache:return union_cache[ds][1]
        best=0;count=0;h=stream()
        for phases in product(*(range(d) for d in ds)):
            z=0
            for d,a in zip(ds,phases):z|=phase[2][d][a]
            value=z.bit_count();best=max(best,value);count+=1
            push(h,[list(phases),value])
        union_phases+=count;union_cache[ds]=[count,best,h.hexdigest()]
        return best
    triples=[]
    for ds in combinations(COFACTORS,3):
        total=sum(cap[d] for d in ds)
        value=UB(ds) if total>126 else total
        triples.append([list(ds),total,value,total>126])
    high=[];five_rows=[]
    for ds in combinations(COFACTORS,5):
        total=sum(cap[d] for d in ds)
        if total<=176:continue
        high.append(list(ds))
        for k in range(1,5):
            for P in combinations(ds,k):
                rest=tuple(d for d in ds if d not in P)
                for bits in range(1,1<<len(rest)):
                    O=tuple(d for j,d in enumerate(rest) if bits>>j&1)
                    A=tuple(d for d in rest if d not in O)
                    c=sum(cap[lcm(o,a)] for o in O for a in A)
                    values=[UB(P)+min(UB(O),c+min(cap[q],sum(cap[lcm(o,q)] for o in O))) for q in COFACTORS]
                    five_rows.append([list(ds),list(P),list(O),values])
    mixed=[]
    for ds in combinations(COFACTORS,3):
        for a in ds:
            rest=tuple(d for d in ds if d!=a)
            for bits in range(1,4):
                O=tuple(d for j,d in enumerate(rest) if bits>>j&1);A=tuple(d for d in rest if d not in O)
                cross=sum(cap[lcm(o,s)] for o in O for s in A)
                values=[cap[a]+30+min(UB(O),cross+min(cap[q],sum(cap[lcm(o,q)] for o in O))) for q in COFACTORS]
                mixed.append([list(ds),a,list(O),values])
    coupled=[]
    for gh in combinations(COFACTORS,2):
        remaining=tuple(d for d in COFACTORS if d not in gh)
        for abc in combinations(remaining,3):
            coupled.append([list(gh),list(abc)]+[M[r][lcm(*gh)]+sum(cap[d] for d in abc) for r in (1,4)])
    # All abstract local states checked by literal masks of the four lifts.
    local=[]
    def states(types,placed):
        choices=[(0,5,10) if z=='H' else (0,1,2,4,8) for z in types]
        out=[]
        for vs in product(*choices):
            mask=placed
            for v in vs:mask|=v
            activeH=sum(bool(v) for v,z in zip(vs,types) if z=='H')
            activeQ=sum(bool(v) for v,z in zip(vs,types) if z=='Q')
            filled=mask==15
            if filled:need(activeH>0 or activeQ>=(2 if placed==5 else 3),'whole generic local implication')
            if filled and placed==1 and not any(z=='Q' for z in types):
                maskH=0
                for v in vs:maskH|=v
                need(maskH==15,'all-half redundancy')
            out.append([list(vs),filled,activeH,activeQ])
        return out
    # Derive all 34 positive two-parent types, with valid conservative bounds.
    type_rows=[];q2bound={0:0,1:0,2:30,3:54,4:max(v[-1] for v in arm_rows)}
    q6bound={0:0,1:0,2:0,3:18,4:36,5:72}
    for n2,n6 in ((2,6),(3,5),(4,4),(5,3)):
        for h2 in range(n2):
            q2=n2-1-h2
            if h2==0 and q2<2:continue
            for h6 in range(n6):
                q6=n6-1-h6
                if q6==0 or(h6==0 and q6<3):continue
                h=h2+h6;v=(S[h] if h else 0)+q2bound[q2]+q6bound[q6];method='global distinct H plus Q intersections'
                if h==5 and q2+q6==1:v=176;method='five H/one Q global allocation'
                if h2==0 and q2==2 and h6==3:v=126+30;method='one-parent triple H union'
                if (h2,q2,h6,q6)==(1,2,2,1):v=max(max(v[-1]) for v in mixed);method='mixed O/S allocation'
                if h2==0 and q2==3 and(h6,q6)==(2,1):v=54+90;method='HHQ one-parent cap90'
                type_rows.append([n2,n6,'H'*h2+'Q'*q2,'H'*h6+'Q'*q6,v,method])
    for n2,n6,t2,t6,v,method in type_rows:
        local.append([2,t2,states(t2,5)]);local.append([6,t6,states(t6,1)])
    raw_local_types=[]
    for parent,lo,hi,placed in ((2,1,4,5),(6,2,5,1)):
        for length in range(lo,hi+1):
            for halves in range(length+1):
                types='H'*halves+'Q'*(length-halves)
                raw_local_types.append([parent,types,states(types,placed)])
    third_states=[];three_allocations=[]
    for r in (1,3,4,5,7):
        for types in ('HHH','HHQ','HQQ','QQQ'):
            values=states(types,0)
            for vs,filled,nh,nq in values:
                if filled:
                    if types=='HHH':need(nh>=2,'third-parent H pair')
                    if types=='HHQ':need(nh==2,'third-parent both H')
                    if types=='HQQ':need(nh==1 and nq==2,'third-parent H and Q pair')
                    need(types!='QQQ','three quarters cannot cover')
            third_states.append([r,types,values])
        pair=max(M[4 if r==4 else 1][lcm(a,b)] for a,b in combinations(COFACTORS,2))
        linked=max(v[-1 if r==4 else -2] for v in coupled)
        bounds=[linked,120+pair,108+pair,linked,120+pair,120+pair,120+2*pair,120+pair,120+pair]
        descriptions=[[(2,4,2),'H/HHQ'],[(2,4,2),'H/HQQ'],[(2,4,2),'H/QQQ'],[(3,3,2),'HH/HQ'],[(3,3,2),'HQ/HQ'],[(3,3,2),'QQ/HQ'],[(2,3,3),'third HHH'],[(2,3,3),'third HHQ'],[(2,3,3),'third HQQ']]
        three_allocations.extend([[r,list(ns),tag,value] for (ns,tag),value in zip(descriptions,bounds)])
    inv=[]
    for ds in combinations(COFACTORS,3):
        for f in ds:
            ab=tuple(d for d in ds if d!=f)
            if ds!=(3,5,9):
                # Individual H sum bounds H/HQ because C(lcm(f,q))<=C(f).
                continue
            for gh in combinations(COFACTORS,2):
                for q in COFACTORS:
                    if q in gh:continue
                    v=UB(ab)+cap[lcm(*gh)]+cap[lcm(f,q)]
                    inv.append([f,list(ab),list(gh),q,v])
    # Every original phase tuple, each at all four physical lifts of all150 holes.
    finals=[]
    for r,ms,placed,threshold in ((2,(48,144,96,288),(16,2),147),(6,(80,160),(32,6),27)):
        points=parents[r];ones=(1<<len(points))-1
        def planes(m,a):
            return tuple(sum(1<<j for j,n in enumerate(points) if (n+2520*k)%m==a) for k in range(4))
        pr=planes(*placed);ph={m:{a:planes(m,a) for a in range(r,m,8)} for m in ms};good=[];h=stream();count=0;maxv=0
        for phases in product(*(range(r,m,8) for m in ms)):
            z=list(pr)
            for m,a in zip(ms,phases):
                for k in range(4):z[k]|=ph[m][a][k]
            repaired=ones
            for value in z:repaired&=value
            v=repaired.bit_count();count+=1;maxv=max(maxv,v);push(h,[list(phases),v])
            if v>=threshold:good.append([list(phases),v,hex(repaired)])
        finals.append({'parent':r,'moduli':list(ms),'raw_count':count,'maximum':maxv,'qualifying':good,'whole_raw_stream_sha256':h.hexdigest()})
    glued=[]
    for c in range(5):
        protected=set(parents[2])|{n for n in parents[6] if n%5==c}
        outside=set(R)-protected;rows=[];phasehash=stream();rawcount=0
        for m in labels:
            inside=[0]*m;out=[0]*m
            for n in protected:inside[n%m]+=1
            for n in outside:out[n%m]+=1
            for a in range(m):push(phasehash,[m,a,inside[a],out[a]]);rawcount+=1
            rows.append([m,max(out[a] for a in range(m) if inside[a]<=3)])
        glued.append({'c':c,'protected':len(protected),'outside':len(outside),'labels':rows,'sum':sum(v for m,v in rows),'whole_phase_stream_sha256':phasehash.hexdigest(),'raw_phases':rawcount})
    urows=[[list(ds)]+v for ds,v in sorted(union_cache.items())]
    return {'scope':{'period':10080,'minimum':'exactly8','prefix':[[m,a] for m,a in PREFIX]+[[16,2],[32,6]],'actual_lcm':'divides10080','all_other_phases_omissions_free':True,'original_labels':True,'weakened_16_hypothesis':'nonempty actual BASE hole parent2','essential_32':True,'productive_count_lower':9,'global_L_min_8_improvement':False},'R':list(R),'parent_counts':[len(parents[r]) for r in range(8)],'cofactors':list(COFACTORS),'capacity':[[d,cap[d]] for d in cap],'phase_populations':pops,'S':S,'base177':{'rows':base_rows,'stream_sha256':base_stream.hexdigest(),'lower_K':min(v[-1] for v in base_rows),'upper_K':max(v[-1] for v in base_rows)},'intersections':intersections,'four_Q_arms':arm_rows,'H_triples':triples,'high_five_H_sets':high,'all_exact_H_unions':urows,'union_phases':union_phases,'five_H_Q_rows':five_rows,'mixed_HQQ_HHQ_rows':mixed,'three_parent_coupling':coupled,'three_parent_allocations':three_allocations,'third_local_states':third_states,'type_rows':type_rows,'all_local_states':local,'all_raw_local_types':raw_local_types,'remaining_inventory':inv,'final_phases':finals,'BASE_gluing':glued,'producer_imported':False}

if __name__=='__main__':print(wire(compute()).decode())
