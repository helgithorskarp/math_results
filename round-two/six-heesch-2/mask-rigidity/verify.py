"""Inverse-incidence reconstruction and solver-free negative-unit auditing."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
from rup import UnitReader

HERE = Path(__file__).resolve().parent
DIRS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
IDENTITY = (1,0,0,1,0,0)


def apply(g,p):
    a,b,c,d,u,v = g
    x,y = p
    return a*x+b*y+u,c*x+d*y+v


def invert(g):
    a,b,c,d,u,v = g
    determinant = a*d-b*c
    assert determinant in (-1,1)
    aa,bb,cc,dd = d*determinant,-b*determinant,-c*determinant,a*determinant
    return aa,bb,cc,dd,-aa*u-bb*v,-cc*u-dd*v


def compose(g,h):
    a,b,c,d,u,v = g
    e,f,i,j,w,z = h
    return a*e+b*i,a*f+b*j,c*e+d*i,c*f+d*j,a*w+b*z+u,c*w+d*z+v


def check_mirrors(fixture):
    poses = [tuple(r['pose']) for r in fixture['placements']]
    assert len(poses)==58 and fixture['depth']==4
    assert Counter(r['level'] for r in fixture['placements'])=={0:1,1:5,2:11,3:17,4:24}
    assert poses[0]==IDENTITY and fixture['placements'][0]['level']==0
    for g in poses:
        a,b,c,d,_,_ = g
        assert {(a*x+b*y,c*x+d*y) for x,y in DIRS}==set(DIRS)
        assert compose(invert(g),g)==IDENTITY
    axes = set()
    pairs = 0
    for i,g in enumerate(poses):
        for h in poses[i+1:]:
            relative = compose(invert(g),h)
            a,b,c,d,u,v = relative
            if a*d-b*c!=-1 or compose(relative,relative)!=IDENTITY:
                continue
            pairs += 1
            normal,rhs = ((a-1,b),-u) if (a-1,b)!=(0,0) else ((c,d-1),-v)
            divisor = math.gcd(*normal)
            assert rhs%divisor==0
            nx,ny = (t//divisor for t in normal)
            rhs //= divisor
            if nx<0 or nx==0 and ny<0:
                nx,ny,rhs = -nx,-ny,-rhs
            axes.add((nx,ny,rhs))
    assert pairs==17 and len(axes)==9
    selected = ((4,51,(0,1,1,0,-12,12)),
                (32,48,(0,1,1,0,12,-12)),
                (1,28,(1,0,-1,-1,0,-7)),
                (4,11,(1,0,-1,-1,0,10)),
                (46,56,(-1,-1,0,1,-4,0)),
                (25,48,(-1,-1,0,1,19,0)))
    for i,j,expected in selected:
        assert compose(invert(poses[i]),poses[j])==expected
    return {'reflection_pairs':pairs,'mirror_axes':sorted(map(list,axes))}


def domain(n):
    """Enumerate mirror coordinates A=x-y,B=x+2y and enforce integrality."""
    cells = []
    for a in range(-12*n+1,12*n):
        for b in range(-7*n+1,10*n):
            if -4*n<a+b<19*n and (2*a+b)%3==0:
                assert (b-a)%3==0
                cells.append(((2*a+b)//3,(b-a)//3))
    return tuple(sorted(cells))


def rebuild(n,fixture):
    cells = domain(n)
    index = {p:i+1 for i,p in enumerate(cells)}
    poses = [tuple(r['pose'][:4]+[n*t for t in r['pose'][4:]])
             for r in fixture['placements']]
    levels = [r['level'] for r in fixture['placements']]
    inverses = list(map(invert,poses))
    images = [apply(g,p) for g in poses for p in cells]
    xmin,xmax = min(x for x,y in images),max(x for x,y in images)
    ymin,ymax = min(y for x,y in images),max(y for x,y in images)
    del images
    prefixes = [dict() for _ in range(5)]
    zero = set()
    conflicts = set()
    global_cells = 0
    # Reconstruct local-variable occurrences by scanning global cells and
    # taking inverse poses, instead of forwarding every prototype variable.
    for x in range(xmin,xmax+1):
        for y in range(ymin,ymax+1):
            row = []
            for j,g in enumerate(inverses):
                v = index.get(apply(g,(x,y)))
                if v is not None:
                    row.append((j,v))
            if not row:
                continue
            global_cells += 1
            mult = Counter(v for j,v in row)
            zero.update(v for v,m in mult.items() if m>1)
            distinct = sorted(mult)
            for i,a in enumerate(distinct):
                conflicts.update((a,b) for b in distinct[i+1:])
            for k in range(5):
                providers = tuple(sorted({v for j,v in row if levels[j]<=k}))
                if providers:
                    prefixes[k][x,y] = providers
    implications = set()
    for k in range(4):
        for j,g in enumerate(poses):
            if levels[j]>k:
                continue
            for p,v in index.items():
                x,y = apply(g,p)
                for a,b in DIRS:
                    providers = prefixes[k+1].get((x+a,y+b),())
                    if v not in providers:
                        implications.add((-v,)+providers)
    if n>1:
        for (x,y),v in index.items():
            implications.add((-v,)+tuple(sorted(index[x+a,y+b] for a,b in DIRS
                                                if (x+a,y+b) in index)))
    clauses = {(-v,) for v in zero}
    clauses.update((-a,-b) for a,b in conflicts)
    clauses.update(implications)
    clauses = tuple(sorted(clauses))
    h = hashlib.sha256()
    for c in clauses:
        h.update((' '.join(map(str,c))+' 0\n').encode())
    counts = {'variables':len(cells),'global_cells':global_cells,
              'packing_units':len(zero),'packing_conflicts':len(conflicts),
              'implications':len(implications),'clauses':len(clauses),
              'cnf_sha256':h.hexdigest()}
    return cells,clauses,counts


def check_case(case,fixture):
    n = case['scale']
    assert type(n) is int and 1<=n<=5
    cells,clauses,counts = rebuild(n,fixture)
    assert all(case[k]==v for k,v in counts.items())
    reader = UnitReader(len(cells),clauses)
    assert len(case['negative_units'])==len(set(case['negative_units']))
    for v in case['negative_units']:
        reader.read_negative(v)
    anchor = cells.index((0,0))+1
    if n==1:
        # An incorrect negative anchor must be rejected by the same reader.
        try:
            reader.read_negative(anchor)
        except ValueError:
            pass
        else:
            raise AssertionError('Reader accepted a false negative anchor')
        reader.add_positive(anchor)
        assert all(reader.assignment[1:])
        selected = tuple(p for i,p in enumerate(cells,1) if reader.assignment[i]==1)
        assert selected==tuple(sorted(map(tuple,fixture['tile'])))
        result = 'unique anchored prototype is S17'
        positive = len(selected)
    else:
        assert all(v==-1 for v in reader.assignment[1:])
        assert reader.assignment[anchor]==-1
        result = 'no nonempty prototype satisfying necessary non-isolation'
        positive = 0
    return dict(scale=n,**counts,negative_units_checked=len(case['negative_units']),
                derived_zeros=reader.assignment.count(-1),derived_ones=positive,result=result)


def controls():
    r = UnitReader(2,[(-1,2),(-1,-2)])
    r.read_negative(1)
    try:
        r.read_negative(2)
    except ValueError:
        pass
    else:
        raise AssertionError('False RUP accepted')
    for bad in (0,3,True):
        try:
            r.read_negative(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('Malformed unit accepted')


def main():
    start = time.monotonic()
    controls()
    fixture_bytes = (HERE.parent/'seed.json').read_bytes()
    fixture = json.loads(fixture_bytes)
    certificate_bytes = (HERE/'certificate.json').read_bytes()
    certificate = json.loads(certificate_bytes)
    assert certificate['format']=='negative-unit-rup-v1'
    assert certificate['fixture_sha256']==hashlib.sha256(fixture_bytes).hexdigest()
    assert [c['scale'] for c in certificate['cases']]==list(range(1,6))
    mirrors = check_mirrors(fixture)
    sys.path.insert(0,str(HERE.parent))
    from check_geometry import check_coronas
    seed_stats,_,_ = check_coronas(tuple(map(tuple,fixture['tile'])),fixture['placements'],False)
    cases = []
    for case in certificate['cases']:
        row = check_case(case,fixture)
        cases.append(row)
        print(json.dumps(row,sort_keys=True),flush=True)
    summary = {'agent':'six-heesch-2','role':'researcher','mirror_audit':mirrors,
               'seed_coronas':seed_stats,'cases':cases,
               'certificate_sha256':hashlib.sha256(certificate_bytes).hexdigest()}
    expected = HERE/'expected.json'
    if '--write-expected' in sys.argv:
        expected.write_text(json.dumps(summary,indent=2)+'\n')
    else:
        assert summary==json.loads(expected.read_text())
    print(json.dumps(dict(summary,seconds=round(time.monotonic()-start,3),
                          max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),sort_keys=True))


if __name__=='__main__':
    main()
