"""Fresh original-set q19 comparison and complete capacity-envelope reconstruction."""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
from flow import need,canon,sha,check_literal,equal_interval

def carrier(k,m):
    need(type(k) is int and type(m) is int and k>=4 and m>=4,'original coefficient carrier count domain')
    g=3+k+m;X=set(range(3,3+k));Y=set(range(3+k,g));S={frozenset()}
    for r in (1,2):S.update(frozenset(t) for t in combinations(range(g),r))
    S.add(frozenset((0,1,2)))
    for z in X|Y:
        S.add(frozenset((0,1,z)));S.add(frozenset((0,2,z)))
    for z in Y:S.add(frozenset((1,2,z)))
    values=sorted(S,key=lambda v:(len(v),tuple(sorted(v))));need(all(frozenset(x) in S for v in S for r in range(len(v)+1) for x in combinations(v,r)),'whole literal downclosure')
    q=k+m;N=(q*q+13*q+16)//2-k;s=3*q+4;h=N-s
    need(len(values)==N and sum(0 in v for v in values)==s,'literal N and largest star')
    stars=[sum(i in v for v in values) for i in range(g)]
    need(stars==[s,s-k,s-k]+[q+5]*k+[q+6]*m and max(stars)==s,'all original star sizes, unique maximum')
    def typ(v):return (sum(1<<i for i in (0,1,2) if i in v),len(v&X),len(v&Y))
    return values,typ,N,s,h

def comparison(data):
    # The source table is q17 defining DATA. We use no q17 numerical theorem.
    need(type(data) is dict and data['q']==17 and data['k']==8 and data['N']==255 and data['s']==55 and data['h']==200 and data['denominator']==32768 and data['free_pair_type_count']==143,'exposed defining-table metadata')
    need(data['parent_PSD_factors_or_floors_used'] is False,'table is definition, no PSD theorem')
    records=data['free_pair_values'];need(type(records) is list and len(records)==143,'complete source143')
    a={};uq=[]
    for row in records:
        need(type(row) is dict and set(row)=={'types','numerator'} and type(row['numerator']) is int and row['numerator']%31==0,'exact integer31 division')
        labels=row['types'];need(type(labels) is list and len(labels)==2 and all(type(v) is list and len(v)==3 and all(type(j) is int for j in v) for v in labels),'all exact type triples')
        t,u=map(tuple,labels);need(t<=u and (t,u) not in a,'canonical complete type pair')
        v=row['numerator']//31;a[t,u]=Q(29*v,32768);uq.append([list(t),list(u),v])
    sets,typ,N,s,h=carrier(9,10);proper=sets[1:];star=[i for i,v in enumerate(proper) if 0 in v];B=[i for i,v in enumerate(proper) if 0 not in v];anchor=proper.index(frozenset((0,)));other=[i for i in range(N-1) if i!=anchor]
    C=[[Q(0)]*(N-1) for _ in proper];seen=set()
    for i in range(N-1):
        C[i][i]=Q(s-1)
        for j in range(i):
            if proper[i]&proper[j]:v=Q(-1)
            elif anchor in (i,j):continue
            else:
                key=tuple(sorted((typ(proper[i]),typ(proper[j]))));need(key in a,'all literal free original pair types');seen.add(key);v=a[key]
            C[i][j]=C[j][i]=v
    need(seen==set(a),'all143 defining pairs occur on current carrier')
    for i in B:C[i][anchor]=C[anchor][i]=-sum(C[i][j] for j in star if j!=anchor)
    need(all(sum(row[j] for j in star)==0 for row in C),'all proper centered-star rows, comparison only')
    budgets=[1-sum(row) for row in C];loop=1+sum(sum(row) for row in C)-s
    need(loop==h-s-sum(budgets[i] for i in B),'actual loop from full proper double sum')
    K=[i for i in B if budgets[i]<0];G=set(B)-set(K);kt={typ(proper[i]) for i in K}
    need(kt=={(0,0,2),(2,0,1),(4,0,1),(6,0,1)} and len(K)==75,'exact current bad set, not parent counts')
    ell={}
    for i in B:
        t=typ(proper[i]);need(t not in ell or ell[t]==budgets[i],'every individual original budget equals typed value');ell[t]=budgets[i]
    deficits=[-ell[t] for t in ((0,0,2),(2,0,1),(4,0,1),(6,0,1))];D=-sum(budgets[i] for i in K);P0=(D-loop)/2
    edges=[];counts={'KK':0,'KG':0,'GG':0};groups={};kkroles={};Kset=set(K)
    for i,j in combinations(B,2):
        if proper[i]&proper[j]:continue
        cat='KK' if i in Kset and j in Kset else 'KG' if (i in Kset)!=(j in Kset) else 'GG';cap=1+C[i][j];need(cap>=0,'all current nonstar capacities nonnegative');counts[cat]+=1
        edges.append([i,j,cat,str(cap)])
        if cat!='GG':
            weight=Q(1) if cat=='KK' else Q(1,2);groups[cap]=groups.get(cap,Q(0))+weight
        if cat=='KK':
            ti,tj=typ(proper[i]),typ(proper[j]);key=tuple(sorted((ti,tj)));need(key not in kkroles or kkroles[key]==cap,'every original KK capacity is uniform');kkroles[key]=cap
    caps=[kkroles[key] for key in [((0,0,2),(0,0,2)),((0,0,2),(2,0,1)),((0,0,2),(4,0,1)),((0,0,2),(6,0,1)),((2,0,1),(4,0,1))]]
    need(deficits==[Q(362147,32768),Q(10683,32768),Q(10683,32768),Q(13379,16384)],'fresh exact deficits')
    need(caps==[Q(84533,32768),Q(17921,16384),Q(17921,16384),Q(19371,16384),Q(25083,32768)],'fresh all five KK caps')
    need(counts=={'KK':1800,'KG':10820,'GG':11245} and len(edges)==23865,'whole individual NN edge partition')
    need(D==Q(16777855,32768) and loop==Q(2089103,8192) and P0==Q(8421443,65536),'fresh D/actual loop/P0')
    # Closed endpoint flow interpolation proves the entire one-dimensional interval.
    ts=[Q(0),caps[4]];flows=[];eq=[]
    for tau in ts:
        flows.append(check_literal(10,deficits,caps,tau));e=equal_interval(10,[deficits[0],deficits[1],deficits[3]],[caps[0],caps[1],caps[3],caps[4]],tau);eq.append({k:[str(z) for z in v] if isinstance(v,list) else str(v) for k,v in e.items()})
    # Beyond cap[4] a nonnegative B/C decrement cannot fit its negative cap.
    need(caps[4]>0 and all(x['edges']==1800 for x in flows),'flow endpoints and exact obstruction')
    # Full piecewise linear envelope: every KK/KG individual edge retained.
    def envelope(tau):return P0+38*tau+sum(w*max(Q(0),tau-c) for c,w in groups.items())
    def envdirect(tau):return P0+38*tau+sum((Q(1) if cat=='KK' else Q(1,2))*max(Q(0),tau-Q(cap)) for i,j,cat,cap in edges if cat!='GG')
    breakpoints=sorted(groups);pieces=[];intercept=P0;slope=Q(38)
    lo=Q(0)
    for hi in breakpoints+[None]:
        for x in [lo]+([] if hi is None else [hi]):need(envelope(x)==envdirect(x)==intercept+slope*x,'whole piecewise boundary and individual envelope')
        pieces.append(dict(lo=str(lo),hi=None if hi is None else str(hi),intercept=str(intercept),slope=str(slope)))
        if hi is not None:intercept-=groups[hi]*hi;slope+=groups[hi];lo=hi
    yyx=[e for e in edges if e[2]=='KG' and {typ(proper[e[0]]),typ(proper[e[1]])}=={(0,0,2),(0,1,0)}]
    need(len(yyx)==405 and all(Q(e[3])==Q(3755,8192) for e in yyx),'all405 early KG edges and exact capacity')
    raw=dict(C=[[str(x) for x in row] for row in C],budgets=[str(x) for x in budgets],loop=str(loop),edges=edges,sets=[sorted(x) for x in sets],defining_u=uq)
    b=canon(raw)
    return dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',scope='ONLY original capacity/degree and necessary cost claims of10332; no PSD/witness/attainment/chart verdict',N=N,s=s,h=h,proper=N-1,B=len(B),K=len(K),defining_pairs=143,all_original_star_kernel_rows=True,all_exact31_divisions=True,whole_original_comparison_positions=(N-1)**2,whole_nn_edges=len(edges),edge_partition=counts,deficits=[str(x) for x in deficits],KK_capacities=[str(x) for x in caps],D=str(D),actual_loop=str(loop),P0=str(P0),KK_flow_interval=['0',str(caps[4])],complete_endpoint_flows=flows,source_equal_intervals=eq,early_KG=dict(edges=405,capacity='3755/8192',weight='405/2'),full_envelope_groups=[dict(capacity=str(c),weight=str(w)) for c,w in sorted(groups.items())],full_piecewise_envelope=pieces,whole_original_record_bytes=len(b),whole_original_record_sha256=__import__('hashlib').sha256(b).hexdigest()),raw
