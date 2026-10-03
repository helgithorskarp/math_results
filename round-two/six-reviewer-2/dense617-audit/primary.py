"""Fresh core and weighted-row enumerations; never reads author certificates."""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from model import bits, canon, complete_model_record, digest, graph, increasing, require

def domains():
    S, T, rows, columns, supports = graph()
    levels, _ = increasing(rows)
    cores = []
    for a, C in levels[5]:
        for size in range(6, C.bit_count()+1):
            for b in itertools.combinations(bits(C), size):
                mask = sum(1 << j for j in b)
                costs = sorted(((mask & ~row).bit_count(), q)
                               for q, row in enumerate(rows) if q not in a)
                cores.append((a, C, b, costs))
    cores.sort(key=lambda x: (x[0], x[2]))
    return S, T, rows, columns, cores

def core_record():
    S, T, rows, columns, cores = domains()
    result = {}
    for name, a, b, cap in (("original10x12",10,12,10),
                            ("original11x11",11,11,11),
                            ("global10x12",10,12,12)):
        minimum_common = b-(5*cap//a)
        cases = [c for c in cores if len(c[2]) >= minimum_common]
        hist = Counter(b-len(c[2])+sum(w for w, q in c[3][:a-5]) for c in cases)
        survivors = [c for c in cases if b-len(c[2])+sum(w for w,q in c[3][:a-5]) <= cap]
        result[name] = dict(side_sizes=[a,b], cap=cap, minimum_common=minimum_common,
            count=len(cases), lower_histogram=sorted(hist.items()),
            survivors=len(survivors),
            domain_sha256=digest([(c[0],c[1],c[2]) for c in cases]),
            survivors_sha256=digest([(c[0],c[1],c[2]) for c in survivors]),
            surviving_common_sizes=sorted(set(len(c[2]) for c in survivors)))
    return result

def selections(weighted, choose, budget):
    """Increasing cost/index recursion, including all 303 available rows.

    The exact lower bound is the sum of the next `need` sorted weights.
    No assumed list of 0/1/2 cost patterns is used.
    """
    prefix = [0]
    for w, q in weighted:
        prefix.append(prefix[-1]+w)
    def walk(start, need, left, picked):
        if not need:
            yield tuple(sorted(picked))
            return
        for i in range(start, len(weighted)-need+1):
            if prefix[i+need]-prefix[i] > left:
                break
            w, q = weighted[i]
            yield from walk(i+1, need-1, left-w, picked+(q,))
    yield from walk(0, choose, budget, ())

def extension(which, start, stop, output):
    S, T, rows, columns, cores = domains()
    a, b, cap = (11,11,11) if which == "balanced" else (10,12,12)
    domain = [c for c in cores if len(c[2]) >= b-(5*cap//a)
              and b-len(c[2])+sum(w for w,q in c[3][:a-5]) <= cap]
    require(0 <= start <= stop <= len(domain), "range")
    h = hashlib.sha256()
    hist = Counter()
    per_core = []
    with output.open("w") as f:
        for number in range(start, stop):
            A0, C, B0, costs = domain[number]
            costmap = dict((q,w) for w,q in costs)
            ext = sorted(selections(costs, a-5, cap-(b-len(B0))))
            require(len(ext) == len(set(ext)), "duplicated rows")
            local = Counter()
            for added in ext:
                A = tuple(sorted(A0+added))
                require(len(A) == a and len(set(A)) == a, "row selection")
                mask = sum(1 << q for q in A)
                g = sum(costmap[q] for q in added)
                outside = sorted((a-(mask & col).bit_count(), j)
                                 for j, col in enumerate(columns) if not C >> j & 1)
                best = tuple(outside[:b-len(B0)])
                missing = g+sum(w for w,j in best)
                record = [list(A0), list(B0), list(added), g,
                          [[w,j] for w,j in best], missing]
                line = canon(record)
                f.write(line)
                h.update(line.encode())
                hist[missing] += 1
                local[missing] += 1
            per_core.append([number,len(ext),sorted(local.items())])
    return dict(which=which, total_domain=len(domain), range=[start,stop],
                count=sum(hist.values()), histogram=sorted(hist.items()),
                minimum=min(hist) if hist else None, stream_sha256=h.hexdigest(),
                per_core_sha256=digest(per_core))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("model","cores","extension"))
    ap.add_argument("--which", choices=("balanced","stronger"), default="balanced")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--stop", type=int)
    ap.add_argument("--stream", type=Path)
    args = ap.parse_args()
    if args.mode == "model":
        x = complete_model_record()
    elif args.mode == "cores":
        x = core_record()
    else:
        require(args.stop is not None and args.stream is not None, "explicit batch/output")
        require(not args.stream.exists(), "fresh stream required")
        x = extension(args.which,args.start,args.stop,args.stream)
    print(canon(x),end="")

if __name__ == "__main__":
    main()
