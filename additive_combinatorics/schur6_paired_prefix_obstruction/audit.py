"""Independent full CNF audit for paired ordinary prefixes."""
import argparse
import itertools
import json
from pathlib import Path


def independent(N,k=5):
    table={};rows=[];variable=0
    for q in range(N//5+1):
        specifications=[([5*q+1,5*q+2],(0,*range(2,k)),[0,1]),
                        ([5*q+3,5*q+4],(0,*range(2,k)),[1,0]),
                        ([5*q+5],tuple(range(k)),None)]
        for points,labels,special in specifications:
            if points[0]>N:continue
            values={}
            for label in labels:variable+=1;values[label]=variable
            rows.append(values)
            for j,x in enumerate(points):
                if x>N:continue
                for label,value in values.items():
                    colour=special[j] if special is not None and label==0 else label
                    table[x,colour]=value
    result=set()
    for row in rows:
        result.add(tuple(sorted(row.values())))
        for left,right in itertools.combinations(row.values(),2):result.add(tuple(sorted([-left,-right])))
    equations=0
    for z in range(2,N+1):
        for x in range(1,z//2+1):
            equations+=1
            for colour in range(k):
                keys=[(w,colour) for w in (x,z-x,z)]
                if all(key in table for key in keys):
                    result.add(tuple(sorted({-table[key] for key in keys})))
    for index,row in enumerate(rows):
        for c in range(3,k):
            result.add(tuple(sorted([-row[c]]+[prior[c-1] for prior in rows[:index]])))
    return variable,result,equations


def audit(N):
    from prefix import encoding
    m,cnf=encoding(N)
    variables,literal,equations=independent(N)
    assert variables==m['variables'] and literal==set(cnf)
    return dict(endpoint=N,variables=variables,clauses=len(literal),
                ordinary_equations=equations,
                status='FULL_LITERAL_CNF_EQUALITY')


def small_assignments():
    from prefix import encoding,decode
    from verify import paired
    m,plain=encoding(14,4,False);_,normalized=encoding(14,4,True)
    rows=list(m['rows'].values());count=valid=0
    for assignment in itertools.product(*(tuple(row) for row in rows)):
        truth={row[c] for row,c in zip(rows,assignment)}
        word=decode(m,truth)
        encoded=all(any(v in truth if v>0 else -v not in truth for v in cl) for cl in plain)
        try:
            paired(word,4);actual=True
        except AssertionError:
            actual=False
        assert encoded==actual
        count+=1
        if actual:
            valid+=1;palette={}
            for c in assignment:
                if c>=2 and c not in palette:palette[c]=len(palette)+2
            image={row[palette.get(c,c)] for row,c in zip(rows,assignment)}
            assert all(any(v in image if v>0 else -v not in image for v in cl) for cl in normalized)
            paired(decode(m,image),4)
    assert (count,valid)==(11664,242)
    return dict(endpoint=14,colours=4,assignments=count,valid=valid,
                every_truth_value_and_valid_normalization_checked=True)


def all_checks():
    from boundary import check
    from verify import check_witnesses
    return dict(cnf_audits=[audit(N) for N in (14,109,110)],
                small_assignments=small_assignments(),boundary=check(),
                witnesses=check_witnesses())


if __name__=='__main__':
    report=all_checks()
    expected=json.loads((Path(__file__).parent/'expected.json').read_text())
    assert report==expected
    print(json.dumps(dict(status='ALL_AUDITS_MATCH_EXPECTED',
                         cnf_audits=report['cnf_audits'],
                         small_assignments=report['small_assignments'],
                         boundary_cases=report['boundary']['maximal_axis_support_count'],
                         new_s6_bound=False),indent=2))
