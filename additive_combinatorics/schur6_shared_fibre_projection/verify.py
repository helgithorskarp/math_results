"""Exact checks for the shared-fibre projection lemma; standard library only.

The all-parameter proof is in README.md. These checks validate the explicit
certificates and exhaust every symmetric assignment over the small Z7 axis.
They do not prove Schur Number Five or an unrestricted bound on S(6).
"""
import itertools
import json
from pathlib import Path


def sf(A,a):
    return all((x+y)%a not in A for x in A for y in A)


def diff(A,a):
    return {(x-y)%a for x in A for y in A}


def expand_half(half,zero):
    return [zero]+list(half)+list(reversed(half))


def sets(E,Q):
    a=len(E)
    axis=[{x for x in range(1,a) if E[x]==c} for c in range(6)]
    fibres={c:{x for x in range(a) if Q[x]==c} for c in (0,2,3,4,5)}
    return axis,fibres


def criterion(E,Q):
    a=len(E);axis,fibres=sets(E,Q)
    return (all(sf(B,a) for B in axis)
            and all(sf(fibres[c],a) for c in (2,3,4,5))
            and not (axis[0]|axis[1])&diff(fibres[0],a)
            and all(not axis[c]&diff(fibres[c],a) for c in (2,3,4,5)))


def shared_word(E,Q):
    a=len(E);out=[]
    for x in range(1,5*a):
        aa,b=x%a,x%5
        if b==0:out.append(E[aa])
        elif Q[aa]!=0:out.append(Q[aa])
        else:out.append(0 if b in (1,4) else 1)
    return out


def projection(E,Q):
    """Five labels on the nonzero residues modulo2a, whether valid or not."""
    a=len(E);out=[]
    for x in range(1,2*a):
        label=E[x%a] if x%2==0 else Q[x%a]
        out.append(0 if label in (0,1) else label-1)
    return out


def modular_bad(word):
    n=len(word)+1;row=[-1]+word
    return [(x,y,(x+y)%n) for x in range(1,n) for y in range(x,n)
            if (x+y)%n and row[x]==row[y]==row[(x+y)%n]]


def verify_word(word,k):
    if any(type(c) is not int or not 0<=c<k for c in word):raise ValueError('bad label')
    n=len(word)+1
    if any(word[x-1]!=word[n-x-1] for x in range(1,n)):raise ValueError('reflection fails')
    bad=modular_bad(word)
    if bad:raise ValueError(('modular Schur violation',bad[0]))
    integer_pairs=0
    for x in range(1,n):
        for y in range(x,n-x):
            integer_pairs+=1
            if word[x-1]==word[y-1]==word[x+y-1]:raise ValueError('integer Schur violation')
    return dict(endpoint=n-1,colours=k,integer_pairs=integer_pairs,
                modular_pairs=(n-1)**2//2,class_sizes=[word.count(c) for c in range(k)])


def fixture_check(data):
    a=data['axis_factor']
    if a%2!=1 or a%5==0:raise ValueError('invalid cyclic CRT parameters')
    if len(data['axis_half'])!=(a-1)//2 or len(data['fibre_half'])!=(a-1)//2:
        raise ValueError('wrong half-word size')
    if any(type(c) is not int or not 0<=c<6 for c in data['axis_half']):
        raise ValueError('bad axis state')
    if any(type(c) is not int or c not in (0,2,3,4,5) for c in data['fibre_half']):
        raise ValueError('bad fibre state')
    E=expand_half(data['axis_half'],-1);Q=expand_half(data['fibre_half'],0)
    if not criterion(E,Q):raise ValueError('set criterion fails')
    word=shared_word(E,Q)
    if word!=data['word']:raise ValueError('full certificate mismatch')
    checked=verify_word(word,6)
    axis,fibres=sets(E,Q);merged=sf(axis[0]|axis[1],a)
    projected=projection(E,Q)
    if projected!=data['projection']:raise ValueError('projection certificate mismatch')
    bad=modular_bad(projected)
    if merged:
        projected_check=verify_word(projected,5)
        if a>79:raise ValueError('fixture would contradict the imported S(5)=160 theorem')
    else:
        if not bad:raise ValueError('a non-sum-free merged axis projected to a valid word')
        projected_check=dict(endpoint=2*a-1,defects=len(bad))
    # For either case, every projected violation must be entirely in the even
    # copy of E0 union E1. This verifies the exact source of a failed projection.
    if any(any(x%2 for x in triple) or any(projected[x-1]!=0 for x in triple) for triple in bad):
        raise ValueError('a projected violation escaped the merged axis')
    return dict(axis_factor=a,shared=checked,merged_axis_sumfree=merged,
                projection=projected_check,residual_size=len(fibres[0]),
                common_class_sizes=[len(fibres[c]) for c in (2,3,4,5)])


def exhaustive_small():
    a=7;n=35;total=valid=mergeable=0
    triples=[(x,y,(x+y)%n) for x in range(1,n) for y in range(x,n) if (x+y)%n]
    for eh in itertools.product(range(6),repeat=3):
        E=expand_half(eh,-1)
        merged_set={x for x in range(1,a) if E[x] in (0,1)}
        merged=sf(merged_set,a)
        for qh in itertools.product((0,2,3,4,5),repeat=3):
            Q=expand_half(qh,0)
            row=[-1]+shared_word(E,Q)
            literal=all(not row[x]==row[y]==row[z] for x,y,z in triples)
            if literal!=criterion(E,Q):raise ValueError('small set/literal criterion disagreement')
            total+=1
            if not literal:continue
            valid+=1;bad=modular_bad(projection(E,Q))
            if bool(bad)==merged:raise ValueError('small projection equivalence failed')
            if any(any(x%2 for x in triple) for triple in bad):raise ValueError('unexpected odd defect')
            mergeable+=merged
    return dict(assignments=total,valid=valid,mergeable=mergeable)


def main():
    root=Path(__file__).resolve().parent
    fixtures=json.loads((root/'fixtures.json').read_text())
    report=dict(status='PASS',fixtures=[fixture_check(f) for f in fixtures],
                exhaustive=exhaustive_small())
    expected_path=root/'expected.json'
    if expected_path.exists() and report!=json.loads(expected_path.read_text()):
        raise ValueError('expected complete report differs')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
