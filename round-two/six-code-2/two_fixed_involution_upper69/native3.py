import maps3
from paths import INPUTS, WORK
"""Separate literal twin-expansion upper checks with a pinned native kernel."""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import time
import maps3
from carrier import STANDARD_G, check_code, literal_residual, points, require
from quotient import encoded

SOURCE_SHA='0cec8c9692d3af1d4ba1d3a481bd78bccaf2ed793f6002607b5ebbbb42f617fa'


def expanded(anchor):
    orbits=literal_residual(anchor)
    actual=tuple(tuple(frozenset(points(w)) for w in orbit) for orbit in orbits)
    # Weight-many adjacent true twins for each orbit; literal cross compatibility.
    clones=tuple(i for i,orbit in enumerate(orbits) for _ in orbit)
    legal=tuple(tuple(i==j or all(len(a&b)<=2 for a in actual[i] for b in actual[j])
                      for j in range(len(orbits))) for i in range(len(orbits)))
    adjacency=tuple(tuple(j for j,b in enumerate(clones) if i!=j and legal[a][b])
                    for i,a in enumerate(clones))
    return adjacency,orbits


def query(binary,adjacency,target):
    text=[f'{len(adjacency)} {target}']+[str(len(row))+' '+ ' '.join(map(str,row)) for row in adjacency]
    p=subprocess.run([str(binary)],input='\n'.join(text)+'\n',capture_output=True,text=True,timeout=35)
    require(p.returncode==0 and p.stderr.startswith('COMPLETE '),'native incomplete: '+p.stderr)
    return p


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--roots',type=Path,default=(WORK/'swapped-m3-roots.json'))
    parser.add_argument('--color',type=Path,default=(WORK/'swapped-m3-completions/summary.json'))
    parser.add_argument('--cases',type=int,nargs='+')
    parser.add_argument('--sanitized',action='store_true')
    args=parser.parse_args();args.work.mkdir(parents=True,exist_ok=True);started=time.monotonic()
    source=INPUTS/'cliques.cpp'
    require(hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA,'changed native input')
    binary=(args.work/'cliques').resolve()
    flags=['g++','-std=c++17','-Wall','-Wextra','-Werror','-O1' if args.sanitized else '-O2']
    if args.sanitized:flags+=['-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-fno-pie','-no-pie']
    p=subprocess.run(flags+[str(source),'-o',str(binary)],capture_output=True,text=True,timeout=60)
    require(p.returncode==0,'native build failed: '+p.stderr)
    control=subprocess.run([str(binary),'--self-test'],capture_output=True,text=True,timeout=35)
    require(control.returncode==0 and control.stdout.startswith('COMPLETE exhaustive-small 6144 '),
            'native6144 small-graph control')
    roots=json.loads(args.roots.read_text())['roots']; color=json.loads(args.color.read_text())['records']
    by_case={r['root']:r for r in color};indices=args.cases if args.cases is not None else list(range(len(roots)))
    records=[]
    for ri in indices:
        root=roots[ri];anchor=tuple(root['normalized']);old=by_case[ri]
        require(old['status']=='COMPLETE_MAXIMUM','incomplete producer record')
        witness=tuple(old['witness']); reps=check_code(witness,STANDARD_G)
        require(set(anchor)<=set(witness) and reps[:2]==(20,20) and len(witness)==37+old['residual_weight'],
                'wrong positive lower witness')
        adjacency,orbits=expanded(anchor)
        require(len(orbits)==old['vertices'],'literal residual census differs')
        target=old['residual_weight']+1
        p=query(binary,adjacency,target)
        require(p.stdout=='' and int(p.stderr.split()[2])==0,'native larger clique found')
        record={'root':ri,'fixture':root['fixture'],'orbit_vertices':len(orbits),
                'expanded_vertices':len(adjacency),'upper':old['residual_weight'],
                'native_nodes':int(p.stderr.split()[1]),'larger_cliques':0,
                'status':'COMPLETE_EXACT_UPPER_AND_LITERAL_LOWER',
                'literal_expansion_sha256':hashlib.sha256(encoded(adjacency)).hexdigest()}
        (args.work/f'case-{ri:03d}.json').write_bytes(encoded(record));records.append(record)
        if len(records)%50==0:print(json.dumps({'completed':len(records),'root':ri}),flush=True)
    result={'agent':'six-code-2','role':'researcher','status':'COMPLETE_REQUESTED_NATIVE_BOUNDS',
            'cases':len(records),'inventory_roots':len(roots),'records':records,
            'sanitized':args.sanitized,'native_small_cases':6144,'seconds':time.monotonic()-started,
            'peak_RSS_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'child_peak_RSS_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'trust':'integer-weight true-twin equivalence; independently written reviewed kernel, not independent review of this new theorem'}
    (args.work/'summary.json').write_bytes(encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k!='records'},sort_keys=True),flush=True)


if __name__=='__main__':main()
