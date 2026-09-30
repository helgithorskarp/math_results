#!/usr/bin/env python3
"""Definition-level kernel controls, corrupted inputs and sanitizer replay."""
import argparse
import importlib.util
from itertools import combinations
from pathlib import Path
import json
import subprocess
import tempfile
import time

SOURCE=Path(__file__).resolve().parent


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def kernel_controls():
    models=load('double221_models',SOURCE/'models.py');verifier=load('double221_verifier',SOURCE/'verify.py')
    count=0;calls=0
    domains=[]
    for bits in range(1<<10):domains.append((5,bits))
    for seed in range(64):
        bits=(1103515245*(seed+1)+12345)&((1<<28)-1);domains.append((8,bits))
    for n,bits in domains:
        edges=list(combinations(range(n),2));adj=[0]*n;conflicts=[set() for _ in range(n)]
        for k,(a,b) in enumerate(edges):
            if bits>>k&1:adj[a]|=1<<b;adj[b]|=1<<a
            else:conflicts[a].add(b);conflicts[b].add(a)
        exact=0
        for subset in range(1<<n):
            vertices=[z for z in range(n) if subset>>z&1]
            if len(vertices)>exact and all(adj[a]>>b&1 for a,b in combinations(vertices,2)):exact=len(vertices)
        witness,_=models.maximum(adj)
        if len(witness)!=exact:raise RuntimeError('primary maximum differs from definition')
        for target in range(n+2):
            result,_=verifier.independent_set_at_least(conflicts,target)
            if result!=(exact>=target):raise RuntimeError('binary exclusion differs from definition')
            calls+=1
        order,bounds=models.proper_color((1<<n)-1,adj)
        if sorted(order)!=list(range(n)):raise RuntimeError('coloring omitted a vertex')
        for a,b in combinations(range(n),2):
            if bounds[a]==bounds[b] and adj[order[a]]>>order[b]&1:raise RuntimeError('invalid proper color class')
        count+=1
    try:verifier.independent_set_at_least([set()],1,node_cap=0)
    except RuntimeError as e:
        if 'INCOMPLETE' not in str(e):raise
    else:raise RuntimeError('zero-cap search silently accepted')
    return dict(graphs=count,binary_decision_checks=calls,zero_cap_rejected=True)


def native_controls(work):
    output=work/'audit-native.output';input_path=work/'audit-native.input'
    bad=[('negative columns','-1 0 1\n0\n'),('excess columns','121 0 1\n0\n'),
         ('excess rows','120 1335 6\n0\n'),('zero width','0 0 0\n0\n'),
         ('excess width','0 0 7\n0\n'),('negative word','1 1 1\n-1 0\n0\n'),
         ('excess word','1 1 1\n131072 0\n0\n'),('bad row column','1 1 1\n1 1\n0\n'),
         ('duplicate row column','2 1 2\n1 0 0\n0\n'),('duplicate word','2 2 1\n1 0\n1 1\n0\n'),
         ('bad case index','1 0 1\n1\n1 0\n'),('duplicate forbidden column','2 0 1\n1\n0 2 1 1\n'),
         ('truncated case','1 0 1\n1\n0 1\n'),('trailing input','0 0 1\n0\nunexpected\n')]
    for name,text in bad:
        input_path.write_text(text)
        r=subprocess.run([str(work/'bitset'),str(input_path),str(output)],text=True,capture_output=True,timeout=20)
        if r.returncode!=2 or 'INCOMPLETE' in r.stderr:raise RuntimeError('malformed input not rejected: '+name)
    positive=work/'highstar_s2_000.input'
    r=subprocess.run([str(work/'bitset'),str(positive),str(output),'1'],text=True,capture_output=True,timeout=20)
    if r.returncode!=2 or 'INCOMPLETE' not in r.stderr:raise RuntimeError('node guard not visible')
    r=subprocess.run([str(work/'bitset'),str(positive),str(output),'200001'],text=True,capture_output=True,timeout=20)
    if r.returncode!=2 or 'invalid node cap' not in r.stderr:raise RuntimeError('raised node cap accepted')
    for name in ['transport','scan']:
        input_path.write_text('4\n')
        r=subprocess.run([str(work/name),str(input_path),str(output)],text=True,capture_output=True,timeout=20)
        if r.returncode!=2:raise RuntimeError('wrong template count accepted')
        text=(work/'scan.input').read_text().split()
        text[1]='131072';input_path.write_text(' '.join(text)+'\n')
        r=subprocess.run([str(work/name),str(input_path),str(output)],text=True,capture_output=True,timeout=20)
        if r.returncode!=2:raise RuntimeError('excess template mask accepted')
    return dict(malformed_sparse_inputs=len(bad),transport_input_rejections=4,node_guard_rejected=True,raised_cap_rejected=True)


def fixture_controls(work):
    fixture=json.loads((SOURCE/'witness58.json').read_text())
    original=fixture['word_masks'];rejected=0
    bad=original[:];bad[0]&=bad[0]-1
    mutations=[bad]
    bad=original[:];bad[1]=bad[0];mutations.append(bad)
    bad=original[:];w=bad[0];removed=w&-w
    add=next(1<<z for z in range(18) if not(w>>z&1));bad[1]=(w^removed)|add;mutations.append(bad)
    bad=original[:-1];mutations.append(bad)
    verifier=load('double221_fixture_verifier',SOURCE/'verify.py')
    with tempfile.TemporaryDirectory(prefix='fixture-audit-',dir=work) as tmp:
        path=Path(tmp);verifier.SOURCE=path
        (path/'acl69.txt').write_bytes((SOURCE/'acl69.txt').read_bytes())
        for words in mutations:
            bad=dict(fixture,word_masks=words)
            (path/'witness58.json').write_text(json.dumps(bad))
            try:verifier.witness_check()
            except RuntimeError:rejected+=1
            else:raise RuntimeError('verifier accepted corrupted fixture')
    return dict(corrupted_fixtures_rejected=rejected)


def sanitizers(work):
    flags=['-std=c++17','-O1','-g','-Wall','-Wextra','-Wpedantic','-fsanitize=address,undefined','-fno-omit-frame-pointer']
    for name in ['bitset','transport','scan']:
        subprocess.run(['g++',*flags,str(SOURCE/(name+'.cpp')),'-o',str(work/(name+'-san'))],check=True)
    cases=['highstar_s0_000','highstar_s0_004','highstar_s1_004','highstar_s2_000','highstar_s3_000','highstar_s3_100','highstar_s3_611']
    for name in cases:
        out=work/'audit-sanitized.jsonl'
        r=subprocess.run([str(work/'bitset-san'),str(work/(name+'.input')),str(out)],text=True,capture_output=True,timeout=20)
        if r.returncode or r.stderr:raise RuntimeError('sanitizer failure in '+name+': '+r.stderr)
        expected=json.loads((work/(name+'.jsonl')).read_text())
        if json.loads(out.read_text())!=expected:raise RuntimeError('sanitized cover mismatch')
    for name,inp,expected in [('transport','transport.input','couple.jsonl'),('scan','scan.input','brute.jsonl')]:
        out=work/(name+'-san.jsonl')
        r=subprocess.run([str(work/(name+'-san')),str(work/inp),str(out)],text=True,capture_output=True,timeout=60)
        if r.returncode or r.stderr:raise RuntimeError('sanitizer failure in '+name+': '+r.stderr)
        if out.read_bytes()!=(work/expected).read_bytes():raise RuntimeError('sanitized transport mismatch')
    return dict(bitset_cases=len(cases),transport_branches=9,complete_scan_branches=9,complete_scan_maps=58786560,diagnostics=0)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work-dir',type=Path,required=True)
    parser.add_argument('--sanitizers',action='store_true');args=parser.parse_args();work=args.work_dir.resolve();start=time.monotonic()
    result=dict(agent='six-code-3',role='researcher',kernels=kernel_controls(),native=native_controls(work),fixtures=fixture_controls(work))
    if args.sanitizers:result['sanitizers']=sanitizers(work)
    result.update(status='COMPLETE',seconds=round(time.monotonic()-start,6))
    (work/('audit-sanitizers.json' if args.sanitizers else 'audit.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
