"""Bit-intersection verification, literal W rows; no other module imported."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path


def need(ok, text):
    if not ok:
        raise ValueError(text)


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length()-1
        mask ^= low


def cliques(rows, candidates, size, prefix=0):
    if size == 0:
        yield prefix
    else:
        while candidates.bit_count() >= size:
            low = candidates & -candidates
            candidates ^= low
            v = low.bit_length()-1
            yield from cliques(rows, candidates & rows[v], size-1, prefix | low)


def audit(g, density):
    need(type(g) is dict and sorted(g) == ['n','red_edges'], 'schema')
    need(type(g['n']) is int and g['n'] == 20, 'n')
    need(type(g['red_edges']) is list, 'edges')
    rows = [0]*20
    previous = (-1,-1)
    for e in g['red_edges']:
        need(type(e) is list and len(e) == 2 and all(type(v) is int for v in e), 'pair')
        a,b = e
        need(0 <= a < b < 20 and (a,b) > previous, 'pair range/order/duplicate')
        rows[a] |= 1 << b
        rows[b] |= 1 << a
        previous = (a,b)
    degree = [row.bit_count() for row in rows]
    need(density in (92,93) and sum(degree) == 2*density, 'density')
    need(rows[0] == 0b11000011110000000000 and rows[1] == 0b11111100000000000000, 'marked rows')
    need([(rows[v] >> 2) & 255 for v in range(2,10)] == [30,45,115,179,205,206,180,120], 'W rows')
    full = (1 << 20)-1
    blue = [full ^ (1 << v) ^ rows[v] for v in range(20)]
    need(next(cliques(rows, full, 4), None) is None, 'red K4')
    need(next(cliques(blue, full, 5), None) is None, 'blue K5')
    cone = [r | (1 << 20) for r in rows] + [full]
    full21 = (1 << 21)-1
    cone_blue = [full21 ^ (1 << v) ^ cone[v] for v in range(21)]
    need(next(cliques(cone, full21, 5), None) is None, 'red cone K5')
    need(next(cliques(cone_blue, full21, 5), None) is None, 'blue cone K5')
    margins = [19-degree[v] if v < 2 else 20-degree[v] for v in range(20)]
    outside_red = density+32
    need(sum(margins) == 398-2*density, 'cross total')
    need(2*outside_red+sum(margins) == 462, 'outside stars')
    need(margins[:2] == [13,13] and min(margins) >= 0 and max(margins) <= 22, 'row margins')
    details = dict(red_triangle_masks=sorted(cliques(rows,full,3)), blue_K4_masks=sorted(cliques(blue,full,4)))
    # The checked-set counts describe the covered domain, not recursion visits.
    return dict(n=20, red_edges=sum(degree)//2, degrees=degree, marked_common_red=list(bits(rows[0]&rows[1])),
                W_blue_mask=5388912, red_K4=0, blue_K5=0, cone_red_K5=0, cone_blue_K5=0,
                cone_red_edges=density+20, checked_H_four_sets=4845, checked_H_five_sets=15504,
                checked_cone_five_sets=20349,
                lift=dict(H_original_labels=list(range(1,11))+list(range(20,24))+list(range(33,37))+[41,42],
                          required_red_cross_degrees=margins, required_red_cross_total=sum(margins),
                          outside_order=22, required_outside_red_edges=outside_red,
                          required_outside_blue_edges=199-density,
                          outside_original_labels=[11,12,13,14,15,16,17,18,19,24,25,26,27,28,29,30,31,32,37,38,39,40],
                          outside_marked_patterns=[1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3]),
                red_triangles=len(details['red_triangle_masks']), blue_K4s=len(details['blue_K4_masks']),
                clique_detail_sha256=hashlib.sha256(json.dumps(details,sort_keys=True,separators=(',',':')).encode()).hexdigest()), details


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--report',type=Path,required=True)
    a=p.parse_args(); reports={}
    for d in (92,93):
        path=a.directory/f'H{d}.json'
        reports[d]=audit(json.loads(path.read_text()),d)[0]
        reports[d]['graph_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    with a.report.open('x') as f:
        json.dump(dict(status='BIT_GRAPHS_AND_NECESSARY_LIFT_MARGINS_CHECKED',cases=reports),f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(reports),flush=True)


if __name__=='__main__':
    main()
