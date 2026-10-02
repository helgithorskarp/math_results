"""Constant-count interval predicates for the literal T_k polyhex family.

The ordinary all-k argument is STRIP_COLUMN_LEMMA.md. Bounded materialized
comparisons below validate this implementation and prove no Heesch upper.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import time

DIRS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
UV_DIRS = tuple((x+2*y,y) for x,y in DIRS)

def require(condition, message):
    if not condition:
        raise ValueError(message)

def columns(k):
    require(type(k) is int and k >= 1, 'k must be a positive integer')
    return {-2:[(k-1,k-1)], -1:[(k,k)], 0:[(0,k)],
            1:[(1,k)], 2:[(2,k+1)], 3:[(2,k+1)]}

def halo_columns(k):
    raw = {}
    for du,dv in ((0,0),)+UV_DIRS:
        for u,intervals in columns(k).items():
            for lo,hi in intervals:
                raw.setdefault(u+du,[]).append((lo+dv,hi+dv))
    result = {}
    for u,intervals in raw.items():
        merged = []
        for lo,hi in sorted(intervals):
            if merged and lo <= merged[-1][1]+1:
                merged[-1] = (merged[-1][0],max(hi,merged[-1][1]))
            else:
                merged.append((lo,hi))
        result[u] = merged
    return result

def conjugated_d6():
    result = []
    for s in (1,-1):
        for r in range(6):
            p,q = DIRS[r][0],DIRS[(r+s)%6][0]
            c,d = DIRS[r][1],DIRS[(r+s)%6][1]
            result.append((p+2*c,q+2*d-2*p-4*c,c,d-2*c))
    return tuple(result)

MATRICES = conjugated_d6()

def ceil_div(a,b):
    return -((-a)//b)

def intersection_count(k,matrix,shift,target):
    require(matrix in MATRICES,'Non-D6 matrix')
    alpha,beta,gamma,delta = matrix
    a,b = shift
    umin,umax = min(target),max(target)
    total = 0
    for u,intervals in columns(k).items():
        for lo,hi in intervals:
            if beta == 0:
                image_u = alpha*u+a
                endpoints = (gamma*u+delta*lo+b,gamma*u+delta*hi+b)
                image_lo,image_hi = min(endpoints),max(endpoints)
                for target_lo,target_hi in target.get(image_u,[]):
                    total += max(0,min(image_hi,target_hi)-max(image_lo,target_lo)+1)
            else:
                offset = alpha*u+a
                if beta > 0:
                    first,last = ceil_div(umin-offset,beta),(umax-offset)//beta
                else:
                    first,last = ceil_div(umax-offset,beta),(umin-offset)//beta
                for v in range(max(lo,first),min(hi,last)+1):
                    image_u,image_v = offset+beta*v,gamma*u+delta*v+b
                    total += any(l <= image_v <= h for l,h in target.get(image_u,[]))
    return total

def counts(k,matrix,shift):
    root = intersection_count(k,matrix,shift,columns(k))
    closed = intersection_count(k,matrix,shift,halo_columns(k))
    require(closed >= root,'Closed halo lost root cells')
    return root,closed-root

def literal_cells(k):
    cells = {(0,0),(-2*k,k-1),(-2*k-1,k)}
    for r in range(k):
        cells.update({(-2*r-1,r+1),(-2*r-1,r+2),
                      (-2*r-2,r+1),(-2*r-2,r+2)})
    return {(x+2*y,y) for x,y in cells}

def materialize(cols):
    return {(u,v) for u,intervals in cols.items() for lo,hi in intervals for v in range(lo,hi+1)}

def main():
    start = time.monotonic()
    require(len(set(MATRICES)) == 12,'Incomplete D6')
    require(sum(m[1] == 0 for m in MATRICES) == 4 and
            sum(abs(m[1]) == 3 for m in MATRICES) == 8,'Wrong spine coefficients')
    tested = 0
    maxima = {'root_nonparallel':0,'closed_halo_nonparallel':0}
    for k in range(1,9):
        root = literal_cells(k)
        require(root == materialize(columns(k)) and len(root) == 4*k+3,'Column formula disagrees')
        closed = root | {(u+du,v+dv) for u,v in root for du,dv in UV_DIRS}
        require(closed == materialize(halo_columns(k)),'Halo intervals disagree')
        for matrix in MATRICES:
            alpha,beta,gamma,delta = matrix
            shifts = {(a,b) for a in range(-7,8) for b in range(-4,k+5)}
            shifts |= {(a,b) for a in (-3*k,-2*k,-k,k,2*k,3*k)
                       for b in (-2*k,-k,0,k,2*k)}
            for a,b in sorted(shifts):
                image = {(alpha*u+beta*v+a,gamma*u+delta*v+b) for u,v in root}
                got = counts(k,matrix,(a,b))
                expected = (len(image & root),len(image & (closed-root)))
                require(got == expected,'Interval predicate disagrees with materialized cells')
                if beta:
                    require(got[0] <= 10 and sum(got) <= 18,'Universal bound violated')
                    maxima['root_nonparallel'] = max(maxima['root_nonparallel'],got[0])
                    maxima['closed_halo_nonparallel'] = max(maxima['closed_halo_nonparallel'],sum(got))
                tested += 1
    # Huge k must not expand its cells or iterate through its length.
    huge = 10**100
    huge_checks = [(matrix,counts(huge,matrix,(0,0))) for matrix in MATRICES]
    for matrix,(root,opened) in huge_checks:
        if matrix[1]:
            require(root <= 10 and root+opened <= 18,'Large-integer bound violated')
    identity = MATRICES[0]
    require(counts(huge,identity,(0,0)) == (4*huge+3,0),'Large parallel interval identity failed')
    evidence = {'agent':'six-heesch-2','role':'researcher','complete_bounded_comparison':True,
                'parameter_sample':list(range(1,9)),'sample_queries':tested,'sample_maxima':maxima,
                'large_parameter_decimal_digits':101,'large_queries':len(huge_checks),
                'normal_or_optimized':'normal' if __debug__ else 'optimized',
                'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'claim_scope':'Bounded implementation check; all-k ordinary lemma is a separate proof; no Heesch upper',
                'checked_utc':datetime.now(timezone.utc).isoformat(),
                'seconds':round(time.monotonic()-start,3),
                'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    out = Path(__file__).absolute().with_name('strip-columns-'+evidence['normal_or_optimized']+'.json')
    out.write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence,sort_keys=True),flush=True)

if __name__ == '__main__':
    main()
