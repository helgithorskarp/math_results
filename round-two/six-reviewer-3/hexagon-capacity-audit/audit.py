"""Independent two-cap perimeter audit using rigorous rational quadrature.

No author imports, angle series, floating arithmetic, solver or proof input.
Geometry is the separate written proof in REVIEW.md. Precision and both
closed covers are fixed here before certification.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

ROOT_SCALE = 10**18
VALUE_SCALE = 10**24
PANELS = 256
GRID = 10**6
LEFT, RIGHT = Q(14,25), Q(3,5)
DECLARED = ((5972815,5930593),(5940024,5872936),(5905902,5814904),
            (5870453,5756484),(5833678,5697663))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


@lru_cache(maxsize=None)
def root(x):
    """Integer bisection at a decimal grid, with endpoint-square checks."""
    x = Q(x)
    need(0 <= x <= 4, 'fixed root domain')
    if x in (0,4):
        return (Q(0),Q(0)) if x == 0 else (Q(2),Q(2))
    lo, hi = 0, 2*ROOT_SCALE
    target = x.numerator*ROOT_SCALE**2
    for _ in range(64):
        if hi-lo == 1:
            break
        m = (lo+hi)//2
        difference = m*m*x.denominator-target
        if difference == 0:
            return Q(m,ROOT_SCALE),Q(m,ROOT_SCALE)
        if difference < 0:
            lo = m
        else:
            hi = m
    need(hi-lo == 1, 'complete fixed root bisection')
    a,b = Q(lo,ROOT_SCALE),Q(hi,ROOT_SCALE)
    need(a*a <= x <= b*b, 'outward root rounding')
    return a,b


def integrate_atan(z, panels=PANELS):
    """Composite Simpson for integral_0^z 1/(1+t^2), with |f''''|<=24.

    Every rational node value is itself enclosed on a 10^-24 grid before
    adding. This keeps denominator growth bounded without losing rigor.
    """
    z = Q(z)
    need(0 <= z <= 2 and type(panels) is int and panels > 0 and panels % 2 == 0,
         'fixed integration domain and even positive panel count')
    if z == 0:
        return Q(0),Q(0)
    total_lo = total_hi = 0
    for i in range(panels+1):
        t = z*i/panels
        f = 1/(1+t*t)
        low = f.numerator*VALUE_SCALE//f.denominator
        high = -((-f.numerator*VALUE_SCALE)//f.denominator)
        need(Q(low,VALUE_SCALE) <= f <= Q(high,VALUE_SCALE), 'node outward rounding')
        weight = 1 if i in (0,panels) else 4 if i % 2 else 2
        total_lo += weight*low
        total_hi += weight*high
    a = z*total_lo/(3*panels*VALUE_SCALE)
    b = z*total_hi/(3*panels*VALUE_SCALE)
    error = 24*z**5/(180*panels**4)
    return max(Q(0),a-error), b+error


@lru_cache(maxsize=None)
def angle_point(x):
    x = Q(x)
    need(-1 <= x <= 1, 'inverse cosine real domain')
    if x == -1:
        a,b = integrate_atan(Q(1))
        return 4*a,4*b
    a,b = root((1-x)/(1+x))
    first,last = integrate_atan(a),integrate_atan(b)
    return 2*first[0],2*last[1]


def angle_interval(ab):
    a,b = ab
    need(-1 <= a <= b <= 1, 'inverse cosine interval domain')
    return angle_point(b)[0], angle_point(a)[1]


def round_out(ab, grid=GRID):
    a,b = ab
    lo = Q(a.numerator*grid//a.denominator,grid)
    hi = Q(-((-b.numerator*grid)//b.denominator),grid)
    need(lo <= a <= b <= hi, 'outward output rounding')
    return lo,hi


def perimeter(c, tolerance):
    """Direct tangent-foot dot product, not the author's half-angle formula."""
    c,e = Q(c),Q(tolerance)
    cosine2 = 2*c*c/(1+c-e)
    sine2 = 1-cosine2
    tangent_dot = (c-sine2)/cosine2
    bearing2 = (sine2/cosine2)*(1-c)/(1+c)
    need(0 < cosine2 < 1 and 0 < sine2 < 1 and -1 < tangent_dot < 1
         and 0 < bearing2 < 1, 'complete spherical support branch domain')
    segment = angle_point(tangent_dot)
    alpha = angle_interval(root(bearing2))
    sr = root(sine2)
    need(segment[0] > 0 and alpha[0] > 0, 'positive boundary pieces')
    return 2*segment[0]+4*sr[0]*alpha[0],2*segment[1]+4*sr[1]*alpha[1]


def budget(c,tolerance):
    a,b = angle_point(Q(c)-Q(tolerance))
    return 6*a,6*b


def geometry_domain(tolerance):
    e = Q(tolerance)
    need(0 <= e < LEFT-Q(1,2), 'short six-cycle hemisphere domain')
    need(1-RIGHT-e > 0, 'noncrossing edge margin')
    # 1+c-e-2c^2 is concave; 5c^2-ec+e-1 is increasing.
    radial = min(1+c-e-2*c*c for c in (LEFT,RIGHT))
    stadium = 5*LEFT*LEFT-e*LEFT+e-1
    need(radial > 0 and 10*LEFT-e > 0 and stadium > 0,
         'positive cap and two-cap hemispherical domains everywhere')
    need(2+LEFT-2*e > 0, 'radius decreases with c everywhere')
    return {'k_lower':str(LEFT-e),'crossing_margin_lower':str(1-RIGHT-e),
            'cap_radicand_numerator_lower':str(radial),
            'two_cap_domain_polynomial_lower':str(stadium)}


def complete_cover(tolerance,cells,margin):
    need(type(cells) is int and cells > 0, 'positive complete cell count')
    geometry = geometry_domain(tolerance)
    endpoints = [LEFT+(RIGHT-LEFT)*i/cells for i in range(cells+1)]
    need(endpoints[0] == LEFT and endpoints[-1] == RIGHT
         and all(a < b for a,b in zip(endpoints,endpoints[1:])), 'closed complete cover')
    rows = []
    for a,b in zip(endpoints,endpoints[1:]):
        p = round_out(perimeter(b,tolerance))
        l = round_out(budget(a,tolerance))
        gap = p[0]-l[1]
        need(gap > Q(margin), 'uniform spherical perimeter contradiction margin')
        rows.append({'c_lower':str(a),'c_upper':str(b),
                     'stadium_lower_at_upper':str(p[0]),'stadium_upper_at_upper':str(p[1]),
                     'six_edges_lower_at_lower':str(l[0]),'six_edges_upper_at_lower':str(l[1]),
                     'gap_lower':str(gap)})
    return {'edge_tolerance':str(tolerance),'complete_cells':cells,
            'uniform_perimeter_gap_lower':str(margin),'actual_smallest_cell_gap':
            str(min(Q(row['gap_lower']) for row in rows)), 'geometry_domain':geometry,'cells':rows}


def controls():
    need(root(Q(9,16)) == (Q(3,4),Q(3,4)), 'exact rational square control')
    need(angle_point(Q(1)) == (0,0), 'zero-angle control')
    pi = angle_point(Q(-1))
    need(3 < pi[0] < pi[1] < Q(22,7), 'integrated pi enclosure')
    # Rational polynomial integration supplies an independent quadrature test:
    # Simpson is exact for constants, linears, quadratics and cubics.
    for power in range(4):
        n = 8
        total = sum((1 if i in (0,n) else 4 if i%2 else 2)*Q(i,n)**power
                    for i in range(n+1))/(3*n)
        need(total == Q(1,power+1), 'Simpson exactness through degree three')
    need(Q(32,5)-Q(20,3) == -24*Q(1,90),
         'quartic Simpson error and exact Peano-kernel mass')
    rejected = []
    tasks = {'root-negative':lambda:root(Q(-1)), 'root-too-large':lambda:root(Q(5)),
             'angle-too-large':lambda:angle_point(Q(1001,1000)),
             'odd-panels':lambda:integrate_atan(Q(1),255),
             'invalid-hemisphere':lambda:geometry_domain(Q(1,10)),
             'false-perimeter-margin':lambda:complete_cover(Q(1,100),1,Q(1)),
             'false-wider-band':lambda:complete_cover(Q(1,40),40,Q(0))}
    for name,task in tasks.items():
        try:
            task()
        except ValueError:
            rejected.append(name)
    need(len(rejected) == len(tasks), 'all meaningful damages rejected')
    return {'exact_cubic_quadrature_controls':4,'rejected_controls':rejected,
            'pi_interval':list(map(str,round_out(pi,10**9)))}


def main():
    original = complete_cover(Q(1,100),5,Q(1,25))
    for row,(pl,lu) in zip(original['cells'],DECLARED):
        c = Q(row['c_upper']);a = Q(row['c_lower'])
        need(perimeter(c,Q(1,100))[0] >= Q(pl,GRID)
             and budget(a,Q(1,100))[1] <= Q(lu,GRID), 'every stated author endpoint bound')
    strengthened = complete_cover(Q(1,60),40,Q(1,100))
    e = Q(1,60)
    need(LEFT-e > RIGHT**2, 'all unequal-neighbor radial derivatives negative')
    k = RIGHT-e
    angle_cosine = (RIGHT-k*k)/(1-k*k)
    need(angle_cosine == Q(187,475) < Q(1,2), 'near-contact maximum-degree-five bound')
    p,l = perimeter(LEFT,Q(1,40)),budget(LEFT,Q(1,40))
    bad = round_out((p[0]-l[1],p[1]-l[0]))
    need(bad[1] < 0, 'wider1/40 fails this scalar route, not geometry itself')
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'status':'VERIFIED','method':'rational composite Simpson with global fourth-derivative error',
            'panels':PANELS,'root_decimal_scale':ROOT_SCALE,'integrand_decimal_scale':VALUE_SCALE,
            'outward_grid':GRID,'original':original,'strengthened':strengthened,
            'near_contact_tangent_cosine_upper':str(angle_cosine),
            'wider1_40_same_endpoint_gap':list(map(str,bad)),'controls':controls()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    result = main()
    if args.output:
        args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'complete_evidence_sha256':canonical_hash(result),
                      'original_cells':result['original']['complete_cells'],
                      'strengthened_cells':result['strengthened']['complete_cells'],
                      'strengthened_smallest_gap':result['strengthened']['actual_smallest_cell_gap'],
                      'rejected_controls':len(result['controls']['rejected_controls'])},sort_keys=True))
