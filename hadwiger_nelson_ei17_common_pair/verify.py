"""Solver-free certificate checker. Run with Python 3.11+ and no packages."""
import argparse
import hashlib
import json
from itertools import combinations, product
from pathlib import Path
from intervals import I, Q, ONE, norm, subtract, squared_distance
from seed import certify, require

HERE = Path(__file__).resolve().parent


def frame(points, pair, reverse, mirror):
    i, j = pair[::-1] if reverse else pair
    a, b = points[i], points[j]
    dx, dy = subtract(b, a)
    length = norm((dx, dy)).sqrt()
    answer = []
    for z in points:
        x, y = subtract(z, a)
        u = (x * dx + y * dy) / length
        v = (y * dx - x * dy) / length
        answer.append((u, -v if mirror else v))
    return answer


def validate_word(points, word):
    require(isinstance(word, str) and len(word) == len(points), 'colour word length')
    require(set(word) <= set('0123'), 'colour alphabet')
    same, different = 0, 0
    unit_gap = None
    # Coordinate endpoints are integers over Q. Work over Q**2 directly.
    for i, j in combinations(range(len(points)), 2):
        p, q = points[i], points[j]
        if word[i] != word[j]:
            require(any(a.hi < b.lo or b.hi < a.lo for a,b in zip(p,q)),
                    f'different colours could coincide: {i},{j}')
            different += 1
            continue
        lower = upper = 0
        for a, b in zip(p, q):
            lo, hi = a.lo - b.hi, a.hi - b.lo
            lower += 0 if lo <= 0 <= hi else min(lo*lo, hi*hi)
            upper += max(lo*lo, hi*hi)
        gap = max(lower - Q*Q, Q*Q - upper)
        require(gap > 0, f'same-colour distance might equal one: {i},{j}')
        unit_gap = gap if unit_gap is None else min(unit_gap, gap)
        same += 1
    return dict(labels=len(points), pairs=same+different, same_colour_pairs=same,
                different_colour_pairs=different,
                same_colour_squared_unit_gap_lower_units_1e_minus_12=
                0 if unit_gap is None else unit_gap * 10**12 // (Q*Q))


def pair_partition(points, certificate):
    require(isinstance(certificate, list) and len(certificate) > 0, 'empty certificate')
    seen, bounds = set(), []
    for c in certificate:
        require(isinstance(c, dict) and set(c) == {'pairs', 'word'}, 'group schema')
        require(isinstance(c['pairs'], list) and len(c['pairs']) > 0, 'empty pair group')
        intervals = []
        for pair in c['pairs']:
            require(isinstance(pair, list) and len(pair) == 2, 'pair schema')
            u, v = pair
            require(type(u) is int and type(v) is int and 0 <= u < v < 17, 'pair labels')
            require((u,v) not in seen, 'repeated source pair')
            seen.add((u,v))
            intervals.append(squared_distance(points[u], points[v]))
        bounds.append((min(d.lo for d in intervals), max(d.hi for d in intervals)))
    require(seen == set(combinations(range(17), 2)), 'incomplete source pair coverage')
    ordered = sorted(bounds)
    require(all(a[1] < b[0] for a,b in zip(ordered, ordered[1:])), 'pair groups overlap')
    gap = min(b[0] - a[1] for a,b in zip(ordered, ordered[1:])) if len(ordered)>1 else 0
    return gap * 10**12 // Q


def first_circle_completion(points):
    answer = list(points)
    included = []
    four, quarter, half = I.rational(4), I.rational('1/4'), I.rational('1/2')
    for i,j in combinations(range(17),2):
        a,b = points[i],points[j]
        dx,dy = subtract(b,a)
        d2 = norm((dx,dy))
        require(d2.lo > 0 and not d2.contains(4), 'circle tangency or duplicate centre unresolved')
        if d2.lo > four.hi:
            continue
        require(d2.hi < four.lo, 'circle existence unresolved')
        factor = (ONE/d2-quarter).sqrt()
        mx,my = (a[0]+b[0])*half,(a[1]+b[1])*half
        for sign in (-1,1):
            s = I.rational(sign)
            answer.append((mx-s*dy*factor, my+s*dx*factor))
        included.append([i,j])
    return answer,included


def verify():
    points, root = certify()
    certificate = json.loads((HERE/'fan_certificate.json').read_text())
    group_gap = pair_partition(points,certificate)
    fans=[]
    for number,c in enumerate(certificate):
        union=[]
        for pair in c['pairs']:
            for reverse,mirror in product((False,True),repeat=2):
                union.extend(frame(points,pair,reverse,mirror))
        report=validate_word(union,c['word'])
        report.update(group=number,source_pairs=len(c['pairs']),frames=4*len(c['pairs']))
        fans.append(report)
    circles,included=first_circle_completion(points)
    circle_word=(HERE/'circle_word.txt').read_text().strip()
    circle=validate_word(circles,circle_word)
    circle.update(centre_pairs_with_two_intersections=len(included))
    report=dict(seed=root,interval_denominator=str(Q),pair_groups=len(fans),
                source_pairs=sum(x['source_pairs'] for x in fans),
                total_frames=sum(x['frames'] for x in fans),
                total_labels=sum(x['labels'] for x in fans),
                largest_fan_labels=max(x['labels'] for x in fans),
                checked_fan_pairs=sum(x['pairs'] for x in fans),
                separated_squared_distance_groups_gap_lower_units_1e_minus_12=group_gap,
                every_common_pair_assembly_four_colourable=True,
                first_circle_completion=circle,fans=fans,
                certificate_sha256=hashlib.sha256((HERE/'fan_certificate.json').read_bytes()).hexdigest())
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check-expected',action='store_true')
    args=parser.parse_args()
    result=verify()
    if args.check_expected:
        require(result==json.loads((HERE/'expected.json').read_text()),'expected output mismatch')
    rendered=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.write_text(rendered)
    print(json.dumps({k:v for k,v in result.items() if k!='fans'},sort_keys=True,indent=2))
