"""Post-seal physical wedge, graph-scope and corruption checks."""
import copy
from itertools import combinations
from math import comb
import rows,oracle


def moore(adjacency):
    n=len(adjacency)
    rows.need(n>0 and all(len(s)==3 for s in adjacency),'nonempty cubic graph')
    rows.need(all(all(type(q)==int and 0<=q<n and q!=p and p in adjacency[q] for q in ns) for p,ns in enumerate(adjacency)),'actual simple undirected graph')
    rows.need(all(not(adjacency[a]&adjacency[b]) for a in range(n) for b in adjacency[a]),'no triangle')
    rows.need(all(len(adjacency[a]&adjacency[b])<2 for a,b in combinations(range(n),2)),'no square')
    for p in range(n):
        children=[v for q in adjacency[p] for v in adjacency[q]-{p}]
        rows.need(len(children)==len(set(children))==6 and p not in children and not(set(children)&adjacency[p]),'actual three/six distinct point layers')
    rows.need(n>=10,'ordinary classical Moore bound')


def compute(stars,proof):
    # The independently frozen JSON carrier decodes tuple pairs/categories
    # as lists. Restore exactly these representation-only tuples before
    # calling the unchanged sealed literal oracle, and verify a positive
    # undamaged control before any rejection tests.
    proof=copy.deepcopy(proof)
    for r in proof['rows']:r['high_edges']=[tuple(edge) for edge in r['high_edges']]
    for branch in proof['boundaries']:branch['categories']=[tuple(c) for c in branch['categories']]
    oracle.compute(stars,proof)
    coefficients=[]
    for m in range(1,6):
        n=18-m;B=4*n-comb(n,3)-120*m+740;w0=20+10*m-5*m*m
        coefficients.append({'m':m,'n':n,'B':B,'w0':w0,'C':w0-2*B})
    rows.need([v['C'] for v in coefficients]==[9,12,35,76,133],'all corrected global coefficients')
    rows.need(all(comb(5-j,3)==10-6*j+3*comb(j,2)-comb(j,3) for j in range(6)),'all physical word hub counts')
    tuples=[]
    # Independent literal integer arithmetic from inequalities at P34;
    # finite ranges follow the nonnegative slack3, Q>=4N5 and T>=1.
    for N5 in range(2):
        for T in range(1,3):
            for X in range(3):
                for tau in range(2):
                    for Q in range(6):
                        if Q>=4*N5 and 2*T+2*X+4*tau+Q-N5<=3:tuples.append([N5,T,X,tau,Q])
    rows.need(tuples==[[0,1,0,0,0],[0,1,0,0,1]],'complete global boundary arithmetic')
    wedges=[]
    for r in proof['rows']:
        if (r['e'],r['k'],r['q'],r['sigma'])!=(1,1,0,0):continue
        hub=r['hubs'][0];sat=set(r['high'])-{hub}
        rows.need(r['delta'][hub]==2 and len(sat)==3 and all(r['delta'][p]==1 for p in sat),'actual2111 role projection')
        rows.need(set(map(frozenset,r['high_edges']))=={frozenset(t) for t in combinations(sat,2)},'complete physical neighbor wedge triangle')
        star=stars[r['star']]
        rows.need(all(not any(set(t)<=set(w) for w in star) for t in combinations(sat,2)),'allthree actual unowned neighbor pairs')
        wedges.append([r['star'],hub,sorted(sat)])
    rows.need(wedges,'nonvacuous physical cubic-role controls')
    missing=[r for r in proof['rows'] if r['e']==4 and r['k']==1 and r['sigma']==0]
    rows.need(len(missing)==1 and missing[0]['margin']==9,'genuine missing-link-point retained and budget-excluded')
    labels=[]
    def reject(label,fn):
        try:fn()
        except ValueError:labels.append(label);return
        raise ValueError('damaged input accepted: '+label)
    for label,edit in [
        ('missing quad',lambda x:x[0].pop()),
        ('duplicate quad',lambda x:x[0].__setitem__(1,x[0][0])),
        ('out of range point',lambda x:x[0][0].__setitem__(0,17)),
        ('boolean point',lambda x:x[0][0].__setitem__(0,True)),
        ('repeated point',lambda x:x[0][0].__setitem__(1,x[0][0][0]))]:
        damaged=copy.deepcopy(stars);edit(damaged);reject(label,lambda:rows.marks(damaged))
    for label,edit in [
        ('deleted actual five-hub exceptions',lambda p:p.__setitem__('rows',[r for r in p['rows'] if r['I5']==0])),
        ('wrong actual hub',lambda p:p['rows'][1]['hubs'].__setitem__(0,16)),
        ('wrong q',lambda p:p['rows'][0].update(q=1)),
        ('wrong eligibility',lambda p:p['rows'][0].update(eligible=True)),
        ('consistent wrong psi and margin',lambda p:p['rows'][0].update(psi=1,margin=1)),
        ('erased I5 correction',lambda p:next(r for r in p['rows'] if r['I5']).update(I5=0)),
        ('wrong saturated excess',lambda p:p['rows'][0].update(sigma=1)),
        ('deleted unique boundary pattern',lambda p:p['boundaries'][1].update(complete_population_vectors=[])),
        ('truncated boundary category',lambda p:p['boundaries'][0]['categories'].pop())]:
        damaged=copy.deepcopy(proof);edit(damaged);reject(label,lambda:oracle.compute(stars,damaged))
    reject('uncorrected wider scope',lambda:rows.need(all(r['old_margin']>=0 for r in proof['rows']),'actual eight countermarks'))
    reject('missing-point silently omitted',lambda:rows.need(all(max(r['delta'])<5 for r in proof['rows']),'actual absent point'))
    reject('empty closed graph',lambda:moore([]))
    reject('triangle allowed',lambda:moore([set(range(4))-{p} for p in range(4)]))
    reject('four-cycle allowed',lambda:moore([set(range(3,6))]*3+[set(range(3))]*3))
    # New maps selected separately from author maps: literal relabellings,
    # no given automorphism group/quotient filter is used.
    transports=[]
    for perm in ([16]+list(range(1,16))+[0],[(p+4)%17 for p in range(17)],[(7*p+3)%17 for p in range(17)]):
        inverse=[perm.index(p) for p in range(17)]
        moved=[[[perm[p] for p in w] for w in star] for star in stars]
        fresh=rows.marks(moved)
        for r in fresh:
            for field in ['hubs','high']:r[field]=sorted(inverse[p] for p in r[field])
            r['delta']=[r['delta'][perm[p]] for p in range(17)]
            r['high_edges']=sorted(tuple(sorted(inverse[p] for p in edge)) for edge in r['high_edges'])
        fresh.sort(key=lambda r:(r['star'],r['k'],r['hubs']))
        rows.need(fresh==proof['rows'],'every actual transported mark field after inverse coordinates')
        rows.need(rows.boundaries(fresh)==proof['boundaries'],'whole transported boundary census')
        transports.append(list(perm))
    # Additional exact graph certificate: every triangle-free six-point
    # cubic pattern has six nonedge pairs with three distinct common
    # neighbors, hence six independent unique-low-neighbor violations.
    violations=[];edges=list(combinations(range(6),2))
    for chosen in combinations(edges,9):
        adjacent=[set() for _ in range(6)]
        for a,b in chosen:adjacent[a].add(b);adjacent[b].add(a)
        if any(len(s)!=3 for s in adjacent) or any(adjacent[a]&adjacent[b] for a,b in chosen):continue
        witnesses=[(a,b,sorted(adjacent[a]&adjacent[b])) for a,b in edges if b not in adjacent[a]]
        rows.need(len(witnesses)==6 and all(len(c)==3 for a,b,c in witnesses),'all actual same-part triple common-neighbor witnesses')
        violations.append({'edges':chosen,'nonedge_witnesses':witnesses})
    rows.need(len(violations)==10,'allten abstract trianglefree cubic patterns have explicit violations')
    return {'coefficients':coefficients,'whole_boundary_integer_tuples':tuples,'physical2111_wedge_rows':len(wedges),'missing_point_row_retained_margin9':True,'semantic_damage_checks':len(labels),'rejected_labels':labels,'three_actual_point_maps':transports,'transported_whole_rows':1278,'explicit_unique_low_neighbor_nonedge_witnesses':sum(len(v['nonedge_witnesses']) for v in violations),'all10_six_point_patterns':violations,'scope':'Abstract necessary graph obstruction and literal local wedges, no hypothetical packing construction/whole-classification/stronger global endpoint.'}
