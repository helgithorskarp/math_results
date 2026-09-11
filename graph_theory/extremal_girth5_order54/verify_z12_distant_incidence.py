#!/usr/bin/env python3
"""Exact certificate replay and finite controls for z12_distant_incidence_bound.md.

Standard library only. The written proof gives whole-subclass coverage;
these controls do not enumerate all order-54 graphs.
"""
import copy
import hashlib
import json
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
from forest_constraints import model
from verify import require, graph, local_types, hoffman_singleton_edges

HERE = Path(__file__).resolve().parent


def reconstructed_model():
    """Independently fill columns from the mathematical variable meanings."""
    types = list(local_types())
    edges = [(i,j) for i in range(len(types)) for j in range(i,len(types))
             if types[i][1][types[j][0]-6] and types[j][1][types[i][0]-6]]
    nt = len(types)
    sizes = (16,26,12)
    pairs = list(combinations(range(3),2))
    eq = [{} for _ in range(6+3*nt)]
    ub = [{} for _ in range(6+3*nt)]
    erhs = list(sizes)+[0]*(3+3*nt)
    urhs = [sizes[j]*(sizes[j]-1) for j in range(3)]
    urhs += [sizes[j]*sizes[k] for j,k in pairs]+[0]*(3*nt)
    def add(rows,r,i,value):
        if value:
            rows[r][i] = rows[r].get(i,0)+value
    for i,(d,ns) in enumerate(types):
        add(eq,d-6,i,1)
        for p,(j,k) in enumerate(pairs):
            add(eq,3+p,i,(d==j+6)*ns[k]-(d==k+6)*ns[j])
        for j in range(3):
            add(eq,6+3*i+j,i,-ns[j])
            add(ub,j,i,ns[j]*(ns[j]-1)+(d==j+6)*ns[j])
            add(ub,6+3*i+j,i,ns[j]-sizes[j]-(d-1)*(d==j+6))
        for p,(j,k) in enumerate(pairs):
            add(ub,3+p,i,ns[j]*ns[k]+(d==j+6)*ns[k])
    for col,(i,j) in enumerate(edges,nt):
        for root,neighbor in ([(i,j)] if i==j else [(i,j),(j,i)]):
            nd,nc = types[neighbor]
            add(eq,6+3*root+nd-6,col,1)
            for k in range(3):
                add(ub,6+3*root+k,col,nc[k])
    return types,edges,eq,erhs,ub,urhs


def certificate(data=None):
    data = copy.deepcopy(data) if data is not None else json.loads(
        (HERE/'z12_four_defects_certificate.json').read_text())
    standard = model((16,26,12),edge_bounds=False)
    rebuilt = reconstructed_model()
    for a,b in zip(standard,rebuilt):
        if a and isinstance(a[0],dict):
            a = [{i:v for i,v in row.items() if v} for row in a]
        require(a==b,'independent model reconstruction mismatch')
    types,edges,eq,erhs,ub,urhs = rebuilt
    eq.append({i:5-ns[1]-2*ns[2] for i,(d,ns) in enumerate(types) if d==8})
    erhs.append(4)
    dimensions = [len(types),len(edges),len(eq),len(ub)]
    require(dimensions == [72,1638,223,222] == data['dimensions'],'dimensions')
    require(data['sizes']==[16,26,12] and data['total_high_far_count']==4,'scope')
    require(type(data['denominator']) is int and data['denominator']>0,'denominator')
    n = len(types)+len(edges)
    coefficients = [Fraction(0)]*n
    rhs = Fraction(0)
    for key,rows,bs in [('equality_multipliers',eq,erhs),
                        ('inequality_multipliers',ub,urhs)]:
        seen = set()
        for entry in data[key]:
            require(isinstance(entry,list) and len(entry)==2,'multiplier shape')
            i,a = entry
            require(type(i) is int and 0<=i<len(rows) and i not in seen,'row index')
            require(type(a) is int,'integer numerator')
            require(key=='equality_multipliers' or a<=0,'inequality sign')
            seen.add(i)
            mul = Fraction(a,data['denominator'])
            rhs += mul*bs[i]
            for j,value in rows[i].items():
                coefficients[j] += mul*value
    objective = [Fraction(0)]*n
    for i,(d,ns) in enumerate(types):
        if d==8:
            objective[i] = Fraction(ns[2],2)
    error = max([Fraction(0)]+[coefficients[i]-objective[i] for i in range(n)])
    require(data['variable_budget']==428,'variable budget')
    bound = rhs-428*error
    require(rhs==Fraction(data['uncorrected_bound'])==Fraction(981743,500000),'rhs')
    require(error==Fraction(data['max_coefficient_error'])==Fraction(11,500000),'error')
    require(bound==Fraction(data['corrected_bound'])==Fraction(195407,100000)
            and bound>1,'strict lower bound')
    high = [(ns[1]+2*ns[2],ns[2]) for d,ns in types if d==8]
    return {'dimensions':dimensions,'columns_checked':n,
            'nonsink_high_types_retained':sum(s<5 for s,h in high),
            'coefficient_rhs':str(rhs),'max_coefficient_excess':str(error),
            'corrected_m_lower_bound':str(bound),
            'certificate_sha256':hashlib.sha256(
                (HERE/'z12_four_defects_certificate.json').read_bytes()).hexdigest()}


def corrupted_certificates():
    data = json.loads((HERE/'z12_four_defects_certificate.json').read_text())
    variants = []
    x = copy.deepcopy(data);x['inequality_multipliers'][0][1]=1;variants.append(x)
    x = copy.deepcopy(data);x['equality_multipliers'][0][1]+=1000;variants.append(x)
    x = copy.deepcopy(data);x['total_high_far_count']=3;variants.append(x)
    x = copy.deepcopy(data);x['equality_multipliers'].append(x['equality_multipliers'][0]);variants.append(x)
    for x in variants:
        try:
            certificate(x)
        except ValueError:
            pass
        else:
            raise ValueError('corrupted certificate accepted')
    return len(variants)


def partitions(n,lower=1):
    if not n:
        yield ()
    for k in range(lower,n+1):
        for tail in partitions(n-k,k):
            yield (k,)+tail


def local_and_coverage_checks():
    count = 0
    negatives = set()
    for d in (6,7):
        for c in range(d+1):
            phi = (c-3)*(c-2)//2 if d==6 else (c-1)*(c-2)//2
            require(phi>=0,'inventory sign')
            for b in range(d-c+1):
                eps = b+2*c-(8 if d==6 else 7)
                gap = eps*eps if d==6 else eps*(eps-1)
                require(gap>=max(-eps,0),'negative epsilon budget')
                if d==6:
                    require((c-3)*eps>=0,'six sign')
                    if c==4:require(eps>=0,'four-set far capacity')
                elif (c-3)*eps<0:negatives.add((c,eps))
                if gap==max(-eps,0) and eps<0:
                    require(d==6 and eps==-1,'negative-budget equality case')
                count += 1
    require(negatives=={(1,1),(2,1),(2,2)},'negative types')
    high_checks = 0
    for a,h in product(range(6),range(3)):
        if 5-a-2*h<0:continue
        require(h*a<=a+(h==2),'R upper bound')
        require(a*(a+4)>=5*a,'high gap floor')
        high_checks += 1
    deficits = {str(A):[list(p) for p in partitions(A)
                       if sum(a*(a+4) for a in p)<=28] for A in range(7)}
    require(deficits['4']==[[1,1,1,1],[1,1,2],[1,3],[2,2]],'A4 coverage')
    require(deficits['5']==[[1,1,1,1,1],[1,1,1,2]],'A5 coverage')
    require(not deficits['6'],'A>=6 gap exclusion')
    a5_cases=[]
    for m in range(1,4):
        for k in range(4-m):
            B=3-m-k;lower=22-2*m-k;upper=9*B
            require(lower>upper,'A5 m>=1 coverage')
            a5_cases.append([m,k,lower,upper])
    require(2*(9+3)<27,'A5 m0')
    a4_reduced=[]
    for m in range(2,5):
        for k in range(5-m):
            for q in range(5-m-k):
                B=4-m-k-q;lower=20-2*m-k+4*q
                if (m,k,q)==(2,0,0):
                    a4_reduced.append([m,k,q]);continue
                require(B<=2 and lower>9*B,'A4 inventory reduction')
    require(a4_reduced==[[2,0,0]],'unique A4 inventory')
    # Exact equality chain after the individual set argument has forced b1=0.
    states=[]
    for deficit in deficits['4']:
        highgap=sum(a*(a+4) for a in deficit)
        for p7 in range(3):
            for Q in range(max(-1,28-highgap-4*p7)+1):
                for N in range(Q+1):
                    P=8+N
                    for b2 in range(16+p7,P+1):
                        states.append([deficit,p7,Q,N,P,b2])
    require(states==[[[1,1,1,1],0,8,8,16,16]],'equality chain coverage')
    for R in range(5):
        for positive in range(10):
            if positive-16==R-20:
                require(R==4 and positive==0,'R equality')
    return {'low_neighbor_compositions':count,'high_types_checked':high_checks,
            'gap_allowed_deficit_multisets':deficits,'A5_m_positive_cases':a5_cases,
            'A4_inventory_survivor':a4_reduced[0],
            'post_incidence_equality_states':states}


def set_checks():
    T=set(range(12));U=set(range(4));V=set(range(4,8));K=set(range(8,12))
    p=8;Z=K-{p}
    # Different singleton complements cannot be high-neighbor triples of
    # distinct vertices; identical triples also identify the vertex.
    for a,b in product(K,repeat=2):
        require(a==b or len((K-{a}) & (K-{b}))==2,'singleton complements')
    cap=[min(2+a,5-a) for a in range(4)]
    require(max(cap)==3,'A1 incidence capacity')
    single=double=0
    # A2 far from U but not V: two further sets must be disjoint triples
    # forming a partition with U and its own pair Y.
    for yt in combinations(sorted(T-U),2):
        Y=set(yt)
        if len(Y&V)>1 or len(Y&Z)>1:continue
        triples=[set(x) for x in combinations(sorted(T-U-Y),3)]
        for L in triples:
            M=T-U-Y-L
            if len(M)!=3:continue
            single+=1
            require(len(L&V)>1 or len(M&V)>1,'A2 unique-four exclusion')
    # A2 far from U and V: the final set may have any size <=3 and may
    # overlap U or V (a nonzero commutator correction is allowed).
    for yt in combinations(sorted(K),2):
        Y=set(yt)
        if len(Y&Z)>1:continue
        for size in range(4):
            for rt in combinations(sorted(T-Y),size):
                R=set(rt)
                if U|V|Y|R!=T:continue
                double+=1
                require(len(R&Z)>1,'A2 two-four exclusion')
    # Terminal high matching: no high-neighbor set of size >=2 avoids
    # both the chosen high vertex and its mate while remaining independent.
    match=[{0,1},{2,3}];terminal=0
    for t in range(4):
        mate=next(iter(next(e for e in match if t in e)-{t}))
        for size in range(2,5):
            for ct in combinations(range(4),size):
                C=set(ct);terminal+=1
                require(t in C or mate in C or any(e<=C for e in match),
                        'terminal missed-vertex obstruction')
    return {'singleton_pairs':16,'A1_capacity_by_high_deficit':cap,
            'A2_one_four_candidate_partitions':single,
            'A2_two_four_cover_candidates':double,
            'terminal_matching_candidate_sets':terminal}


def graph_controls():
    fixture=json.loads((HERE/'lower_bound_54_185.json').read_text())
    base=fixture['edges']
    cases=[('known185',54,base)]
    cases += [('delete_'+str(i),54,[e for j,e in enumerate(base) if i!=j])
              for i in range(len(base))]
    hs=sorted(hoffman_singleton_edges())
    cases += [('delete_0_6',54,[e for i,e in enumerate(base) if i not in (0,6)]),
              ('delete_0_6_69',54,[e for i,e in enumerate(base) if i not in (0,6,69)])]
    cases += [('HS',50,hs),('HS_minus_edge',50,[e for e in hs if e!=(0,1)])]
    ngraphs=equations=corrections=high_nonsinks=0
    correction_values=set()
    first_deletion=None
    for name,n,edges in cases:
        adj=graph(n,edges);degree=list(map(len,adj))
        far=[]
        for v in range(n):
            reached={v}|adj[v]
            for u in adj[v]:reached |= adj[u]
            far.append(set(range(n))-reached)
        for x,y in combinations(range(n),2):
            require(len(adj[x]&adj[y])<=1,'control C4')
            require(y not in adj[x] or not adj[x]&adj[y],'control triangle')
        T={v for v in range(n) if degree[v]==8}
        high_nonsinks += sum(bool(far[t]) for t in T)
        for t in T:
            for v in range(n):
                lhs=(8-degree[v])*(t in adj[v])+sum(t in adj[u] for u in far[v])
                correction=len(far[t]&adj[v])
                require(lhs==8-degree[v]+correction,'corrected high equation')
                equations+=1;corrections+=bool(correction);correction_values.add(correction)
                if not far[t] and degree[v]==8:
                    require(not (far[v]&adj[t]),'missed vertex avoids high sinks')
        # Check the general commutator also when no vertex has degree eight.
        for u in range(n):
            for v in range(n):
                require(len(adj[u]&far[v])-len(far[u]&adj[v])
                        ==(degree[u]-degree[v])*(v not in adj[u]),'general commutator')
        if name=='delete_0':
            first_deletion={'removed_edge':base[0],
                            'high_nonsinks':[[t,len(far[t])] for t in sorted(T) if far[t]]}
        ngraphs+=1
    require(corrections>0 and high_nonsinks>0 and correction_values=={0,1,2,3},
            'controls must exercise corrections zero through three')
    require(first_deletion=={'removed_edge':[0,2],'high_nonsinks':[[50,1],[53,1]]},
            'first deletion diagnostic')
    return {'graphs':ngraphs,'high_vertex_equations':equations,
            'nonzero_correction_entries':corrections,
            'correction_values':sorted(correction_values),
            'high_nonsinks_across_controls':high_nonsinks,
            'first_edge_deletion':first_deletion}


def main():
    result={'theorem':'z12 implies total high distant incidences A<=3',
            'certificate':certificate(),'corrupted_certificates_rejected':corrupted_certificates(),
            'coverage':local_and_coverage_checks(),'individual_sets':set_checks(),
            'actual_graph_controls':graph_controls()}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
