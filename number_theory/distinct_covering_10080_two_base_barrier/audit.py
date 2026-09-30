"""Complete raw Cartesian replay with ordinary10080-point weight sums.

Imports no producer. Every base/tail phase of all36weights is recomputed.
Physical base unions are checked to repeat every1440points. The proved
projection bridge then checks density maxima without a solver or floats.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource
import struct
import time


ROOT = Path(__file__).resolve().parent


def audit():
    start = time.monotonic()
    expected = json.loads((ROOT/'expected.json').read_text())
    data = json.loads((ROOT/'weights.json').read_text())
    raw = (ROOT/'near_cover.tsv').read_bytes()
    if data['fixture_sha256'] != hashlib.sha256(raw).hexdigest():
        raise ValueError('Fixture hash mismatch')
    B,N,p = 1440,10080,7
    rows = [tuple(map(int,l.split())) for l in raw.decode().splitlines()]
    if ([m for a,m in rows] != [d for d in range(8,N+1) if N % d == 0] or
            any(not 0 <= a < m for a,m in rows)):
        raise ValueError('Not the full allowed divisor fixture')
    base = {m:a for a,m in rows if m % p}
    tails = [m for a,m in rows if m % p == 0]
    ds = [m//p for m in tails]
    coefficients,initials,gaps,quantities = [],[],[],[]
    for rec in data['vectors']:
        f,previous = [0]*B,-1
        for z,w in rec['nonzero_weights']:
            if type(z) is not int or type(w) is not int or not previous < z < B or w < 1:
                raise ValueError('Malformed integer weight')
            f[z] = w; previous = z
        weights = [f[x % B] for x in range(N)]
        c = {m:[sum(weights[x] for x in range(a,N,m)) for a in range(m)] for m in base}
        tail_capacity = sum(max(sum(weights[x] for x in range(a,N,m)) for a in range(m)) for m in tails)
        initial = sum(c[m][a] for m,a in base.items())
        gap = sum(weights)-tail_capacity
        if any(v % p for values in c.values() for v in values):
            raise ValueError('Physical base weights are not sevenfold')
        coefficients.append(c); initials.append(initial); gaps.append(gap)
        quantities.append(dict(initial=initial//p,threshold=(gap+p-1)//p,W=sum(f),T=tail_capacity,g=gap,max_weight=max(f)))
    if len(coefficients) != 36 or quantities != expected['weight_quantities']:
        raise ValueError('Every-phase physical weight quantities differ')
    physical_masks = {m:[sum(1 << x for x in range(a,N,m)) for a in range(m)] for m in base}
    projected_masks = {d:[sum(1 << z for z in range(a,B,d)) for a in range(d)] for d in ds}
    allbig,allsmall = (1 << N)-1,(1 << B)-1
    repetition = allbig//allsmall

    def density_bound(physical):
        H = physical & allsmall
        h = H.bit_count()
        if physical != H*repetition or physical.bit_count() != p*h:
            raise ValueError('Physical base residual is not periodic')
        upper = sum(min(h,B//d) for d in ds)
        if upper < p*h:
            return h,upper,0
        for i,d in enumerate(ds):
            # Full cofactor phase traversal, rather than the producer's early
            # stopping at a known footprint ceiling.
            cap = max((H & mask).bit_count() for mask in projected_masks[d])
            upper += cap-min(h,B//d)
            if upper < p*h:
                return h,upper,i+1
        raise ValueError('Unproved physical density case')

    small_counts = [0,0]
    small = [()] + [((m,a),) for m,old in base.items() for a in range(m) if a != old]
    for changes in small:
        selected = base | dict(changes)
        if not any(sum(c[m][a] for m,a in selected.items()) < g for c,g in zip(coefficients,gaps)):
            covered = 0
            for m,a in selected.items():
                covered |= physical_masks[m][a]
            density_bound(allbig ^ covered)
        small_counts[len(changes)] += 1
    total = admitted = density_closed = 0
    counts = [0]*36
    depthcounts = [0]*36
    signature = hashlib.sha256()
    blocks = []
    for m,n in itertools.combinations(base,2):
        pre = [v-c[m][base[m]]-c[n][base[n]] for v,c in zip(initials,coefficients)]
        fixed = 0
        for q,a in base.items():
            if q not in (m,n):
                fixed |= physical_masks[q][a]
        bt = ba = bw = bd = 0
        for a in range(m):
            if a == base[m]:
                continue
            for b in range(n):
                if b == base[n]:
                    continue
                total += 1; bt += 1
                if pre[0]+coefficients[0][m][a]+coefficients[0][n][b] < gaps[0]:
                    counts[0] += 1
                    continue
                admitted += 1; ba += 1
                for j in range(1,36):
                    if pre[j]+coefficients[j][m][a]+coefficients[j][n][b] < gaps[j]:
                        counts[j] += 1; bw += 1
                        signature.update(struct.pack('<7I',m,a,n,b,j,0,0))
                        break
                else:
                    physical = allbig ^ (fixed | physical_masks[m][a] | physical_masks[n][b])
                    h,upper,depth = density_bound(physical)
                    density_closed += 1; bd += 1; depthcounts[depth] += 1
                    signature.update(struct.pack('<7I',m,a,n,b,36,h,upper))
        blocks.append([m,n,bt,ba,bw,bd])
    observed = dict(zero_change_options=small_counts[0],one_change_options=small_counts[1],
                    two_change_options=total,all_radius_two_options=sum(small_counts)+total,
                    original_admitted=admitted,first_failed_weight_counts=counts,
                    partial_density_closed=density_closed,partial_density_depth_counts=depthcounts,
                    event_sha256=signature.hexdigest(),block_sha256=hashlib.sha256(json.dumps(blocks).encode()).hexdigest())
    if any(expected[k] != v for k,v in observed.items()) or total != sum(counts)+density_closed:
        raise ValueError('Full raw physical Cartesian classification differs')
    # The supplied65-class object is a near cover, not a claimed witness.
    coverage = bytearray(N)
    for a,m in rows:
        for x in range(a,N,m):
            coverage[x] = 1
    if coverage.count(0) != expected['original_fixture_holes']:
        raise ValueError('Fixture holes changed')
    return dict(agent='six-covering-1',role='researcher',
                status='COMPLETE_PHYSICAL_WEIGHT_AND_CARTESIAN_AUDIT_PASSED',
                **observed,ordinary_weight_phase_values=len(coefficients)*(sum(base)+sum(tails)),
                seconds=time.monotonic()-start,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                trust_boundary='Exact Python integers, literal physical weights/base masks,'
                               ' and the written coprime tail-projection proof. No solver, floats, or imported proof trace.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path)
    args = ap.parse_args()
    result = audit()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
