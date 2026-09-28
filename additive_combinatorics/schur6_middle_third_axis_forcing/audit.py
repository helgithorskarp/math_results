"""Compare expanded reduced CNF with every literal modular equation.

No geometric cell builder, axis-edge generator or short-interval Schur-edge
generator is imported. The target variable maps are used only as a numbering
scheme. Auxiliary support variables are eliminated using their verified OR
definitions, and the resulting clause set is compared by mutual subsumption
with the word definition projected at every nonzero modular equation. Literal
doubling projections also contain ternary clauses subsumed by binary clauses.
"""
import argparse
import itertools
import json
from pathlib import Path
from model import encoding, maximal_supports, ELABELS, QLABELS


def audit_clauses(a):
    m,cnf=encoding(a,False);h=(a-1)//2;s=(a-1)//3;n=5*a
    E,Q,P=m['E'],m['Q'],m['P'];positions=set(range(1,s+1))|set(range(a-s,a))
    assert set(E)=={(u,c) for u in range(1,h+1) for c in (0,1,2,3,4,5)}
    assert set(Q)=={(x,c) for x in positions for c in (0,3,4,5)}
    assert set(P)=={(x,c) for x in range(1,s+1) for c in (3,4,5)}
    allvars=[*E.values(),*Q.values(),*P.values()]
    assert len(allvars)==len(set(allvars))==m['variables']
    normalize=lambda cl:tuple(sorted(set(cl)))
    actual={normalize(cl) for cl in cnf};expanded=set();pids=set(P.values())
    definitions=set();choices={}
    for (u,c),p in P.items():
        x,y=Q[u,c],Q[a-u,c];choices[p]=(x,y)
        definitions.update(map(normalize,([p,-x],[p,-y],[-p,x,y])))
    if not definitions<=actual:raise RuntimeError('missing auxiliary definition')
    for cl in actual-definitions:
        if any(abs(v) in pids for v in cl):
            if not all(v<0 and -v in pids for v in cl):raise RuntimeError('unexpected auxiliary use')
            for xs in itertools.product(*(choices[-v] for v in cl)):
                expanded.add(normalize(-x for x in xs))
        else:expanded.add(cl)
    expected=set()
    def onehot(values):
        expected.add(normalize(values))
        expected.update(normalize((-u,-v)) for u,v in itertools.combinations(values,2))
    for u in range(1,h+1):onehot([E[u,c] for c in (0,1,2,3,4,5)])
    for x in sorted(positions):onehot([Q[x,c] for c in (0,3,4,5)])
    def indicator(x,c):
        aa,b=x%a,x%5
        if b==0:return E.get((min(aa,a-aa),c))
        if aa==0:return 'T' if c==(0 if b in (1,4) else 1) else None
        if a<3*aa<2*a:return 'T' if c==2 else None
        qx=aa if b in (1,2) else a-aa
        if c in (3,4,5):return Q[qx,c]
        if c==(0 if b in (1,4) else 1):return Q[qx,0]
        return None
    table={(x,c):indicator(x,c) for x in range(1,n) for c in range(6)}
    pairs=0
    for x in range(1,n):
        for y in range(x,n):
            z=(x+y)%n
            if not z:continue
            pairs+=1
            for c in range(6):
                terms=[table[t,c] for t in (x,y,z)]
                if None in terms:continue
                expected.add(normalize(-v for v in terms if v!='T'))
    def require_implied(clauses,other):
        count=0
        for cl in clauses-other:
            if not any(tuple(sub) in other for size in range(len(cl))
                       for sub in itertools.combinations(cl,size)):
                raise RuntimeError(('no subsuming clause',a,cl))
            count+=1
        return count
    redundant_literal=require_implied(expected,expanded)
    redundant_reduced=require_implied(expanded,expected)
    return dict(axis_factor=a,modulus=n,literal_pairs=pairs,
                distinct_projected_clauses=len(expected),auxiliary_definitions=len(definitions),
                clauses_before_expansion=len(actual),expanded_reduced_clauses=len(expanded),
                subsumed_literal_clauses=redundant_literal,subsumed_reduced_clauses=redundant_reduced,
                status='EXACT_CLAUSE_EQUIVALENCE_BY_SUBSUMPTION')


def audit_small():
    a=7;n=35;model,cnf=encoding(a,False);canonical,canonical_cnf=encoding(a,True)
    assert all(model[k]==canonical[k] for k in ('E','Q','P'))
    def truth_for(e,q):
        truth={v for (u,c),v in model['E'].items() if e[u]==c}
        truth.update(v for (x,c),v in model['Q'].items() if q[x]==c)
        truth.update(v for (u,c),v in model['P'].items() if q[u]==c or q[a-u]==c)
        return truth
    def satisfies(clauses,truth):
        return all(any((lit in truth) if lit>0 else (-lit not in truth) for lit in cl) for cl in clauses)
    def literal_word(e,q):
        E={x:e[min(x,a-x)] for x in range(1,a)}
        Q={0:0,3:2,4:2,**q};row=[-1]
        for x in range(1,n):
            u,b=x%a,x%5
            if b==0:row.append(E[u]);continue
            state=Q[u] if b<=2 else Q[-u%a]
            row.append((0 if b in (1,4) else 1) if state==0 else state)
        return row
    triples=[(x,y,(x+y)%n) for x in range(1,n) for y in range(x,n) if (x+y)%n]
    cases=valid=canonical_valid=0
    for ec in itertools.product(ELABELS,repeat=3):
        e=dict(zip(range(1,4),ec))
        for qc in itertools.product(QLABELS,repeat=4):
            q=dict(zip((1,2,5,6),qc));row=literal_word(e,q);truth=truth_for(e,q)
            expected=all(not row[x]==row[y]==row[z] for x,y,z in triples)
            actual=satisfies(cnf,truth)
            if actual!=expected:raise RuntimeError(('literal mismatch',e,q,expected,actual))
            cases+=1
            if not expected:continue
            valid+=1;has_representative=False
            for perm in itertools.permutations((3,4,5)):
                relabel={0:0,1:1,2:2,**dict(zip((3,4,5),perm))}
                eq={u:relabel[c] for u,c in e.items()};qq={x:relabel[c] for x,c in q.items()}
                for swap in (False,True):
                    ee={u:(1-c if swap and c in (0,1) else c) for u,c in eq.items()}
                    if satisfies(canonical_cnf,truth_for(ee,qq)):
                        has_representative=True;break
                if has_representative:break
            if not has_representative:raise RuntimeError(('normal form lost',e,q))
            canonical_valid+=1
    report=dict(status='REDUCED_REFLECTED_ENCODING_AUDIT_OK',axis_factor=a,
                complete_assignments=cases,valid_assignments=valid,
                valid_assignments_with_canonical_representative=canonical_valid)
    return report


def audit_axis(a):
    I = {x for x in range(a) if a < 3*x < 2*a}
    diff = {(x-y) % a for x in I for y in I}
    allowed = [u for u in range(1, (a+1)//2) if u not in diff]
    J = set(allowed) | {a-u for u in allowed}
    edges = {tuple(sorted({min(t, a-t) for t in (x, y, (x+y) % a)}))
             for x in J for y in J if (x+y) % a in J}
    m = (a-1)//3
    expected_edges = set() if a % 3 == 2 else {(m, m+1)}
    if edges != expected_edges:
        raise RuntimeError(('unexpected colour2 edge', a, edges))
    supports = maximal_supports(a)
    for support in supports:
        if not support <= set(allowed) or any(set(e) <= support for e in edges):
            raise RuntimeError('proposed support is invalid')
    index = {u: i for i, u in enumerate(allowed)}
    edge_masks = [sum(1 << index[u] for u in e) for e in edges]
    support_masks = [sum(1 << index[u] for u in s) for s in supports]
    valid = 0
    for mask in range(1 << len(allowed)):
        if any(mask & e == e for e in edge_masks):
            continue
        valid += 1
        if not any(mask & ~s == 0 for s in support_masks):
            raise RuntimeError(('axis support not covered', a, mask))
    return dict(axis_factor=a, allowed_orbits=allowed, forbidden_hyperedges=sorted(edges),
                subsets=1 << len(allowed), valid_subsets=valid,
                maximal_supports=[sorted(s) for s in supports], status='SATURATION_COVER_OK')


def audit_small_words():
    # Build words directly from coordinate residues, independently of the
    # encoding and its word_from_assignment helper.
    a, n = 7, 35
    pairs=[(x,y,(x+y)%n) for x in range(1,n) for y in range(x,n) if (x+y)%n]
    def literal(e,q):
        first={0:0,3:2,4:2,**q}
        row=[-1]
        for x in range(1,n):
            u,b=x%a,x%5
            if b==0:row.append(e[min(u,a-u)])
            else:
                state=first[u if b in (1,2) else -u%a]
                row.append(state if state else (0 if b in (1,4) else 1))
        return row
    valid=images=0
    for ec in itertools.product(range(6),repeat=3):
        e=dict(zip((1,2,3),ec))
        for qc in itertools.product((0,3,4,5),repeat=4):
            q=dict(zip((1,2,5,6),qc));row=literal(e,q)
            if any(row[x]==row[y]==row[z] for x,y,z in pairs):continue
            valid+=1;axis_two={u for u,c in e.items() if c==2};covered=False
            for support in maximal_supports(a):
                if not axis_two<=support:continue
                covered=True;ee={u:2 if u in support else c for u,c in e.items()}
                image=literal(ee,q)
                if any(image[x]==image[y]==image[z] for x,y,z in pairs):
                    raise RuntimeError(('saturation spoiled a word',e,q,support))
                images+=1
            if not covered:raise RuntimeError('valid small word not covered')
    return dict(status='FULL_WORD_SATURATION_AUDIT_OK',assignments=6**3*4**4,
                valid_words=valid,checked_saturations=images)



if __name__=="__main__":
    result={"status":"PASS","clauses":[audit_clauses(a) for a in (7,47,109)],
            "small":audit_small(),"axis_cover":[audit_axis(a) for a in (7,47,83,109)],
            "saturation":audit_small_words()}
    expected=json.loads(Path(__file__).with_name("expected.json").read_text())["audit"]
    # JSON turns tuple-valued hyperedges into lists.
    result=json.loads(json.dumps(result))
    if result!=expected:raise RuntimeError(("audit report differs",result))
    print(json.dumps(result,indent=2))
