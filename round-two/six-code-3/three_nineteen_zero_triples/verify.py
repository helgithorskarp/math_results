"""Producer-free point-set reconstruction and maximal-clique carrier replay."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
MANIFEST_SHA='83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca'
CENTERS=(15,16,17)


def check(ok,message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()


def sha(value):
    return hashlib.sha256(encode(value)).hexdigest()


def bits(points):
    return sum(1 << p for p in points)


def points(word):
    check(type(word) is int and 0<=word<(1 << 18),'word mask domain')
    return frozenset(i for i in range(18) if word & (1 << i))


def packing(words,size):
    check(len(words)==len(set(words))==size,'literal packing cardinality')
    check(all(len(w)==5 and all(type(i) is int and 0<=i<18 for i in w) for w in words),
          'literal five-subset domain')
    triples=[frozenset(t) for w in words for t in combinations(sorted(w),3)]
    check(len(triples)==len(set(triples))==10*size,'literal repeated triple')


def stats(words,center):
    quads=[w-{center} for w in words if center in w]
    check(len(quads)==19 and all(len(w)==4 for w in quads),'literal center degree')
    pairsets=[frozenset(p) for q in quads for p in combinations(sorted(q),2)]
    check(len(pairsets)==len(set(pairsets))==114,'literal link pair repeat')
    rho=[sum(i in q for q in quads) for i in range(18) if i!=center]
    check(max(rho)<=5,'literal pair cap')
    labels=[i for i in range(18) if i!=center]
    low={i for i,r in zip(labels,rho) if r==5}
    m=len({frozenset(p) for p in combinations(sorted(low),2)}-set(pairsets))
    return {'m':m,'rho':rho,'positive_deficits':sorted(5-r for r in rho if r<5)}


def inputs():
    raw=(HERE.parent/'nineteen_star_classification'/'expected.json').read_bytes()
    check(hashlib.sha256(raw).hexdigest()==MANIFEST_SHA,'prior census checksum')
    manifest=json.loads(raw)
    holes=set()
    offset=0
    for length in (2,3):
        cycle=list(range(offset,offset+length))
        for a,b in zip(cycle,cycle[1:]+cycle[:1]):
            holes.add((a,a));holes.add((a,b))
        offset+=length
    cells=sorted((r,c) for r in range(5) for c in range(5) if (r,c) not in holes)
    rows=[frozenset(i for i,(r,c) in enumerate(cells) if r==j) for j in range(5)]
    cols=[frozenset(i for i,(r,c) in enumerate(cells) if c==j) for j in range(5)]
    # Independent candidate decoder: select four rows and a point from each.
    matching=[]
    for chosen in combinations(range(5),4):
        for q in product(*(sorted(rows[j]) for j in chosen)):
            if len({cells[i][1] for i in q})==4:
                matching.append(tuple(sorted(q)))
    matching=sorted(matching)
    check(len(matching)==len(set(matching))==96,'legacy matching decoder')
    check(not any(t['low_low_pairs']==2 for t in manifest['models'][0]['marked_classes']),
          'first anchor form coverage')
    reps=[t for t in manifest['models'][1]['marked_classes'] if t['low_low_pairs']==2]
    check(len(reps)==6,'six marked input classes')
    output=[]
    for rep in reps:
        private=[frozenset(matching[i]) for i in rep['clique']]
        fixed=[r|{15,17} for r in rows]+[c|{16,17} for c in cols]+[q|{17} for q in private]
        packing(fixed,19)
        check(stats(fixed,17)['m']==2,'marked input m')
        star={'clique':rep['clique'],'row':[bits(r) for r in rows],
              'col':[bits(c) for c in cols],'private':[bits(q) for q in private],
              'fixed':sorted(bits(w) for w in fixed)}
        output.append((star,rows,cols,fixed))
    return cells,output


def partitions(rows,cols,fixed):
    triples=[]
    for chosen in combinations(range(5),3):
        for q in product(*(sorted(rows[j]) for j in chosen)):
            t=frozenset(q)
            if all(len(t&c)<=1 for c in cols) and all(len((t|{15,16})&w)<=2 for w in fixed):
                triples.append(t)
    triples=sorted(set(triples),key=lambda t:tuple(sorted(t)))
    # Direct global-word check audits the row/column reduction as well.
    literal=[frozenset(t) for t in combinations(range(15),3)
             if all(len((frozenset(t)|{15,16})&w)<=2 for w in fixed)]
    check(triples==literal,'third triple universe disagreement')
    incident={i:[t for t in triples if i in t] for i in range(15)}
    output=[]
    nodes=0
    start=time.monotonic()
    def visit(left,chosen):
        nonlocal nodes
        nodes+=1
        if nodes>2000000 or time.monotonic()-start>20:
            raise RuntimeError('INCOMPLETE literal partition guard')
        if not left:
            output.append(tuple(sorted(bits(t) for t in chosen)))
            return
        # Different from the producer's minimum-domain pivot.
        for t in incident[min(left)]:
            if t<=left:
                visit(left-t,chosen+[t])
    visit(frozenset(range(15)),[])
    check(len(output)==len(set(output)),'literal duplicate partition')
    return [bits(t) for t in triples],sorted(output)


def base(groups,fixed,center):
    quads=set()
    for chosen in combinations(range(5),4):
        for q in product(*(sorted(groups[j]) for j in chosen)):
            word=frozenset(q)|{center}
            if all(len(word&w)<=2 for w in fixed):
                quads.add(frozenset(q))
    quads=sorted(quads,key=lambda q:tuple(sorted(q)))
    words=[q|{center} for q in quads]
    literal=[frozenset(q)|{center} for q in combinations(range(15),4)
             if all(len((frozenset(q)|{center})&w)<=2 for w in fixed)]
    check(words==literal,'private-word universe disagreement')
    pairsets=[{frozenset(p) for p in combinations(sorted(q),2)} for q in quads]
    adjacent=[{j for j,b in enumerate(pairsets) if i!=j and a.isdisjoint(b)}
              for i,a in enumerate(pairsets)]
    for i,a in enumerate(words):
        for j,b in enumerate(words):
            check((j in adjacent[i])==(i!=j and len(a&b)<=2),'private graph disagreement')
    return words,adjacent


def nine_cliques(adjacent,vertices,node_cap=2000000,seconds=20,target=9):
    check(type(target) is int and target>0,'literal target domain')
    check(type(node_cap) is int and 0<node_cap<=2000000,'literal node guard domain')
    check(0<seconds<=20,'literal time guard domain')
    output=set()
    nodes=0
    start=time.monotonic()
    def visit(chosen,possible,previous):
        nonlocal nodes
        nodes+=1
        if nodes>node_cap or time.monotonic()-start>seconds:
            raise RuntimeError('INCOMPLETE literal clique guard')
        if len(chosen)+len(possible)<target:
            return
        if not possible:
            if not previous:
                for q in combinations(sorted(chosen),target):
                    output.add(q)
            return
        pivot=max(possible|previous,key=lambda v:(len(adjacent[v]&possible),-v))
        for v in sorted(possible-adjacent[pivot]):
            visit(chosen+[v],possible & adjacent[v],previous & adjacent[v])
            possible.remove(v);previous.add(v)
    visit([],set(vertices),set())
    return sorted(output),nodes


def compare(a,b,message):
    check(encode(a)==encode(b),message)


def replay(work,case_ids=None):
    cells,all_inputs=inputs()
    summary=json.loads((work/'summary.json').read_text())
    check(summary['status']=='COMPLETE' and len(summary['cases'])==6,'producer incomplete')
    compare(cells,summary['cells'],'cell carrier mismatch')
    total_counts=Counter()
    requested=set(range(6) if case_ids is None else case_ids)
    check(bool(requested) and requested<=set(range(6)),'requested case domain')
    for k,(star,rows,cols,fixed) in enumerate(all_inputs):
        if k not in requested:
            continue
        start=time.monotonic()
        ts,ps=partitions(rows,cols,fixed)
        yw,ya=base(rows,fixed,15);zw,za=base(cols,fixed,16)
        header={'star':star,'triples':ts,'partitions':ps,
                'y_words':[bits(w) for w in yw], 'y_adjacent':[bits(a) for a in ya],
                'z_words':[bits(w) for w in zw], 'z_adjacent':[bits(a) for a in za]}
        compare(header,json.loads((work/f'header-{k}.json').read_text()),'whole base carrier mismatch')
        counts=Counter();joints=[];bk_nodes=0
        with (work/f'carrier-{k}.jsonl').open('r') as stream:
            for pi,p in enumerate(ps):
                if time.monotonic()-start>60:
                    raise RuntimeError('INCOMPLETE literal whole-star guard')
                extra=[points(t)|{15,16} for t in p]
                ys=[i for i,w in enumerate(yw) if all(len(w&t)<=2 for t in extra)]
                yc,nodes=nine_cliques(ya,ys);bk_nodes+=nodes
                y2=[q for q in yc if stats([w for w in fixed if 15 in w]+extra+[yw[i] for i in q],15)['m']==2]
                record={'partition':p,'y_candidates':ys,'y_nine':yc,'y_two':y2,'z_cases':[]}
                counts.update({'partitions':1,'y_nine':len(yc),'y_two':len(y2)})
                for q in yc:
                    private_y=[yw[i] for i in q]
                    zs=[i for i,w in enumerate(zw) if all(len(w&t)<=2 for t in extra+private_y)]
                    zc,nodes=nine_cliques(za,zs);bk_nodes+=nodes
                    record['z_cases'].append({'y':q,'z_candidates':zs,'z_nine':zc})
                    counts.update({'z_nine':len(zc)})
                    for r in zc:
                        words=fixed+extra+private_y+[zw[i] for i in r]
                        packing(words,42)
                        profiles=[stats(words,c) for c in CENTERS]
                        check(all(s['m'] in (1,2) for s in profiles),'literal local census mismatch')
                        blocks=sorted(bits(w) for w in words)
                        joint={'case':k,'partition_index':pi,'y':q,'z':r,'profiles':profiles,
                               'blocks':blocks,'core_sha256':sha(blocks)}
                        joints.append(joint)
                line=stream.readline()
                check(bool(line),'truncated producer carrier')
                compare(record,json.loads(line),'entrywise partition/graph/solution mismatch')
            check(not stream.readline(),'extra producer carrier records')
        compare(joints,json.loads((work/f'joints-{k}.json').read_text()),'whole joint packing mismatch')
        case=summary['cases'][k]
        for label,value in counts.items():
            check(case['counts'][label]==value,'finite count mismatch')
        check(case['partition_count']==len(ps) and case['joint_count']==len(joints),'case total mismatch')
        compare(case['m_census'],dict(sorted(Counter(
            ','.join(str(p['m']) for p in j['profiles']) for j in joints).items())),
                'm count mismatch')
        check(case['header_sha256']==sha(header) and case['joints_sha256']==sha(joints),'carrier hash mismatch')
        total_counts.update(counts)
        record={'case':k,'status':'COMPLETE_ENTRYWISE','seconds':time.monotonic()-start,
                'maximal_clique_nodes':bk_nodes,'counts':dict(counts),'summary_sha256':sha(summary),
                'header_sha256':sha(header),'joints_sha256':sha(joints),
                'carrier_sha256':hashlib.sha256((work/f'carrier-{k}.jsonl').read_bytes()).hexdigest()}
        (work/f'verified-case-{k}.json').write_bytes(encode(record))
        print(json.dumps(record),flush=True)
    result={'status':'COMPLETE_ENTRYWISE','cases':sorted(requested),'counts':dict(total_counts),
            'joint_cores':sum(summary['cases'][k]['joint_count'] for k in requested),
            'summary_sha256':sha(summary)}
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--cases',type=int,nargs='+')
    args=parser.parse_args()
    replay(args.work,args.cases)
