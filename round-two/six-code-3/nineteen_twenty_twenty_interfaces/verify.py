"""Literal point-set reconstruction, unused-triple covers, and maximal-clique replay."""
import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations,product
import json
from pathlib import Path
import time

from native import Native

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
BACKEND=ROOT/'three_nineteen_zero_triples'/'verify.py'
if hashlib.sha256(BACKEND.read_bytes()).hexdigest()!='c9f63e88d033595c3be6c4144a689945d2f425773a28f3badfb83a6d5566891e':
    raise ValueError('prior literal helper changed')
spec=importlib.util.spec_from_file_location('literal_helpers',BACKEND)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)


def inputs():
    raw=(ROOT/'nineteen_star_classification'/'expected.json').read_bytes()
    v.check(hashlib.sha256(raw).hexdigest()==v.MANIFEST_SHA,'classification binding')
    manifest=json.loads(raw)
    output=[]
    for model_id,model in enumerate(manifest['models']):
        holes=set();offset=0
        for length in model['cycle_half_lengths']:
            cycle=list(range(offset,offset+length))
            for a,b in zip(cycle,cycle[1:]+cycle[:1]):
                holes.add((a,a));holes.add((a,b))
            offset+=length
        v.check(offset==5,'anchor form size')
        cells=[(r,c) for r in range(5) for c in range(5) if (r,c) not in holes]
        rows=[frozenset(i for i,(r,c) in enumerate(cells) if r==j) for j in range(5)]
        cols=[frozenset(i for i,(r,c) in enumerate(cells) if c==j) for j in range(5)]
        matchings=[]
        for chosen in combinations(range(5),4):
            for q in product(*(sorted(rows[j]) for j in chosen)):
                if len({cells[i][1] for i in q})==4:
                    matchings.append(tuple(sorted(q)))
        matchings=sorted(matchings)
        v.check(len(matchings)==len(set(matchings))==model['candidate_count'],'matching reconstruction')
        for marked_id,rep in enumerate(model['marked_classes']):
            private=[frozenset(matchings[i]) for i in rep['clique']]
            fixed=[r|{15,17} for r in rows]+[c|{16,17} for c in cols]+[q|{17} for q in private]
            v.packing(fixed,19)
            v.check(v.stats(fixed,17)['m']==rep['low_low_pairs'],'initial marked leave count')
            star={'model':model_id,'marked':marked_id,'m':rep['low_low_pairs'],'cells':cells,'clique':rep['clique'],
                  'row':[v.bits(r) for r in rows],'col':[v.bits(c) for c in cols],
                  'private':[v.bits(q) for q in private],'fixed':sorted(v.bits(w) for w in fixed)}
            output.append((star,rows,cols,fixed))
    v.check(len(output)==46,'complete forty-six marked inputs')
    return output



def covers(fixed):
    begun=time.monotonic()
    triples=[frozenset(q) for q in combinations(range(15),3)
             if all(len((frozenset(q)|{15,16})&w)<=2 for w in fixed)]
    index={t:i for i,t in enumerate(triples)}
    incident={i:[t for t in triples if i in t] for i in range(15)}
    output=[];nodes=0
    def visit(left,chosen):
        nonlocal nodes
        nodes+=1
        if nodes>2000000 or time.monotonic()-begun>20:
            raise RuntimeError('INCOMPLETE unused-triple cover guard')
        if not left:
            v.check(len(chosen)==4,'four-tail cover count')
            output.append(tuple(sorted(index[t] for t in chosen)))
            return
        for tail in incident[min(left)]:
            if tail<=left:
                visit(left-tail,chosen+[tail])
    # Every four-tail set has one unique unused triple. For that triple,
    # smallest-point recursion generates the remaining partition once.
    for unused in combinations(range(15),3):
        visit(frozenset(range(15))-set(unused),[])
    v.check(len(output)==len(set(output)),'duplicate literal four-tail cover')
    return triples,sorted(output),nodes


def replay(work,executable,case,start=0,size=None):
    v.check(type(case) is int and 0<=case<46,'case request')
    begun=time.monotonic()
    star,rows,cols,fixed=inputs()[case]
    ts,cs,cover_nodes=covers(fixed)
    v.check(type(start) is int and 0<=start<len(cs),'chunk start')
    v.check(size is None or type(size) is int and size>0,'chunk size')
    finish=len(cs) if size is None else min(len(cs),start+size)
    yw,ya=v.base(rows,fixed,15);zw,za=v.base(cols,fixed,16)
    primary_header=json.loads((work/f'header-{case}.json').read_text())
    header={'star':star,'triples':[v.bits(t) for t in ts],'covers':cs,
            'y_words':[v.bits(w) for w in yw],'y_adjacent':[v.bits(a) for a in ya],
            'z_words':[v.bits(w) for w in zw],'z_adjacent':[v.bits(a) for a in za]}
    v.compare(header,{k:value for k,value in primary_header.items() if k!='cover_nodes'},'literal header')
    yt=[{i for i,w in enumerate(yw) if len(w&(t|{15,16}))<=2} for t in ts]
    zt=[{i for i,w in enumerate(zw) if len(w&(t|{15,16}))<=2} for t in ts]
    counts=Counter();joints=[];native_nodes=0;max_query_nodes=0
    y_profile=Counter()
    with Native(executable,[ya,za]) as engine,(work/f'carrier-{case}.jsonl').open() as stream:
        for unused in range(start):
            v.check(bool(stream.readline()),'truncated skipped carrier prefix')
        for ci in range(start,finish):
            cover=cs[ci]
            if time.monotonic()-begun>60:
                raise RuntimeError('INCOMPLETE independent whole-case guard')
            extra=[ts[i]|{15,16} for i in cover]
            ys=sorted(set.intersection(*(yt[i] for i in cover)))
            yc,nodes=engine.query(0,ys,target=11)
            native_nodes+=nodes;max_query_nodes=max(max_query_nodes,nodes)
            counts.update(covers=1,y_eleven=len(yc))
            record={'cover':ci,'y_candidates':ys,'y_eleven':yc,'z_cases':[]}
            for q in yc:
                private_y=[yw[i] for i in q]
                prefix=fixed+extra+private_y
                v.packing(prefix,34)
                y_words=[w for w in prefix if 15 in w]
                v.check(len(y_words)==20,'literal finished y20 degree')
                rho=[sum(i in w for w in y_words) for i in range(18) if i!=15]
                v.check(max(rho)<=5 and sum(rho)==80,'literal y20 pair capacities')
                y_profile[tuple(sorted(5-r for r in rho if r<5))]+=1
                zs=sorted(i for i in set.intersection(*(zt[i] for i in cover))
                          if all(len(zw[i]&a)<=2 for a in private_y))
                zc,nodes=engine.query(1,zs,target=11)
                native_nodes+=nodes;max_query_nodes=max(max_query_nodes,nodes)
                counts.update(z_eleven=len(zc))
                record['z_cases'].append({'y':q,'z_candidates':zs,'z_eleven':zc})
                for r in zc:
                    words=prefix+[zw[i] for i in r]
                    v.packing(words,45)
                    v.check([sum(c in w for w in words) for c in (17,15,16)]==[19,20,20],
                            'literal finished degrees')
                    v.check([sum({a,b}<=w for w in words) for a,b in ((17,15),(17,16),(15,16))]==[5,5,4],
                            'literal center pair counts')
                    v.check(not any({15,16,17}<=w for w in words),'literal uncovered triple')
                    blocks=sorted(v.bits(w) for w in words)
                    joints.append({'case':case,'cover':ci,'y':q,'z':r,
                                   'blocks':blocks,'core_sha256':v.sha(blocks)})
            line=stream.readline()
            v.check(bool(line),'truncated primary carrier')
            v.compare(record,json.loads(line),'entrywise four-tail selection and complete clique lists')
        if finish==len(cs):
            v.check(not stream.readline(),'extra primary carrier')
    all_joints=json.loads((work/f'joints-{case}.json').read_text())
    v.compare(joints,[c for c in all_joints if start<=c['cover']<finish],'literal joint cores')
    expected=json.loads((work/f'case-{case}.json').read_text())
    v.check(expected['case']==case and expected['status']=='COMPLETE_PRODUCER_ONLY','primary completion status')
    if start==0 and finish==len(cs):
        for key,count in counts.items():
            v.check(expected['counts'][key]==count,'complete count mismatch')
    for key,path in [('header_sha256',work/f'header-{case}.json'),
                     ('carrier_sha256',work/f'carrier-{case}.jsonl'),
                     ('joints_sha256',work/f'joints-{case}.json')]:
        v.check(hashlib.sha256(path.read_bytes()).hexdigest()==expected[key],'complete byte binding')
    result={'case':case,'status':'COMPLETE_ENTRYWISE_CHUNK','start':start,'finish':finish,
            'total_covers':len(cs),'counts':dict(counts),'joint_count':len(joints),
            'literal_cover_nodes':cover_nodes,'native_nodes':native_nodes,'max_query_nodes':max_query_nodes,
            'y_profiles':{','.join(map(str,k)):n for k,n in sorted(y_profile.items())},
            'seconds':time.monotonic()-begun,'header_sha256':expected['header_sha256'],
            'carrier_sha256':expected['carrier_sha256'],'joints_sha256':expected['joints_sha256']}
    (work/f'verified-{case}-{start}-{finish}.json').write_bytes(v.encode(result))
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--case',type=int,required=True)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--executable',type=Path,required=True)
    ap.add_argument('--start',type=int,default=0)
    ap.add_argument('--size',type=int)
    args=ap.parse_args()
    replay(args.work,args.executable,args.case,args.start,args.size)
