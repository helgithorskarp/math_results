"""Exact degree-filtered enumeration of the four outside C3 cycles."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

from incidence import root_rows

PAIRS = tuple(itertools.combinations(range(4),2))
SPINES_B = tuple([(3*i,3*i+1) for i in range(4)] +
                [(3*i,3*j+k) for i,j in PAIRS for k in range(3)])
POPCOUNT = tuple(x.bit_count() for x in range(8))


def pair_rows(i,j,mask):
    rows = [0]*12
    for t in range(3):
        for k in range(3):
            if mask>>k&1:
                u,v = 3*i+t,3*j+(t+k)%3
                rows[u] |= 1<<v
                rows[v] |= 1<<u
    return tuple(rows)


def outside_graphs(profiles, deadline):
    targets = {}
    result = {profile:[] for profile in profiles}
    for profile in profiles:
        for internal in range(16):
            sums = tuple(profile[i]-2*(internal>>i&1) for i in range(4))
            targets.setdefault(sums,[]).append((profile,internal))
    table = [[pair_rows(i,j,m) for m in range(8)] for i,j in PAIRS]
    # Each internal orbit is a triangle.
    triangles = [tuple(sum(1<<(3*i+s) for s in range(3) if s!=t) if u//3==i else 0
                       for u in range(12) for t in [u%3]) for i in range(4)]
    degree_matches = {profile:0 for profile in profiles}
    cross_count = 0
    for masks in itertools.product(range(8),repeat=6):
        cross_count += 1
        if cross_count%4096==0 and time.monotonic()>deadline:
            return result,degree_matches,cross_count,False
        a,b,c,d,e,f = map(POPCOUNT.__getitem__,masks)
        sums = (a+b+c,a+d+e,b+d+f,c+e+f)
        choices = targets.get(sums)
        if not choices:
            continue
        base = [0]*12
        for p,mask in enumerate(masks):
            component = table[p][mask]
            for u in range(12):
                base[u] |= component[u]
        for profile,internal in choices:
            degree_matches[profile] += 1
            rows = base.copy()
            for i in range(4):
                if internal>>i&1:
                    for u in range(3*i,3*i+3):
                        rows[u] |= triangles[i][u]
            if any(rows[3*i].bit_count()!=profile[i] for i in range(4)):
                raise RuntimeError('outside degree calculation disagrees')
            good = True
            for u,v in SPINES_B:
                red = bool(rows[u]>>v&1)
                common = rows[u]&rows[v] if red else 4095^((1<<u)|(1<<v)|rows[u]|rows[v])
                if common.bit_count()>(3 if red else 5):
                    good = False
                    break
            if good:
                result[profile].append(dict(internal=internal,masks=list(masks),rows=rows,
                    code=internal+sum(mask<<(4+3*p) for p,mask in enumerate(masks))))
    return result,degree_matches,cross_count,True


def base_rows(code,patterns):
    rows = root_rows(code)+[0]*13
    rows[21] = 511
    for a in range(9):
        rows[a] |= 1<<21
    for j,masks in enumerate(patterns):
        for a in range(9):
            for t in range(3):
                if masks[a//3]>>((t-a)%3)&1:
                    b = 9+3*j+t
                    rows[a] |= 1<<b
                    rows[b] |= 1<<a
    return rows


def bad_spine(rows):
    for u,v in itertools.combinations(range(22),2):
        red = bool(rows[u]>>v&1)
        common = rows[u]&rows[v] if red else ((1<<22)-1)^((1<<u)|(1<<v)|rows[u]|rows[v])
        if common.bit_count()>(3 if red else 6):
            return u,v,red,common.bit_count()
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--incidences',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--seconds',type=int,default=30)
    args = parser.parse_args()
    started = time.monotonic()
    cases = json.loads(args.incidences.read_text())
    if any(case['status']!='COMPLETE' for case in cases):
        raise ValueError('cannot claim coverage from incomplete incidences')
    profiles = set()
    for case in cases:
        for patterns in case['incidence_representatives']:
            full = [10]*4 if case['placement']=='inside' else [9,10,10,10]
            profiles.add(tuple(d-sum(m.bit_count() for m in pattern) for d,pattern in zip(full,patterns)))
    graphs,degree_matches,coverage,complete = outside_graphs(sorted(profiles),time.monotonic()+args.seconds)
    report = dict(status='COMPLETE' if complete else 'INCOMPLETE',
                  cross_assignments=coverage,expected_cross_assignments=8**6,
                  outside_profiles=[dict(degrees=profile,degree_matches=degree_matches[profile],
                    necessary_page_survivors=len(graphs[profile]),
                    candidate_sha256=hashlib.sha256(''.join(str(code)+'\n' for code in sorted(
                        candidate['code'] for candidate in graphs[profile])).encode()).hexdigest())
                    for profile in sorted(profiles)],
                  cases=[],valid_completions=[],seconds_budget=args.seconds)
    print(json.dumps({k:v for k,v in report.items() if k not in ('cases','valid_completions')}),flush=True)
    if complete:
        for case in cases:
            counts = []
            full = [10]*4 if case['placement']=='inside' else [9,10,10,10]
            digest = hashlib.sha256()
            for patterns in case['incidence_representatives']:
                profile = tuple(d-sum(m.bit_count() for m in pattern) for d,pattern in zip(full,patterns))
                base = base_rows(case['code'],patterns)
                expected_A = [9]*3+[10]*6 if case['placement']=='inside' else [10]*9
                if [row.bit_count() for row in base[:9]]!=expected_A or base[21].bit_count()!=9:
                    raise RuntimeError('incidence has wrong root-side degrees')
                rejected = 0
                for candidate in graphs[profile]:
                    rows = base.copy()
                    for u in range(12):
                        rows[u+9] |= candidate['rows'][u]<<9
                    if sum(row.bit_count() for row in rows)!=216:
                        raise RuntimeError('completed graph has wrong edge count')
                    failure = bad_spine(rows)
                    digest.update(json.dumps([patterns,candidate['internal'],candidate['masks'],failure],
                                             separators=(',',':')).encode()+b'\n')
                    if failure is None:
                        report['valid_completions'].append(dict(placement=case['placement'],
                            code=case['code'],patterns=patterns,candidate=candidate))
                    else:
                        rejected += 1
                counts.append(dict(profile=profile,tested=len(graphs[profile]),rejected=rejected))
            record = dict(placement=case['placement'],code=case['code'],
                          incidence_representatives=len(counts),
                          completions_tested=sum(x['tested'] for x in counts),
                          completions_rejected=sum(x['rejected'] for x in counts),
                          per_incidence=counts,completion_sha256=digest.hexdigest())
            report['cases'].append(record)
            print(json.dumps({k:v for k,v in record.items() if k!='per_incidence'}),flush=True)
            args.output.write_text(json.dumps(report,indent=2)+'\n')
    report['seconds'] = time.monotonic()-started
    report['rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('complete',complete,'valid completions',len(report['valid_completions']),
          'seconds',report['seconds'],'RSS KiB',report['rss_kib'],flush=True)


if __name__ == '__main__':
    main()
