"""Check a period-10080 weighted tail-repair certificate from definitions.

Actual author six-covering-1, researcher. Standard library only. No LP,
SAT, CRT updater, search driver, or projected-capacity code is imported.
All physical residues and all eligible tail phases are evaluated exactly.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path


def ordinary_audit(N, B, C, rows, weights):
    if (N != B*C or math.gcd(B,C) != 1 or len(weights) != B
            or any(isinstance(w,bool) or not isinstance(w,int) or w < 0 for w in weights)
            or len({m for a,m in rows}) != len(rows)
            or any(m < 1 or N % m or not 0 <= a < m for a,m in rows)):
        raise ValueError('Invalid weighted residue instance')
    physical = [weights[x % B] for x in range(N)]
    base_resources, tail_resources = [], []
    R, evaluated_phases = 0, 0
    for a,m in rows:
        # Ordinary physical predicates: a phase is the bucket x % m.
        # No CRT formula or projected footprint supplies these sums.
        sums = [0]*m
        for x,w in enumerate(physical):
            sums[x % m] += w
        evaluated_phases += m
        if m % C == 0:
            tail_resources.append(dict(modulus=m, maximum=max(sums),
                                       maximizing_phase=sums.index(max(sums))))
        else:
            if B % m or any(s % C for s in sums):
                raise ValueError('Common-base phase multiplicity differs')
            coefficient = sums[a]//C
            R += coefficient
            base_resources.append(dict(modulus=m, fixed_phase=a,
                                       phase_weight=coefficient,
                                       maximum_phase_weight=max(sums)//C))
    capacity = sum(r['maximum'] for r in tail_resources)
    full_total, maximum = sum(physical), max(physical,default=0)
    if maximum == 0:
        raise ValueError('Zero weight vector supplies no certificate')
    gap = full_total-capacity
    residual_gap = max(0,gap-C*R)
    lower = (residual_gap+maximum-1)//maximum
    holes = [x for x in range(N) if not any(x % m == a for a,m in rows)]
    missed_weight = sum(physical[x] for x in holes)
    if missed_weight < residual_gap or len(holes) < lower:
        raise ValueError('Literal assignment violates counting inequality')
    return dict(base_weight_total=sum(weights),full_weight_total=full_total,
                tail_capacity=capacity,weighted_gap=gap,max_weight=maximum,
                fixed_base_phase_weight_sum=R,minimum_physical_holes=lower,
                required_base_phase_weight_sum=max(0,(gap+C-1)//C),
                literal_fixture_holes=len(holes),literal_fixture_missed_weight=missed_weight,
                support_size=sum(w>0 for w in weights),
                physical_residues=N,ordinary_phase_sums=evaluated_phases,
                ordinary_tail_phases=sum(r['modulus'] for r in tail_resources),
                ordinary_base_phases=sum(r['modulus'] for r in base_resources),
                base_resources=base_resources,tail_resources=tail_resources)


def read_certificate(assignment, certificate):
    rows=[tuple(map(int,line.split())) for line in assignment.read_text().splitlines()]
    obj=json.loads(certificate.read_text())
    N,B,C=obj['period'],obj['base_period'],obj['prime']
    if ((N,B,C) != (10080,1440,7)
            or obj['specified_assignment_sha256'] != hashlib.sha256(assignment.read_bytes()).hexdigest()
            or [m for a,m in rows] != [m for m in range(8,N+1) if N%m == 0]
            or min(m for a,m in rows) != 8 or math.lcm(*(m for a,m in rows)) != N):
        raise ValueError('Wrong specified complete near-cover')
    f=[0]*B; previous=-1
    for pair in obj['nonzero_weights']:
        if (not isinstance(pair,list) or len(pair) != 2
                or any(isinstance(x,bool) or not isinstance(x,int) for x in pair)):
            raise ValueError('Weights must be sorted integer point/weight pairs')
        z,w=pair
        if not previous < z < B or w < 1:
            raise ValueError('Duplicate, invalid or unsorted weight entry')
        f[z]=w; previous=z
    result=ordinary_audit(N,B,C,rows,f)
    if result['fixed_base_phase_weight_sum'] != 0:
        raise ValueError('Specified fixed base has positive weight')
    for key,value in obj['expected'].items():
        if isinstance(value,bool) or not isinstance(value,int) or result.get(key) != value:
            raise ValueError('Expected exact certificate total differs: '+key)
    if (result['minimum_physical_holes'] != 41
            or result['literal_fixture_holes'] != 87
            or result['required_base_phase_weight_sum'] != 23):
        raise ValueError('Advertised hole bound or phase condition differs')
    result.update(agent='six-covering-1',role='researcher',
                  status='EXACT_WEIGHT_CERTIFICATE_PASSED_LITERAL_PHYSICAL_CHECK',
                  assignment_sha256=hashlib.sha256(assignment.read_bytes()).hexdigest(),
                  certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest(),
                  scope='Specified30base congruences fixed; any subset and arbitrary full phases of35eligible tail congruences. Atleast41holes, not an exact optimum or global exclusion.')
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('assignment',type=Path)
    ap.add_argument('certificate',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    result=read_certificate(args.assignment,args.certificate)
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('base_resources','tail_resources')}))


if __name__=='__main__':main()
