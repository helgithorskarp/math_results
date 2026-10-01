"""Literal coverage, exact-cover, actual-group and pivot checks.

No primary model module is imported. Both implementations are by six-code-2.
"""
from itertools import combinations, permutations, product
from pathlib import Path
import json
import subprocess
import time

TAILS = [frozenset(t) for t in [(2,4,6),(3,5,7),(8,10,12),(9,11,13)]]
S = frozenset(range(14,18))
W = frozenset(range(2,14))
FIXED = [frozenset([0,1]) | t for t in TAILS]
ROOTS = [(2,14,15,16),(2,5,14,15),(2,8,14,15)]

def flip(b):
    return frozenset(v^1 for v in b)

def points(mask):
    return frozenset(v for v in range(18) if mask >> v & 1)

def triple_orbits(b):
    return frozenset(min(tuple(t),tuple(sorted(v^1 for v in t)))
                     for t in combinations(sorted(b),3))

def local_model():
    fixed_triples = frozenset(t for b in FIXED for t in triple_orbits(b))
    rows, triples = [],[]
    for q in combinations(range(2,18),4):
        ts = triple_orbits(frozenset(q) | {0})
        if len(ts)==10 and not ts & fixed_triples:
            rows.append(frozenset(q))
            triples.append(ts)
    graph = [frozenset(j for j,ts in enumerate(triples) if j!=i and not ts & own)
             for i,own in enumerate(triples)]
    mandatory = frozenset(frozenset(p) for p in combinations(range(2,18),2)
                          if (frozenset(p)<=S or
                              (frozenset(p)<=W and not any(frozenset(p)<=t for t in TAILS))))
    if len(rows)!=864 or len(mandatory)!=60:
        raise ValueError('literal candidate/column coverage')
    return rows,graph,mandatory

def exact_covers(rows, graph, mandatory, root):
    columns = [frozenset(frozenset(p) for p in combinations(sorted(q),2)) & mandatory for q in rows]
    column_rows = {p:frozenset(i for i,c in enumerate(columns) if p in c) for p in mandatory}
    i = rows.index(frozenset(root))
    results = []
    nodes = 0
    started = time.monotonic()
    def search(pool, missing, quota, chosen):
        nonlocal nodes
        nodes += 1
        if nodes>1000000 or time.monotonic()-started>30:
            raise TimeoutError('INCOMPLETE')
        if not missing:
            if len(chosen)==16 and not any(quota.values()):
                results.append(tuple(sorted(tuple(sorted(rows[j])) for j in chosen)))
            return
        if len(chosen)>=16:
            return
        pool = frozenset(j for j in pool if all(quota[v]>0 for v in rows[j]))
        if any(sum(v in rows[j] for j in pool)<q for v,q in quota.items()):
            return
        p = min(missing,key=lambda p:(len(pool & column_rows[p]),tuple(sorted(p))))
        for j in sorted(pool & column_rows[p]):
            if not columns[j]<=missing:
                raise ValueError('repeated mandatory pair')
            next_quota = {v:q-int(v in rows[j]) for v,q in quota.items()}
            search(pool & graph[j], missing-columns[j],next_quota,chosen+[j])
    search(graph[i],mandatory-columns[i],{v:4-int(v in rows[i]) for v in range(2,18)},[i])
    if len(set(results))!=len(results):
        raise ValueError('duplicate literal covers')
    return sorted(results),nodes

def direct_group():
    result = set()
    for swap,p0,p1,f0,f1,swap_s,fs0,fs1 in product(
            range(2),permutations(range(3)),permutations(range(3)),
            range(2),range(2),range(2),range(2),range(2)):
        p = list(range(18))
        for source,perm,orientation in [(0,p0,f0),(1,p1,f1)]:
            destination = source ^ swap
            for i in range(3):
                for bit in range(2):
                    p[2*(1+3*source+i)+bit] = 2*(1+3*destination+perm[i])+(bit^orientation)
        for i,orientation in [(0,fs0),(1,fs1)]:
            for bit in range(2):
                p[2*(7+i)+bit] = 2*(7+(i^swap_s))+(bit^orientation)
        if sorted(p)!=list(range(18)) or any(p[v^1]!=(p[v]^1) for v in range(18)):
            raise ValueError('invalid direct group map')
        if {frozenset(p[v] for v in b) for b in FIXED}!=set(FIXED):
            raise ValueError('wrong anchor transport')
        result.add(tuple(p))
    return sorted(result)

def witness_check(raw):
    if any(len(b)!=5 or sorted(set(b))!=sorted(b) or any(type(v)!=int or v<0 or v>=18 for v in b) for b in raw):
        raise ValueError('malformed witness')
    F = {frozenset(b) for b in raw}
    if len(F)!=len(raw) or len(F)!=60 or {flip(b) for b in F}!=F:
        raise ValueError('witness size/uniqueness/involution')
    if any(len(a&b)>2 for a,b in combinations(F,2)):
        raise ValueError('witness intersection')
    Q = [b-{0} for b in F if 0 in b]
    if len(Q)!=20:
        raise ValueError('witness saturation')
    rho = {v:sum(v in b for b in Q) for v in range(1,18)}
    H = frozenset(v for v,r in rho.items() if r==4)
    if H!=frozenset([1,14,15,16,17]) or any(r not in [4,5] for r in rho.values()):
        raise ValueError('witness unit profile')
    leave = {frozenset(p) for p in combinations(range(1,18),2)}-{frozenset(p) for b in Q for p in combinations(sorted(b),2)}
    if {p for p in leave if p<=H}!={frozenset([1,v]) for v in S}:
        raise ValueError('witness high leave')
    return True

def verify(work, source, sanitizer=False):
    analysis = json.loads((work/'analysis.json').read_text())
    native_rows = [points(b) for b in analysis['rows']]
    rows,graph,mandatory = local_model()
    literal = {tuple(sorted(rows[i])):frozenset(tuple(sorted(rows[j])) for j in c) for i,c in enumerate(graph)}
    native = {tuple(sorted(native_rows[i])):frozenset(tuple(sorted(native_rows[j])) for j in c)
              for i,c in enumerate(analysis['local_adjacency'])}
    if literal!=native:
        raise ValueError('entrywise local graph mismatch')
    local_summary = []
    for k,root in enumerate(ROOTS):
        actual,nodes = exact_covers(rows,graph,mandatory,root)
        expected = sorted(tuple(sorted(tuple(sorted(native_rows[v])) for v in sol)) for sol in analysis['cases'][k])
        if actual!=expected:
            raise ValueError('entrywise local covers mismatch')
        local_summary.append({'root':list(root),'covers':len(actual),'nodes':nodes})
    group = direct_group()
    if group != [tuple(p) for p in analysis['group_elements']]:
        raise ValueError('entrywise actual point-group mismatch')
    index = {q:i for i,q in enumerate(native_rows)}
    all_covers = {tuple(sol) for case in analysis['cases'] for sol in case}
    remaining = set(all_covers)
    classes = []
    while remaining:
        seed = min(remaining)
        orbit = {tuple(sorted(index[frozenset(p[v] for v in native_rows[i])] for i in seed)) for p in group}
        remaining -= orbit
        classes.append({'representative':list(min(orbit)),'orbit_size':len(orbit),
                        'root_hits':[sum(tuple(s) in orbit for s in ss) for ss in analysis['cases']]})
    classes.sort(key=lambda c:c['representative'])
    if classes!=analysis['classes']:
        raise ValueError('entrywise class mismatch')
    pivot = work/('pivot-sanitize' if sanitizer else 'pivot-reference')
    flags = ['-std=c++20','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer'] if sanitizer else ['-std=c++20','-O3']
    subprocess.run(['g++',*flags,'-Wall','-Wextra','-Wconversion','-pedantic',str(source/'pivot.cpp'),'-o',str(pivot)],check=True)
    residual_summary = []
    for k,report in enumerate(analysis['residual']):
        anchor = [points(b) for b in report['anchor']]
        covered = frozenset(t for b in anchor for t in triple_orbits(b))
        candidates,triples = [],[]
        for t in combinations(range(18),5):
            b = frozenset(t)
            if tuple(sorted(b))>=tuple(sorted(flip(b))):
                continue
            own = triple_orbits(b)
            if len(own)==10 and not own & covered:
                candidates.append(b)
                triples.append(own)
        if candidates != [points(b) for b in report['rows']]:
            raise ValueError('all-18-point candidate mismatch')
        adjacency = [frozenset(j for j,ts in enumerate(triples) if i!=j and not ts & own)
                     for i,own in enumerate(triples)]
        if [sorted(c) for c in adjacency]!=report['adjacency']:
            raise ValueError('entrywise residual graph mismatch')
        graph_file = work/f'literal-residual-{k}.txt'
        with graph_file.open('w') as f:
            f.write(str(len(adjacency))+'\n')
            for c in adjacency:
                f.write(' '.join(map(str,[len(c)]+sorted(c)))+'\n')
        output = work/f'pivot-maxima-{k}.txt'
        run = subprocess.run([str(pivot),str(graph_file),str(output),'50000000','30'],check=True,capture_output=True,text=True)
        if not run.stdout.startswith('COMPLETE '):
            raise ValueError('pivot not complete')
        actual = sorted(tuple(map(int,line.split())) for line in output.read_text().splitlines())
        expected = [tuple(sol) for sol in report['maxima']]
        if actual!=expected or not actual or any(len(sol)!=12 for sol in actual):
            raise ValueError('entrywise pivot maxima mismatch')
        witness_check(report['witness'])
        residual_summary.append({'case':k,'vertices':len(candidates),'max_cliques':len(actual),'pivot':run.stdout.strip()})
    return {'status':'COMPLETE','local':local_summary,'group_elements':len(group),
            'classes':len(classes),'residual':residual_summary,'all_entrywise':True}
