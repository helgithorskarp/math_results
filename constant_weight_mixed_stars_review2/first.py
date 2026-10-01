"""Independent incidence-domain reduction and complete first-star pair covers.

No target-author executable module is imported. Binary edge decisions differ
from the published cross-edge generator; point partitions differ from its
pair-MRV proof engine. Small exact primitives and the native kernel are reused
from this reviewer's previous audited publications.
"""
from itertools import combinations, permutations, product
from collections import Counter
from pathlib import Path
import json, subprocess, time, hashlib
from exact import insist, mask, bits, pairs, packing, encoded


def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def leave(shape):
    cores=[((0,1),(0,2)),((0,1),(1,2)),((0,2),(1,2)),((0,1),(0,2),(1,2),(15,16))]
    cohorts=[(range(3,8),range(8,14),range(14,17)),(range(3,9),range(9,14),range(14,17)),
             (range(3,9),range(9,15),range(15,17)),(range(3,8),range(8,13),range(13,15))]
    return frozenset(cores[shape]) | frozenset((h,z) for h,g in enumerate(cohorts[shape]) for z in g)


def graph_domain(parts, degrees, forbidden=()):
    n=len(degrees)
    group_of={x:i for i,g in enumerate(parts) for x in g}
    edges=tuple(e for e in combinations(range(n),2) if group_of[e[0]]!=group_of[e[1]] and e not in forbidden)
    adjacent=tuple(e[1] for e in edges if e[0]==0)
    remainder=tuple(e for e in edges if e[0]!=0)
    answers=set(); total=0; max_nodes=0
    suffix=[[0]*n for _ in range(len(remainder)+1)]
    for i in range(len(remainder)-1,-1,-1):
        suffix[i]=suffix[i+1].copy()
        for z in remainder[i]:suffix[i][z]+=1
    for root in combinations(adjacent,degrees[0]):
        residual=list(degrees);residual[0]=0
        chosen=[(0,z) for z in root]
        for z in root:residual[z]-=1
        if min(residual)<0:continue
        nodes=0;started=time.monotonic()
        def visit(i):
            nonlocal nodes
            nodes+=1
            if nodes>200000 or (nodes%1024==0 and time.monotonic()-started>10):
                raise RuntimeError('INCOMPLETE incidence edge-decision root guard')
            if any(d<0 or d>suffix[i][z] for z,d in enumerate(residual)):return
            if i==len(remainder):
                if not any(residual):answers.add(tuple(sorted(chosen)))
                return
            a,b=remainder[i]
            if residual[a] and residual[b]:
                residual[a]-=1;residual[b]-=1;chosen.append((a,b))
                visit(i+1)
                chosen.pop();residual[a]+=1;residual[b]+=1
            visit(i+1)
        visit(0);total+=nodes;max_nodes=max(max_nodes,nodes)
    insist(all(Counter(x for e in g for x in e)==Counter(dict(enumerate(degrees))) for g in answers),'incidence degrees')
    return sorted(answers),{'nodes':total,'maximum_root_nodes':max_nodes,'graphs':len(answers)}


def maps_on_parts(parts):
    for images in product(*(permutations(part) for part in parts)):
        p=list(range(sum(map(len,parts))))
        for part,image in zip(parts,images):
            for x,y in zip(part,image):p[x]=y
        yield tuple(p)


def edge_image(g,p):
    return tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in g))


def orbits(domain,maps):
    remaining=set(domain);result=[]
    while remaining:
        rep=min(remaining);orbit={edge_image(rep,p) for p in maps}
        insist(orbit<=remaining,'incidence orbit cover')
        remaining-=orbit;result.append((rep,len(orbit)))
    return result


def fixed_words(graph,shape):
    if shape in (0,1):
        parts=((0,1,2),(3,4),(5,6,7)); common=(1,2,3,4)
        cohorts={(1,2):tuple(range(5,8)),(0,2):tuple(range(8,14)),(0,1):tuple(range(14,17))}
    elif shape==2:
        parts=((0,1),(2,3),(4,5,6,7));common=(0,1,15,16)
        cohorts={(1,2):tuple(range(3,9)),(0,2):tuple(range(9,15)),(0,1):()}
    else:
        parts=((0,1,2),(3,4,5),(6,7,8,9));common=None
        cohorts={(1,2):tuple(range(3,8)),(0,2):tuple(range(8,13)),(0,1):tuple(range(13,15))}
    group_of={v:h for h,part in enumerate(parts) for v in part}
    row=[{group_of[v]} for v in range(sum(map(len,parts)))]
    if shape==3:
        for q in (0,3,6):row[q].add(15)
        for q in (1,4,7):row[q].add(16)
    for pair,labels in cohorts.items():
        es=[e for e in graph if tuple(sorted((group_of[e[0]],group_of[e[1]])))==pair]
        insist(len(es)==len(labels),'cohort edge count')
        for e,z in zip(es,labels):
            for v in e:row[v].add(z)
    words=sorted(mask(q) for q in row)+([] if common is None else [mask(common)])
    if shape==1:
        p=[1,0,2]+list(range(9,14))+list(range(3,9))+list(range(14,17))
        words=sorted(mask(p[z] for z in bits(w)) for w in words)
    words=tuple(sorted(words));used=[e for w in words for e in pairs(w)]
    insist(all(w.bit_count()==4 and w&7 for w in words) and len(set(words))==len(words),'high words')
    insist(len(used)==len(set(used)) and not set(used)&leave(shape),'high pairs')
    covered_high={e for e in combinations(range(17),2) if e[0]<3 and e not in leave(shape)}
    insist(covered_high<=set(used),'high coverage')
    insist([sum(w>>h&1 for w in words) for h in range(3)]==[3,3,4],'high replications')
    return words


def domain():
    path,ps=graph_domain(((0,1,2),(3,4),(5,6,7)),(3,)*8)
    pm=tuple(maps_on_parts(((0,1,2),(3,4),(5,6,7))))
    cube,cs=graph_domain(((0,1),(2,3),(4,5,6,7)),(3,)*8,tuple(combinations(range(4),2)))
    cm=tuple(maps_on_parts(((0,1),(2,3),(4,5,6,7))))
    triangular,ts=graph_domain(((0,1,2),(3,4,5),(6,7,8,9)),(2,2,3,2,2,3,2,2,3,3),
                             ((0,3),(0,6),(3,6),(1,4),(1,7),(4,7)))
    tm=[]
    for swap,free in product(range(2),repeat=2):
        p=list(range(10))
        if swap:
            for a,b in ((0,1),(3,4),(6,7)):p[a],p[b]=p[b],p[a]
        if free:p[8],p[9]=p[9],p[8]
        tm.append(tuple(p))
    po,co,to=orbits(path,pm),orbits(cube,cm),orbits(triangular,tm)
    insist((len(path),len(cube),len(triangular),len(po),len(co),len(to))==(408,24,2408,8,1,612),'incidence census')
    records=[]
    for shape,os in ((0,po),(1,po),(2,co),(3,to)):
        for i,(g,weight) in enumerate(os):records.append({'shape':shape,'index':i,'orbit_size':weight,'graph':g,'fixed':fixed_words(g,shape)})
    return records,{'path':ps,'cube':cs,'triangle':ts,'cases':len(records),'group_orders':[len(pm),len(cm),len(tm)]}


def transport(words,p):
    return tuple(sorted(mask(p[z] for z in bits(w)) for w in words))


def isomorphisms(source,target):
    # Derive actual point maps by bijections of high incidence rows. Shared
    # mathematical construction is disclosed, and every final point map is checked.
    shared=[w for w in source if (w&7).bit_count()==2]
    common_target=[w for w in target if (w&7).bit_count()==2]
    insist(len(shared)==len(common_target)==1,'one high-pair block')
    source_rows=[tuple(w for w in source if w>>h&1 and w!=shared[0]) for h in range(3)]
    target_rows=[tuple(w for w in target if w>>h&1 and w!=common_target[0]) for h in range(3)]
    sr=sum(source_rows,());tr=sum(target_rows,())
    specials=tuple(z for z in bits(shared[0]) if z>=3)
    target_specials=tuple(z for z in bits(common_target[0]) if z>=3)
    incidences={tuple(i for i,w in enumerate(tr) if w>>z&1):z for z in range(3,17) if z not in target_specials}
    answer=set()
    for images in product(*(permutations(range(sum(map(len,source_rows[:h])),sum(map(len,source_rows[:h+1])))) for h in range(3))):
        rowmap=sum(images,())
        p=list(range(18));valid=True
        for z in range(3,17):
            if z in specials:continue
            signature=tuple(sorted(rowmap[i] for i,w in enumerate(sr) if w>>z&1))
            if signature not in incidences:valid=False;break
            p[z]=incidences[signature]
        if not valid:continue
        for sp in permutations(target_specials):
            for a,b in zip(specials,sp):p[a]=b
            if len(set(p))==18 and transport(source,p)==tuple(target):answer.add(tuple(p))
    return tuple(sorted(answer))


def literal_covers(rows,columns):
    rows=frozenset(rows); columns=tuple((w,pairs(w)) for w in columns)
    nodes=0;started=time.monotonic()
    def visit(rem,chosen):
        nonlocal nodes
        nodes+=1
        if nodes>200000 or (nodes%256==0 and time.monotonic()-started>10):raise RuntimeError('INCOMPLETE literal-cover guard')
        if not rem:return [tuple(sorted(chosen))]
        pivot=min(rem);answer=[]
        for w,ps in columns:
            if pivot in ps and ps<=rem:answer+=visit(rem-ps,chosen+(w,))
        return answer
    answers=tuple(sorted(visit(rows,())))
    insist(len(set(answers))==len(answers),'literal duplicate cover')
    return answers,nodes


def run_native(work,n,columns,exclusions,tag='active'):
    pair_list=tuple(combinations(range(n),2));index={e:i for i,e in enumerate(pair_list)}
    lines=[f'{n} {len(columns)} {len(exclusions)}',*map(str,columns)]
    for i,edges in enumerate(exclusions):
        excluded=sorted(index[e] for e in edges)
        lines.append(f'{i} {len(excluded)} '+' '.join(map(str,excluded)))
    inp,out=work/(tag+'.input'),work/(tag+'.jsonl')
    inp.write_text('\n'.join(lines)+'\n')
    p=subprocess.run([str(work/'partition'),str(inp),str(out)],capture_output=True,text=True,timeout=45)
    insist(p.returncode==0 and not p.stderr,'INCOMPLETE native cover: '+p.stderr)
    records=[json.loads(line) for line in out.read_text().splitlines()]
    insist([r['index'] for r in records]==list(range(len(exclusions))),'native coverage/order')
    return records


def classify(work,expected):
    work.mkdir(parents=True,exist_ok=True)
    records,stats=domain();all_stars={i:[] for i in range(4)};native_nodes=literal_nodes=0;max_native=0
    for i,d in enumerate(records):
        used=frozenset(e for w in d['fixed'] for e in pairs(w))
        old=frozenset(e for e in leave(d['shape'])|used if e[0]>=3)
        excluded=frozenset((a-3,b-3) for a,b in old)
        cols=tuple(sorted(mask(q) for q in combinations(range(14),4) if not pairs(mask(q))&excluded))
        out=run_native(work,14,cols,[excluded],'first-active')[0]
        rem=frozenset(combinations(range(14),2))-excluded
        reference,nn=literal_covers(rem,cols)
        insist(tuple(map(tuple,out['covers']))==reference,'entrywise independent first-star cover mismatch')
        native_nodes+=out['states'];literal_nodes+=nn;max_native=max(max_native,out['states'])
        for cover in reference:
            star=tuple(sorted(d['fixed']+tuple(w<<3 for w in cover)))
            insist(len(star)==20 and len(set(star))==20 and all(w.bit_count()==4 for w in star),'full first star')
            covered=[e for w in star for e in pairs(w)]
            insist(len(covered)==len(set(covered))==120 and frozenset(combinations(range(17),2))-set(covered)==leave(d['shape']),'first-star full leave')
            all_stars[d['shape']].append(star)
        if (i+1)%100==0:print(json.dumps({'first_cases_complete':i+1,'total':629}),flush=True)
    insist([len(all_stars[i]) for i in range(4)]==[2,2,2,0],'complete first-star census differs')
    templates=[tuple(t['star']) for t in expected['templates']]
    group=[]
    for shape,t in enumerate(templates):
        insist(all(isomorphisms(s,t) for s in all_stars[shape]),'first template misses computed class')
        group.append(isomorphisms(t,t))
        gset=set(group[-1]);insist(tuple(range(18)) in gset and all(tuple(p[q[z]] for z in range(18)) in gset for p,q in product(gset,repeat=2)),'literal group closure')
    insist(list(map(len,group))==[6,6,4],'first-star checked groups')
    result={'status':'COMPLETE independently classified first stars','stats':stats,'stars_by_shape':[len(all_stars[i]) for i in range(4)],'native_nodes':native_nodes,'literal_nodes':literal_nodes,'max_native_case_states':max_native,'groups':group,'templates':templates}
    (work/'first.json').write_bytes(encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('groups','templates')}),flush=True)
    return result


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--classification',type=Path,required=True)
    args=p.parse_args(); classify(args.work,json.loads((args.classification/'expected.json').read_text()))
