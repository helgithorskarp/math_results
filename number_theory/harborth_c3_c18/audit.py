#!/usr/bin/env python3
"""Exact semantic controls, affine coverage, and definition-level witness check.

These controls supplement, and do not replace, the written encoding proof
and the three independently checked refutations.
"""
import collections
import itertools
import json
from pathlib import Path
from encode import build
from check_witness import check


def normalizer(total):
    a,b=total
    if b%3:
        u=1
        v=(-a*pow(b%3,-1,3))%3
        epsilon=1 if b%3==1 else -1
        c=((1-epsilon*b)//3)%6
        representative=(0,1)
    else:
        u=1 if a==0 else pow(a,-1,3)
        v=0
        epsilon=1
        c=(-b//3)%6
        representative=(0 if a==0 else 1,0)
    return u,v,epsilon,c,representative


def affine_coverage():
    points=list(itertools.product(range(3),range(18)))
    counts=collections.Counter()
    additions=0
    records=[]
    for total in points:
        u,v,e,c,representative=normalizer(total)
        def phi(p):return ((u*p[0]+v*p[1])%3,e*p[1]%18)
        image=[(phi(p)[0],(phi(p)[1]+c)%18) for p in points]
        if len(set(image))!=54:raise ValueError("affine map is not a permutation")
        for p in points:
            for q in points:
                lhs=phi(((p[0]+q[0])%3,(p[1]+q[1])%18))
                rhs=((phi(p)[0]+phi(q)[0])%3,(phi(p)[1]+phi(q)[1])%18)
                if lhs!=rhs:raise ValueError("linear part is not a homomorphism")
                additions+=1
        pt=phi(total)
        transformed=(pt[0],(pt[1]+21*c)%18)
        if transformed!=representative:raise ValueError("total normalization failed")
        if (21*c-3*c)%18:raise ValueError("complement equivariance failed")
        counts[representative]+=1
        records.append({"total":list(total),"u":u,"v":v,"epsilon":e,
                        "translation_second_coordinate":c,
                        "representative":list(representative)})
    return {"covered_totals":sum(counts.values()),
            "representative_sizes":{str(k):v for k,v in sorted(counts.items())},
            "homomorphism_additions_checked":additions,"maps":records}


def unit_conflict(clauses, primary_assignment):
    """Elementary unit propagation on the actual CNF, no SAT library."""
    values=dict(primary_assignment)
    while True:
        changed=False
        for clause in clauses:
            open_literals=[]
            satisfied=False
            for lit in clause:
                value=values.get(abs(lit))
                if value is None:open_literals.append(lit)
                elif value==(lit>0):
                    satisfied=True
                    break
            if satisfied:continue
            if not open_literals:return True
            if len(open_literals)==1:
                lit=open_literals[0]
                values[abs(lit)]=lit>0
                changed=True
        if not changed:return False


def canonical_path_model(cnf, paths, points, selected, moduli, total, size):
    values={i:False for i in range(1,cnf.nv+1)}
    for i in selected:values[i+1]=True
    weights=[[1]*len(points)]+[[p[c] for p in points] for c in range(2)]
    for j,q in enumerate(paths):
        state=0
        values[q[0][0]]=True
        for i in range(len(points)):
            if i in selected:state+=weights[j][i]
            if j:state%=moduli[j-1]
            if state>=len(q[i+1]):return False
            values[q[i+1][state]]=True
    return all(any(values[abs(lit)]==(lit>0) for lit in clause)
               for clause in cnf.clauses)


def small_semantics():
    records=[]
    # Complete primary-assignment tests at both sides of known thresholds.
    for moduli,sizes in [((2,4),(5,6)),((3,3),(4,5))]:
        points=list(itertools.product(range(moduli[0]),range(moduli[1])))
        for size in sizes:
            formulas={t:build(moduli,size,t) for t in points}
            checked=0;bad_sets=set();sat_fixed_assignments=0
            for mask in range(1<<len(points)):
                selected={i for i in range(len(points)) if mask>>i&1}
                sums=tuple(sum(points[i][c] for i in selected)%moduli[c] for c in range(2))
                zero_sum_exists=any(
                    all(sum(points[i][c] for i in ids)%moduli[c]==0 for c in range(2))
                    for ids in itertools.combinations(sorted(selected),moduli[1]))
                assignment={i+1:i in selected for i in range(len(points))}
                for total,(cnf,meta,paths,_) in formulas.items():
                    truth=len(selected)==size and sums==total and not zero_sum_exists
                    conflict=unit_conflict(cnf.clauses,assignment)
                    if conflict==truth:raise ValueError("CNF/direct-definition mismatch")
                    if truth:
                        if not canonical_path_model(cnf,paths,points,selected,moduli,total,size):
                            raise ValueError("valid set has no canonical extension")
                        bad_sets.add(mask);sat_fixed_assignments+=1
                    checked+=1
            if bool(bad_sets)!=(size==sizes[0]):raise ValueError("known small threshold mismatch")
            records.append({"moduli":list(moduli),"size":size,
                            "fixed_primary_assignments_and_totals_checked":checked,
                            "bad_sets":len(bad_sets),"satisfiable_pairs":sat_fixed_assignments})
    return records


def production_clauses():
    # A second enumeration: ordered pairs determine the third point.
    records=[]
    points=list(itertools.product(range(3),range(18)))
    index={p:i for i,p in enumerate(points)}
    for total in [(0,0),(1,0),(0,1)]:
        cnf,meta,_,forbidden=build(total=total)
        independent=set()
        for i,p in enumerate(points):
            for j,q in enumerate(points):
                r=((total[0]-p[0]-q[0])%3,(total[1]-p[1]-q[1])%18)
                k=index[r]
                if len({i,j,k})==3:independent.add(tuple(sorted((i,j,k))))
        if independent!={tuple(t) for t in forbidden}:raise ValueError("triple clause mismatch")
        records.append({k:v for k,v in meta.items() if k!="points"})
    return records


def run():
    witness=json.loads(Path(__file__).with_name("witness20.json").read_text())["points"]
    result={"affine_coverage":affine_coverage(),"small_semantics":small_semantics(),
            "production_clause_audit":production_clauses(),"lower_witness":check(witness)}
    # Explicit negative controls for the definition-level witness checker.
    rejected=0
    for bad in [witness[:-1]+[witness[0]], [[0,0]]*20,
                [[0,y] for y in range(18)]+[[1,0],[2,0]]]:
        try:check(bad)
        except ValueError:rejected+=1
        else:raise ValueError("bad witness was accepted")
    result["malformed_or_false_witnesses_rejected"]=rejected
    return result


if __name__=="__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
