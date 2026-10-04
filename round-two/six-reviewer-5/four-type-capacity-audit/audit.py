"""Generic exact linear elimination; no capacity-interval formula imported."""
from fractions import Fraction as Q
from math import comb
from itertools import combinations
from flow import need,graph,parameters,witness,check_literal,from_orbits,sha

def eliminate(m,d,c,tau):
    n=Q(comb(m-1,2));p=Q(m-2);a=Q(comb(m-2,2));r=Q(m-1)
    rows=[[a,p,p,p,Q(0),d[0]+tau],[Q(0),n,Q(0),Q(0),r,d[1]+tau],[Q(0),Q(0),n,Q(0),r,d[2]+tau],[Q(0),Q(0),Q(0),n,Q(0),d[3]+tau]]
    columns=[0,1,2,3,4] if m>=4 else [1,2,3,4]
    mat=[[row[j] for j in columns]+[row[-1]] for row in rows];pivots=[];k=0
    for j in range(len(columns)):
        ix=next((i for i in range(k,len(mat)) if mat[i][j]),None)
        if ix is None:continue
        mat[k],mat[ix]=mat[ix],mat[k];v=mat[k][j];mat[k]=[x/v for x in mat[k]]
        for i in range(len(mat)):
            if i!=k:
                v=mat[i][j];mat[i]=[x-v*y for x,y in zip(mat[i],mat[k])]
        pivots.append(j);k+=1
    need(k==4,'all four independent demands')
    free=[j for j in range(len(columns)) if j not in pivots];need(len(free)==(1 if m>=4 else 0),'exact nullity')
    terms={}
    for i,j in enumerate(pivots):terms[columns[j]]=(mat[i][-1],-mat[i][free[0]] if free else Q(0))
    if free:terms[columns[free[0]]]=(Q(0),Q(1))
    lo=[];hi=[];possible=True
    for j,(v,slope) in terms.items():
        U=c[j]-tau
        if slope>0:lo.append(-v/slope);hi.append((U-v)/slope)
        elif slope<0:lo.append((U-v)/slope);hi.append(-v/slope)
        else:possible &= 0<=v<=U
    if free:
        need(columns[free[0]]==4,'independent free variable eta');lower=max(lo);upper=min(hi);possible &=lower<=upper
    else:lower=upper=terms[4][0]
    return bool(possible),lower,upper,terms

def incidences(m):
    vs,es=graph(m);rows=[[0]*5 for _ in vs]
    for i,j,r in es:rows[i][r]+=1;rows[j][r]+=1
    a=comb(m-2,2);p=m-2;n=comb(m-1,2)
    expected={'YY':[a,p,p,p,0],'B':[0,n,0,0,m-1],'C':[0,0,n,0,m-1],'BC':[0,0,0,n,0]}
    need(all(row==expected[t] for (t,ys),row in zip(vs,rows)),'all original individual orbit incidences')
    return dict(m=m,vertices=len(vs),edges=len(es),all_incidence_record_sha256=sha(rows))

def run():
    inputs=[];records=[];inc=[incidences(m) for m in range(3,13)]
    for m in (3,4,5,7,10):
        tau=Q(1,16);values=[Q(0) if m==3 else Q(1,8),Q(1,4),Q(1,2),Q(3,4),Q(1,8)]
        c=[Q(-100) if m==3 else Q(1,2),Q(1,2),Q(3,4),Q(1),Q(1,4)]
        seed=from_orbits(m,values,c,tau);d=[Q(x) for x in seed['demands']]
        ok,lo,hi,terms=eliminate(m,d,c,tau);v=parameters(m,d,c,tau)
        need(ok and (lo,hi)==(v['lo'],v['hi']),'generic elimination equals full closed feasible interval')
        for eta in sorted(set([lo,(lo+hi)/2,hi])):records.append(check_literal(m,d,c,tau,eta))
        inputs.append(dict(m=m,d=[str(x) for x in d],c=[str(x) for x in c],tau=str(tau)))
        for j in (1,2,3,4):
            cb=c[:];cb[j]=tau-Q(1,100);ok2,low2,high2,term2=eliminate(m,d,cb,tau);v2=parameters(m,d,cb,tau)
            need(not ok2 and not (0<=v2['beta']<=v2['U'][3] and v2['lo']<=v2['hi']),'actual negative-edge-cap obstruction agrees')
        # A positive-capacity obstruction: insufficient YY/B capacity for its demand.
        cb=c[:];cb[1]=tau;cb[4]=tau;ok2,*_=eliminate(m,d,cb,tau);v2=parameters(m,d,cb,tau)
        need(not ok2 and v2['lo']>v2['hi'],'no-flow nonnegative-capacity obstruction')
    # Necessity for individual non-invariant real flows is ordinary group averaging.
    # Show a nonuniform exact flow whose averages recover the same degrees.
    m=4;seed=inputs[1];d=list(map(Q,seed['d']));c=list(map(Q,seed['c']));tau=Q(seed['tau']);vals,v=witness(m,d,c,tau,Q(1,8));vs,es=graph(m);weights=[vals[r] for i,j,r in es]
    lookup={frozenset((i,j)):z for z,(i,j,r) in enumerate(es)};B={ys[0]:i for i,(t,ys) in enumerate(vs) if t=='B'};C={ys[0]:i for i,(t,ys) in enumerate(vs) if t=='C'}
    # B0-C2-B1-C3-B0 has four allowed edges and alternating circulation.
    cycle=[(B[0],C[2]),(B[1],C[2]),(B[1],C[3]),(B[0],C[3])]
    eps=Q(1,64)
    for z,edge in enumerate(cycle):weights[lookup[frozenset(edge)]]+=eps if z%2==0 else -eps
    deg=[Q(0)]*len(vs);sums=[Q(0)]*5;counts=[0]*5
    for (i,j,r),x in zip(es,weights):need(0<=x<=c[r]-tau,'individual nonuniform capacities');deg[i]+=x;deg[j]+=x;sums[r]+=x;counts[r]+=1
    need(any(weights[z]!=vals[r] for z,(i,j,r) in enumerate(es)) and all(value==d[{'YY':0,'B':1,'C':2,'BC':3}[t]]+tau for (t,ys),value in zip(vs,deg)),'nonuniform individual demands')
    need([sums[r]/counts[r] for r in range(5)]==vals,'exact full orbit means')
    return dict(incidence_counts=inc,unequal_inputs=inputs,closed_endpoint_records=records,nonuniform_flow=dict(m=m,cycle_size=4,epsilon=str(eps),entire_record_sha256=sha([[i,j,r,str(x)] for (i,j,r),x in zip(es,weights)])),generic_elimination_cases=30,feasible_unequal_instances=5,absent_YY_edge_cap_ignored_at_m3=True,unbounded_real_extension='ordinary S_m averaging and exact Gaussian degree elimination, not enumeration')
