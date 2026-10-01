"""Definition-level H8 audit through literal orbits and AP reversal classes.

Neither full discrete logarithms nor Euler-quotient labels are used. All
field supports, case clauses and the cyclic-window spectrum are recovered.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

from rup import clauses, need

P, M = 617, 77


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def quotient():
    need(all(P % d for d in range(2, 25)), 'Prime field by complete trial division')
    generator = pow(3, 77, P)
    subgroup = []
    x = 1
    while x not in subgroup:
        subgroup.append(x)
        x = x * generator % P
    need(x == 1 and len(subgroup) == 8, 'Exact subgroup order')
    labels, cosets, x = {}, [], 1
    for i in range(M):
        orbit = sorted(x * h % P for h in subgroup)
        need(len(set(orbit)) == 8 and not set(orbit).intersection(labels), 'Disjoint literal cosets')
        labels.update({z: i for z in orbit})
        cosets.append(orbit)
        x = x * 3 % P
    need(len(labels) == P-1 and x in subgroup, 'Complete quotient and cyclic return')
    need(all(labels[z*3 % P] == (i+1) % M for z,i in labels.items()), 'Literal field rotation')
    return labels, cosets


def reconstruct():
    labels, cosets = quotient()
    supports, witnesses = set(), {}
    retained = excluded = 0
    # (a,d) and (a+6d,-d) have identical seven terms in reverse order.
    # Exactly one difference lies in 1..308. No orbit has a fixed point.
    for difference in range(1, (P+1)//2):
        for start in range(P):
            terms = [(start+j*difference) % P for j in range(7)]
            if 0 in terms:
                excluded += 1
                continue
            retained += 1
            support = tuple(sorted({labels[z] for z in terms}))
            supports.add(support)
            witnesses.setdefault(support, [start, difference])
    need(retained+excluded == P*(P-1)//2 and excluded == 2156 and retained == 187880,
         'Complete actual AP reversal-class coverage')
    need(len(supports) == 23177, 'Complete support count')
    ranks = dict(sorted(Counter(map(len, supports)).items()))
    need(ranks == {4:77,5:231,6:4543,7:18326}, 'Actual quotient support ranks')
    span_counts = Counter()
    minimizing, best = [], M
    for edge in sorted(supports):
        gaps = [((edge[(j+1) % len(edge)]-edge[j]) % M,j) for j in range(len(edge))]
        largest, j = max(gaps)
        width = M-largest+1
        span_counts[width] += 1
        if width < best:
            best, minimizing = width, []
        if width == best:
            start = edge[(j+1) % len(edge)]
            shape = tuple(sorted((z-start) % M for z in edge))
            minimizing.append([list(edge), witnesses[edge], start, list(shape)])
    need(best == 19 and len(minimizing) == 77 and
         {tuple(z[3]) for z in minimizing} == {(0,1,2,8,18)}, 'Sharp single-AP window classification')
    critical = [3+34*j for j in range(7)]
    critical_labels = [labels[z] for z in critical]
    need(critical_labels == [1,8,1,2,0,18,8], 'Ordered critical AP labels')
    scalar = 1
    for shift in range(M):
        need([labels[z*scalar % P] for z in critical] ==
             [(z+shift) % M for z in critical_labels], 'All scaled ordered critical APs')
        scalar = scalar*3 % P
    info = {'status':'LITERAL_ORBIT_AND_REVERSAL_CLASS_CENSUS_VERIFIED',
            'AP_reversal_classes':retained+excluded,'retained_classes':retained,'zero_classes':excluded,
            'ordered_APs_covered':2*(retained+excluded),'ordered_retained_APs':2*retained,
            'ordered_zero_APs':2*excluded,'supports':len(supports),'ranks':ranks,
            'support_sha256':digest(sorted(supports)),'literal_cosets_sha256':digest(cosets),
            'critical_AP':critical,'critical_labels':critical_labels,'scaled_critical_checks':M,
            'minimum_AP_window':best,'minimizing_supports':len(minimizing),
            'minimizing_shapes':sorted({tuple(z[3]) for z in minimizing}),
            'window_histogram':dict(sorted(span_counts.items())),
            'minimal_example':minimizing[0]}
    return supports, info


def expected_clauses(length, supports):
    need(type(length) is int and 2 <= length <= 18, 'Exact longest-run case')
    rows = []
    for support in supports:
        positive = tuple(z+1 for z in support)
        rows.extend([positive, tuple(-z for z in positive)])
    for start in range(M):
        window = tuple((start+j) % M+1 for j in range(length+1))
        rows.extend([window, tuple(-z for z in window)])
    rows.extend([(-i,) for i in range(1,length+1)])
    rows.extend([(length+1,), (M,)])
    return rows


def compare(length, path, supports):
    nvars, rows = clauses(path)
    mathematical = expected_clauses(length,supports)
    need(nvars == M, 'Exact coset variable domain')
    canonical = lambda row: tuple(sorted(row))
    need(Counter(map(canonical,rows)) == Counter(map(canonical,mathematical)),
         'Complete literal clause multiset equality')
    need(len(rows) == 46510+length, 'Complete case dimensions')
    return {'length':length,'variables':nvars,'clauses':len(rows),
            'literals':sum(map(len,rows)),'CNF_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case-dir',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    began = time.monotonic()
    supports, result = reconstruct()
    result['cases'] = [compare(length,args.case_dir/f'run-{length}.cnf',supports)
                       for length in range(2,19)]
    result.update(agent='six-reviewer-5',role='independent reviewer',
                  optimization=sys.flags.optimize,python=sys.version.split()[0],
                  seconds=time.monotonic()-began,maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
