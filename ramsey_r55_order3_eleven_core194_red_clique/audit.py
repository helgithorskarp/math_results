#!/usr/bin/env python3
"""Independent physical empty-set semantics and normalization; no producer."""
from itertools import combinations, product
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('physical_orbit_util',ROOT.parent/'ramsey_r55_order3_eleven_core194_attachments/audit.py')
physical=importlib.util.module_from_spec(spec);spec.loader.exec_module(physical)
need=physical.need


def tail_for(empty):
    ids=physical.primary();empty=set(empty);rows=[]
    need({33,34}<=empty<=set(range(33,43)),'marked pair included')
    for f in sorted(empty-{33,34}):
        rows += [(-x,) for x in sorted({ids[a,f] for a in range(12)})]
    rows += [(ids[u,v],) for u,v in combinations(sorted(empty),2) if (u,v)!=(33,34)]
    for f in sorted(set(range(33,43))-empty):
        rows.append(tuple(sorted({ids[a,f] for a in range(12)})))
    return rows


def expected(q):
    need(q in (2,3,4),'admissible exact empty cardinality')
    return tail_for(range(33,33+q))


def mapping(p,ids):
    physical.check_permutation(p,ids)
    return {x:ids[tuple(sorted((p[u],p[v])))] for (u,v),x in ids.items()}


def transport(rows,m):
    return {tuple(sorted(m[abs(x)]*(1 if x>0 else -1) for x in row)) for row in rows}


def cover():
    ids=physical.primary();census={2:0,3:0,4:0};permutations=set()
    for mask in range(256):
        empty={33,34}|{35+k for k in range(8) if mask>>k&1};q=len(empty)
        if q not in census:continue
        census[q]+=1
        order=sorted(range(35,43),key=lambda f:f not in empty)
        p=list(range(43))
        for new,old in enumerate(order,35):p[old]=new
        need(p[:35]==list(range(35)),'ordered pair and moving vertices fixed')
        need({p[f] for f in empty}==set(range(33,33+q)),'exact empty-set transport')
        m=mapping(p,ids);permutations.add(tuple(p))
        need(transport(tail_for(empty),m)==set(expected(q)),'entire physical tail transported')
    need(census=={2:1,3:8,4:28},'complete 256-pattern classification')
    prefix_checks=0;clique_checks=0
    for q in (2,3,4):
        tail=expected(q)
        # Every independent four-bit core prefix is characterized exactly.
        for f in range(35,43):
            variables=sorted({ids[a,f] for a in range(12)})
            rows=[row for row in tail if set(map(abs,row))<=set(variables)]
            for bits in product((False,True),repeat=4):
                values=dict(zip(variables,bits))
                holds=all(any(values[abs(x)]==(x>0) for x in row) for row in rows)
                need(holds==(not any(bits) if f<33+q else any(bits)),'exact prefix truth table')
                prefix_checks+=1
        redvars=[ids[u,v] for u,v in combinations(range(33,33+q),2) if (u,v)!=(33,34)]
        for bits in product((False,True),repeat=len(redvars)):
            values=dict(zip(redvars,bits));rows=[row for row in tail if set(map(abs,row))<=set(redvars)]
            holds=all(any(values[abs(x)]==(x>0) for x in row) for row in rows)
            need(holds==all(bits),'exact red clique truth table');clique_checks+=1
        used={abs(x) for row in tail for x in row}
        free_contacts={ids[a,f] for f in (33,34) for a in range(12,33,3)}
        free_contacts|={ids[u,f] for u in (33,34) for f in range(33+q,43)}
        need(not used&free_contacts,'no RR/RB/BR/BB restriction imposed on exterior contacts')
    return dict(empty_patterns=256,allowed_patterns=census,distinct_normalizers=len(permutations),
        prefix_truth_assignments=prefix_checks,clique_truth_assignments=clique_checks,
        no_exterior_contact_restriction=True)


def base_symmetries(base):
    ids=physical.primary()
    with base.open() as f:
        need(f.readline()=='p cnf 320 364095\n','complete RED header')
        rows={tuple(map(int,line.split()[:-1])) for line in f}
    need(len(rows)==364095,'complete RED clause count')
    generators=[]
    for f in range(35,42):
        p=list(range(43));p[f],p[f+1]=f+1,f;m=mapping(p,ids)
        need(transport(rows,m)==rows,'complete RED base invariant under fixed generator')
        generators.append([f,f+1])
    return dict(generators=generators,clause_images_checked=364095*7)
