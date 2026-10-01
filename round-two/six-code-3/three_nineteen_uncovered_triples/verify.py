"""Literal point-set reconstruction and native maximal-clique replay."""
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
            if rep['low_low_pairs']!=1:
                continue
            private=[frozenset(matchings[i]) for i in rep['clique']]
            fixed=[r|{15,17} for r in rows]+[c|{16,17} for c in cols]+[q|{17} for q in private]
            v.packing(fixed,19)
            v.check(v.stats(fixed,17)['m']==1,'initial marked leave count')
            star={'model':model_id,'marked_id':marked_id,'cells':cells,'clique':rep['clique'],
                  'row':[v.bits(r) for r in rows],'col':[v.bits(c) for c in cols],
                  'private':[v.bits(q) for q in private],'fixed':sorted(v.bits(w) for w in fixed)}
            output.append((star,rows,cols,fixed))
    v.check(len(output)==40,'complete forty marked inputs')
    return output


def replay(work,executable,case):
    v.check(type(case) is int and 0<=case<40,'case request')
    start=time.monotonic()
    star,rows,cols,fixed=inputs()[case]
    ts,ps=v.partitions(rows,cols,fixed)
    yw,ya=v.base(rows,fixed,15);zw,za=v.base(cols,fixed,16)
    header={'star':star,'triples':ts,'partitions':ps,
            'y_words':[v.bits(w) for w in yw],'y_adjacent':[v.bits(a) for a in ya],
            'z_words':[v.bits(w) for w in zw],'z_adjacent':[v.bits(a) for a in za]}
    v.compare(header,json.loads((work/f'header-{case}.json').read_text()),'whole independent header')
    counts=Counter();joints=[];native_nodes=0
    with Native(executable,[ya,za]) as engine, (work/f'carrier-{case}.jsonl').open() as stream:
        for pi,part in enumerate(ps):
            if time.monotonic()-start>60:
                raise RuntimeError('INCOMPLETE literal per-case guard')
            extra=[v.points(t)|{15,16} for t in part]
            ys=[i for i,w in enumerate(yw) if all(len(w&t)<=2 for t in extra)]
            yc,nodes=engine.query(0,ys);native_nodes+=nodes
            y1=[q for q in yc if v.stats([w for w in fixed if 15 in w]+extra+[yw[i] for i in q],15)['m']==1]
            record={'partition':part,'y_candidates':ys,'y_nine':yc,'y_one':y1,'z_cases':[]}
            counts.update(partitions=1,y_nine=len(yc),y_one=len(y1))
            for q in y1:
                private_y=[yw[i] for i in q]
                zs=[i for i,w in enumerate(zw) if all(len(w&t)<=2 for t in extra+private_y)]
                zc,nodes=engine.query(1,zs);native_nodes+=nodes
                z1=[r for r in zc if v.stats([w for w in fixed if 16 in w]+extra+[zw[i] for i in r],16)['m']==1]
                record['z_cases'].append({'y':q,'z_candidates':zs,'z_nine':zc,'z_one':z1})
                counts.update(z_nine=len(zc),z_one=len(z1))
                for r in z1:
                    words=fixed+extra+private_y+[zw[i] for i in r]
                    v.packing(words,42)
                    profiles=[v.stats(words,c) for c in (15,16,17)]
                    v.check(all(p['m']==1 for p in profiles),'literal three-center m=1 domain')
                    blocks=sorted(v.bits(w) for w in words)
                    joints.append({'case':case,'partition_index':pi,'y':q,'z':r,
                                   'profiles':profiles,'blocks':blocks,'core_sha256':v.sha(blocks)})
            line=stream.readline()
            v.check(bool(line),'truncated three-star carrier')
            v.compare(record,json.loads(line),'entrywise partitions/graphs/cliques')
        v.check(not stream.readline(),'extra three-star carrier entry')
    v.compare(joints,json.loads((work/f'joints-{case}.json').read_text()),'whole literal joint carrier')
    summary=json.loads((work/'summary.json').read_text())
    v.check(summary['status']=='COMPLETE' and len(summary['cases'])==40,'primary coverage status')
    expected=summary['cases'][case]
    v.check(expected['case']==case and expected['joint_count']==len(joints),'case/core totals')
    for label,count in counts.items():
        v.check(expected['counts'][label]==count,'finite census mismatch')
    v.check(v.sha(header)==expected['header_sha256'] and v.sha(joints)==expected['joints_sha256'],
            'independent carrier binding')
    v.check(hashlib.sha256((work/f'carrier-{case}.jsonl').read_bytes()).hexdigest()==expected['carrier_sha256'],
            'independent complete carrier binding')
    result={'status':'COMPLETE_ENTRYWISE','case':case,'counts':dict(counts),'cores':len(joints),
            'native_nodes':native_nodes,'seconds':time.monotonic()-start,
            'header_sha256':v.sha(header),'joints_sha256':v.sha(joints)}
    (work/f'verified-case-{case}.json').write_bytes(v.encode(result))
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--executable',type=Path,required=True)
    parser.add_argument('--case',type=int,required=True)
    args=parser.parse_args()
    replay(args.work,args.executable,args.case)
