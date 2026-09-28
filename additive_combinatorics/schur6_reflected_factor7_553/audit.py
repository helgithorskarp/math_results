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
from model import encoding


def audit_clauses(a,p=7):
    m,cnf=encoding(a,p,symmetry=False);h=(a-1)//2;n=p*a;t=(p-1)//2
    common=tuple(range(t,6));qlabels=(0,*common)
    E,Q,P=m['E'],m['Q'],m['P'];positions=set(range(1,a))
    assert set(E)=={(u,c) for u in range(1,h+1) for c in range(6)}
    assert set(Q)=={(x,c) for x in positions for c in qlabels}
    assert set(P)=={(x,c) for x in range(1,h+1) for c in common}
    allvars=[*E.values(),*Q.values(),*P.values()]
    assert len(allvars)==len(set(allvars))==m['variables']
    normalize=lambda cl:tuple(sorted(set(cl)))
    actual={normalize(cl) for cl in cnf};expanded=set();pids=set(P.values())
    definitions=set();choices={}
    for (u,c),aux in P.items():
        x,y=Q[u,c],Q[a-u,c];choices[aux]=(x,y)
        definitions.update(map(normalize,([aux,-x],[aux,-y],[-aux,x,y])))
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
    for u in range(1,h+1):onehot([E[u,c] for c in range(6)])
    for x in sorted(positions):onehot([Q[x,c] for c in qlabels])
    def indicator(x,c):
        aa,b=x%a,x%p
        if b==0:return E[min(aa,a-aa),c]
        special=min(b,p-b)-1
        if aa==0:return 'T' if c==special else None
        qx=aa if b<=t else a-aa
        if c in common:return Q[qx,c]
        if c==special:return Q[qx,0]
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
    return dict(axis_factor=a,short_factor=p,modulus=n,literal_pairs=pairs,
                distinct_projected_clauses=len(expected),auxiliary_definitions=len(definitions),
                clauses_before_expansion=len(actual),expanded_reduced_clauses=len(expanded),
                subsumed_literal_clauses=redundant_literal,subsumed_reduced_clauses=redundant_reduced,
                status='EXACT_CLAUSE_EQUIVALENCE_BY_SUBSUMPTION')


def audit_small():
    a=5;short=7;n=35
    model,cnf=encoding(a,short,symmetry=False);canonical,ccnf=encoding(a,short)
    def truth_for(e,q):
        truth={v for (u,c),v in model['E'].items() if e[u]==c}
        truth|={v for (x,c),v in model['Q'].items() if q[x]==c}
        truth|={v for (u,c),v in model['P'].items() if q[u]==c or q[a-u]==c}
        return truth
    def satisfies(clauses,truth):
        return all(any(v in truth if v>0 else -v not in truth for v in cl) for cl in clauses)
    triples=[(x,y,(x+y)%n) for x in range(1,n) for y in range(x,n) if (x+y)%n]
    valid=total=0
    for ec in itertools.product(range(6),repeat=2):
        e=dict(zip((1,2),ec))
        for qc in itertools.product((0,3,4,5),repeat=4):
            q={0:0,**dict(zip((1,2,3,4),qc))};row=[-1]
            for x in range(1,n):
                u,b=x%a,x%short
                if b==0:c=e[min(u,a-u)]
                else:
                    state=q[u if b<=3 else -u%a]
                    c=state if state else min(b,short-b)-1
                row.append(c)
            expected=all(not row[x]==row[y]==row[z] for x,y,z in triples)
            if expected!=satisfies(cnf,truth_for(e,q)):
                raise RuntimeError('small literal disagreement')
            total+=1
            if not expected:continue
            valid+=1;common={};special={}
            for u in (1,2):
                for c in (q[u],q[a-u],e[u]):
                    if c>=3 and c not in common:common[c]=3+len(common)
                if e[u]<3 and e[u] not in special:special[e[u]]=len(special)
            ee={u:(common[c] if c>=3 else special[c]) for u,c in e.items()}
            qq={x:(common[c] if c>=3 else c) for x,c in q.items()}
            if not satisfies(ccnf,truth_for(ee,qq)):
                raise RuntimeError('canonical representative lost')
    return dict(status='PASS',assignments=total,valid_words=valid,
                all_valid_words_canonicalized=True)



def audit_orientations():
    result=[]
    for signs in itertools.product((1,-1),repeat=3):
        T={sign*x%7 for sign,x in zip(signs,(1,2,3))}
        negative={-x%7 for x in T}
        if len(T)!=3 or T&negative or T|negative!=set(range(1,7)):
            raise RuntimeError("not a skew short-coordinate set")
        positive=next(((x,y,(x+y)%7) for x in sorted(T) for y in sorted(T)
                       if (x+y)%7 in T),None)
        reflected=next(((x,y,(x+y)%7) for x in sorted(T) for y in sorted(T)
                        if (x+y)%7 in negative),None)
        if positive is None or reflected is None:
            raise RuntimeError("common sum conditions not both witnessed")
        for j in T:
            S={j,-j%7}
            if any((x+y)%7 in S for x in S for y in S):
                raise RuntimeError("a special short pair is not sum-free")
        result.append({"T":sorted(T),"positive_sum":positive,"negative_sum":reflected})
    return result


if __name__=="__main__":
    report={"status":"PASS","clauses":[audit_clauses(a,7) for a in (5,13,79)],
            "small":audit_small(),"orientations":audit_orientations()}
    report=json.loads(json.dumps(report))
    expected=json.loads(Path(__file__).with_name("expected.json").read_text())["audit"]
    if report!=expected:raise RuntimeError(("audit report differs",report))
    print(json.dumps(report,indent=2))
