#!/usr/bin/env python3
"""Check restricted QBF semantics against direct degree and colouring definitions."""
from hashlib import sha256
import itertools
import json
from pathlib import Path
import time
import encode_degree as enc
import verify_dual as previous

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def fixtures():
    cases=previous.fixtures()
    clique=lambda n:list(itertools.combinations(range(n),2))
    cases.extend([
        dict(name='K5_plus_isolate',n=6,edges=clique(5),cross=[],patterns=[[]],budget=6),
        dict(name='unselected_degree_witness',n=9,
             edges=sorted(clique(5)+[(0,5),(5,6),(5,7),(5,8)]),cross=[],patterns=[[]],budget=5),
        dict(name='boundary_K4',n=4,edges=clique(4),cross=[(0,v) for v in range(4)],patterns=[[0]],budget=4),
        dict(name='boundary_K3',n=3,edges=clique(3),cross=[(a,v) for a in range(2) for v in range(3)],
             patterns=[[0,1]],budget=3),
        dict(name='peeling_cascade',n=5,edges=[(0,1),(1,2),(2,3),(3,4)],
             cross=[(a,v) for a in range(2) for v in range(5)],patterns=[[0,1]],budget=5),
        dict(name='duplicate_boundary_colours',n=3,edges=clique(3),
             cross=[(a,v) for a in range(3) for v in range(3)],patterns=[[0,0,0],[1,1,1]],budget=3)
    ])
    return cases


def colour(case,X):
    # Direct backtracking with edge checks, independent of SAT encodings.
    neighbours={v:set() for v in range(case['n'])}
    for a,b in case['edges']:neighbours[a].add(b);neighbours[b].add(a)
    order=sorted(X,key=lambda v:(-len(neighbours[v]&X),v))
    for j,p in enumerate(case['patterns']):
        forbidden={v:{p[a] for a,w in case['cross'] if w==v} for v in X}
        c={}
        def visit(i):
            if i==len(order):return True
            v=order[i]
            for k in range(4):
                if k in forbidden[v] or any(c.get(u)==k for u in neighbours[v]):continue
                c[v]=k
                if visit(i+1):return True
                del c[v]
            return False
        if visit(0):return j,dict(c)
    return None


def deficient(case,X):
    # Recount incident edges directly instead of using the generator's degree tables.
    return sorted(v for v in X if
        sum(1 for a,b in case['edges'] if (a==v and b in X) or (b==v and a in X))+
        sum(1 for a,w in case['cross'] if w==v)<4)


def peel_and_lift(case,X):
    Y=set(X);removed=[]
    while True:
        bad=deficient(case,Y)
        if not bad:break
        removed.append(bad[0]);Y.remove(bad[0])
    answer=colour(case,Y)
    if answer is None:return None,Y,removed
    j,c=answer
    for v in reversed(removed):
        used={c[b] for a,b in case['edges'] if a==v and b in c}
        used|={c[a] for a,b in case['edges'] if b==v and a in c}
        used|={case['patterns'][j][a] for a,w in case['cross'] if w==v}
        enc.base.require(len(used)<=3,'extension degree bound')
        c[v]=next(k for k in range(4) if k not in used)
    enc.base.require(set(c)==X,'lift domain')
    enc.base.require(all(c[a]!=c[b] for a,b in case['edges'] if a in X and b in X),'lifted pool edge')
    enc.base.require(all(c[v]!=case['patterns'][j][a] for a,v in case['cross'] if v in X),'lifted cross edge')
    return (j,c),Y,removed


def abstract_checks():
    solver=enc.base.load('degree_dpll',REPO/'hadwiger_nelson_parts509_quantified_selector/verify_controls.py')
    rows=[]
    for case in fixtures():
        args={k:case[k] for k in ['n','edges','cross','patterns','budget']}
        raw,meta=enc.encode(**args)
        prefix,cnf=previous.parse(raw)
        universal=prefix[0][1] if prefix[0][0]=='a' else []
        enc.base.require(universal==list(range(1,case['n']+1)),'universal selectors')
        old_fail=[];new_fail=[];relaxed=[];lifted=0;longest=0
        for mask in range(1<<case['n']):
            X={v for v in range(case['n']) if (mask>>v)&1}
            proper=colour(case,X) is not None
            low=deficient(case,X)
            expected=len(X)>case['budget'] or bool(low) or proper
            actual=solver.sat(cnf,[v if v-1 in X else -v for v in universal])
            enc.base.require(actual==expected,('restricted matrix',case['name'],mask))
            fixed,fm=enc.encode(**args,selection=X)
            fp,fc=previous.parse(fixed)
            enc.base.require([q for q,_ in fp]==['e'],'fixed prefix')
            enc.base.require(solver.sat(fc,[])==expected,('fixed matrix',case['name'],mask))
            lift,core,removed=peel_and_lift(case,X)
            enc.base.require((lift is not None)==proper,('peeling equivalence',case['name'],mask))
            enc.base.require(not deficient(case,core),'terminal core')
            longest=max(longest,len(removed))
            lifted+=lift is not None
            if len(X)<=case['budget'] and not proper:
                old_fail.append(mask)
                if low:relaxed.append(mask)
            if not actual:new_fail.append(mask)
        enc.base.require(bool(old_fail)==bool(new_fail),('family truth changed',case['name']))
        rows.append(dict(name=case['name'],selections_checked=1<<case['n'],
            family_truth=not old_fail,restricted_failing_masks=new_fail,
            uncolourable_selections_accepted_by_guard=relaxed,
            peeling_colourings_lifted=lifted,longest_peeling=longest,
            qdimacs_sha256=meta['qdimacs_sha256']))
    lookup={r['name']:r for r in rows}
    enc.base.require(63 in lookup['K5_plus_isolate']['uncolourable_selections_accepted_by_guard'],
                     'must expose pointwise non-equivalence')
    enc.base.require(31 in lookup['K5_plus_isolate']['restricted_failing_masks'],'K5 core must survive')
    enc.base.require(31 in lookup['unselected_degree_witness']['restricted_failing_masks'],
                     'unselected vertex cannot witness deficiency')
    enc.base.require(lookup['peeling_cascade']['longest_peeling']==5,'cascade not exercised')
    return rows


def compute():
    old=enc.check_inputs()
    checks=abstract_checks()
    source,U=old.pool_input()
    raw,meta=enc.encode(**source,budget=134)
    previous.parse(raw)
    compact={k:v for k,v in meta.items() if k not in ['color_variables','pattern_variables']}
    real=[]
    for name,deleted in [('record509',None),('delete397',397)]:
        H=old.restrict(source,[i for i,v in enumerate(U) if v<509 and v!=deleted])
        selection=set(range(H['n']))
        child,cm=enc.encode(**H,budget=H['n'],selection=selection)
        original,om=enc.base.encode(**H,budget=H['n'],selection=selection)
        previous.parse(child)
        if name=='record509':
            enc.base.require(not cm['fixed_deficient_vertices'] and child==original,'certified509 control changed')
            cert=json.loads((REPO/'hadwiger_nelson_parts509_quantified_dual/benchmark_summary.json').read_text())['record509_proof']
            enc.base.require(sha256(enc.base.to_cnf(child)).hexdigest()==cert['cnf_sha256'],'existing DRAT CNF mismatch')
        real.append(dict(name=name,qdimacs_sha256=cm['qdimacs_sha256'],
            unchanged_from_base=child==original,fixed_deficient_vertices=cm['fixed_deficient_vertices'],
            variables=cm['variables'],clauses=cm['clauses']))
    certificate=json.loads((REPO/'hadwiger_nelson_parts509_pool_cover_residual30/certificate.json').read_text())
    labels=(set(range(374,509))-set(certificate['R']))|set(certificate['A'])
    X={i for i,v in enumerate(U) if v in labels}
    enc.base.require(len(X)==134 and {U[i] for i in X}==labels,'residual selection')
    enc.base.require(not deficient(source,X),'residual degree condition')
    child,cm=enc.encode(**source,budget=134,selection=X)
    original,_=enc.base.encode(**source,budget=134,selection=X)
    enc.base.require(child==original,'admissible positive control changed')
    p=certificate['p'];c=certificate['c']
    enc.base.require(len(c)==len(U) and all(c[v] in '0123' for v in X),'residual colours')
    enc.base.require(all(c[a]!=c[b] for a,b in source['edges'] if a in X and b in X),'residual pool edge')
    enc.base.require(all(int(c[v])!=source['patterns'][p][a] for a,v in source['cross'] if v in X),'residual cross edge')
    positive={cm['color_variables'][i][int(c[i])] for i in X}|{cm['pattern_variables'][p]}
    _,rows=previous.parse(child)
    enc.base.require(all(any((v>0)==(abs(v) in positive) for v in row) for row in rows),'residual matrix colouring')
    real.append(dict(name='published_residual30',vertices=508,
        edges=1860+sum(a in X and b in X for a,b in source['edges'])+sum(v in X for a,v in source['cross']),
        unchanged_from_base=True,minimum_selected_degree_at_least_four=True,proper_colouring_and_matrix_checked=True,
        qdimacs_sha256=cm['qdimacs_sha256'],variables=cm['variables'],clauses=cm['clauses']))
    Y=set(range(source['n']));removed=[];trace=[]
    while True:
        bad=deficient(source,Y)
        if not bad:break
        v=bad[0]
        neighbours=sorted({b for a,b in source['edges'] if a==v and b in Y}|
                          {a for a,b in source['edges'] if b==v and a in Y})
        trace.append(dict(vertex=U[v],remaining_pool_neighbours=[U[w] for w in neighbours],
                          fixed_L_degree=sum(w==v for a,w in source['cross'])))
        removed.append(U[v]);Y.remove(v)
    return dict(status='MINIMUM-DEGREE FAMILY REDUCTION CHECKS VERIFIED',abstract_cases=len(checks),
        selector_assignments_checked=sum(r['selections_checked'] for r in checks),
        fixed_specializations_checked=sum(r['selections_checked'] for r in checks),
        lifted_colourings_checked=sum(r['peeling_colourings_lifted'] for r in checks),
        abstract_controls=checks,full_instance=compact,real_controls=real,
        global_peeling_order=removed,global_peeling_trace=trace,surviving_full_pool_vertices=len(Y),
        full_family_solved=False,new_family_closure=False,target_record_established=False)


def main():
    result=compute()
    enc.base.require(result==json.loads((HERE/'expected.json').read_text()),'recorded results differ')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
