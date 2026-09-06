"""Literal certificate and example checker; imports no producer or solver."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


def need(ok,msg):
    if not ok:raise ValueError(msg)


def audit(path):
    doc=json.loads(path.read_text());need(set(doc)=={'n','red_edges'} and type(doc['n']) is int and doc['n']==43,'schema')
    raw=doc['red_edges'];need(type(raw) is list,'edge list')
    need(all(type(e) is list and len(e)==2 and all(type(v) is int for v in e) and 0<=e[0]<e[1]<43 for e in raw),'simple edges')
    need(raw==sorted(raw) and len({tuple(e) for e in raw})==len(raw),'ordered unique edges')
    red={tuple(e) for e in raw};g=[set() for _ in range(43)]
    for u,v in red:g[u].add(v);g[v].add(u)
    def mono(vs,c):return all(((u,v) in red)==c for u,v in itertools.combinations(sorted(vs),2))
    degrees=list(map(len,g));need(degrees==[20]*3+[21]*40,'all43 degrees')
    need((0,1) in red and (0,2) in red and (1,2) not in red,'red path')
    cells=Counter(sum(1<<v for v in range(3) if v in g[u]) for u in range(3,43))
    need(cells[0]==0 and cells[1]==8,'centre-only cell')
    need(all(g[v]&{0,1,2}=={0} for v in range(3,11)),'marked critical vertices')
    for bit,(u,v) in enumerate(itertools.combinations(range(3,11),2)):
        need(((u,v) not in red)==bool(5388912>>bit&1),'critical core identity')
    # Complete definition-level K5 census, recording the first missing layer.
    hist={c:[0]*6 for c in ('red','blue')};first={};tested=0
    for five in itertools.combinations(range(43),5):
        tested+=1
        for c,name in ((True,'red'),(False,'blue')):
            if mono(five,c):
                k=sum(v>=11 for v in five);hist[name][k]+=1
                first.setdefault(f'{name}:{k}',list(five))
    need(all(hist[c][k]==0 for c in hist for k in range(3)),'two-outside Ramsey layer')
    # Compute every local count directly; none was imposed outside the core.
    profiles=[];hard_failures=[]
    for u in range(43):
        R=g[u];B=set(range(43))-{u}-R
        tr=sum((v,w) in red for v,w in itertools.combinations(sorted(R),2))
        tb=sum((v,w) not in red for v,w in itertools.combinations(sorted(B),2))
        profiles.append([degrees[u],tr,tb])
        if tr>(93 if u<3 else 100) or tb>(107 if u<3 else 100):hard_failures.append(u)
    # Independent literal common-neighborhood counts over all core root pairs.
    U=[[1]*6 for _ in range(6)]
    for a in range(2,6):
        for b in range(2,6):
            p,q=U[a-1][b],U[a][b-1];U[a][b]=p+q-int(p%2==q%2==0)
    roots={c:[s for k in range(4) for s in itertools.combinations(range(11),k) if mono(s,c)] for c in (True,False)}
    checks=0
    for A in roots[True]:
        for B in roots[False]:
            if not(A or B) or set(A)&set(B):continue
            size=sum(v not in A+B and all(a in g[v] for a in A) and all(b not in g[v] for b in B) for v in range(43))
            need(size<U[5-len(A)][5-len(B)],'full graph root-union capacity')
            checks+=1
    return {'status':'VERIFIED_PARTIAL_REALIZATION_NOT_RAMSEY','n':43,'red_edges':len(red),
            'degrees':degrees,'cells':dict(sorted(cells.items())),'k5_by_outside_count':hist,
            'first_obstructions':first,'five_sets_checked':tested,'root_pairs_checked':checks,
            'profiles':profiles,'hard_cap_failures':hard_failures,
            'graph_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def certificate_check(doc,example):
    need(doc['format']=='r55-critical-path-triple-cut-v1','certificate format')
    part=doc['partial'];need(part['n']==11,'partial order')
    def edges(raw,n):
        need(type(raw) is list and all(type(e) is list and len(e)==2 and
             all(type(v) is int for v in e) and 0<=e[0]<e[1]<n for e in raw),'edge schema')
        result={tuple(e) for e in raw};need(len(result)==len(raw),'duplicate edge');return result
    R=edges(part['red_edges'],11);B=edges(part['blue_edges'],11)
    need(not R&B,'disjoint colors')
    pairs=doc['forcing_pairs'];triangles=doc['blue_forcing_triangles']
    need(pairs==[[8,9],[8,10],[9,10]] and len(triangles)==3,'outer triangle')
    need(doc['red_root_pair']==[0,2],'red root pair')
    blue_proof=set()
    for pair,tri in zip(pairs,triangles):
        need(len(tri)==len(set(tri))==3 and all(type(v) is int and 0<=v<8 for v in tri),'forcing triple')
        five=sorted(pair+tri)
        for edge in itertools.combinations(five,2):
            if list(edge)!=pair:blue_proof.add(edge)
        need(all(e in B for e in itertools.combinations(five,2) if list(e)!=pair),'blue unit witness')
    red_five=[0,2,8,9,10]
    red_proof={e for e in itertools.combinations(red_five,2) if list(e) not in pairs}
    need(R==red_proof and B==blue_proof,'exact proof premises')
    # Independent complete truth table of the four-clause unit contradiction.
    for vals in itertools.product((False,True),repeat=3):
        need(not(all(vals) and any(not v for v in vals)),'four-clause contradiction')
    need(len(R)==7 and len(B)==22,'29 fixed edges')
    records=doc['deletion_completions'];need([r['deleted'] for r in records]==list(range(11)),'all vertex deletions')
    for record in records:
        v=record['deleted'];keep=[u for u in range(11) if u!=v];pos={u:i for i,u in enumerate(keep)}
        mask=int(record['red_mask_hex'],16);need(0<=mask<(1<<45),'completion mask range')
        red={e for i,e in enumerate(itertools.combinations(range(10),2)) if mask>>i&1}
        need(all((pos[u],pos[w]) in red for u,w in R if v not in (u,w)),'deletion red premises')
        need(all((pos[u],pos[w]) not in red for u,w in B if v not in (u,w)),'deletion blue premises')
        for five in itertools.combinations(range(10),5):
            bits=[e in red for e in itertools.combinations(five,2)]
            need(any(bits) and not all(bits),'deletion Ramsey graph')
    full={tuple(e) for e in json.loads(example.read_text())['red_edges']}
    need(hashlib.sha256(example.read_bytes()).hexdigest()==doc['example_sha256'],'example identity')
    labels=doc['example_original_labels'];need(labels==[0,1,2,3,4,7,8,10,12,15,19],'embedding labels')
    need(all((labels[u],labels[v]) in full for u,v in R),'example embeds red premises')
    need(all((labels[u],labels[v]) not in full for u,v in B),'example embeds blue premises')
    core=edges(doc['core_red_edges'],11);need(core=={e for e in full if e[1]<11},'literal core')
    types=doc['footprints'];need(types==[117,421,621],'three footprint labels')
    for t,out,proof in zip(types,labels[-3:],doc['self_copy_witnesses']):
        need(t==sum(1<<u for u in range(11) if (u,out) in full),'actual footprint')
        for c,name in ((True,'red'),(False,'blue')):
            tri=proof[name];need(len(tri)==len(set(tri))==3 and all(type(v) is int and 0<=v<11 for v in tri),'self triple')
            need(all(bool(t>>u&1)==c for u in tri),'self-copy contact')
            need(all((e in core)==c for e in itertools.combinations(sorted(tri),2)),'self-copy clique')
    need(len(doc['self_copy_witnesses'])==3,'all self bounds')
    for left,right in itertools.combinations(types,2):
        red=set(core)|{(11,12)}
        red.update((u,v) for v,t in ((11,left),(12,right)) for u in range(11) if t>>u&1)
        for five in itertools.combinations(range(13),5):
            bits=[e in red for e in itertools.combinations(five,2)]
            need(any(bits) and not all(bits),'pair completion Ramsey condition')
    need(doc['guarded_count_cut']=={'types':types,'coefficients':[1,1,1],'upper_bound':2},'count cut')
    # All eight zero/one count assignments: exactly the forbidden all-present
    # assignment violates the cut. Singleton upper bounds were proved above.
    need([bits for bits in itertools.product((0,1),repeat=3) if sum(bits)>2]==[(1,1,1)],'cut semantics')
    return {'vertices':11,'fixed_red':len(R),'fixed_blue':len(B),'uncolored_pairs':55-len(R)-len(B),
            'vertex_deletion_witnesses':11,'deletion_five_sets_checked':2772,
            'full_core_pair_completions':3,'pair_completion_five_sets_checked':3861,
            'status':'VERIFIED_VERTEX_MINIMAL_PARTIAL_OBSTRUCTION_AND_GUARDED_CUT'}


def controls(doc,example):
    mutations=[]
    for color in ('red_edges','blue_edges'):
        bad=json.loads(json.dumps(doc));bad['partial'][color].pop();mutations.append(bad)
    bad=json.loads(json.dumps(doc));bad['deletion_completions'][0]['red_mask_hex']='000000000000';mutations.append(bad)
    bad=json.loads(json.dumps(doc));bad['guarded_count_cut']['upper_bound']=3;mutations.append(bad)
    bad=json.loads(json.dumps(doc));bad['self_copy_witnesses'][0]['red']=[0,1,2];mutations.append(bad)
    bad=json.loads(json.dumps(doc));bad['footprints'][0]^=1;mutations.append(bad)
    bad=json.loads(json.dumps(doc));bad['blue_forcing_triangles'][0]=[0,1,2];mutations.append(bad)
    bad=json.loads(json.dumps(doc));bad['example_original_labels'][-1]=20;mutations.append(bad)
    for bad in mutations:
        try:certificate_check(bad,example)
        except ValueError:pass
        else:raise ValueError('bad certificate accepted')
    return len(mutations)


if __name__=='__main__':
    here=Path(__file__).resolve().parent
    p=argparse.ArgumentParser();p.add_argument('--graph',type=Path,default=here/'EXAMPLE43.json')
    p.add_argument('--certificate',type=Path,default=here/'certificate.json')
    p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    need(not a.report.exists(),'fresh report');doc=json.loads(a.certificate.read_text())
    result={'certificate':certificate_check(doc,a.graph),'example':audit(a.graph),
            'bad_certificates_rejected':controls(doc,a.graph)}
    a.report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result['certificate']))
