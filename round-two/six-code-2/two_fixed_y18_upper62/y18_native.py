#!/usr/bin/env python3
"""P/X plus first-fit-color replay of every Y18 maximum family."""
from pathlib import Path
from hashlib import sha256
from itertools import combinations
import argparse
import json
import resource
import subprocess
import time
import interface as Y

M, N = Y.M, Y.N


def compile_native(work, sanitized=False):
    source = Path(__file__).resolve().with_name('y18_pivot.cpp')
    executable = work/'pivot'
    command = ['g++','-std=c++20','-Wall','-Wextra','-Werror','-O1' if sanitized else '-O2']
    if sanitized:
        command += ['-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-fno-pie','-no-pie']
    call = subprocess.run(command+[str(source),'-o',str(executable)],capture_output=True,text=True,timeout=60)
    (work/'compiler.log').write_text(call.stdout+call.stderr)
    M.require(call.returncode == 0, 'new native compiler failed')
    return executable


def controls(executable, work):
    edges = tuple(combinations(range(5),2))
    for code in range(1<<len(edges)):
        adjacency = [0]*5
        for j,(a,b) in enumerate(edges):
            if code>>j&1:
                adjacency[a] |= 1<<b
                adjacency[b] |= 1<<a
        cliques = tuple(q for t in range(1,6) for q in combinations(range(5),t)
                        if all(adjacency[a]>>b&1 for a,b in combinations(q,2)))
        alpha = max(map(len,cliques))
        literal = tuple(q for q in cliques if len(q)==alpha)
        actual,_ = N.pivot(executable,work,'control-small',tuple(adjacency),alpha)
        M.require(actual == literal, 'native differs on a labeled five-vertex graph')
    selected = (0,63,64,127,128,191)
    adjacency = tuple(sum(1<<w for w in selected if w!=v) if v in selected else 0 for v in range(192))
    actual,_ = N.pivot(executable,work,'control-bit-boundaries',adjacency,6)
    M.require(actual == (selected,), 'native bit-boundary control')
    complete5 = tuple(31^(1<<v) for v in range(5))
    N.pivot(executable,work,'control-larger',complete5,4,expected='LARGER_CLIQUE')
    N.pivot(executable,work,'control-incomplete',complete5,5,cap=1,expected='INCOMPLETE')
    bad = work/'control-asymmetric.graph'
    bad.write_text('3\n1 1\n0\n0\n')
    call = subprocess.run([str(executable),str(bad),str(work/'bad.cliques'),'100','1','1'],
                          capture_output=True,text=True,timeout=5)
    M.require(call.returncode == 2 and 'ERROR asymmetric graph' in call.stderr,'asymmetry control')
    return ['all-1024-labeled-five-vertex-graphs','192-vertex-bit-boundaries',
            'larger-clique-rejected','incomplete-guard-rejected','asymmetric-input-rejected']


def run(args):
    args.work.mkdir(parents=True,exist_ok=True)
    executable = compile_native(args.work,args.sanitized)
    started = time.monotonic()
    data = json.loads(args.inventory.read_text())
    anchors = data['anchors']
    anchor_hash = sha256(M.encoded(anchors)).hexdigest()
    M.require(anchor_hash == data['anchors_sha256'], 'inventory hash differs')
    resources, rows = M.orbit_carrier()
    indices = [int(i) for i in args.cases.split(',')] if args.cases else range(len(anchors))
    records = []
    for i in indices:
        anchor = tuple(anchors[i]['words'])
        available, adjacency = Y.finite_graph(anchor,resources,rows)
        saved = json.loads((args.color/f'case-{i:03}.json').read_text())
        graph_hash = sha256(M.encoded(dict(vertices=[r['representative'] for r in available],
                                         adjacency=adjacency))).hexdigest()
        M.require(saved['status']=='COMPLETE' and saved['graph_sha256']==graph_hash and
                  saved['anchor_sha256']==anchor_hash, 'bad color input')
        expected_path = args.color/f'case-{i:03}.maxima.json'
        expected = tuple(tuple(q) for q in json.loads(expected_path.read_text()))
        M.require(sha256(M.encoded(expected)).hexdigest()==saved['maxima_sha256'],'maxima hash differs')
        other,nodes = N.pivot(executable,args.work,f'case-{i:03}',adjacency,saved['alpha'])
        M.require(other==expected,'color and new P/X differ entrywise')
        record = dict(case=i,vertices=len(adjacency),alpha=saved['alpha'],families=len(other),
                      maxima_sha256=saved['maxima_sha256'],nodes=nodes,graph_sha256=graph_hash)
        (args.work/f'case-{i:03}.json').write_bytes(M.encoded(record))
        records.append(record)
        if len(records)%100==0:
            print('native COMPLETE',len(records),'cases',flush=True)
    names = controls(executable,args.work)
    stable = dict(status='COMPLETE entrywise native Y18 replay',cases=len(records),records=records,
                  controls=names,sanitized=args.sanitized)
    (args.work/'summary.json').write_bytes(M.encoded(stable))
    metrics = dict(seconds=time.monotonic()-started,
                   child_peak_RSS_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (args.work/'metrics.json').write_bytes(M.encoded(metrics))
    print(json.dumps({k:v for k,v in stable.items() if k!='records'}|metrics,sort_keys=True),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inventory',type=Path,required=True)
    p.add_argument('--color',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--cases')
    p.add_argument('--sanitized',action='store_true')
    run(p.parse_args())
