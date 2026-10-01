"""Literal positive/negative controls for both finite proof boundaries."""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess

from native import Native
import verify_residual as r

HERE=Path(__file__).resolve().parent


def rejects(function):
    try:
        function()
    except (ValueError,TypeError,RuntimeError):
        return
    raise ValueError('malformed evidence was accepted')


def run(work,executable):
    labels=[0,63,64,127,255]
    edges=list(combinations(range(5),2))
    decisions=0
    for code in range(1 << len(edges)):
        adjacent=[set() for _ in range(256)]
        literal=[set() for _ in range(5)]
        for bit,(a,b) in enumerate(edges):
            if code & (1 << bit):
                adjacent[labels[a]].add(labels[b]);adjacent[labels[b]].add(labels[a])
                literal[a].add(b);literal[b].add(a)
        with Native(executable,[adjacent]) as engine:
            for target in range(1,6):
                expected=[[labels[i] for i in q] for q in combinations(range(5),target)
                          if all(b in literal[a] for a,b in combinations(q,2))]
                actual,nodes=engine.query(0,labels,target=target)
                r.check(actual==expected,'exhaustive small literal/native mismatch')
                decisions+=1
    bad_native=[
        '1\n257\n',
        '1\n2\n1 1\n0\n',
        '1\n2\n1 0\n0\n',
        '1\n3\n2 2 1\n0\n0\n',
        '1\n2\n0\n0\n0 1 2000000 20000 2 0 0\n',
        '1\n2\n0\n0\n0 0 2000000 20000 2 0 1\n',
        '1\n2\n0\n0\n0 1 0 20000 2 0 1\n',
        '1\n2\n0\n0\n0 1 2000000 20000 1 2\n',
        '1\n2\n1 1\n1 0\n0 2 1 20000 2 0 1\n',
    ]
    for data in bad_native:
        result=subprocess.run([str(executable.resolve())],input=data,text=True,capture_output=True,timeout=3)
        r.check(result.returncode!=0 and not result.stdout.strip(),'invalid/guarded native job reported completion')
    cores=[c for k in range(40) for c in json.loads((work/f'joints-{k}.json').read_text())]
    certs=json.loads((HERE/'residual.json').read_text())['certificates']
    core=cores[0];cert=certs[0]
    r.check_one(core,cert)
    bad=[]
    c=copy.deepcopy(cert);c['core_sha256']='0'*64;bad.append((core,c))
    c=copy.deepcopy(cert);c['candidate_sha256']='0'*64;bad.append((core,c))
    c=copy.deepcopy(cert);c['candidate_count']+=1;bad.append((core,c))
    c=copy.deepcopy(cert);c['limit']=20;bad.append((core,c))
    c=copy.deepcopy(cert);c['tree']={'kind':'size'};bad.append((core,c))
    c=copy.deepcopy(cert);c['tree']={'kind':'color','colors':[0]*c['candidate_count']};bad.append((core,c))
    c=copy.deepcopy(cert);c['tree']['colors'][0]=21;bad.append((core,c))
    c=copy.deepcopy(cert);c['tree']['colors'][0]=True;bad.append((core,c))
    c=copy.deepcopy(cert);c['tree']['colors'].pop();bad.append((core,c))
    q=copy.deepcopy(core);q['blocks'][0]=q['blocks'][1];bad.append((q,cert))
    branch=next(c for c in certs if c['tree']['kind']=='branch')
    corresponding=next(c for c in cores if c['core_sha256']==branch['core_sha256'])
    c=copy.deepcopy(branch);c['tree']['branches'].pop();bad.append((corresponding,c))
    c=copy.deepcopy(branch);c['tree']['branches'].append(copy.deepcopy(c['tree']['branches'][0]));bad.append((corresponding,c))
    for q,c in bad:rejects(lambda q=q,c=c:r.check_one(q,c))
    witness=json.loads((HERE/'witness63.json').read_text())
    witness_core=next(c for c in cores if c['core_sha256']==witness['core_sha256'])
    positive=r.witness_record(witness,witness_core)
    q=copy.deepcopy(witness);q['residual_indices'].pop();rejects(lambda:r.witness_record(q,witness_core))
    q=copy.deepcopy(witness);q['blocks'][0]=q['blocks'][1];rejects(lambda:r.witness_record(q,witness_core))
    baseline=(HERE/'baseline69.txt').read_bytes()
    r.check(hashlib.sha256(baseline).hexdigest()=='cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d',
            'public baseline checksum')
    lines=baseline.decode().splitlines()
    r.check(len(lines)==69 and all(len(line)==18 and set(line)<={'0','1'} for line in lines),'baseline domain')
    masks=[int(line,2) for line in lines]
    r.check(len(set(masks))==69 and all(w.bit_count()==5 for w in masks),'baseline weight/cardinality')
    distances=Counter((a ^ b).bit_count() for a,b in combinations(masks,2))
    degrees=Counter(sum(bool(w & (1 << i)) for w in masks) for i in range(18))
    r.check(dict(distances)=={6:1264,8:637,10:445} and dict(degrees)=={12:1,18:2,19:3,20:12},
            'established baseline mismatch')
    result={'status':'PASSED','small_graphs':1024,'clique_decisions':decisions,'vertex_labels':labels,
            'native_bad_or_guard_rejections':len(bad_native),'bad_capacity_or_witness_rejections':len(bad)+2,
            'positive_words':positive['words'],'baseline_words':69,'baseline_min_distance':min(distances),
            'baseline_degrees':dict(sorted(degrees.items()))}
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--executable',type=Path,required=True)
    args=parser.parse_args()
    run(args.work,args.executable)
