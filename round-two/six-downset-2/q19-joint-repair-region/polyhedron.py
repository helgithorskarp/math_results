"""Exact compact entry-polyhedron vertex test; spectral outputs are new.

All four-active-facet subsets are exhausted. A nonsingular subset is
solved with a verified complete inverse, and singular subsets have a
verified nonzero null vector. This is a bounded finite calculation,
not a numerical LP solver or an arbitrary-grid argument.
"""
from binding import check_current
check_current()
from fractions import Fraction as F
from itertools import combinations
import json
import resource
import time
from entries import affine_rows, evaluate, primitive
from joint import model, table_at, PARENT


def facets():
    p0=F(8421443,65536)
    return [
        ('tau',(F(0),F(1),F(0),F(0),F(0))),
        ('pXX',(F(0),F(0),F(1),F(0),F(0))),
        ('pX',(F(0),F(0),F(0),F(1),F(0))),
        ('pY',(p0,F(38),F(-1),F(-1),F(0))),
        ('empty_XX',(F(1043037,16384),F(-18),F(-1),F(0),F(0))),
        ('empty_X',(F(1080063,16384),F(-9,2),F(0),F(-1),F(0))),
        ('empty_Y',(F(649645,16384)-p0,F(-43),F(1),F(1),F(0))),
        ('d',(F(0),F(0),F(0),F(0),F(1))),
        ('anchor_YY',(F(827,32768),F(-1),F(0),F(0),F(1))),
        ('empty_anchor',(F(91211,16384),F(-32),F(0),F(0),F(-45))),
    ]


def inverse_or_null(A):
    n=len(A)
    rows=[list(row)+[F(int(i==j)) for j in range(n)] for i,row in enumerate(A)]
    pivots=[]; rank=0
    for col in range(n):
        pivot=next((i for i in range(rank,n) if rows[i][col]),None)
        if pivot is None: continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        value=rows[rank][col]
        rows[rank]=[a/value for a in rows[rank]]
        for i in range(n):
            if i!=rank:
                a=rows[i][col]
                rows[i]=[x-a*y for x,y in zip(rows[i],rows[rank])]
        pivots.append(col);rank+=1
    if rank<n:
        free=next(i for i in range(n) if i not in pivots)
        v=[F(0)]*n;v[free]=F(1)
        for i,col in enumerate(pivots): v[col]=-rows[i][free]
        model.require(any(v) and all(sum(a*b for a,b in zip(row,v))==0 for row in A),
                      'every singular subset has an exact nonzero null witness')
        return None, v
    inverse=[row[n:] for row in rows]
    model.require(all(sum(A[i][k]*inverse[k][j] for k in range(n))==int(i==j)
                      and sum(inverse[i][k]*A[k][j] for k in range(n))==int(i==j)
                      for i in range(n) for j in range(n)),
                  'both full inverse products for each nonsingular active subset')
    return inverse,None


def vertices_of(fs):
    vertices={}; singular=[]; infeasible=[]; solved=0
    for active in combinations(range(len(fs)),4):
        A=[fs[i][1][1:] for i in active]
        inv,null=inverse_or_null(A)
        if null is not None:
            singular.append(dict(active=active,null=[str(a) for a in null]));continue
        solved+=1
        rhs=[-fs[i][1][0] for i in active]
        x=tuple(sum(a*b for a,b in zip(row,rhs)) for row in inv)
        model.require(all(evaluate(fs[i][1],x)==0 for i in active),
                      'each nonsingular subset solution solves all four original equations')
        vals=[evaluate(row,x) for name,row in fs]
        if min(vals)<0:
            j=min(range(len(vals)),key=lambda i:vals[i])
            infeasible.append(dict(active=active,violated_facet=j,value=str(vals[j])))
        else:
            vertices.setdefault(x,[]).append(active)
    model.require(len(singular)+len(infeasible)+sum(len(a) for a in vertices.values())==210,
                  'all 210 four-facet subsets accounted for exactly')
    return vertices,dict(active_subsets=210,singular_subsets=singular,
                         nonsingular_subsets=solved,infeasible_subsets=infeasible)


def run():
    start=time.monotonic()
    raw=model.coefficient_input(PARENT/'COEFFICIENTS.json')
    full=affine_rows(raw);fs=facets()
    available={primitive(row) for row in full.values()}
    model.require(all(primitive(row) in available for name,row in fs),
                  'each compact facet is an actual original entry or domain condition')
    vertices,coverage=vertices_of(fs)
    checks=[]
    all_entry=True;all_psd=True
    for x,active in sorted(vertices.items()):
        values={key:evaluate(row,x) for key,row in full.items()}
        minimum=min(values.values())
        all_entry &= minimum>=0
        table,recipe=table_at(raw,*x)
        blocks={tag:model.exact_ldl(block['matrix'],block['metric'],F(1,1024))
                for tag,block in model.sector_forms(table,9,10).items()}
        if not all(v['positive_definite'] for v in blocks.values()):
            for tag,test in blocks.items():
                if not test['positive_definite']:
                    block=model.sector_forms(table,9,10)[tag]
                    test['unshifted_test']=model.exact_ldl(block['matrix'],block['metric'],F(0))
            all_psd=False
        checks.append(dict(coords=[str(a) for a in x],active_subsets=active,
                           active_facets=[name for name,row in fs if evaluate(row,x)==0],
                           entire_180_entry_rows_and_5_domain_conditions_pass=minimum>=0,
                           minimum_affine_surplus=str(minimum),blocks=blocks))
    return dict(agent='six-downset-2',role='researcher',
                status='exact full vertex calculation; ordinary compactness/completeness proof in PROOF.md',
                facets=[dict(name=name,coefficients=[str(a) for a in row]) for name,row in fs],
                coverage=coverage,vertices=checks,vertex_count=len(vertices),
                all_vertices_entry_feasible=all_entry,
                all_vertices_twelve_shifted_forms_positive=all_psd,
                tau_projection=['0',str(F(219637,2523136))],
                observed_seconds=time.monotonic()-start,
                peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                no_global_optimizer_domain_or_H_nonexistence_claim=True)


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
