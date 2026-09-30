#!/usr/bin/env python3
"""Separate set/degree-neighborhood/closure/Dancing-Links reconstruction.

No import from the generator or earlier mathematical source. This is a
different implementation by the same researcher, not a peer review.
"""
import argparse
import hashlib
import itertools as it
import json
import resource
import subprocess
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
MULT = ((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
PAIRS = list(it.combinations(range(16), 2))
PI = {e: j for j, e in enumerate(PAIRS)}

def require(value, message):
    if not value:
        raise ValueError(message)

def encode(block):
    return sum(1 << p for p in block)

def decode(mask, width=16):
    require(type(mask) is int and 0 <= mask < (1 << width), 'malformed word mask')
    return frozenset(p for p in range(width) if mask & (1 << p))

def edge_encode(edges):
    return sum(1 << PI[e] for e in edges)

def encoded(value):
    return (json.dumps(value, separators=(',', ':'), sort_keys=True) + '\n').encode()

def save(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_bytes(encoded(value))
    temporary.replace(path)

def field_plane():
    plane = frozenset([frozenset(4*x+y for y in range(4)) for x in range(4)] +
                      [frozenset(4*x+(MULT[m][x]^b) for x in range(4))
                       for m in range(4) for b in range(4)])
    require(len(plane) == 20 and all(len(b) == 4 for b in plane) and
            all(sum(a in b and c in b for b in plane) == 1 for a, c in PAIRS),
            'invalid field plane')
    return plane

def plane_group(plane):
    functions = [lambda x,y:(x^1,y), lambda x,y:(x^2,y),
                 lambda x,y:(x,y^1), lambda x,y:(x,y^2),
                 lambda x,y:(MULT[2][x],y), lambda x,y:(x,MULT[2][y]),
                 lambda x,y:(y,x), lambda x,y:(x^y,y),
                 lambda x,y:(MULT[x][x],MULT[y][y])]
    generators = [tuple(4*f(*divmod(p,4))[0]+f(*divmod(p,4))[1] for p in range(16))
                  for f in functions]
    identity = tuple(range(16))
    found, queue = {identity}, [identity]
    for g in queue:
        for h in generators:
            v = tuple(h[g[p]] for p in range(16))
            if v not in found:
                if len(found) >= 6000:
                    raise RuntimeError('INCOMPLETE group closure')
                require(set(v) == set(range(16)) and
                        frozenset(frozenset(v[p] for p in b) for b in plane) == plane,
                        'invalid plane permutation')
                found.add(v)
                queue.append(v)
    require(len(found) == 5760, 'unexpected plane-group closure')
    return sorted(found)

def degree_graphs(degrees, node_cap=200000):
    """Fill the least remaining vertex's entire neighborhood; complete simple graphs."""
    answer, nodes = set(), 0
    def visit(d, edges):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise RuntimeError('INCOMPLETE degree-graph enumeration')
        active = [v for v, r in enumerate(d) if r]
        if not active:
            answer.add(frozenset(edges))
            return
        if sum(d) % 2 or any(d[v] > len(active)-1 for v in active):
            return
        v = active[0]
        for neighbors in it.combinations(active[1:], d[v]):
            remaining = list(d)
            remaining[v] = 0
            for w in neighbors:
                remaining[w] -= 1
            visit(remaining, edges + tuple((v,w) for w in neighbors))
    visit(list(degrees), ())
    return answer

def orbit_cover(domain, group, action, key):
    todo, output = set(domain), []
    for first in sorted(domain, key=key):
        if first not in todo:
            continue
        orbit = {action(first, g) for g in group}
        require(orbit <= todo, 'omitted, overlapping, or invalid symmetry orbit')
        todo -= orbit
        output.append((first, len(orbit)))
    require(not todo and sum(size for _, size in output) == len(domain), 'incomplete orbit cover')
    return output

def components(vertices, edges):
    todo, answer = set(vertices), []
    while todo:
        seed = min(todo)
        seen, queue = {seed}, [seed]
        for v in queue:
            for a, b in edges:
                if v not in (a,b):
                    continue
                w = b if v == a else a
                if w not in seen:
                    seen.add(w)
                    queue.append(w)
        require(seen <= todo, 'invalid component')
        todo -= seen
        answer.append(frozenset(seen))
    return answer

def missing_lines(edges):
    """Independent recognition by components and the unique degree-six hub."""
    support = frozenset(p for e in edges for p in e)
    degrees = {p: sum(p in e for e in edges) for p in support}
    if set(degrees.values()) == {3}:
        parts = components(support, edges)
        blocks = parts if sorted(map(len, parts)) == [4,4] else []
    else:
        hubs = [p for p, d in degrees.items() if d == 6]
        require(len(hubs) == 1 and all(d in (3,6) for d in degrees.values()), 'unexpected leave profile')
        hub = hubs[0]
        others = support - {hub}
        parts = components(others, frozenset(e for e in edges if hub not in e))
        blocks = [part | {hub} for part in parts] if sorted(map(len, parts)) == [3,3] else []
    if not blocks:
        return []
    pairs = [set(it.combinations(sorted(b), 2)) for b in blocks]
    require(len(blocks) == 2 and len(pairs[0]) == len(pairs[1]) == 6 and
            not (pairs[0] & pairs[1]) and (pairs[0] | pairs[1]) == set(edges),
            'invalid two-line completion')
    return sorted(blocks, key=encode)

def prepare():
    plane = field_plane()
    group = plane_group(plane)
    abstract = [degree_graphs([3]*8), degree_graphs([2]*6)]
    require(list(map(len, abstract)) == [19355,70], 'abstract graph domain mismatch')
    collinear = frozenset(frozenset(it.combinations(t,2)) for line in plane
                         for t in it.combinations(sorted(line),3))
    require(len(collinear) == 80, 'collinear triple domain mismatch')
    groups, leaves = [], []
    for profile in range(2):
        if profile == 0:
            domain = {frozenset(s) for s in it.combinations(range(16),8)}
            action = lambda s,g:frozenset(g[p] for p in s)
            key = encode
        else:
            domain = {(frozenset(s),p) for s in it.combinations(range(16),7) for p in s}
            action = lambda v,g:(frozenset(g[p] for p in v[0]),g[v[1]])
            key = lambda v:(encode(v[0]),v[1])
        supports = orbit_cover(domain,group,action,key)
        require(len(supports) == (10 if profile == 0 else 25), 'support domain mismatch')
        for si,(value,support_size) in enumerate(supports):
            support,hub = (value,None) if profile == 0 else value
            order = sorted(support) if hub is None else sorted(support - {hub})
            stabilizer = [g for g in group if frozenset(g[p] for p in support) == support and
                          (hub is None or g[hub] == hub)]
            require(len(stabilizer)*support_size == 5760, 'support stabilizer mismatch')
            candidates = {frozenset(tuple(sorted((order[a],order[b]))) for a,b in graph) |
                          (frozenset() if hub is None else
                           frozenset(tuple(sorted((hub,p))) for p in order))
                          for graph in abstract[profile]}
            local = orbit_cover(candidates,stabilizer,
                                lambda e,g:frozenset(tuple(sorted((g[a],g[b]))) for a,b in e),
                                edge_encode)
            counts = Counter()
            for edges,size in local:
                require(len(edges) == 12, 'leave edge count mismatch')
                if any(t <= edges for t in collinear):
                    kind = 0
                elif missing_lines(edges):
                    kind = 1
                    require(all(all(len(b & line) <= 2 for line in plane)
                                for b in missing_lines(edges)), 'missing line is not a P-arc')
                else:
                    kind = 2
                counts[kind] += 1
                leaves.append([len(leaves),profile,si,edge_encode(edges),size,kind])
            groups.append([profile,si,encode(support),hub,support_size,len(stabilizer),
                           len(candidates),len(local),[counts[k] for k in range(3)]])
    require(sum(r[4]*r[6] for r in groups) == 254704450 and len(leaves) == 45100,
            'leave coverage mismatch')
    allowed = [frozenset(b) for b in it.combinations(range(16),4)
               if all(len(frozenset(b) & line) <= 2 for line in plane)]
    require(len(allowed) == 840, 'four-arc domain mismatch')
    return {'plane':sorted(map(encode,plane)),'groups':groups,'leaves':leaves,
            'allowed':list(map(encode,allowed))}

def matrix(path, allowed, leaves):
    with path.open('w') as out:
        out.write(f'120 {len(allowed)} 6\n')
        for raw in allowed:
            block = decode(raw)
            row = [PI[e] for e in it.combinations(sorted(block),2)]
            require(len(row) == len(set(row)) == 6, 'incorrect quadruple row')
            out.write(' '.join(map(str,[raw]+row))+'\n')
        out.write(str(len(leaves))+'\n')
        for index,row in enumerate(leaves):
            edges = [j for j in range(120) if row[3] & (1 << j)]
            require(len(edges) == 12, 'incorrect forbidden columns')
            out.write(' '.join(map(str,[index,12]+edges))+'\n')

def check_witness(path):
    witness = json.loads(path.read_text())
    require(witness['x'] == 17 and witness['y'] == 16, 'incorrect named coordinates')
    words = [decode(b,18) for b in witness['words']]
    require(len(words) == len(set(words)) == 62 and all(len(b) == 5 for b in words), 'bad fixture cardinality')
    require(all(len(a & b) <= 2 for a,b in it.combinations(words,2)), 'incompatible fixture words')
    require([sum(p in b for b in words) for p in [17,16]] == [20,18] and
            not any({16,17} <= b for b in words), 'incorrect fixture degrees or pair')
    return [sum(p in b for b in words) for p in range(18)]

def run(args):
    started = time.monotonic()
    domain = prepare()
    domain_bytes = encoded(domain)
    primary = json.loads(args.primary.read_text())
    require(primary['status'] == 'COMPLETE finite exclusion', 'generator incomplete')
    domain_hash = hashlib.sha256(domain_bytes).hexdigest()
    require(domain_hash == primary['domain_sha256'], 'independent finite domain differs')
    require(domain_bytes == (args.primary.parent/'domain.json').read_bytes(), 'domain bytes differ')
    degrees = check_witness(HERE/'witness62.json')
    args.work.mkdir(parents=True,exist_ok=True)
    save(args.work/'domain.json',domain)
    leaves = [r for r in domain['leaves'] if r[5] == 2]
    engine = args.engine.resolve()
    fingerprint = {'domain_sha256':domain_hash,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()}
    digest = hashlib.sha256()
    totals = {'cases':0,'covers':0,'nodes':0,'max_leaf_nodes':0}
    for start in range(0,len(leaves),1000):
        selected = leaves[start:start+1000]
        prefix = args.work/f'batch_{start:05d}'
        inp,out,meta = [prefix.with_suffix(s) for s in ['.in','.jsonl','.meta.json']]
        if meta.exists():
            record = json.loads(meta.read_text())
            require(record['status'] == 'COMPLETE' and record['fingerprint'] == fingerprint and
                    record['start'] == start and record['count'] == len(selected),'invalid resumed check')
            require(record['output_sha256'] == hashlib.sha256(out.read_bytes()).hexdigest(),'output changed')
            result_summary = record['summary']
        else:
            matrix(inp,domain['allowed'],selected)
            run_started = time.monotonic()
            result = subprocess.run([str(engine),str(inp),str(out)],capture_output=True,text=True)
            record = {'start':start,'count':len(selected),'fingerprint':fingerprint,
                      'exit_code':result.returncode,'seconds':time.monotonic()-run_started,
                      'stderr':result.stderr,'stdout':result.stdout}
            if result.returncode:
                record['status'] = 'INCOMPLETE; no exclusion from this unfinished batch'
                save(prefix.with_suffix('.failure.json'),record)
                raise RuntimeError('INCOMPLETE independent cover replay')
            result_summary = json.loads(result.stdout)
            require(result_summary['status'] == 'COMPLETE' and result_summary['cases'] == len(selected),
                    'incomplete native output')
            record.update(status='COMPLETE',summary=result_summary,
                          output_sha256=hashlib.sha256(out.read_bytes()).hexdigest())
            save(meta,record)
        results = [json.loads(s) for s in out.read_text().splitlines()]
        require(len(results) == len(selected) and
                [r['index'] for r in results] == list(range(len(selected))), 'missing native case')
        require(sum(r['nodes'] for r in results) == result_summary['nodes'] and
                sum(len(r['covers']) for r in results) == result_summary['covers'], 'incorrect native totals')
        for row,result in zip(selected,results):
            require(result['covers'] == [], 'counterexample to exclusion')
            digest.update(encoded({'index':row[0],'covers':result['covers']}))
        for k in ['cases','covers','nodes']:
            totals[k] += result_summary[k]
        totals['max_leaf_nodes'] = max(totals['max_leaf_nodes'],max(r['nodes'] for r in results))
        progress = {'status':'INCOMPLETE until every batch finishes','totals':totals,
                    'seconds':time.monotonic()-started}
        save(args.work/'progress.json',progress)
        print(json.dumps(progress),flush=True)
    require(totals['cases'] == primary['totals']['cases'] == 34398 and totals['covers'] == 0 and
            digest.hexdigest() == primary['exclusion_sha256'],'independent exclusions differ')
    counts = [[sum(r[1] == p and r[5] == k for r in domain['leaves']) for k in range(3)] for p in range(2)]
    require(counts == primary['profile_counts'],'classification counts differ')
    expected = json.loads(args.expected.read_text())
    require(expected['domain_sha256'] == domain_hash and
            expected['exclusion_sha256'] == digest.hexdigest() and
            expected['profile_counts'] == counts and expected['exclusion_cases'] == totals['cases'] and
            expected['exclusion_covers'] == totals['covers'] and
            expected['restricted_maximum'] == 62 and expected['witness_degrees'] == degrees,
            'complete check differs from compact expected record')
    summary = {'agent':'six-code-3','role':'researcher','status':'COMPLETE separate-algorithm check',
               'peer_review':False,'formal_proof':False,'domain_sha256':domain_hash,
               'exclusion_sha256':digest.hexdigest(),'labelled_leaves':254704450,
               'leaf_orbits':45100,'profile_counts':counts,'totals':totals,
               'restricted_maximum':62,'witness_degrees':degrees,
               'seconds':time.monotonic()-started,
               'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'max_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    save(args.work/'summary.json',summary)
    print(json.dumps(summary),flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--primary',type=Path,required=True)
    parser.add_argument('--engine',type=Path,required=True)
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--expected',type=Path,default=HERE/'expected.json')
    run(parser.parse_args())
