"""Independent common residual ceilings via literal conflict clique covers.

Branch into containing/excluding a maximum-conflict vertex. Each pruning
partition is checked to cover the active vertices by actual conflict cliques.
The target's smaller individual residual maxima are outside this checker;
only the common sharp total bounds58/57 are established here.
"""
from pathlib import Path
from itertools import combinations,product
import json,time,resource,argparse
from exact import insist,mask,bits,pairs,packing,encoded
from first import digest,transport


def upper_decision(words,threshold,limit=200000):
    insist(type(threshold) is int and threshold>=0 and type(limit) is int and 0<=limit<=200000,'invalid threshold or guard')
    words=tuple(words);n=len(words)
    conflict=[sum(1<<j for j,z in enumerate(words) if j!=i and (w&z).bit_count()>=3) for i,w in enumerate(words)]
    nodes=0;started=time.monotonic();prunes=0
    def classes(active):
        answer=[];remaining=active
        while remaining:
            available=remaining;part=0
            while available:
                pool=tuple(bits(available))
                v=max(pool,key=lambda x:((conflict[x]&available).bit_count(),-x))
                bit=1<<v;part|=bit;remaining^=bit
                available &= conflict[v]
            members=tuple(bits(part))
            insist(all((words[a]&words[b]).bit_count()>=3 for a,b in combinations(members,2)),'false conflict-clique bound')
            answer.append(part)
        insist(sum(p.bit_count() for p in answer)==active.bit_count() and sum(answer)==active,'clique partition does not cover active domain')
        return answer
    def visit(active,need,chosen):
        nonlocal nodes,prunes
        nodes+=1
        if nodes>limit or (nodes%256==0 and time.monotonic()-started>10):raise RuntimeError('INCOMPLETE residual threshold guard')
        if need==0:return chosen
        if active.bit_count()<need:return None
        cover=classes(active)
        if len(cover)<need:prunes+=1;return None
        v=max(bits(active),key=lambda x:((conflict[x]&active).bit_count(),-x));bit=1<<v
        included=visit(active&~(conflict[v]|bit),need-1,chosen|bit)
        if included is not None:return included
        return visit(active^bit,need,chosen)
    witness=visit((1<<n)-1,threshold,0)
    if witness is not None:insist(all((words[a]&words[b]).bit_count()<=2 for a,b in combinations(tuple(bits(witness)),2)),'false residual positive')
    return witness,{'nodes':nodes,'bound_prunes':prunes,'seconds':time.monotonic()-started}


def small_controls():
    # Realize every five-vertex compatibility graph by literal sets: each
    # nonedge receives three private atoms shared only by its endpoints.
    all_edges=tuple(combinations(range(5),2));checked=0
    for graph in range(1<<10):
        adjacency=[0]*5
        for i,(a,b) in enumerate(all_edges):
            if graph>>i&1:adjacency[a]|=1<<b;adjacency[b]|=1<<a
        exact=max((s.bit_count() for s in range(32) if all(adjacency[a]>>b&1 for a,b in combinations(tuple(bits(s)),2))),default=0)
        realized=[1<<v for v in range(5)];atom=5
        for i,(a,b) in enumerate(all_edges):
            if not graph>>i&1:
                triple=7<<atom;atom+=3;realized[a]|=triple;realized[b]|=triple
        for threshold in (exact,exact+1):
            witness,_=upper_decision(realized,threshold)
            insist((witness is not None)==(threshold<=exact),'actual threshold engine vs exhaustive subset control')
        checked+=1
    # Literal packing realization, with known positive/negative thresholds.
    fixtures=[(3,7,12),(7,11,19,35,67),(31,47,55,59,61)]
    for words in fixtures:
        truth=max(s.bit_count() for s in range(1<<len(words)) if all((words[a]&words[b]).bit_count()<=2 for a,b in combinations(tuple(bits(s)),2)))
        for threshold in (truth,truth+1):
            result,_=upper_decision(words,threshold)
            insist((result is not None)==(threshold<=truth),'literal threshold control')
    try:
        upper_decision((31,),1,limit=0)
    except RuntimeError as e:
        insist('INCOMPLETE' in str(e),'zero guard status')
    else:
        raise ValueError('zero residual guard accepted')
    return {'five_vertex_compatibility_graphs':checked,'realized_graph_threshold_checks':2*checked,
            'literal_threshold_controls':6,'zero_guard_incomplete':True}


def candidates(fixed):
    return tuple(mask(q) for q in combinations(range(1,17),5) if all((mask(q)&w).bit_count()<=2 for w in fixed))


def mixed_orbits(work,shape,group):
    state=json.loads((work/f'mixed_s{shape}.json').read_text())
    insist(state['status']=='COMPLETE independent mixed census','incomplete mixed census is no exclusion')
    positive={tuple(p['star']) for model in state['models'] for p in model['positives']}
    all_stars={transport(s,g) for s in positive for g in group}
    pending=set(all_stars);records=[]
    while pending:
        rep=min(pending);orbit={transport(rep,p) for p in group}
        insist(orbit<=pending,'mixed joint orbit cover');pending-=orbit
        records.append({'star':rep,'orbit_size':len(orbit)})
    insist((len(all_stars),len(records))==((120,20) if shape==0 else (60,15)),'mixed actual stars/orbits')
    return records


def check_witness(words,first_template,profiles):
    packing(words,size=len(words));insist(all(0<=w<1<<18 for w in words),'witness range')
    insist(sum(w>>0&1 for w in words)==sum(w>>17&1 for w in words)==20,'witness saturated centers')
    insist(sum((w&1)!=0 and (w>>17&1)!=0 for w in words)==3,'witness pair multiplicity')
    for h,p in ((17,profiles[0]),(0,profiles[1])):
        row=sorted(5-sum((w>>h&1)!=0 and (w>>z&1)!=0 for w in words) for z in range(18) if z!=h)
        insist([v for v in row if v]==p,'witness deficit profile')
    insist(tuple(sorted(w^(1<<17) for w in words if w>>17&1))==first_template,'witness first-star marking')


def run(args):
    started=time.monotonic();first=json.loads((args.work/'first.json').read_text())
    double=json.loads((args.work/'double.json').read_text());expected_double=json.loads((args.classification/'expected.json').read_text())
    expected_mixed=json.loads((args.target/'expected.json').read_text())
    result=[];nodes=0;maximum=0
    for mode in ('double','mixed0','mixed2'):
        if mode=='double':orbit_records=double['orbits'];ceiling=21
        else:
            shape=int(mode[-1]);group=tuple(map(tuple,first['groups'][shape]));ceiling=21 if shape==0 else 20
            orbit_records=[dict(r,first=shape) for r in mixed_orbits(args.work,shape,group)]
        rows=[]
        for index,record in enumerate(orbit_records):
            shape=record['first'];template=tuple(first['templates'][shape]);fixed=tuple(sorted(set(tuple(w|1<<17 for w in template)+tuple(record['star']))))
            packing(fixed,size=37);words=candidates(fixed)
            if mode=='double':
                old=expected_double['residual_cases'][index]
                insist(old['candidate_sha256']==digest(words) and old['candidates']==len(words) and old['orbit_size']==record['orbit_size'],'double candidate entry differs')
            witness,metrics=upper_decision(words,ceiling+1)
            if witness is not None:
                (args.work/'unexpected_residual_witness.json').write_bytes(encoded({'mode':mode,'index':index,'words':fixed+tuple(words[z] for z in bits(witness))}))
                raise ValueError('claimed common upper ceiling fails')
            nodes+=metrics['nodes'];maximum=max(maximum,metrics['nodes'])
            rows.append({'index':index,'first':shape,'orbit_size':record['orbit_size'],'star':record['star'],'candidates':len(words),'candidate_sha256':digest(words),'proved_residual_ceiling':ceiling,'nodes':metrics['nodes']})
        result.append({'mode':mode,'cases':rows,'restricted_upper_bound':37+ceiling})
        print(json.dumps({'mode':mode,'cases':len(rows),'common_residual_ceiling':ceiling,'nodes':sum(r['nodes'] for r in rows)}),flush=True)
    # Exact attaining fixtures provide the matching lower bounds for common maxima.
    double_witness=json.loads((args.classification/'witness58.json').read_text())['word_masks']
    # The double witness has shape0 as its first marking.
    check_witness(double_witness,tuple(first['templates'][0]),([1,2,2],[1,2,2]))
    witnesses=[{'scope':'double','words':double_witness}]
    for shape in (0,2):
        words=expected_mixed['shapes'][[0,2].index(shape)]['attaining_words']
        check_witness(words,tuple(first['templates'][shape]),([1,2,2],[1,1,1,2]))
        insist(len(words)==(58 if shape==0 else 57),'mixed attaining size')
        witnesses.append({'scope':'mixed'+str(shape),'words':words})
    record={'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'COMPLETE independently established sharp common bounds58/58/57','cases':result,'witnesses':witnesses,'controls':small_controls(),'nodes':nodes,'max_case_nodes':maximum,'seconds':time.monotonic()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (args.work/'residual.json').write_bytes(encoded(record))
    print(json.dumps({k:v for k,v in record.items() if k not in ('cases','witnesses')},sort_keys=True),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--classification',type=Path,required=True);p.add_argument('--target',type=Path,required=True)
    run(p.parse_args())
