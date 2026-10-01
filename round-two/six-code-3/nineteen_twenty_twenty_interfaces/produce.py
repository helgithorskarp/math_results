"""Exact bounded exploration: uncovered 19/20/20 centers, pairs 5,5,4.

Incomplete searches give no exclusion. Candidate universes and every
completed eleven-clique query are recorded for separate entrywise replay. The imported nineteen-star census is a premise.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
from native import Native
BACKEND = ROOT/'three_nineteen_zero_triples'/'produce.py'
if hashlib.sha256(BACKEND.read_bytes()).hexdigest() != '3e0611eaf25d34bc88d476880c71d548aadff6b02cafd0481ecfafaa19d8b195':
    raise ValueError('imported helper changed')
spec = importlib.util.spec_from_file_location('prior_mask',BACKEND)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


def inputs():
    raw = p.MANIFEST.read_bytes()
    p.require(hashlib.sha256(raw).hexdigest() == p.MANIFEST_SHA,'census changed')
    output = []
    for mid, model in enumerate(json.loads(raw)['models']):
        holes = set()
        offset = 0
        for length in model['cycle_half_lengths']:
            holes.update((offset+i,offset+j) for i in range(length)
                         for j in (i,(i+1)%length))
            offset += length
        cells = sorted(set(product(range(5),repeat=2))-holes)
        row = [sum(1 << i for i,(r,c) in enumerate(cells) if r == j) for j in range(5)]
        col = [sum(1 << i for i,(r,c) in enumerate(cells) if c == j) for j in range(5)]
        quads = [sum(1 << i for i in q) for q in combinations(range(15),4)
                 if all(sum(bool((1 << i)&t) for i in q) <= 1 for t in row+col)]
        p.require(len(quads) == model['candidate_count'],'quad universe')
        for marked, rep in enumerate(model['marked_classes']):
            private = [quads[i] for i in rep['clique']]
            fixed = [t|(1 << 15)|(1 << 17) for t in row]
            fixed += [t|(1 << 16)|(1 << 17) for t in col]
            fixed += [t|(1 << 17) for t in private]
            p.check_packing(fixed,19)
            p.require(p.link_stats(fixed,17)['m'] == rep['low_low_pairs'],'m decoding')
            output.append({'model':mid,'marked':marked,'m':rep['low_low_pairs'],
                           'cells':cells,'row':row,'col':col,'private':private,
                           'clique':rep['clique'],'fixed':sorted(fixed)})
    p.require(len(output) == 46,'all marked star types')
    return output


def prepare(case, work):
    star = inputs()[case]
    triples = [sum(1 << i for i in q) for q in combinations(range(15),3)
               if all(((sum(1 << i for i in q)|(1 << 15)|(1 << 16))&w).bit_count() <= 2
                      for w in star['fixed'])]
    adjacent = [sum(1 << j for j,b in enumerate(triples) if not a&b)
                for a in triples]
    covers, nodes = p.cliques(adjacent,(1 << len(triples))-1,target=4)
    yw,ya = p.base_graph(star,15)
    zw,za = p.base_graph(star,16)
    header = {'star':star,'triples':triples,'covers':covers,'cover_nodes':nodes,
              'y_words':yw,'y_adjacent':ya,'z_words':zw,'z_adjacent':za}
    path = work/f'header-{case}.json'
    if path.exists():
        p.require(path.read_bytes() == p.canonical(header),'header replay disagreement')
    else:
        path.write_bytes(p.canonical(header))
    return header


def check_joint(words):
    p.check_packing(words,45)
    p.require([sum(bool(w&(1 << c)) for w in words) for c in (17,15,16)] == [19,20,20],
              'completed center degrees')
    p.require([sum(w&t == t for w in words) for t in ((1 << 17)|(1 << 15),
              (1 << 17)|(1 << 16),(1 << 15)|(1 << 16))] == [5,5,4], 'center pair counts')
    p.require(not any(w&sum(1 << c for c in (15,16,17)) == sum(1 << c for c in (15,16,17))
                      for w in words),'covered center triple')



def run(case, work, executable):
    begun=time.monotonic()
    work.mkdir(parents=True,exist_ok=True)
    header=prepare(case,work)
    star=header['star']
    yw,ya,zw,za=(header[k] for k in ('y_words','y_adjacent','z_words','z_adjacent'))
    graphs=[[{i for i in range(len(a)) if row&(1 << i)} for row in a] for a in (ya,za)]
    y_tail=[];z_tail=[]
    for tail in header['triples']:
        word=tail|(1 << 15)|(1 << 16)
        y_tail.append(sum(1 << i for i in p.selected(yw,[word])))
        z_tail.append(sum(1 << i for i in p.selected(zw,[word])))
    counts=Counter();joints=[]
    with Native(executable,graphs) as engine, (work/f'carrier-{case}.jsonl').open('wb') as stream:
        for ci,cover in enumerate(header['covers']):
            if time.monotonic()-begun>60:
                raise RuntimeError('INCOMPLETE whole-case guard; no exclusion')
            extra=[header['triples'][i]|(1 << 15)|(1 << 16) for i in cover]
            ym=(1 << len(yw))-1;zm=(1 << len(zw))-1
            for i in cover:
                ym &= y_tail[i];zm &= z_tail[i]
            ys=[i for i in range(len(yw)) if ym&(1 << i)]
            yc,yn=engine.query(0,ys,target=11)
            record={'cover':ci,'y_candidates':ys,'y_eleven':yc,'z_cases':[]}
            counts.update(covers=1,y_eleven=len(yc),y_nodes=yn)
            for q in yc:
                private_y=[yw[i] for i in q]
                zs=[i for i in range(len(zw)) if zm&(1 << i)
                    and all((zw[i]&a).bit_count()<=2 for a in private_y)]
                zc,zn=engine.query(1,zs,target=11)
                record['z_cases'].append({'y':q,'z_candidates':zs,'z_eleven':zc})
                counts.update(z_eleven=len(zc),z_nodes=zn)
                for r in zc:
                    words=sorted(star['fixed']+extra+private_y+[zw[i] for i in r])
                    check_joint(words)
                    joints.append({'case':case,'cover':ci,'y':q,'z':r,
                                   'blocks':words,'core_sha256':p.digest(words)})
            stream.write(p.canonical(record))
    (work/f'joints-{case}.json').write_bytes(p.canonical(joints))
    result={'case':case,'model':star['model'],'marked':star['marked'],'m':star['m'],
            'status':'COMPLETE_PRODUCER_ONLY','triples':len(header['triples']),
            'covers':len(header['covers']),'cover_nodes':header['cover_nodes'],
            'counts':dict(counts),'joint_count':len(joints),'seconds':time.monotonic()-begun,
            'header_sha256':p.digest(header),'joints_sha256':p.digest(joints),
            'carrier_sha256':hashlib.sha256((work/f'carrier-{case}.jsonl').read_bytes()).hexdigest()}
    (work/f'case-{case}.json').write_bytes(p.canonical(result))
    print(json.dumps(result),flush=True)
    return result


def summarize(work):
    cases=[]
    for k in range(46):
        case=json.loads((work/f'case-{k}.json').read_text())
        p.require(case['case']==k and case['status']=='COMPLETE_PRODUCER_ONLY','incomplete case')
        p.require(hashlib.sha256((work/f'header-{k}.json').read_bytes()).hexdigest()==case['header_sha256'],
                  'header checksum')
        p.require(hashlib.sha256((work/f'carrier-{k}.jsonl').read_bytes()).hexdigest()==case['carrier_sha256'],
                  'carrier checksum')
        p.require(hashlib.sha256((work/f'joints-{k}.json').read_bytes()).hexdigest()==case['joints_sha256'],
                  'joint checksum')
        cases.append({key:value for key,value in case.items() if key not in ('status','seconds')})
    result={'format':1,'status':'COMPLETE','classification_sha256':p.MANIFEST_SHA,
            'cases':cases,'totals':dict(sum((Counter(c['counts']) for c in cases),Counter())),
            'joint_count':sum(c['joint_count'] for c in cases)}
    (work/'summary.json').write_bytes(p.canonical(result))
    print(json.dumps({'status':'COMPLETE','cases':46,'joint_count':result['joint_count'],
                      'totals':result['totals'],'summary_sha256':p.digest(result)}),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--case',type=int)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--executable',type=Path)
    ap.add_argument('--summary',action='store_true')
    args=ap.parse_args()
    if args.summary:
        summarize(args.work)
    else:
        p.require(type(args.case) is int and 0<=args.case<46 and args.executable is not None,'case request')
        run(args.case,args.work,args.executable)
