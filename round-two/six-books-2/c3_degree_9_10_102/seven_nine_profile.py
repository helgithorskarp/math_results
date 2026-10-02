"""Literal necessary-case audits for the ordinary7^3,9^7,10^12 proof."""
from argparse import ArgumentParser
from itertools import combinations,combinations_with_replacement,product
from pathlib import Path
from collections import Counter
import hashlib,json,time,resource

def local(word):
    H=[]
    for u in range(9):
        row=set();i,t=divmod(u,3)
        for v in range(9):
            if u==v:continue
            j,s=divmod(v,3)
            bit=i if i==j else {(0,1):3,(0,2):6,(1,2):9}[min(i,j),max(i,j)]+((s-t)%3 if i<j else (t-s)%3)
            if word>>bit&1:row.add(v)
        H.append(row)
    return H

def caps(H,DG):
    return {(u,v):(2 if v in H[u] else DG[u]+DG[v]-15)-len(H[u]&H[v]) for u,v in combinations(range(9),2)}

def phi(values):return sum(m*(m-1)//2 for m in values)

def derive():
    root_cases=[]
    for marks in [(7,9,9),(7,9,10),(7,10,10),(9,9,10),(9,10,10),(10,10,10)]:
        DA=3*sum(marks);Dx=171-2*DA
        root_cases.append(dict(marks=list(marks),degree_sum=DA,root_deficit=Dx,budget_kept=0<=Dx<=15))
    if [r['marks'] for r in root_cases if r['budget_kept']]!=[[7,9,10],[7,10,10],[9,9,10]]:
        raise ValueError('Entire seven/nine root marks')
    # DA78 requires W-Dx=0, but mixed deficit has odd parity (DA-rootdegree).
    if (78-9)%2!=1 or 15-(171-2*78)!=0:raise ValueError('Tight-root mixed parity contradiction')

    third_count=0
    third_rows=[]
    for word in range(4096):
        H=local(word);h=list(map(len,H))
        if sum(h)!=24 or max(h)>3:continue
        C=caps(H,[9]*6+[10]*3)
        if sum(C.values())<93:continue
        if sum(C.values())!=93 or h[6]!=2:raise ValueError('A9/9/10 tight capacity')
        third_count+=1
        for u in range(6):
            total=5+sum(C[min(u,v),max(u,v)] for v in range(9) if v!=u)
            if total!=23 or any(25-3*q==total for q in range(4)):
                raise ValueError('A9 row weighted-Gram congruence')
            third_rows.append((word,u,total))

    counts=Counter();h9_forced=[];h12_lowtriangle=[]
    DG=[7]*3+[10]*6
    for word in range(4096):
        H=local(word);h=list(map(len,H));edge=sum(h)//2
        if edge not in [9,12] or max(h)>3:continue
        counts['H'+str(edge)+'_max3_words']+=1
        # Every L pair must be red, since a blue L pair has negative capacity.
        if any(v not in H[u] for u,v in combinations(range(3),2)):continue
        counts['H'+str(edge)+'_low_triangle_words']+=1
        C=caps(H,DG);total=sum(C.values())
        if edge==9:
            if total<96:continue
            if total!=96 or h[0]!=3:raise ValueError('H9 complete capacity equality')
            counts['H9_capacity_words']+=1
            # AA is tight; nonroot deficit6 gives D_L<=2, hence all three X neighbors high10.
            if [q for q in range(4) if 0<=7-2*q<=2]!=[3]:raise ValueError('H9 low incident deficit')
            grow=[3+sum(C[min(u,v),max(u,v)] for v in range(9) if v!=u) for u in range(3)]
            if grow!=[15]*3:continue
            counts['H9_forced_shape_words']+=1;h9_forced.append(word)
            M=next(set(range(3*i,3*i+3)) for i in [1,2] if h[3*i]==1)
            T=set(range(3,9))-M
            if any(len(H[u]&M)!=1 or len(H[u]&set(range(3)))!=2 for u in range(3)):raise ValueError('H9 low matching')
            if any(H[u]-set(range(3)) for u in M):raise ValueError('H9 mid only low matching')
            if any(H[u]!=T-{u} for u in T):raise ValueError('H9 isolated top triangle')
            if any(C[min(u,v),max(u,v)]!=5 for u,v in combinations(sorted(M),2)):raise ValueError('H9 mid pair target')
            if any(C[min(u,v),max(u,v)]!=1 for u,v in combinations(sorted(T),2)):raise ValueError('H9 top pair target')
            if any(sum(C[min(u,v),max(u,v)] for v in M)!=4 for u in range(3)):raise ValueError('H9 L-M row target')
        else:
            if total<72:continue
            if total!=78 or h[0]!=3:raise ValueError('H12 low degree/capacity equality')
            counts['H12_capacity_words']+=1;h12_lowtriangle.append(word)
            for u in range(3):
                neighbor=next(v for v in H[u] if v>=3)
                grow=3+sum(C[min(u,v),max(u,v)] for v in range(9) if v!=u)
                if grow!=16-h[neighbor]:raise ValueError('H12 low full Gram row formula')
            M=next(set(range(3*i,3*i+3)) for i in [1,2] if h[3*i]==2)
            T=set(range(3,9))-M
            if H[0]&M:
                counts['H12_chain_shape_words']+=1
                if any(sum(C[min(u,v),max(u,v)] for v in M)!=4 for u in range(3)):raise ValueError('H12 L-M cap row')
                if any(C[min(u,v),max(u,v)]!=5 for u,v in combinations(sorted(M),2)):raise ValueError('H12 M pair target')
                if any(C[min(u,v),max(u,v)]!=1 for u,v in combinations(sorted(T),2)):raise ValueError('H12 T pair target')

    # Weighted graph of nonroot deficit orbits: seven loops plus twenty-one cross pairs.
    edge_types=[(i,i) for i in range(7)]+list(combinations(range(7),2))
    column_modes={'G7':(4,4,3,5),'GM':(3,4,4,5),'G6':(4,4,4,4),'both_sixes_at9':(3,3,5,5)}
    projected=[]
    for mode,sizes in column_modes.items():
        target=[1,1,0]+[(s+1)%2 for s in sizes]
        AA_units=(78-3*sum(s*(s-1)//2 for s in sizes))//3
        all_parity=[];kept=[]
        for a,b in combinations_with_replacement(range(28),2):
            edges=[edge_types[a],edge_types[b]];deg=[0]*7
            for u,v in edges:deg[u]+=1;deg[v]+=1
            if [d%2 for d in deg]!=target:continue
            all_parity.append(edges)
            if sum(u<3 and v<3 for u,v in edges)!=AA_units:continue
            kept.append(edges)
        if mode in ['G7','GM']:
            oddB=[i for i in range(3,7) if target[i]]
            required=[(0,1),tuple(oddB)]
            if kept!=[required]:raise ValueError('Whole tight matching projection')
        elif mode=='G6':
            if all_parity:raise ValueError('Six odd orbit classes at two deficit units')
        else:
            expected=[sorted([(0,i),(1,i)]) for i in range(3,7)]
            if sorted(kept)!=sorted(expected):raise ValueError('Whole mixed two-edge paths')
        projected.append(dict(mode=mode,column_sizes=list(sizes),odd_classes=sum(target),AA_deficit_units=AA_units,
                              assignment_domain=406,parity_assignments=len(all_parity),kept_edges=[[list(e) for e in es] for es in kept]))

    scalar=[]
    for mode,sizes,mrow,trow,cross_target in [('H9',(4,4,5,5),8,7,4),('G7',(4,4,5,3),7,6,3),('GM',(3,4,4,5),7,6,3)]:
        # U has low weight2, V weight1, and the two B9 slots low weight0.
        cases=[]
        for m in product(range(4),repeat=4):
            t=[s-r-x for s,r,x in zip(sizes,[0,0,2,1],m)]
            if any(not 0<=x<=3 for x in t):continue
            if sum(m)!=mrow or sum(t)!=trow or 2*m[2]+m[3]!=cross_target:continue
            mp,tp=phi(m),phi(t)
            if mp==5 and tp==1:raise ValueError('Unexpected complete necessary scalar solution')
            cases.append(dict(mid_weights=list(m),top_weights=t,mid_pair_common=mp,top_pair_common=tp))
        scalar.append(dict(mode=mode,column_ranks=list(sizes),mid_row=mrow,top_row=trow,L_mid_row=cross_target,
                           cases=cases,required_mid_pair=5,required_top_pair=1,solutions=0))
    if [len(s['cases']) for s in scalar]!=[2,2,5]:raise ValueError('Complete small scalar case counts')
    return dict(status='COMPLETE_ORDINARY_SEVEN_NINE_PROFILE_BRIDGES',agent='six-books-2',role='researcher',
                root_cases=root_cases,tight_root_parity_rejected=True,A9910_tight_words=third_count,
                A9_weighted_Gram_rows=len(third_rows),H_counts=dict(counts),H9_forced_words=h9_forced,
                H12_low_triangle_words=h12_lowtriangle,projected_deficit_graphs=projected,scalar_cases=scalar,
                trust='All ordinary case/graph/Gram bridges checked literally; no incidence/K/host census or historical classification premise; unformalized, independent peer review pending.')

def main():
    p=ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args();start=time.monotonic()
    record=derive();raw=json.dumps(record,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'
    args.work.mkdir(parents=True,exist_ok=True);(args.work/'seven-nine-profile.json').write_text(raw)
    if time.monotonic()-start>25:raise RuntimeError('INCOMPLETE seven/nine profile checks')
    print(json.dumps(dict(record=record,bytes=len(raw.encode()),sha256=hashlib.sha256(raw.encode()).hexdigest(),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2))

if __name__=='__main__':main()
