#!/usr/bin/env python3
"""Rebuild all finite domains and the exact restricted maximum58."""
import argparse
from itertools import combinations
from pathlib import Path
import hashlib
import json
import resource
import subprocess
import time
import models as m

SOURCE=Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def write(work,name,value):
    (work/name).write_text(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n')


def baseline():
    raw=(SOURCE/'acl69.txt').read_bytes()
    words=[int(row,2) for row in raw.splitlines()]
    if len(words)!=69 or len(set(words))!=69 or any(w.bit_count()!=5 for w in words) or any(
            (a&b).bit_count()>2 for a,b in combinations(words,2)):
        raise RuntimeError('invalid historical69 baseline')
    saturated=[]
    for x in range(18):
        if sum(w>>x&1 for w in words)!=20:continue
        deficits=sorted([5-sum(w>>x&1 and w>>y&1 for w in words) for y in range(18) if y!=x],reverse=True)
        if any(t<0 for t in deficits) or sum(deficits)!=5:raise RuntimeError('bad baseline deficits')
        if [t for t in deficits if t]==[2,2,1]:saturated.append(x)
    if saturated!=[3]:raise RuntimeError('historical marked profile baseline differs')
    return dict(words=69,raw_sha256=hashlib.sha256(raw).hexdigest(),coordinate0='rightmost binary digit',profile221_centers=saturated)


def first_domain():
    domain=[];shapes=[]
    graphs,maps=m.cubic_graphs();reps=m.quotient(graphs,maps)
    for shape in [0,1]:
        shapes.append(dict(shape=shape,raw_graphs=len(graphs),maps=len(maps),graph_orbits=len(reps)))
    for i,(graph,size) in enumerate(reps):
        words=m.cubic_words(graph)
        for shape,fixed in [(0,words),(1,m.shape1_words(words))]:
            domain.append(dict(shape=shape,orbit=i,orbit_size=size,graph=graph,fixed=fixed))
    cube=[(0,1,15,16),(0,9,10,11),(0,12,13,14),(1,3,4,5),(1,6,7,8),
          (2,6,9,12),(2,3,10,13),(2,4,7,14),(2,5,8,11)]
    domain.append(dict(shape=2,orbit=0,orbit_size=1,graph=None,fixed=sorted(sum(1<<z for z in q) for q in cube)))
    shapes.append(dict(shape=2,raw_graphs=1,maps=1,graph_orbits=1))
    graphs,maps=m.triangle_graphs();reps=m.quotient(graphs,maps)
    shapes.append(dict(shape=3,raw_graphs=len(graphs),maps=len(maps),graph_orbits=len(reps)))
    for i,(graph,size) in enumerate(reps):domain.append(dict(shape=3,orbit=i,orbit_size=size,graph=graph,fixed=m.triangle_words(graph)))
    domain.sort(key=lambda d:(d['shape'],d['orbit']))
    for d in domain:m.validate_fixed(d['shape'],d['fixed'])
    return dict(shapes=shapes,cases=domain)


def joint_domain(work,templates):
    inp=work/'transport.input';out=work/'couple.jsonl'
    inp.write_text('3\n'+'\n'.join(' '.join(map(str,d['star'])) for d in templates)+'\n')
    result=subprocess.run([str(work/'transport'),str(inp),str(out)],text=True,capture_output=True,timeout=60)
    (work/'transport.log').write_text(result.stdout+result.stderr)
    if result.returncode:raise RuntimeError('transport failed/incomplete: '+result.stderr)
    branches=[json.loads(line) for line in out.read_text().splitlines()]
    if [(d['first'],d['second']) for d in branches]!=[(f,s) for f in range(3) for s in range(3)]:raise RuntimeError('incomplete transport branches')
    capacities=[];index={}
    masks=[sum(1<<z for z in q) for q in combinations(range(1,17),5)]
    for branch in branches:
        for i,star in enumerate(branch['stars']):
            fixed=sorted(set([w|(1<<17) for w in templates[branch['first']]['star']]+star))
            if len(fixed)!=37 or any((a&b).bit_count()>2 for a,b in combinations(fixed,2)):raise RuntimeError('invalid37-word joint star')
            candidates=[w for w in masks if all((w&f).bit_count()<=2 for f in fixed)]
            index[branch['first'],branch['second'],i]=len(capacities)
            capacities.append(dict(first=branch['first'],second=branch['second'],star_index=i,fixed=fixed,candidates=candidates))
    write(work,'capacity_domain.json',dict(cases=capacities))
    groups=[m.automorphisms(d['star']) for d in templates];orbits=[]
    for branch in branches:
        domain={tuple(star) for star in branch['stars']};seen=set();star_index={tuple(s):i for i,s in enumerate(branch['stars'])}
        for star in sorted(domain):
            if star in seen:continue
            orbit={m.transport(star,p) for p in groups[branch['first']]}
            if not orbit<=domain or orbit&seen or star!=min(orbit):raise RuntimeError('invalid joint orbit')
            seen.update(orbit)
            orbits.append(dict(first=branch['first'],second=branch['second'],star=star,orbit_size=len(orbit),
                               capacity_index=index[branch['first'],branch['second'],star_index[star]]))
        if seen!=domain:raise RuntimeError('missing joint star')
    write(work,'joint_orbits.json',dict(groups=groups,cases=orbits))
    return branches,capacities,groups,orbits


def run(work):
    m.ROOT=work
    for name in ['bitset','transport']:
        subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic',str(SOURCE/(name+'.cpp')),'-o',str(work/name)],check=True)
    base=baseline();domain=first_domain();write(work,'highstar_domain.json',domain)
    records=[];templates=[];covers=[]
    swaps={0:(3,4),1:(9,10),2:(15,16)}
    for i,d in enumerate(domain['cases']):
        name=f'highstar_s{d["shape"]}_{d["orbit"]:03d}'
        report=m.run_case(name,d['shape'],d['fixed'])
        if report['status']!='COMPLETE':raise RuntimeError('first-star census incomplete: '+name)
        raw=json.loads((work/(name+'.jsonl')).read_text())['covers']
        stars=sorted(sorted(d['fixed']+c) for c in raw)
        covers.append(dict(shape=d['shape'],orbit=d['orbit'],stars=stars));records.append(report)
        if stars:
            a,b=swaps[d['shape']]
            p=list(range(18));p[a],p[b]=p[b],p[a]
            if len(stars)!=2 or list(m.transport(stars[0],p))!=stars[1]:raise RuntimeError('first-star transposition mismatch')
            templates.append(dict(shape=d['shape'],star=stars[0],second_star=stars[1],transposition=[a,b]))
        write(work,'progress.json',dict(status='INCOMPLETE',first_cases_completed=i+1,total_first_cases=len(domain['cases'])))
    if [d['shape'] for d in templates]!=[0,1,2]:raise RuntimeError('expected three marked templates')
    write(work,'first_star_templates.json',templates)
    branches,capacities,groups,orbits=joint_domain(work,templates)
    residual=[]
    for i,d in enumerate(orbits):
        case=capacities[d['capacity_index']];candidates=case['candidates']
        adj=[sum(1<<j for j,v in enumerate(candidates) if j!=k and (w&v).bit_count()<=2) for k,w in enumerate(candidates)]
        witness,nodes=m.maximum(adj)
        residual.append(dict(index=i,first=d['first'],second=d['second'],orbit_size=d['orbit_size'],
                             candidates=len(candidates),candidate_sha256=digest(candidates),residual_maximum=len(witness),nodes=nodes,
                             attaining_words=sorted(case['fixed']+[candidates[v] for v in witness])))
    if max(d['residual_maximum'] for d in residual)!=21:raise RuntimeError('restricted maximum is not58')
    write(work,'residual_results.json',dict(status='COMPLETE',cases=residual))
    fixture=json.loads((SOURCE/'witness58.json').read_text())
    words=fixture['word_masks']
    if len(words)!=58 or len(set(words))!=58 or any(w.bit_count()!=5 or w<0 or w>=1<<18 for w in words) or any(
            (a&b).bit_count()>2 for a,b in combinations(words,2)):raise RuntimeError('invalid58-word fixture')
    for x,y in [(17,0),(0,17)]:
        if sum(w>>x&1 for w in words)!=20 or sum(w>>x&1 and w>>y&1 for w in words)!=3:raise RuntimeError('fixture centers or pair differ')
        deficits=sorted([5-sum(w>>x&1 and w>>z&1 for w in words) for z in range(18) if z!=x],reverse=True)
        if [t for t in deficits if t]!=[2,2,1]:raise RuntimeError('fixture row differs')
    result=dict(schema=1,agent='six-code-3',role='researcher',baseline=base,first_shapes=domain['shapes'],
                first_cases=len(records),first_domain_sha256=digest(domain['cases']),first_cover_stream_sha256=digest(covers),
                first_cover_nodes=sum(r['nodes'] for r in records),first_max_case_nodes=max(r['nodes'] for r in records),
                templates=templates,joint_branch_counts=[len(d['stars']) for d in branches],
                joint_map_counts=[d['maps'] for d in branches],joint_stars=148,joint_star_stream_sha256=digest([d['stars'] for d in branches]),
                group_orders=list(map(len,groups)),joint_orbits=len(orbits),joint_orbit_stream_sha256=digest(orbits),
                residual_cases=[{k:v for k,v in d.items() if k not in ['attaining_words','nodes']} for d in residual],
                residual_nodes=sum(d['nodes'] for d in residual),residual_max_case_nodes=max(d['nodes'] for d in residual),
                restricted_maximum=58,witness58_sha256=digest(fixture))
    write(work,'summary.json',result);write(work,'progress.json',dict(status='COMPLETE'))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work-dir',type=Path,required=True)
    parser.add_argument('--check',type=Path);parser.add_argument('--output',type=Path);args=parser.parse_args()
    work=args.work_dir.resolve();work.mkdir(parents=True,exist_ok=True);started=time.monotonic()
    result=run(work)
    if args.check and result!=json.loads(args.check.read_text()):raise RuntimeError('complete manifest mismatch')
    if args.output:args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    meta=dict(status='COMPLETE',first_cases=result['first_cases'],joint_stars=result['joint_stars'],joint_orbits=result['joint_orbits'],
              restricted_maximum=result['restricted_maximum'],seconds=round(time.monotonic()-started,6),
              max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,child_rss_kib_upper=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    write(work,'runtime.json',meta);print(json.dumps(meta))


if __name__=='__main__':main()
