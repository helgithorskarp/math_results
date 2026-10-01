"""Complete three-star interface using integer masks and colored cliques."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
MANIFEST = HERE.parent/'nineteen_star_classification'/'expected.json'
MANIFEST_SHA = '83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca'
CENTERS = (15, 16, 17)
ALL_OLD = (1 << 15)-1


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def load_stars():
    raw = MANIFEST.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==MANIFEST_SHA, 'classification input changed')
    data = json.loads(raw)
    cells = sorted(set(product(range(5), repeat=2))-
                   {(a+i, a+j) for a,s in [(0,2),(2,3)]
                    for i in range(s) for j in [i,(i+1)%s]})
    row = [sum(1 << i for i,(r,c) in enumerate(cells) if r==j) for j in range(5)]
    col = [sum(1 << i for i,(r,c) in enumerate(cells) if c==j) for j in range(5)]
    quads = []
    for q in combinations(range(15),4):
        b = sum(1 << i for i in q)
        if all((b&t).bit_count()<=1 for t in row+col):
            quads.append(b)
    require(len(quads)==96 and len(cells)==15, 'anchor reconstruction')
    require(all(t['low_low_pairs']==1 for t in data['models'][0]['marked_classes']),
            'unexpected first-model double leave')
    reps = [t for t in data['models'][1]['marked_classes'] if t['low_low_pairs']==2]
    require(len(reps)==6, 'marked double-leave coverage')
    output=[]
    for t in reps:
        private = [quads[i] for i in t['clique']]
        fixed = [b | (1 << 15) | (1 << 17) for b in row]
        fixed += [b | (1 << 16) | (1 << 17) for b in col]
        fixed += [b | (1 << 17) for b in private]
        check_packing(fixed,19)
        require(link_stats(fixed,17)['m']==2, 'input does not have two low-low leaves')
        output.append({'clique':t['clique'],'row':row,'col':col,
                       'private':private,'fixed':sorted(fixed)})
    return cells, output


def check_packing(words, size):
    require(len(words)==len(set(words))==size, 'packing cardinality')
    require(all(type(w) is int and 0<=w<(1 << 18) and w.bit_count()==5 for w in words),
            'invalid five-subset')
    require(all((a&b).bit_count()<=2 for a,b in combinations(words,2)),
            'decoded packing repeats a triple')


def link_stats(words, center):
    links = [w ^ (1 << center) for w in words if w & (1 << center)]
    require(len(links)==19, 'center degree must be nineteen')
    rho = {i:sum(bool(w & (1 << i)) for w in links) for i in range(18) if i!=center}
    require(max(rho.values())<=5, 'link point cap')
    saturated = [i for i,r in rho.items() if r==5]
    m = sum(not any(w & (1 << i) and w & (1 << j) for w in links)
            for i,j in combinations(saturated,2))
    return {'m':m, 'rho':[rho[i] for i in sorted(rho)],
            'positive_deficits':sorted(5-r for r in rho.values() if r<5)}


def third_partitions(star):
    triples=[]
    for q in combinations(range(15),3):
        t=sum(1 << i for i in q)
        word=t | (1 << 15) | (1 << 16)
        if all((word&w).bit_count()<=2 for w in star['fixed']):
            triples.append(t)
    incident=[[t for t in triples if t & (1 << i)] for i in range(15)]
    output=[]
    nodes=0
    start=time.monotonic()
    def visit(left,chosen):
        nonlocal nodes
        nodes+=1
        if nodes>2000000 or time.monotonic()-start>20:
            raise RuntimeError('INCOMPLETE third-partition guard')
        if not left:
            output.append(tuple(sorted(chosen)))
            return
        point=min((i for i in range(15) if left & (1 << i)),
                  key=lambda i:sum(t & left==t for t in incident[i]))
        for t in incident[point]:
            if t & left==t:
                visit(left ^ t,chosen+[t])
    visit(ALL_OLD,[])
    require(len(output)==len(set(output)), 'duplicate third partition')
    return triples,sorted(output),nodes


def base_graph(star,center):
    words=[]
    for q in combinations(range(15),4):
        w=sum(1 << i for i in q) | (1 << center)
        if all((w&a).bit_count()<=2 for a in star['fixed']):
            words.append(w)
    adjacent=[sum(1 << j for j,b in enumerate(words) if i!=j and (a&b).bit_count()<=2)
              for i,a in enumerate(words)]
    return words,adjacent


def cliques(adjacent,available,target=9,node_cap=2000000,seconds=20):
    require(type(target) is int and target>0,'clique target domain')
    require(type(node_cap) is int and 0<node_cap<=2000000,'clique node guard domain')
    require(0<seconds<=20,'clique time guard domain')
    output=[]
    nodes=0
    start=time.monotonic()
    def visit(left,chosen):
        nonlocal nodes
        nodes+=1
        if nodes>node_cap or time.monotonic()-start>seconds:
            raise RuntimeError('INCOMPLETE clique guard')
        need=target-len(chosen)
        if need==0:
            output.append(tuple(sorted(chosen)))
            return
        if left.bit_count()<need:
            return
        order,bounds=[],[]
        uncolored=left
        color=0
        while uncolored:
            color+=1
            independent=uncolored
            while independent:
                bit=independent & -independent
                v=bit.bit_length()-1
                order.append(v);bounds.append(color)
                uncolored ^= bit
                independent &= ~bit & ~adjacent[v]
        for k in range(len(order)-1,-1,-1):
            if bounds[k]<need:
                return
            v=order[k]
            visit(left & adjacent[v],chosen+[v])
            left &= ~(1 << v)
    visit(available,[])
    require(len(output)==len(set(output)), 'duplicate nine-clique')
    return sorted(output),nodes


def selected(words,fixed):
    return [i for i,w in enumerate(words) if all((w&a).bit_count()<=2 for a in fixed)]


def run(work):
    work.mkdir(parents=True,exist_ok=True)
    cells,stars=load_stars()
    summary={'format':1,'classification_sha256':MANIFEST_SHA,'cells':cells,
             'cases':[]}
    for k,star in enumerate(stars):
        start=time.monotonic()
        triples,partitions,cover_nodes=third_partitions(star)
        yw,ya=base_graph(star,15); zw,za=base_graph(star,16)
        header={'star':star,'triples':triples,'partitions':partitions,
                'y_words':yw,'y_adjacent':ya,'z_words':zw,'z_adjacent':za}
        (work/f'header-{k}.json').write_bytes(canonical(header))
        stats=Counter()
        joints=[]
        with (work/f'carrier-{k}.jsonl').open('wb') as stream:
            for p_index,p in enumerate(partitions):
                if time.monotonic()-start>60:
                    raise RuntimeError('INCOMPLETE whole-star guard')
                extra=[t | (1 << 15) | (1 << 16) for t in p]
                ys=selected(yw,extra)
                yc,yn=cliques(ya,sum(1 << i for i in ys))
                y2=[q for q in yc if link_stats(
                    [w for w in star['fixed'] if w & (1 << 15)]+extra+[yw[i] for i in q],15)['m']==2]
                record={'partition':p,'y_candidates':ys,'y_nine':yc,'y_two':y2,'z_cases':[]}
                stats.update({'partitions':1,'y_nine':len(yc),'y_two':len(y2),'y_nodes':yn})
                # The anchor pair is unordered in the imported census. Either
                # neighbor can be the second m=2 center, so cover every y star.
                for q in yc:
                    private_y=[yw[i] for i in q]
                    zs=selected(zw,extra+private_y)
                    zc,zn=cliques(za,sum(1 << i for i in zs))
                    record['z_cases'].append({'y':q,'z_candidates':zs,'z_nine':zc})
                    stats.update({'z_nine':len(zc),'z_nodes':zn})
                    for r in zc:
                        words=sorted(star['fixed']+extra+private_y+[zw[i] for i in r])
                        check_packing(words,42)
                        profiles=[link_stats(words,c) for c in CENTERS]
                        require(all(s['m'] in (1,2) for s in profiles), 'three-star m census')
                        joint={'case':k,'partition_index':p_index,'y':q,'z':r,
                               'profiles':profiles,
                               'blocks':words,'core_sha256':digest(words)}
                        joints.append(joint)
                stream.write(canonical(record))
        (work/f'joints-{k}.json').write_bytes(canonical(joints))
        case={'clique':star['clique'],'triple_count':len(triples),
              'partition_count':len(partitions),'cover_nodes':cover_nodes,
              'y_base':len(yw),'z_base':len(zw),'counts':dict(stats),
              'joint_count':len(joints),'m_census':dict(sorted(Counter(
                  ','.join(str(p['m']) for p in j['profiles']) for j in joints).items())),
              'header_sha256':digest(header),
              'carrier_sha256':hashlib.sha256((work/f'carrier-{k}.jsonl').read_bytes()).hexdigest(),
              'joints_sha256':digest(joints)}
        summary['cases'].append(case)
        print(json.dumps({'case':k,'status':'COMPLETE','seconds':time.monotonic()-start,
                          'partitions':len(partitions),'counts':dict(stats),
                          'joint_count':len(joints),'m_census':case['m_census']}),flush=True)
    summary['status']='COMPLETE'
    summary['core_count']=sum(c['joint_count'] for c in summary['cases'])
    (work/'summary.json').write_bytes(canonical(summary))
    print(json.dumps({'status':'COMPLETE','cases':6,'cores':summary['core_count'],
                      'summary_sha256':digest(summary)}),flush=True)
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args()
    run(args.work)
