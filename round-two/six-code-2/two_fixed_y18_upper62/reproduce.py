#!/usr/bin/env python3
"""Exact dual-star and dual-search reproduction of the sharp Y18 bound.

Actual author six-code-2, researcher. Every child is sequential. A failed
guard or incomplete child aborts without a mathematical upper-bound claim.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import argparse
import json
import os
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def source_check(repository):
    manifest = json.loads((HERE/'DEPENDENCIES.json').read_text())
    for record in manifest['source_files']:
        path = repository/record['path']
        raw = path.read_bytes()
        require(len(raw)==record['bytes'] and sha256(raw).hexdigest()==record['sha256'],
                'pinned dependency differs: '+record['path'])
    return manifest


def witness_controls():
    import interface as I
    witness = json.loads((HERE/'witness.json').read_text())
    actual = I.M.check_code(tuple(witness['words']))
    expected = {k:tuple(v) if k=='replications' else v for k,v in witness['code_statistics'].items()}
    require(actual==expected and actual['words']==62 and actual['replications'][16:]==(20,18) and
            actual['fixed_words']==6 and tuple(witness['involution'])==I.M.G and
            sum((w>>16&1)*(w>>17&1) for w in witness['words'])==4,'invalid sharp62 witness')
    names = ['literal-62-word-positive']
    bad = list(witness['words'])
    bad[-1] = bad[0]
    removed = next(w for w in witness['words'] if I.M.image(w)!=w)
    for name,words in [('duplicate-word',bad),('wrong-weight',(1,)),
                       ('nonclosed-orbit',tuple(w for w in witness['words'] if w!=removed))]:
        try:
            I.M.check_code(words)
        except ValueError:
            names.append(name)
        else:
            raise ValueError('corruption control accepted: '+name)
    return names


def assemble(work):
    literal = json.loads((work/'literal.json').read_text())
    primary = json.loads((work/'primary.json').read_text())
    color = json.loads((work/'color/summary.json').read_text())
    native = json.loads((work/'native/summary.json').read_text())
    require(literal['status']=='COMPLETE requested literal Y18 census' and literal['all_Y18_counts'] and
            primary['status']=='COMPLETE fixed-first Y18 census' and primary['paired_first_entrywise'] and
            color['status']=='COMPLETE requested maxima' and color['cases']==3498 and
            native['status']=='COMPLETE entrywise native Y18 replay' and native['cases']==3498,
            'incomplete proof stage')
    require(color['anchor_sha256']==literal['anchors_sha256'],'proof-stage inventory mismatch')
    native_cases = {r['case']:r for r in native['records']}
    descriptors, groups = [], {}
    for r in color['records']:
        n = native_cases[r['case']]
        require((n['vertices'],n['alpha'],n['families'],n['graph_sha256'],n['maxima_sha256']) ==
                (r['vertices'],r['alpha'],r['maximum_families'],r['graph_sha256'],r['maxima_sha256']),
                'two searches differ')
        descriptor = dict(case=r['case'],fixture=r['fixture'],fixed_Y=r['fixed_Y'],vertices=r['vertices'],
                          alpha=r['alpha'],families=r['maximum_families'],graph_sha256=r['graph_sha256'],
                          maxima_sha256=r['maxima_sha256'])
        descriptors.append(descriptor)
        groups.setdefault((r['fixture'],r['fixed_Y']),[]).append(r)
    group_summaries = []
    for (fixture,fixed),records in sorted(groups.items()):
        group_summaries.append(dict(fixture=fixture,fixed_Y=fixed,anchors=len(records),
                                   word_counts=dict(Counter(r['words'] for r in records)),
                                   min_vertices=min(r['vertices'] for r in records),
                                   max_vertices=max(r['vertices'] for r in records)))
    names = witness_controls()
    require(max(r['words'] for r in color['records'])==62,'unexpected upper bound')
    literal_records = [{k:v for k,v in r.items() if k!='seconds'} for r in literal['records']]
    stable = dict(agent='six-code-2',role='researcher',status='COMPLETE',upper_bound=62,sharp=True,
                  statement='cycle2^8*1^2, fixed X20/Y18, pair multiplicity4: sharp maximum62',
                  literal_stars=literal_records,primary_stars=primary['records'],
                  literal_anchor_sha256=literal['anchors_sha256'],
                  canonical_anchor_sha256=primary['canonical_sha256'],anchors=3498,
                  all_Y18_fixed_counts=[0,2,4],fixedY4=392,fixedY2=3106,fixedY0=0,
                  groups=group_summaries,word_counts=dict(Counter(r['words'] for r in color['records'])),
                  completion_records_sha256=sha256(encoded(descriptors)).hexdigest(),
                  maximum_families=sum(r['maximum_families'] for r in color['records']),
                  color_nodes=sum(r['nodes'] for r in color['records']),
                  native_nodes=sum(r['nodes'] for r in native['records']),
                  witness_sha256=sha256((HERE/'witness.json').read_bytes()).hexdigest(),
                  controls=names+native['controls'])
    return stable


def run(args):
    started = time.monotonic()
    repository = args.repository.resolve()
    source_check(repository)
    work = args.work.resolve()
    require(not work.exists() and work!=HERE and HERE not in work.parents,'use a new work directory outside source')
    work.mkdir(parents=True)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
                 'BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        os.environ[name] = '1'
    if args.sanitizers:
        os.environ['ASAN_OPTIONS']='detect_leaks=1:halt_on_error=1'
        os.environ['UBSAN_OPTIONS']='halt_on_error=1:print_stacktrace=1'

    def call(script,argv,label,timeout):
        command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(script)]+list(map(str,argv))
        result=subprocess.run(command,capture_output=True,text=True,timeout=timeout)
        (work/(label+'.log')).write_text(result.stdout+result.stderr)
        require(result.returncode==0,'incomplete/failed proof stage: '+label)
        print(label,'COMPLETE',flush=True)

    if not args.skip_dependency_replay:
        prior=repository/'round-two/six-code-2/two_fixed_saturated_upper60/reproduce.py'
        argv=['--repository',repository,'--work',work/'prior']
        if args.sanitizers:
            argv += ['--sanitizers']
        call(prior,argv,'full-pinned-prior',300)
    call(HERE/'y18_inventory.py',['--output',work/'fixed-four.json'],'fixed-four',60)
    call(HERE/'y18_literal.py',['--primary',work/'fixed-four.json','--output',work/'literal.json',
                              '--fixed','all'],'paired-first',60)
    call(HERE/'y18_primary.py',['--literal',work/'literal.json','--output',work/'primary.json'],
         'fixed-first',60)
    call(HERE/'y18_color.py',['--inventory',work/'literal.json','--work',work/'color'],'color',900)
    argv=['--inventory',work/'literal.json','--color',work/'color','--work',work/'native']
    if args.sanitizers:
        argv += ['--sanitized']
    call(HERE/'y18_native.py',argv,'native',900)
    stable=assemble(work)
    raw=encoded(stable)
    (work/'result.json').write_bytes(raw)
    if args.record_expected:
        (HERE/'expected.json').write_bytes(raw)
    else:
        require(raw==(HERE/'expected.json').read_bytes(),'complete stable record differs')
    metrics=dict(status='COMPLETE',seconds=time.monotonic()-started,
                 own_peak_RSS_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 child_peak_RSS_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                 optimized_python=bool(sys.flags.optimize),sanitizers=args.sanitizers,
                 full_pinned_prior_replayed=not args.skip_dependency_replay)
    (work/'metrics.json').write_bytes(encoded(metrics))
    print(json.dumps(metrics,sort_keys=True),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repository',type=Path,default=HERE.parents[2])
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--sanitizers',action='store_true')
    p.add_argument('--skip-dependency-replay',action='store_true')
    p.add_argument('--record-expected',action='store_true')
    run(p.parse_args())
