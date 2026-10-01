"""Complete source-only reproduction; guards and disagreement abort the claim."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time

import model
import reference

SOURCE = Path(__file__).resolve().parent

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def run(args, complete=True):
    p = subprocess.run([str(a) for a in args],capture_output=True,text=True)
    if complete and (p.returncode!=0 or not p.stdout.startswith('COMPLETE ')):
        raise RuntimeError('INCOMPLETE or failed native phase: '+p.stdout+p.stderr)
    return p

def controls(work, enumerator, pivot, witnesses):
    count = 0
    p = run([enumerator,work/'local.txt',0,1,30,work/'guard-cover.txt'],False)
    if p.returncode==0 or not p.stdout.startswith('INCOMPLETE '):
        raise ValueError('local guard supplied an exclusion')
    count += 1
    p = run([pivot,work/'literal-residual-1.txt',work/'guard-clique.txt',1,30],False)
    if p.returncode==0 or not p.stdout.startswith('INCOMPLETE '):
        raise ValueError('pivot guard supplied an exclusion')
    count += 1
    for content,args in [('864\n',[enumerator,work/'bad.txt',0,1000000,30,work/'bad-cover.txt']),
                         ('2\n1 1\n0\n',[pivot,work/'bad.txt',work/'bad-clique.txt',1000000,30])]:
        (work/'bad.txt').write_text(content)
        p = run(args,False)
        if p.returncode==0 or 'ERROR ' not in p.stderr:
            raise ValueError('malformed native input accepted')
        count += 1
    for n in [12,13]:
        adjacency = [sum(1 << j for j in range(n) if j!=i) for i in range(n)]
        path = work/f'complete-{n}.txt'
        model.write_graph(path,adjacency)
        p = run([pivot,path,work/f'complete-{n}.out',1000000,30],False)
        if n==12:
            if p.returncode!=0 or 'maximum_cliques 1 ' not in p.stdout:
                raise ValueError('positive clique fixture rejected')
        elif p.returncode==0 or not p.stdout.startswith('LARGER_CLIQUE '):
            raise ValueError('larger clique reported as an upper bound')
        count += 1
    for bad in [witnesses[0][:-1], witnesses[0][:-1]+[witnesses[0][0]]]:
        try:
            reference.witness_check(bad)
        except ValueError:
            count += 1
        else:
            raise ValueError('invalid witness accepted')
    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work-dir',type=Path,default=Path('scratch/involution-unit-hub'))
    parser.add_argument('--sanitizers',action='store_true')
    parser.add_argument('--record-expected',action='store_true',help='maintainer: freeze only after all checks pass')
    args = parser.parse_args()
    work = args.work_dir.resolve()
    if work==SOURCE or SOURCE in work.parents:
        raise ValueError('generated state must be outside the contribution directory')
    work.mkdir(parents=True,exist_ok=True)
    (work/'status.json').write_text(json.dumps({'status':'INCOMPLETE'}))
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        os.environ[name] = '1'
    started = time.monotonic()
    qs,adjacency = model.build_local()
    model.write_graph(work/'local.txt',adjacency,qs)
    enumerator = work/('enumerate-sanitize' if args.sanitizers else 'enumerate')
    flags = ['-std=c++20','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer'] if args.sanitizers else ['-std=c++20','-O3']
    subprocess.run(['g++',*flags,'-Wall','-Wextra','-Wconversion','-pedantic',str(SOURCE/'enumerate.cpp'),'-o',str(enumerator)],check=True)
    cases,native_nodes = [],[]
    for k,root in enumerate(model.ROOTS):
        index = qs.index(model.mask(root))
        output = work/f'covers-{k}.txt'
        p = run([enumerator,work/'local.txt',index,1000000,30,output])
        solutions = sorted(tuple(map(int,line.split())) for line in output.read_text().splitlines())
        if len(set(solutions))!=len(solutions):
            raise ValueError('duplicate native covers')
        native_nodes.append(int(p.stdout.split()[4]))
        cases.append(solutions)
    group_order,classes,group_elements = model.classify(qs,adjacency,cases)
    if len(classes)!=2:
        raise ValueError('unexpected class count')
    residual = []
    for k,c in enumerate(classes):
        words = model.anchor(qs,c['representative'])
        rows,graph = model.residual(words)
        maximum,maxima,nodes = model.maximum_cliques(graph)
        if maximum!=12:
            raise ValueError('unexpected completion bound')
        witness = sorted([list(model.points(b)) for b in words]
                         +[list(model.points(b)) for i in maxima[0] for b in [rows[i],model.flip(rows[i])]])
        reference.witness_check(witness)
        residual.append({'anchor':words,'rows':rows,'adjacency':[list(model.bits(a)) for a in graph],
                         'maximum':maximum,'maxima':maxima,'nodes':nodes,'witness':witness})
    analysis = {'rows':qs,'local_adjacency':[list(model.bits(a)) for a in adjacency],
                'cases':cases,'group_elements':group_elements,'classes':classes,'residual':residual}
    (work/'analysis.json').write_text(json.dumps(analysis,separators=(',',':')))
    verified = reference.verify(work,SOURCE,args.sanitizers)
    pivot = work/('pivot-sanitize' if args.sanitizers else 'pivot-reference')
    witnesses = [r['witness'] for r in residual]
    checked_controls = controls(work,enumerator,pivot,witnesses)
    manifest = {'agent':'six-code-2','role':'researcher','claim':'sharp maximum60 in the matched unit-hub involution family',
                'candidate_quads':len(qs),'local_edges':sum(a.bit_count() for a in adjacency)//2,
                'root_cover_counts':[len(c) for c in cases],'native_cover_nodes':native_nodes,
                'literal_cover_nodes':[r['nodes'] for r in verified['local']],
                'group_order':group_order,'classes':classes,
                'local_graph_sha256':digest([qs,analysis['local_adjacency']]),
                'local_covers_sha256':digest(cases),'actual_group_sha256':digest(group_elements),
                'residual':[{'vertices':len(r['rows']),'edges':sum(map(len,r['adjacency']))//2,
                             'maximum':r['maximum'],'max_completions':len(r['maxima']),
                             'color_search_nodes':r['nodes'],
                             'pivot_nodes':int(verified['residual'][k]['pivot'].split()[2]),
                             'graph_sha256':digest([r['rows'],r['adjacency']]),
                             'maxima_sha256':digest(r['maxima']),'witness_sha256':digest(r['witness'])}
                            for k,r in enumerate(residual)],
                'controls':checked_controls,'all_entrywise':verified['all_entrywise']}
    if args.record_expected:
        (SOURCE/'expected.json').write_text(json.dumps(manifest,indent=2)+'\n')
        (SOURCE/'witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')
    else:
        if manifest!=json.loads((SOURCE/'expected.json').read_text()):
            raise ValueError('manifest mismatch')
        if witnesses!=json.loads((SOURCE/'witnesses.json').read_text()):
            raise ValueError('witness mismatch')
    summary = {'status':'COMPLETE','maximum_words':60,'classes':2,
               'root_cover_counts':manifest['root_cover_counts'],
               'completion_maxima':[r['maximum'] for r in residual],
               'completion_counts':[len(r['maxima']) for r in residual],
               'manifest_sha256':digest(manifest),'all_entrywise':True,'controls':checked_controls,
               'sanitizers':args.sanitizers,'seconds':time.monotonic()-started,
               'parent_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               'child_maxrss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (work/'status.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':
    main()
