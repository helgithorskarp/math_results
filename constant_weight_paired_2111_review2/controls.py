"""Literal Python fibers, conjugacies, malformed inputs and real sanitizer census."""
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import subprocess
import time
from audit import points, union_check, check_partition, digest
from incidence import canonical, image, inverse, need

BASE=Path(__file__).resolve().parent


def literal_fiber(a,b,fixed):
    started=time.monotonic()
    tails=[points(w ^ 1,17) for w in b if w & 1]
    source=set().union(*tails)
    free=sorted(set(range(1,17))-source)
    targets=sorted(set(range(1,17))-set(fixed.values()))
    need(len(source)==9 and len(free)==len(targets)==7, 'bad control fiber')
    left=[points(w,17) for w in a if not w&1]
    right=[points(w,17) for w in b if not w&1]
    result=[]
    nodes=0
    for q in permutations(targets):
        nodes+=1
        mapping=dict(fixed)
        mapping.update(zip(free,q))
        if any(len(u & frozenset(mapping[z] for z in v))>2 for u in left for v in right):
            continue
        p=(17,)+tuple(mapping[z] for z in range(1,17))
        l=tuple(w|(1<<17) for w in a)
        r=tuple(1|sum(1<<p[z] for z in range(17) if w>>z&1) for w in b)
        union_check(l,r)
        result.append(p)
    need(nodes==5040 and time.monotonic()-started<=10,'INCOMPLETE literal control fiber')
    return result


def run(work):
    started=time.monotonic();work.mkdir(parents=True,exist_ok=True)
    stars=[tuple(q) for q in json.loads((BASE/'templates.json').read_text())]
    data=('\n'.join(' '.join(map(str,q)) for q in stars)+'\n').encode()
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    exe=work/'raw_pairs'
    flags=['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic','-Werror']
    subprocess.run(flags+[str(BASE/'raw_pairs.cpp'),'-o',str(exe)],check=True,env=env,timeout=60)
    def native(args,raw=data,binary=exe):
        return subprocess.run([str(binary),*args],input=raw,capture_output=True,env=env,timeout=45)
    args=['5','6','200000','10']
    ordinary=native(args);need(ordinary.returncode==0,'control pair census failed')
    maps=[tuple(map(int,l.split()[3:])) for l in ordinary.stdout.decode().splitlines() if l.startswith('MAP ')]
    need(len(maps)==324 and ordinary.stdout.decode().splitlines()[-1]=='PAIR 0 5 362880 1296 6531840 324 324 COMPLETE','control raw census differs')
    a,b=stars[0],stars[5]
    bt=[tuple(sorted(points(w^1,17))) for w in b if w&1]
    at=[tuple(sorted(points(w^1,17))) for w in a if w&1]
    source=tuple(sorted(set().union(*(set(t) for t in bt))))
    tails=set()
    for block_images in permutations(at):
        for triple_images in product(*(tuple(permutations(t)) for t in block_images)):
            d={z:v for t,q in zip(bt,triple_images) for z,v in zip(t,q)}
            tails.add(tuple(d[z] for z in source))
    need(len(tails)==1296, 'independent triple-bijection tail carrier incomplete')
    nine=sorted(set().union(*(set(t) for t in at)))
    filtered=set()
    targets={frozenset(t) for t in at}
    for q in permutations(nine):
        d=dict(zip(source,q))
        if all(frozenset(d[z] for z in t) in targets for t in bt):filtered.add(q)
    need(filtered==tails,'independent complete nine-point tail domains differ')
    positive=sorted({tuple(p[z] for z in source) for p in maps})
    negative=sorted(tails-set(positive))
    need(len(positive)==324 and negative,'unexpected positive/negative fiber control carrier')
    fiber_records=[]
    for tail in positive[:2]+negative[:2]:
        fixed=dict(zip(source,tail))
        got=sorted(literal_fiber(a,b,fixed))
        expected=sorted(p for p in maps if tuple(p[z] for z in source)==tail)
        need(got==expected,'literal Python control accepted maps differ entrywise')
        fiber_records.append(dict(tail=tail,accepted=len(got),nodes=5040,sha256=digest(got)))
    sanitizer=work/'raw_pairs_sanitized'
    subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-Wpedantic','-Werror','-fsanitize=address,undefined','-fno-omit-frame-pointer',str(BASE/'raw_pairs.cpp'),'-o',str(sanitizer)],check=True,env=env,timeout=60)
    checked=native(args,binary=sanitizer)
    need(checked.returncode==0 and not checked.stderr and checked.stdout==ordinary.stdout,'sanitized full positive pair differs or reports diagnostics')
    mutations=[]
    bad=[data[:-20],data+b'1\n',b'0 '+data.split(b' ',1)[1],data.replace(b'30 240',b'30 30',1)]
    # Replication/profile corruption while keeping four bits in a word.
    altered=[list(s) for s in stars];altered[0][0]=15
    bad.append(('\n'.join(' '.join(map(str,s)) for s in altered)+'\n').encode())
    for raw in bad:
        result=native(args,raw)
        need(result.returncode!=0 and b'COMPLETE' not in result.stdout,'malformed template accepted')
        mutations.append(result.stderr.decode().strip())
    invalid=[['5','6','200001','10'],['5','6','-1','10'],['5','6','200000','11'],['5','6','200000','0'],['5x','6','200000','10'],['5','6','200000','10x']]
    for x in invalid:
        r=native(x);need(r.returncode!=0 and b'COMPLETE' not in r.stdout,'invalid native guard accepted')
    incomplete=[]
    for x in (['5','6','1','10'],['5','6','200000','1e-12']):
        r=native(x);need(r.returncode!=0 and b'INCOMPLETE' in r.stderr and b'COMPLETE' not in r.stdout,'tiny guard hides incomplete search')
        incomplete.append(r.stderr.decode().strip())
    conjugacies=0
    for s in stars:
        p=(0,2,3,1)+tuple(range(5,17))+(4,)
        original=canonical(s,17,((0,),(1,2,3),tuple(range(4,17))))
        relabeled=canonical(image(s,p),17,((0,),(1,2,3),tuple(range(4,17))))
        expected={tuple(p[g[inverse(p)[z]]] for z in range(17)) for g in original['automorphisms']}
        need(original['canonical']==relabeled['canonical'] and expected==set(relabeled['automorphisms']),'star canonical/group conjugacy fails')
        conjugacies+=1
    joint_conjugacies=0
    for p in maps[:4]:
        words=union_check(tuple(w|(1<<17) for w in a),tuple(1|sum(1<<p[z] for z in range(17) if w>>z&1) for w in b))
        for colors in (((0,),(17,),tuple(range(1,17))),((0,17),tuple(range(1,17)))):
            # Preserve named centers; rotate every noncenter point.
            q=(0,)+tuple(range(2,17))+(1,17)
            r=canonical(words,18,colors);s=canonical(image(words,q),18,colors)
            need(r['canonical']==s['canonical'] and r['order']==s['order'],'joint relabeling changes class/order')
            joint_conjugacies+=1
    # Explicit finite incidence baseline: one edge has S2, a three-point path
    # has C2; every mapping is independently compared by literal permutations.
    tiny=0
    for n,words in ((2,(3,)),(3,(3,6)),(4,(3,6,12)),(4,(7,14))):
        actual={p for p in permutations(range(n)) if image(words,p)==tuple(sorted(words))}
        r=canonical(words,n,(tuple(range(n)),))
        need(set(r['automorphisms'])==actual,'tiny full-permutation automorphism baseline differs')
        tiny+=1
    candidates=[frozenset((0,1,2,3,4)),frozenset((0,1,2,5,6)),frozenset((3,4,5,6,7))]
    need(check_partition(candidates,[[0,1],[2]])==2,'valid partition control rejected')
    rejected=0
    for part in ([[0,1,2]],[[0,1],[1,2]],[[0],[1]],[[0,1],[2],[]],[[0,True],[2]],[] ):
        try:check_partition(candidates,part)
        except (ValueError,TypeError,IndexError):rejected+=1
        else:raise ValueError('corrupt partition accepted')
    for cap,seconds in ((0,10),(200000,1e-12)):
        try:canonical((3,6),3,((0,1,2),),cap=cap,seconds=seconds)
        except ValueError as e:need('INCOMPLETE' in str(e),'incidence guard lacks incomplete status')
        else:raise ValueError('incidence tiny guard did not fail')
    result=dict(agent='six-reviewer-2',role='independent mathematical reviewer',status='COMPLETE independent controls',
                literal_python_fibers=fiber_records,literal_fiber_nodes=20160,independent_tail_maps=len(tails),filtered_nine_permutations=362880,
                sanitizer_full_assignments=6531840,sanitizer_positive_maps=len(maps),sanitizer_diagnostics=0,
                raw_pair_stream_sha256=hashlib.sha256(ordinary.stdout).hexdigest(),
                malformed_templates=len(bad),invalid_native_guards=len(invalid),visible_native_INCOMPLETE=incomplete,
                star_conjugacies=conjugacies,joint_conjugacies=joint_conjugacies,tiny_full_permutation_groups=tiny,
                corrupt_partitions_rejected=rejected,visible_incidence_INCOMPLETE=2)
    (work/'controls.json').write_text(json.dumps(result,indent=2)+'\n')
    metrics=dict(seconds=time.monotonic()-started,parent_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,child_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (work/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    print(json.dumps(result),flush=True);print(json.dumps(metrics),flush=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();run(a.work.resolve())
