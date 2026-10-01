"""Exact root-to-outside incidence domains; no outside completion claim."""
import argparse
import itertools
import json
from pathlib import Path
import resource
import time

PAIR_A = tuple(itertools.combinations(range(9), 2))


def root_rows(code):
    rows = [0]*9
    for u,v in PAIR_A:
        i,j = u//3,v//3
        position = i if i == j else 3+3*((0,1),(0,2),(1,2)).index((i,j))+(v-u)%3
        if code >> position & 1:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def rotate(mask, shift):
    return sum(((mask >> t) & 1) << ((t+shift)%3) for t in range(3))


def domains(rows, full, outside_degree):
    demands = [full[u]-1-rows[u].bit_count() for u in range(9)]
    caps = [(2 if rows[u]>>v&1 else full[u]+full[v]-15)
            -(rows[u]&rows[v]).bit_count() for u,v in PAIR_A]
    result = []
    for masks in itertools.product(range(8), repeat=3):
        if masks != min(tuple(rotate(m,s) for m in masks) for s in range(3)):
            continue
        counts = tuple(m.bit_count() for m in masks)
        q = sum(counts)
        if q > outside_degree-5:
            continue
        columns = tuple(sum(((masks[a//3] >> ((b-a)%3)) & 1) << a
                            for a in range(9)) for b in range(3))
        good = True
        for column in columns:
            for a in range(9):
                known = (rows[a] & column).bit_count()
                red = bool(column >> a & 1)
                lower = max(0,demands[a]+outside_degree-q-(12 if red else 11))
                bound = 3 if red else full[a]+outside_degree-14
                if known+lower > bound:
                    good = False
                    break
            if not good:
                break
        if not good:
            continue
        contributions = tuple(sum((column>>u&1) and (column>>v&1) for column in columns)
                              for u,v in PAIR_A)
        if any(c>cap for c,cap in zip(contributions,caps)):
            continue
        result.append(dict(masks=list(masks),counts=counts,pairs=contributions))
    return result,tuple(demands[3*i] for i in range(3)),tuple(caps)


def enumerate_incidences(code, inside, deadline):
    rows = root_rows(code)
    full = [9]*3+[10]*6 if inside else [10]*9
    high,demands,caps = domains(rows,full,10)
    low = high if inside else domains(rows,full,9)[0]
    pools = [low,high,high,high]
    visits = 0
    records = []
    complete = True

    def visit(position, lower_index, counts, pairs, chosen):
        nonlocal visits,complete
        visits += 1
        if visits % 1024 == 0 and time.monotonic()>deadline:
            complete = False
            return
        if position == 4:
            if counts == demands:
                records.append([pools[j][key]['masks'] for j,key in enumerate(chosen)])
            return
        remaining = 3-position
        for key in range(lower_index,len(pools[position])):
            pattern = pools[position][key]
            next_counts = tuple(x+y for x,y in zip(counts,pattern['counts']))
            if any(x>target or x+3*remaining<target for x,target in zip(next_counts,demands)):
                continue
            next_pairs = tuple(x+y for x,y in zip(pairs,pattern['pairs']))
            if any(x>cap for x,cap in zip(next_pairs,caps)):
                continue
            next_lower = key if inside or position>=1 else 0
            visit(position+1,next_lower,next_counts,next_pairs,chosen+[key])
            if not complete:
                return

    visit(0,0,(0,0,0),(0,)*len(PAIR_A),[])
    return dict(code=code,placement='inside' if inside else 'outside',
                status='COMPLETE' if complete else 'INCOMPLETE',
                high_domains=len(high),low_domains=len(low),nodes=visits,
                row_demands=list(demands),incidence_representatives=records,
                representatives=len(records),outside_completion_claim=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--seconds',type=int,default=30)
    args = parser.parse_args()
    started = time.monotonic()
    results = []
    for inside,code in ((True,88),(True,624),(True,1545),(True,1616),(False,624)):
        record = enumerate_incidences(code,inside,time.monotonic()+args.seconds)
        results.append(record)
        args.output.write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps({k:v for k,v in record.items() if k!='incidence_representatives'}),flush=True)
        if record['status'] != 'COMPLETE':
            break
    print('seconds',time.monotonic()-started,'peak RSS KiB',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,flush=True)


if __name__ == '__main__':
    main()
