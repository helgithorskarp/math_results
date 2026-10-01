"""Complete marked m=1 three-star interface, with resumable case boundaries."""
import argparse
from collections import Counter
import importlib.util
from itertools import combinations, product
import json
import hashlib
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BACKEND = ROOT/'three_nineteen_zero_triples'/'produce.py'
if hashlib.sha256(BACKEND.read_bytes()).hexdigest() != '3e0611eaf25d34bc88d476880c71d548aadff6b02cafd0481ecfafaa19d8b195':
    raise ValueError('prior producer helper changed')
spec = importlib.util.spec_from_file_location('old_producer', ROOT/'three_nineteen_zero_triples'/'produce.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


def inputs():
    import hashlib
    raw = p.MANIFEST.read_bytes()
    p.require(hashlib.sha256(raw).hexdigest() == p.MANIFEST_SHA, 'census input changed')
    manifest = json.loads(raw)
    output = []
    for model_id, model in enumerate(manifest['models']):
        holes = set()
        offset = 0
        for length in model['cycle_half_lengths']:
            holes.update((offset+i, offset+j) for i in range(length)
                         for j in (i, (i+1) % length))
            offset += length
        cells = sorted(set(product(range(5), repeat=2))-holes)
        rows = [sum(1 << i for i, (r,c) in enumerate(cells) if r == j) for j in range(5)]
        cols = [sum(1 << i for i, (r,c) in enumerate(cells) if c == j) for j in range(5)]
        quads = [sum(1 << i for i in q) for q in combinations(range(15),4)
                 if all(sum(bool((1 << i) & t) for i in q) <= 1 for t in rows+cols)]
        p.require(len(quads) == model['candidate_count'], 'quad universe')
        for marked_id, rep in enumerate(model['marked_classes']):
            if rep['low_low_pairs'] != 1:
                continue
            private = [quads[i] for i in rep['clique']]
            fixed = [t | (1 << 15) | (1 << 17) for t in rows]
            fixed += [t | (1 << 16) | (1 << 17) for t in cols]
            fixed += [t | (1 << 17) for t in private]
            p.check_packing(fixed,19)
            p.require(p.link_stats(fixed,17)['m'] == 1, 'initial m')
            output.append({'model':model_id, 'marked_id':marked_id, 'cells':cells,
                           'clique':rep['clique'],'row':rows,'col':cols,
                           'private':private,'fixed':sorted(fixed)})
    p.require(len(output) == 40, 'forty marked m=1 types')
    return output


def run(k, work):
    start = time.monotonic()
    star = inputs()[k]
    work.mkdir(parents=True,exist_ok=True)
    triples, partitions, cover_nodes = p.third_partitions(star)
    yw, ya = p.base_graph(star,15)
    zw, za = p.base_graph(star,16)
    header = {'star':star,'triples':triples,'partitions':partitions,
              'y_words':yw,'y_adjacent':ya,'z_words':zw,'z_adjacent':za}
    (work/f'header-{k}.json').write_bytes(p.canonical(header))
    counts = Counter()
    joints = []
    with (work/f'carrier-{k}.jsonl').open('wb') as stream:
        for pi, part in enumerate(partitions):
            if time.monotonic()-start > 60:
                raise RuntimeError('INCOMPLETE per-case guard; no negative conclusion')
            extra = [t | (1 << 15) | (1 << 16) for t in part]
            ys = p.selected(yw,extra)
            yc, yn = p.cliques(ya,sum(1 << i for i in ys))
            y1 = [q for q in yc if p.link_stats(
                [w for w in star['fixed'] if w & (1 << 15)]+extra+[yw[i] for i in q],15)['m'] == 1]
            record = {'partition':part,'y_candidates':ys,'y_nine':yc,'y_one':y1,'z_cases':[]}
            counts.update(partitions=1,y_nine=len(yc),y_one=len(y1),y_nodes=yn)
            for q in y1:
                private_y = [yw[i] for i in q]
                zs = p.selected(zw,extra+private_y)
                zc, zn = p.cliques(za,sum(1 << i for i in zs))
                z1 = [r for r in zc if p.link_stats(
                    [w for w in star['fixed'] if w & (1 << 16)]+extra+[zw[i] for i in r],16)['m'] == 1]
                record['z_cases'].append({'y':q,'z_candidates':zs,'z_nine':zc,'z_one':z1})
                counts.update(z_nine=len(zc),z_one=len(z1),z_nodes=zn)
                for r in z1:
                    words = sorted(star['fixed']+extra+private_y+[zw[i] for i in r])
                    p.check_packing(words,42)
                    profiles = [p.link_stats(words,c) for c in p.CENTERS]
                    p.require(all(s['m'] == 1 for s in profiles),'all m=1 branch')
                    joints.append({'case':k,'partition_index':pi,'y':q,'z':r,
                                   'profiles':profiles,'blocks':words,'core_sha256':p.digest(words)})
            stream.write(p.canonical(record))
    (work/f'joints-{k}.json').write_bytes(p.canonical(joints))
    summary = {'case':k,'model':star['model'],'marked_id':star['marked_id'],
               'status':'COMPLETE_PRODUCER_ONLY','counts':dict(counts),'triples':len(triples),
               'cover_nodes':cover_nodes,'joint_count':len(joints),'seconds':time.monotonic()-start,
               'header_sha256':p.digest(header),'joints_sha256':p.digest(joints),
               'carrier_sha256':__import__('hashlib').sha256((work/f'carrier-{k}.jsonl').read_bytes()).hexdigest()}
    (work/f'case-{k}.json').write_bytes(p.canonical(summary))
    print(json.dumps(summary),flush=True)
    return summary


def summarize(work):
    cases=[]
    for k in range(40):
        case=json.loads((work/f'case-{k}.json').read_text())
        p.require(case['case']==k and case['status']=='COMPLETE_PRODUCER_ONLY','incomplete case checkpoint')
        case={key:value for key,value in case.items() if key not in ('seconds','status')}
        for stem,field in [('header','header_sha256'),('joints','joints_sha256')]:
            p.require(p.digest(json.loads((work/f'{stem}-{k}.json').read_text()))==case[field],
                      'resumable carrier checksum')
        p.require(hashlib.sha256((work/f'carrier-{k}.jsonl').read_bytes()).hexdigest()==case['carrier_sha256'],
                  'resumable line carrier checksum')
        cases.append(case)
    summary={'format':1,'status':'COMPLETE','classification_sha256':p.MANIFEST_SHA,
             'cases':cases,'core_count':sum(c['joint_count'] for c in cases)}
    p.require(summary['core_count']==1501,'complete m=1 core count')
    (work/'summary.json').write_bytes(p.canonical(summary))
    print(json.dumps({'status':'COMPLETE','cases':40,'cores':1501,'summary_sha256':p.digest(summary)}),flush=True)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case',type=int)
    parser.add_argument('--summarize',action='store_true')
    parser.add_argument('--work',type=Path,required=True)
    args = parser.parse_args()
    if args.summarize:
        summarize(args.work)
    elif args.case is not None:
        p.require(0<=args.case<40,'case domain')
        run(args.case,args.work)
    else:
        for k in range(40):run(k,args.work)
        summarize(args.work)
