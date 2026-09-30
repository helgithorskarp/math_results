"""Literal rational completion checker; independent of dual reconstruction."""
from collections import defaultdict
from math import gcd, lcm, prod
from time import monotonic
from binary_certificate import prime_powers, need


def verify_fractional(c):
    start=monotonic()
    N, minimum, denominator = c['N'],c['minimum'],c['denominator']
    need(all(type(x) is int for x in [N,minimum,denominator]) and
         N>=2 and minimum>=2 and denominator>0, 'Integer fractional parameters')
    A=c['prefix'];known=dict(A)
    need(len(known)==len(A) and all(type(n) is int and type(a) is int and
                                  n>=minimum and N%n==0 and 0<=a<n for n,a in A), 'Known fractional classes')
    groups=c['groups'];decoded=[];mass=defaultdict(int)
    for group in groups:
        n,w,count=(group[k] for k in ['modulus','numerator','phase_count'])
        need(all(type(x) is int for x in [n,w,count]) and n>=minimum and N%n==0 and
             n not in known and w>0 and count>0, 'Eligible nonnegative fractional group')
        periods=prime_powers(n);axes=group['phase_axes']
        need(len(axes)==len(periods), 'Fractional axes dimension')
        for axis,P in zip(axes,periods):
            need(axis and len(axis)==len(set(axis)) and all(type(a) is int and 0<=a<P for a in axis),
                 'Fractional phase axis')
        masks=[set(axis) for axis in axes]
        phases={a for a in range(n) if all(a%P in axis for P,axis in zip(periods,masks))}
        need(len(phases)==count==prod(len(axis) for axis in axes), 'Literal fractional phase count')
        decoded.append((n,w,count,phases))
        mass[n]+=w
    need(decoded and all(w<=denominator for w in mass.values()), 'Resource mass exceeds one')
    common=lcm(*(count for n,w,count,phases in decoded))
    coverage=[0]*N
    for n,w,count,phases in decoded:
        increment=w*(common//count)
        for a in phases:
            for x in range(a,N,n):coverage[x]+=increment
    residual=[x for x in range(N) if all(x%n!=a for n,a in A)]
    need(residual, 'Nonempty residual benchmark')
    lower=min(coverage[x] for x in residual);unit=denominator*common
    need(lower>=unit,'Uncovered fractional residual point')
    expected={'residual_points':len(residual),'common_phase_count_denominator':common,
              'minimum_scaled_coverage':lower,'coverage_unit':unit,
              'nonzero_groups':len(groups),'used_tail_resources':len(mass)}
    need(c.get('expected',expected)==expected,'Advertised fractional totals differ')
    d=gcd(lower,unit)
    return {**expected,'minimum_coverage_fraction':[lower//d,unit//d],
            'max_resource_numerator':max(mass.values()),'resource_denominator':denominator,
            'all_literal_checks_passed':True,'seconds':monotonic()-start}
