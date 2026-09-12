"""Definition-level physical exchange, CNF and catalogue destination controls."""
from itertools import combinations, product
from pathlib import Path
from math import comb
import json
from exchange import need, decode, encode, clique, validate, violations, descend, receiver_clauses
from catalog import obtain, adjacency, Lookup, isomorphism
from destination import normalize


def literal_exchange_controls():
    tested = 0; violations_seen = 0; good_before = 0
    # Every three-vertex core, both block colors, every proper star word.
    for core_bits in range(8):
        C = [[0]*3 for _ in range(3)]
        for k, (u,v) in enumerate(combinations(range(3),2)):
            C[u][v] = C[v][u] = (core_bits >> k)&1
        for color in (0,1):
            offset = 0 if color else 20
            physical = list(range(offset,offset+4))+[40,41,42]
            inverse = {v:i for i,v in enumerate(physical)}
            variables = {i+1:(u,v) for i,(u,v) in enumerate(combinations(range(43),2))}
            compiled = []
            for clause in receiver_clauses(10,10 if color else 5,C):
                if all(u in inverse and v in inverse for u,v in (variables[abs(x)] for x in clause)):
                    compiled.append([(inverse[variables[abs(x)][0]], inverse[variables[abs(x)][1]], x>0) for x in clause])
            for columns in product(range(15), repeat=3):
                a = [[0]*7 for _ in range(7)]
                for u,v in combinations(range(4),2): a[u][v] = a[v][u] = color
                for v in range(3):
                    for u in range(4): a[u][4+v] = a[4+v][u] = ((columns[v]>>u)&1) if color else 1-((columns[v]>>u)&1)
                for u,v in combinations(range(3),2): a[4+u][4+v] = a[4+v][4+u] = C[u][v]
                red, blue = ([[0,1,2,3]],[]) if color else ([],[[0,1,2,3]])
                core = [4,5,6]; events = list(violations(a,red,blue,core))
                expected = []
                before = sum(a[u][v] for u,v in combinations(core,2))
                for v in core:
                    for w in range(4):
                        newB = sorted((set(range(4))-{w})|{v})
                        if a[v][w] != color and all(a[u][z] == color for u,z in combinations(newB,2)):
                            newC = sorted((set(core)-{v})|{w})
                            after = sum(a[u][z] for u,z in combinations(newC,2))
                            if after > before: expected.append((v,w,after-before))
                need(sorted((x['vertex'],x['displaced'],x['gain']) for x in events) == sorted(expected), 'literal swap')
                # Direct truth of the guarded all-subsets clause, without compiler reuse.
                for v0,v in enumerate(core):
                    for w in range(4):
                        guard = a[v][w] != color and all(a[v][u] == color for u in range(4) if u != w)
                        bad = any(guard and all(a[w][u] for u in S)
                                  for S in combinations([u for u in core if u != v], sum(C[v0])+1))
                        need(bad == any(e[0:2] == (v,w) for e in expected), 'cardinality clauses')
                need(all(any(bool(a[u][v]) == sign for u,v,sign in clause) for clause in compiled) == (not events), 'actual emitted clauses')
                tested += 1; violations_seen += bool(events)
                # Isomorphism-free positive Ramsey transport controls at small order.
                if events and clique(a,range(7),5,0) is None and clique(a,range(7),5,1) is None:
                    e=events[0]; p=list(range(7));p[e['vertex']],p[e['displaced']]=p[e['displaced']],p[e['vertex']]
                    transported=decode(encode(a,p))
                    need(clique(transported,range(7),5,0) is None and clique(transported,range(7),5,1) is None,'small Ramsey preservation')
                    good_before += 1
    return dict(literal_assignments=tested, assignments_with_exchange=violations_seen,
                genuine_small_Ramsey_transports=good_before)


def template(C, q, r, violate):
    a = [[0]*43 for _ in range(43)]
    red=[list(range(4*b,4*b+4)) for b in range(r)]
    blue=[list(range(4*b,4*b+4)) for b in range(r,q)]
    core=list(range(4*q,43))
    for B in red:
        for u,v in combinations(B,2):a[u][v]=a[v][u]=1
    for u,v in combinations(range(len(C)),2):a[core[u]][core[v]]=a[core[v]][core[u]]=C[u][v]
    if violate:
        v0=min(range(len(C)),key=lambda v:sum(C[v]));d=sum(C[v0])
        need(d<len(C)-1,'non-complete core')
        v=core[v0];w=0
        for u in (1,2,3):a[u][v]=a[v][u]=1
        for t in [u for u in core if u!=v][:d+1]:a[w][t]=a[t][w]=1
    validate(a,red,blue,core)
    return a,red,blue,core


def run(data):
    small=literal_exchange_controls(); lines=obtain(data);lookup=Lookup(data)
    transports=0;positive_moves=0;max_steps=0;destinations=set();repair_kinds=set();literal_pairs=0
    fixtures=[]
    for q in range(7,11):
        n=43-4*q
        # All macro strata are exercised; these are interface controls, not coverage evidence.
        C=adjacency(next(raw for raw in lines[n] if min(map(sum,adjacency(raw)))<n-1))
        for r in range(5,q+1):
            for violate in (False,True):
                a,red,blue,core=template(C,q,r,violate)
                out=descend(a,red,blue,core);dest=normalize(a,out,lookup)
                p=dest['new_to_old'];aa=decode(dest['graph'])
                need(all(aa[u][v]==a[p[u]][p[v]] for u,v in combinations(range(43),2)),'all-pair transport')
                literal_pairs+=903
                if dest['physical_five_in_input_labels']:
                    b=dest['physical_five_in_input_labels'];need(all(a[u][v]==b['color'] for u,v in combinations(b['vertices'],2)),'literal rejection')
                need(not list(violations(a,out['red'],out['blue'],out['core'])),'final predicate')
                if violate:need(out['steps'],'forced move')
                positive_moves+=bool(out['steps']);max_steps=max(max_steps,len(out['steps']));destinations.add(dest['task'])
                for e in out['steps']:
                    change='r' if e['after'][0]>e['before'][0] else 'q' if e['after'][1]>e['before'][1] else 'core_edges'
                    repair_kinds.add(change)
                transports+=1
                if q==10 and r==10:fixtures.append(dict(encode(a),red=red,blue=blue,core=core))
    # Two explicit C7 controls exercise q-growth and the inherited augmentation branch.
    C = [[int((u-v)%7 in (1,6)) for v in range(7)] for u in range(7)]
    for kind in ('q_growth','augmentation'):
        a,red,blue,core=template(C,9,9,False)
        if kind=='q_growth':
            for w in (1,2,3): a[w][36]=a[36][w]=1
            for v in (38,40,42): a[0][v]=a[v][0]=1
        else:
            for w in (0,1):
                for v in (36,37): a[w][v]=a[v][w]=1
            for w in (2,3):
                for v in (39,40): a[w][v]=a[v][w]=1
        validate(a,red,blue,core);out=descend(a,red,blue,core);dest=normalize(a,out,lookup)
        need(out['steps'],'explicit branch move')
        first=out['steps'][0]
        need(first['after'][1]>first['before'][1], 'q growth')
        need((first['kind']=='TWO_EDGE_AUGMENTATION')==(kind=='augmentation'),'branch identity')
        p=dest['new_to_old'];aa=decode(dest['graph'])
        need(all(aa[u][v]==a[p[u]][p[v]] for u,v in combinations(range(43),2)),'explicit transport')
        for e in out['steps']:
            repair_kinds.add('r' if e['after'][0]>e['before'][0] else 'q' if e['after'][1]>e['before'][1] else 'core_edges')
        transports+=1;positive_moves+=1;literal_pairs+=903
        max_steps=max(max_steps,len(out['steps']));destinations.add(dest['task'])
        fixtures.append(dict(encode(a),red=red,blue=blue,core=core))
    # All order-3/7 catalogue graphs under a fixed nontrivial relabeling, plus endpoints at 11/15.
    iso_checked=0
    for n,rows in lines.items():
        selected=range(len(rows)) if n<=7 else (0,len(rows)//2,len(rows)-1)
        for i in selected:
            C=adjacency(rows[i]);p=list(reversed(range(n)));D=[[C[p[u]][p[v]] for v in range(n)] for u in range(n)]
            m=isomorphism(D,C);need(m is not None,'permuted catalogue isomorphism')
            need(all(D[m[u]][m[v]]==C[u][v] for u,v in combinations(range(n),2)),'literal map');iso_checked+=1
    # Full actual clause lists for every order-3 core and every q10 stratum.
    clause_count=0
    for raw in lines[3]:
        C=adjacency(raw)
        for r in range(5,11):
            clauses=list(receiver_clauses(10,r,C))
            expected=40*sum(comb(2,sum(row)+1) for row in C if sum(row)+1<=2)
            need(len(clauses)==expected,'clause count')
            need(all(all(1<=abs(v)<=903 for v in cl) and len(set(cl))==len(cl) for cl in clauses),'clause vocabulary')
            clause_count+=len(clauses)
    result=dict(status='PHYSICAL_EXCHANGE_AND_RECEIVER_CONTROLS_VERIFIED',**small,
                complete43_transports=transports, forced_descent_cases=positive_moves, maximum_control_steps=max_steps,
                potential_increase_branches=sorted(repair_kinds), normalized_destinations=len(destinations),
                physical_pair_identities=literal_pairs, exact_catalogue_isomorphism_controls=iso_checked,
                emitted_q10_clauses=clause_count, fixtures_are_good43=False,
                control_scope='Finite controls validate implementation; unrestricted coverage is the written potential proof')
    return result,fixtures

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('out');a=p.parse_args()
    result,fixtures=run(a.data)
    Path(a.out).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    Path(a.out).with_name('FIXTURES.json').write_text(json.dumps(fixtures,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
