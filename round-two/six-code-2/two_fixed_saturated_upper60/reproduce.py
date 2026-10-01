#!/usr/bin/env python3
"""Cold dual enumeration and complete residual maximum-family validation.

Actual author six-code-2, researcher. Same-author algorithmic agreement is
not an independent peer review. Guards never constitute nonexistence evidence.
"""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import argparse
import json
import os
import resource
import subprocess
import sys
import time
import model as M

HERE = Path(__file__).resolve().parent
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')


def check_prior_sources(repository):
    manifest = json.loads((HERE / 'DEPENDENCIES.json').read_text())
    for record in manifest['prior_source_files']:
        path = repository / record['path']
        raw = path.read_bytes()
        M.require(len(raw) == record['bytes'] and sha256(raw).hexdigest() == record['sha256'],
                  'pinned twenty-star dependency differs: ' + record['path'])
    return manifest


def controls(work, executable, stars, witness):
    import seeds
    import second_stars as S
    import native_replay as N
    names = []

    def reject(name, function, exception=ValueError):
        try:
            function()
        except exception:
            names.append(name)
        else:
            raise ValueError('negative control accepted: ' + name)

    stats = M.check_code(tuple(witness['words']))
    M.require(tuple(witness['involution']) == M.G and
              stats == {k:tuple(v) if k == 'replications' else v for k,v in witness['code_statistics'].items()} and
              stats['words'] == 60 and stats['replications'][16:] == (20,20) and
              stats['fixed_words'] == 8 and sum((w >> 16 & 1) and (w >> 17 & 1)
              for w in witness['words']) == 4, 'literal sharp witness')
    names.append('literal-sixty-word-positive')
    duplicate = list(witness['words'])
    duplicate[-1] = duplicate[0]
    reject('duplicate-word', lambda:M.check_code(duplicate))
    reject('wrong-weight', lambda:M.check_code((1,)))
    removed = next(w for w in witness['words'] if M.image(w) != w)
    reject('nonclosed-word-orbit', lambda:M.check_code(tuple(w for w in witness['words'] if w != removed)))
    root = stars['roots'][0]
    mapping = list(root['mapping'])
    mapping[0] = mapping[1]
    reject('broken-normalizing-involution', lambda:seeds.normalize(root['mate'], mapping, root['raw_anchor']))
    reject('primary-Y-guard', lambda:S.cliques((6,5,3),2,cap=0), S.Incomplete)
    # Direct subset comparison on all64 labelled graphs on four vertices.
    edges = tuple(combinations(range(4),2))
    for code in range(1 << len(edges)):
        adjacency = tuple(sum(1 << b for j,(a,b) in enumerate(edges) if code >> j & 1 and a == v) |
                          sum(1 << a for j,(a,b) in enumerate(edges) if code >> j & 1 and b == v)
                          for v in range(4))
        for target in range(5):
            literal = tuple(q for q in combinations(range(4), target)
                            if all(adjacency[a] >> b & 1 for a,b in combinations(q,2)))
            actual,_ = S.cliques(adjacency,target)
            M.require(actual == literal, 'small exact six-first enumerator control')
    names.append('all-four-vertex-graphs-all-cardinalities')
    complete4 = tuple(15 ^ (1 << v) for v in range(4))
    maxima,_ = N.pivot(executable,work,'control-K4',complete4,4)
    M.require(maxima == ((0,1,2,3),), 'native positive')
    names.append('native-K4-positive')
    N.pivot(executable,work,'control-larger',tuple(31 ^ (1 << v) for v in range(5)),4,
            expected='LARGER_CLIQUE')
    names.append('native-larger-clique-rejected')
    N.pivot(executable,work,'control-incomplete',complete4,4,cap=1,expected='INCOMPLETE')
    names.append('native-incomplete-rejected')
    bad = work/'control-asymmetric.graph'
    bad.write_text('3\n1 1\n0\n0\n')
    result = subprocess.run([str(executable),str(bad),str(work/'bad.maxima'),'100','1','1'],
                            capture_output=True,text=True,timeout=5)
    M.require(result.returncode == 2 and 'ERROR asymmetric graph' in result.stderr, 'asymmetry control')
    names.append('native-asymmetry-rejected')
    return names


def run(args):
    repository = args.repository.resolve()
    manifest = check_prior_sources(repository)
    work = args.work.resolve()
    M.require(not work.exists() and work != HERE and HERE not in work.parents, 'work must be new outside source')
    work.mkdir(parents=True)
    for name in THREADS:
        os.environ[name] = '1'
    if args.sanitizers:
        os.environ['ASAN_OPTIONS'] = 'detect_leaks=1:halt_on_error=1'
        os.environ['UBSAN_OPTIONS'] = 'halt_on_error=1:print_stacktrace=1'
    started = time.monotonic()
    if not args.skip_dependency_replay:
        prior = repository/'round-two/six-code-2/free_involution_upper68/reproduce.py'
        command = [sys.executable] + (['-O'] if sys.flags.optimize else []) + [str(prior),'--repository',str(repository),
                   '--work',str(work/'twenty-star-dependency')]
        if args.sanitizers:
            command.append('--sanitizers')
        replay = subprocess.run(command,capture_output=True,text=True,timeout=300)
        work.joinpath('twenty-star-dependency.log').write_text(replay.stdout+replay.stderr)
        M.require(replay.returncode == 0, 'twenty-star dependency replay incomplete or failed')
        print('full pinned twenty-star dependency COMPLETE',flush=True)
    import seeds
    import second_stars as S
    import literal as L
    import completions as C
    import native_replay as N
    resources, rows = M.orbit_carrier()
    M.verify_literal_model(resources,rows)
    S.run(work/'second-stars.json')
    stars = json.loads((work/'second-stars.json').read_text())
    carrier_table = L.verify_root_carriers()
    M.require([r['valid'] for r in carrier_table] == [r['valid'] for r in stars['root_table']],
              'root carrier count mismatch')
    literal_records = []
    for root in stars['roots']:
        anchors, record = L.y_anchors(tuple(root['anchor']))
        expected = tuple(sorted(tuple(r['words']) for r in stars['anchors'] if r['fixture'] == root['fixture']))
        M.require(anchors == expected, 'fixed-first and paired-first second stars differ entrywise')
        record.pop('seconds')
        record['fixture'] = root['fixture']
        literal_records.append(record)
    print('all39 second stars agree entrywise; literal paired-first COMPLETE',flush=True)
    executable = N.compile_pivot(work,args.sanitizers)
    records = []
    for i, anchor in enumerate(stars['anchors']):
        leftovers, adjacency = C.residual_graph(tuple(anchor['words']),resources,rows)
        alpha, maxima, color_nodes = C.color.maximum_cliques(adjacency)
        other, pivot_nodes = N.pivot(executable,work,f'case-{i:02}',adjacency,alpha)
        M.require(maxima == other and len(maxima) > 0, 'color and P/X maximum families differ entrywise')
        words = tuple(sorted(tuple(anchor['words']) + tuple(w for j in maxima[0] for w in leftovers[j]['words'])))
        stats = M.check_code(words)
        M.require(stats['replications'][16:] == (20,20) and len(words) == 36 + 2*alpha, 'case witness')
        graph_hash = sha256(M.encoded(dict(vertices=[r['representative'] for r in leftovers],adjacency=adjacency))).hexdigest()
        record = dict(case=i,fixture=anchor['fixture'],matching=anchor['matching'],vertices=len(adjacency),alpha=alpha,
                      families=len(maxima),color_nodes=color_nodes,pivot_nodes=pivot_nodes,words=len(words),
                      graph_sha256=graph_hash,maxima_sha256=sha256(M.encoded(maxima)).hexdigest())
        records.append(record)
        print('case',i,'COMPLETE',len(adjacency),'vertices',len(words),'words',len(maxima),'maximum families',flush=True)
    witness = json.loads((HERE/'witness.json').read_text())
    names = controls(work,executable,stars,witness)
    stable = dict(agent='six-code-2',role='researcher',status='COMPLETE',
                  statement='two fixed points, both replication20: sharp upper60; pair multiplicity4 case sharp60',
                  root_table=stars['root_table'],roots=stars['roots'],matching_census=stars['records'],
                  anchors_sha256=sha256(M.encoded(stars['anchors'])).hexdigest(),literal_second_stars=literal_records,
                  completions=records,controls=names,witness_sha256=sha256(M.encoded(witness)).hexdigest(),
                  upper_bound=60,own_twenty_star_dependency=manifest['twenty_star_cover']['graph_ref'],
                  reviewed_inputs=[r['graph_ref'] for r in manifest['reviewed_inputs']])
    raw = M.encoded(stable)
    work.joinpath('result.json').write_bytes(raw)
    if args.record_expected:
        HERE.joinpath('expected.json').write_bytes(raw)
    else:
        M.require(raw == HERE.joinpath('expected.json').read_bytes(), 'stable record differs')
    metrics = dict(status='COMPLETE',seconds=time.monotonic()-started,
                   own_peak_RSS_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   child_peak_RSS_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   optimized_python=bool(sys.flags.optimize),sanitizers=args.sanitizers,
                   full_twenty_star_dependency_replayed=not args.skip_dependency_replay)
    work.joinpath('metrics.json').write_bytes(M.encoded(metrics))
    print(json.dumps(metrics,sort_keys=True),flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repository',type=Path,default=HERE.parents[2])
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--sanitizers',action='store_true')
    p.add_argument('--skip-dependency-replay',action='store_true')
    p.add_argument('--record-expected',action='store_true')
    run(p.parse_args())
