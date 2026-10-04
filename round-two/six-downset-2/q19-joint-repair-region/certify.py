"""Small full-domain/result checker for the new joint-region source.

Entry damages are detected in the original matrix, rather than merely by
checking the template's ten inequalities. All real claims still use the
ordinary PROOF.md, with these exact finite computations as evidence.
"""
from binding import check_current
check_current()
from fractions import Fraction as F
from collections import Counter
from entries import affine_rows, evaluate
from joint import model, diagnose, physical, table_at, PARENT
from polyhedron import facets, inverse_or_null, vertices_of


def original_entry_check(raw,x,table=None):
    model.require(len(x)==4 and all(type(a) is F for a in x), 'exact four-coordinate domain')
    tau,pxx,px,d=x
    p0=model.type_budgets(model.comparison(raw,9,10),9,10)['P0']
    model.require(tau>=0 and min(pxx,px,p0+38*tau-pxx-px,d)>=0,
                  'nonnegative floor, masses and release in declared template domain')
    if table is None:table=table_at(raw,*x)[0]
    b=model.type_budgets(model.comparison(raw,9,10),9,10)
    old=model.literal_point(model.comparison(raw,9,10),9,10)
    point=model.literal_point(table,9,10)
    result=diagnose.entry_audit(point,old,b,tau)
    model.require(result['all_entry_inequalities_paid'],'ENTIRE original allowed entry floor')
    return result


def entire_affine_surplus(point,x,rows):
    from affine_check import entry_key
    counts=Counter()
    for i,v in enumerate(point['members']):
        for j,w in enumerate(point['members']):
            if not set(v).isdisjoint(w):continue
            key=entry_key(v,w)
            model.require(key in rows,'every original allowed position has an actual scalar row')
            val=point['L'][i][j]-point['s']*int(i==j)-x[0]
            model.require(evaluate(rows[key],x)==val,'ENTIRE original affine entry identity')
            counts[key]+=1
    model.require(sum(counts.values())==72817 and len(counts)==180,'full original scalar row and position coverage')
    return counts


def all_shifted_forms(table):
    tests=diagnose.certificates(table,9,10)
    model.require(len(tests)==12 and all(t['exact_block_test']['positive_definite'] for t in tests.values()),
                  'all12 entire physical shifted form comparisons')
    return tests


def full_vertex_result(record):
    model.require(record['vertex_count']==16 and len(record['vertices'])==16,
                  'entire declared distinct vertex count')
    expected,coverage=vertices_of(facets())
    observed={tuple(F(a) for a in v['coords']) for v in record['vertices']}
    model.require(observed==set(expected),'ENTIRE independently recomputed physical vertex coordinates')
    for v in record['vertices']:
        model.require(v['entire_180_entry_rows_and_5_domain_conditions_pass'] and
                      len(v['blocks'])==12 and all(b['positive_definite'] for b in v['blocks'].values()),
                      'every original entry and all full spectral vertex records')
    return True
