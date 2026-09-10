"""Definition-level exact checks for point-weight and fractional certificates."""
from fractions import Fraction
from itertools import combinations_with_replacement

def sidon(points):
    sums=[x+y for x,y in combinations_with_replacement(points,2)]
    return len(sums)==len(set(sums))

def valid_row(points,size,domain):
    assert len(points)==size and points==sorted(set(points))
    assert set(points)<=set(domain)

def check_fractional(certificate,ordered,old_weights):
    j=certificate['case'];anchor=certificate['anchor']
    assert anchor==ordered[2*j]
    domain=[x for x in range(84) if x not in anchor]
    row_ids={tuple(row):i for i,row in enumerate(ordered)}
    incidence={x:Fraction(0) for x in domain};totals={10:Fraction(0),11:Fraction(0),33:Fraction(0)}
    for term in certificate['classes']:
        numerator,denominator=term['numerator'],term['denominator']
        assert type(numerator) is int and type(denominator) is int
        assert numerator>0 and denominator>0
        coefficient=Fraction(numerator,denominator)
        points,size=term['points'],term['size']
        valid_row(points,size,domain)
        if size==10:
            assert sidon(points)
        elif size==11:
            assert not certificate['coupled'] and sidon(points)
            assert row_ids[tuple(points)]>=2*j+1
        elif size==33:
            assert certificate['coupled']
            rows=term['eleven_classes'];assert len(rows)==3
            for row in rows:
                valid_row(row,11,domain)
                assert sidon(row) and row_ids[tuple(row)]>=2*j+1
            assert sorted(x for row in rows for x in row)==points
            assert sum(old_weights[x] for x in anchor+points)>=7685948
        else:
            raise AssertionError('unsupported block size')
        totals[size]+=coefficient
        for x in points:incidence[x]+=coefficient
    assert all(v==1 for v in incidence.values())
    assert totals[10]==4
    assert (totals[33]==1 and totals[11]==0) if certificate['coupled'] else (totals[11]==3 and totals[33]==0)
    return {'case':j,'coupled':certificate['coupled'],'support':len(certificate['classes']),
            'point_equalities':73,'exact':True}

def check_exclusion(certificate,ordered,ten_maximum):
    j=certificate['case'];anchor=certificate['anchor'];weights=certificate['weights']
    assert anchor==ordered[2*j] and len(weights)==84
    assert all(type(w) is int and 0<=w<=1000000 for w in weights)
    domain=[x for x in range(84) if x not in anchor]
    assert domain==certificate['domain']
    allowed=[row for row in ordered[2*j+1:] if not set(row)&set(anchor)]
    assert allowed and all(sidon(row) for row in allowed)
    maximum=max(sum(weights[x] for x in row) for row in allowed)
    assert ten_maximum==certificate['M10'] and maximum==certificate['M11']
    total=sum(weights[x] for x in domain)
    gap=total-4*ten_maximum-3*maximum
    assert gap==certificate['gap'] and gap>0
    return {'case':j,'allowed_eleven_sets':len(allowed),'weight_sum':total,
            'M10':ten_maximum,'M11':maximum,'gap':gap,'excluded':True}
