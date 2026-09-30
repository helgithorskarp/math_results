"""Exact complete exclusion of zero, one, or two changes of the saved base.

Actual author six-covering-1, researcher. Standard-library Python only.
All35 tail labels have arbitrary full phases. No global10080 exclusion.
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
B,N,P = 1440,10080,7


def load():
    raw = (ROOT/'near_cover.tsv').read_bytes()
    rows = [tuple(map(int,l.split())) for l in raw.decode().splitlines()]
    if ([m for a,m in rows] != [m for m in range(8,N+1) if N % m == 0] or
            any(not 0 <= a < m for a,m in rows)):
        raise ValueError('Invalid complete distinct divisor fixture')
    certificate = json.loads((ROOT/'weights.json').read_text())
    if (certificate['fixture_sha256'] != hashlib.sha256(raw).hexdigest() or
            certificate['period'] != N or certificate['base_period'] != B):
        raise ValueError('Certificate parameters or fixture changed')
    base = {m:a for a,m in rows if m % P}
    ds = [m//P for a,m in rows if m % P == 0]
    if len(base) != 30 or len(ds) != 35:
        raise ValueError('Wrong complete resource domain')
    cuts = []
    for rec in certificate['vectors']:
        f,previous = [0]*B,-1
        for z,w in rec['nonzero_weights']:
            if type(z) is not int or type(w) is not int or not previous < z < B or w <= 0:
                raise ValueError('Malformed sparse integer vector')
            f[z] = w; previous = z
        if not any(f):
            raise ValueError('Empty weight vector')
        W = sum(f)
        T = sum(max(sum(f[z] for z in range(a,B,d)) for a in range(d)) for d in ds)
        g = P*W-T
        c = {m:[sum(f[z] for z in range(a,B,m)) for a in range(m)] for m in base}
        cuts.append(dict(c=c,initial=sum(c[m][a] for m,a in base.items()),
                         threshold=(g+P-1)//P,W=W,T=T,g=g,max_weight=max(f)))
    if len(cuts) != 36 or cuts[0]['initial'] != 0 or cuts[0]['threshold'] != 23:
        raise ValueError('Incomplete or wrong cut collection')
    masks = {d:[sum(1 << z for z in range(a,B,d)) for a in range(d)]
             for d in dict.fromkeys(list(base)+ds)}
    return rows,base,ds,cuts,masks


def density_bound(H,ds,masks):
    h = H.bit_count()
    upper = sum(min(h,B//d) for d in ds)
    if upper < P*h:
        return upper,0
    for i,d in enumerate(ds):
        ceiling = min(h,B//d)
        maximum = 0
        for mask in masks[d]:
            maximum = max(maximum,(H & mask).bit_count())
            if maximum == ceiling:
                break
        upper += maximum-ceiling
        if upper < P*h:
            return upper,i+1
    return upper,len(ds)


def run():
    start = time.monotonic()
    rows,base,ds,cuts,masks = load()
    fullmask = (1 << B)-1
    small_counts = [0,0]
    for changes in [()] + [((m,a),) for m,old in base.items() for a in range(m) if a != old]:
        selected = base | dict(changes)
        if any(sum(v['c'][m][a] for m,a in selected.items()) < v['threshold'] for v in cuts):
            small_counts[len(changes)] += 1
            continue
        H = fullmask
        for m,a in selected.items():
            H &= ~masks[m][a]
        upper,depth = density_bound(H,ds,masks)
        if upper >= P*H.bit_count():
            raise ValueError('Unproved zero/one-base candidate: '+str(changes))
        small_counts[len(changes)] += 1
    cutcounts = [0]*len(cuts)
    density_depth = [0]*36
    density_closed = original_admitted = 0
    signature = hashlib.sha256()
    alternatives = {m:[a for a in range(m) if a != old] for m,old in base.items()}
    cache,blocks = {},[]
    for m,n in itertools.combinations(base,2):
        pre = [v['initial']-v['c'][m][base[m]]-v['c'][n][base[n]] for v in cuts]
        fixed = 0
        for q,a in base.items():
            if q not in (m,n):
                fixed |= masks[q][a]
        admitted = weighted = density = 0
        for a in alternatives[m]:
            need = cuts[0]['threshold']-pre[0]-cuts[0]['c'][m][a]
            if (n,need) not in cache:
                cache[n,need] = [b for b in alternatives[n] if cuts[0]['c'][n][b] >= need]
            for b in cache[n,need]:
                original_admitted += 1; admitted += 1
                for j in range(1,len(cuts)):
                    v = cuts[j]
                    if pre[j]+v['c'][m][a]+v['c'][n][b] < v['threshold']:
                        cutcounts[j] += 1; weighted += 1
                        signature.update(struct.pack('<7I',m,a,n,b,j,0,0))
                        break
                else:
                    H = fullmask ^ (fixed | masks[m][a] | masks[n][b])
                    h = H.bit_count()
                    upper,depth = density_bound(H,ds,masks)
                    if upper >= P*h:
                        raise ValueError('Unproved two-base candidate: '+str((m,a,n,b,h,upper)))
                    density_closed += 1; density += 1; density_depth[depth] += 1
                    signature.update(struct.pack('<7I',m,a,n,b,36,h,upper))
        total = (m-1)*(n-1)
        cutcounts[0] += total-admitted
        blocks.append([m,n,total,admitted,weighted,density])
    total = sum((m-1)*(n-1) for m,n in itertools.combinations(base,2))
    if (total != 10214513 or small_counts != [1,4863] or
            total != sum(cutcounts)+density_closed or density_closed != sum(density_depth)):
        raise ValueError('Incomplete replacement partition')
    # The actual saved fixture is a near cover, used only to specify the base.
    coverage = bytearray(N)
    for a,m in rows:
        for x in range(a,N,m):
            coverage[x] = 1
    out = dict(agent='six-covering-1',role='researcher',
               status='NO_COMPLETION_WITH_AT_MOST_TWO_BASE_CHANGES',
               base_period=B,period=N,base_resources=len(base),tail_resources=len(ds),
               vectors=len(cuts),zero_change_options=small_counts[0],one_change_options=small_counts[1],
               two_change_options=total,all_radius_two_options=sum(small_counts)+total,
               original_admitted=original_admitted,first_failed_weight_counts=cutcounts,
               partial_density_closed=density_closed,partial_density_depth_counts=density_depth,
               unproved=0,original_fixture_holes=coverage.count(0),
               event_sha256=signature.hexdigest(),block_sha256=hashlib.sha256(json.dumps(blocks).encode()).hexdigest(),
               weight_quantities=[{k:v[k] for k in ('initial','threshold','W','T','g','max_weight')} for v in cuts],
               seconds=time.monotonic()-start,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path)
    args = ap.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
