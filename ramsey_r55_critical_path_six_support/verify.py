"""Independent literal checks; no producer, solver or numerical dependency."""
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


def certificate_check(doc, example):
    need(doc['format']=='r55-critical-path-six-support-v1','format')
    need(doc['core_order']==11 and doc['kernel_layer']==3 and doc['kernel_variables']==15,'dimensions')
    types=doc['types'];need(types==[333,359,587,773,1579,1583],'six types')
    core={(0,v) for v in range(1,11)}
    core|={e for bit,e in enumerate(itertools.combinations(range(3,11),2)) if not(5388912>>bit&1)}
    need(doc['core_red_edges']==[list(e) for e in sorted(core)],'literal core guard')
    pairs=list(itertools.combinations(range(6),2));edges={e:i+1 for i,e in enumerate(pairs)}
    fixed=core|{(u,11+i) for i,t in enumerate(types) for u in range(11) if t>>u&1}
    def mono(vs,c,R):return all((e in R)==c for e in itertools.combinations(sorted(vs),2))
    # Reconstruct the layer by common colored core neighborhoods, not by
    # the producer's complete five-set enumeration.
    expected=set()
    for k in range(4):
        for vs in itertools.combinations(range(6),k):
            for color in (False,True):
                common=[u for u in range(11) if all(bool(types[v]>>u&1)==color for v in vs)]
                if any(mono(cs,color,core) for cs in itertools.combinations(common,5-k)):
                    clause=tuple(sorted((-1 if color else 1)*edges[e] for e in itertools.combinations(vs,2)))
                    expected.add(clause)
    records=doc['kernel_clauses'];actual=[]
    for record in records:
        cl=record['clause'];five=record['five'];color=record['red']
        need(type(color) is bool and len(five)==5 and five==sorted(set(five)) and
             all(type(v) is int and 0<=v<17 for v in five),'K5 witness')
        need(sum(v>=11 for v in five)<=3,'K5 layer')
        known=[e for e in itertools.combinations(five,2) if e[0]<11]
        need(all((e in fixed)==color for e in known),'fixed K5 premises')
        tail=[(u-11,v-11) for u,v in itertools.combinations(five,2) if u>=11]
        need(cl==sorted((-1 if color else 1)*edges[e] for e in tail),'exact residual K5 clause')
        actual.append(tuple(cl))
    need(actual==sorted(expected) and len(actual)==40,'complete exact kernel')
    proof=doc['unit_refutation'];values={};used=[]
    for index,lit in proof['steps']:
        need(type(index) is int and 0<=index<len(actual),'proof index')
        row=actual[index];need(not any(values.get(abs(l))==(l>0) for l in row),'unit not already satisfied')
        need([l for l in row if abs(l) not in values]==[lit],'exact unit consequence')
        values[abs(lit)]=lit>0;used.append(index)
    last=proof['conflict_clause'];need(type(last) is int and 0<=last<len(actual),'conflict index')
    need(all(values.get(abs(l))==(l<0) for l in actual[last]),'all conflict literals false')
    used.append(last);need(sorted(used)==proof['used_clauses'] and len(used)==14,'14-clause proof')
    # A second proof check exhausts all 2^15 tail assignments against the
    # fourteen literal monochromatic-K5 witnesses, independent of propagation.
    for mask in range(1<<15):
        need(any(all(bool(mask>>(abs(l)-1)&1)!=(l>0) for l in actual[i]) for i in used),'tail assignment survives')
    completions=doc['deletion_completions']
    need([r['deleted_type'] for r in completions]==types,'all six outside deletions')
    for i,r in enumerate(completions):
        keep=types[:i]+types[i+1:];mask=r['tail_mask']
        need(type(mask) is int and 0<=mask<1024,'10-edge mask')
        red=set(core)|{(u,11+j) for j,t in enumerate(keep) for u in range(11) if t>>u&1}
        red|={e for bit,e in enumerate(itertools.combinations(range(11,16),2)) if mask>>bit&1}
        for five in itertools.combinations(range(16),5):
            colors=[e in red for e in itertools.combinations(five,2)]
            need(any(colors) and not all(colors),'full deletion completion')
    need(doc['presence_cut']=={'types':types,'relation':'sum of nonzero-count indicators <= 5'},'presence, not count, cut')
    need(hashlib.sha256(example.read_bytes()).hexdigest()==doc['example_sha256'],'example identity')
    example_red={tuple(e) for e in json.loads(example.read_text())['red_edges']}
    footprints=[sum(1<<u for u in range(11) if (u,v) in example_red) for v in range(11,43)]
    need(set(types)<=set(footprints),'example contains six types')
    # Test every pair and every triple of the 32 actual footprint occurrences.
    allowed={}
    for i,j in itertools.combinations(range(32),2):
        allowed[i,j]=[]
        for color in (False,True):
            common=[u for u in range(11) if bool(footprints[i]>>u&1)==color and bool(footprints[j]>>u&1)==color]
            if not any(mono(cs,color,core) for cs in itertools.combinations(common,3)):
                allowed[i,j].append(color)
        need(bool(allowed[i,j]),'pair compatibility')
    hist=Counter()
    for vs in itertools.combinations(range(32),3):
        es=list(itertools.combinations(vs,2));forbid={}
        for color in (False,True):
            common=[u for u in range(11) if all(bool(footprints[v]>>u&1)==color for v in vs)]
            forbid[color]=any(mono(cs,color,core) for cs in itertools.combinations(common,2))
        valid=0
        for colors in itertools.product((False,True),repeat=3):
            if not all(c in allowed[e] for c,e in zip(colors,es)):continue
            if all(colors) and forbid[True]:continue
            if not any(colors) and forbid[False]:continue
            valid+=1
        need(valid>0,'individually feasible triple');hist[valid]+=1
    return {'status':'VERIFIED_SIX_SUPPORT_OBSTRUCTION_WITH_ALL_FIVE_SUPPORTS_REALIZABLE',
            'core_vertices':11,'outside_vertices':6,'fixed_pairs':121,'free_pairs':15,
            'kernel_clauses':len(actual),'proof_clauses':len(used),'unit_steps':len(proof['steps']),
            'tail_assignments_exhausted':32768,'full_deletion_completions':6,
            'deletion_five_sets_checked':26208,'example_types':footprints,
            'example_pair_tests':496,'example_triple_tests':4960,
            'triple_completion_histogram':dict(sorted(hist.items())),
            'guarded_presence_arity':6}


def controls(doc,example):
    import copy
    mutations=[]
    def mutate(action):
        bad=copy.deepcopy(doc);action(bad);mutations.append(bad)
    mutate(lambda d:d['core_red_edges'].pop())
    mutate(lambda d:d['types'].__setitem__(0,332))
    mutate(lambda d:d['kernel_clauses'].pop())
    mutate(lambda d:d['kernel_clauses'][0]['clause'].append(16))
    mutate(lambda d:d['kernel_clauses'][0].__setitem__('red',not d['kernel_clauses'][0]['red']))
    mutate(lambda d:d['kernel_clauses'][0].__setitem__('five',[0,1,2,3,4]))
    mutate(lambda d:d['unit_refutation']['steps'].pop(0))
    mutate(lambda d:d['unit_refutation']['steps'][0].__setitem__(1,-d['unit_refutation']['steps'][0][1]))
    mutate(lambda d:d['deletion_completions'][0].__setitem__('tail_mask',0))
    mutate(lambda d:d['deletion_completions'].pop())
    mutate(lambda d:d['presence_cut'].__setitem__('relation','sum of counts <= 5'))
    mutate(lambda d:d.__setitem__('example_sha256','0'*64))
    for bad in mutations:
        try:certificate_check(bad,example)
        except ValueError:pass
        else:raise ValueError('malformed certificate accepted')
    return len(mutations)


if __name__=='__main__':
    here=Path(__file__).resolve().parent;p=argparse.ArgumentParser()
    p.add_argument('--certificate',type=Path,default=here/'certificate.json')
    p.add_argument('--example',type=Path,default=here/'EXAMPLE43.json')
    p.add_argument('--attachments',type=Path,default=here/'attachments.json')
    p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    need(not a.report.exists(),'fresh report');doc=json.loads(a.certificate.read_text())
    result={'certificate':certificate_check(doc,a.example),'example':audit(a.example),
            'malformed_certificates_rejected':controls(doc,a.example)}
    need(json.loads(a.attachments.read_text())=={'types':result['certificate']['example_types']},'pinned attachments')
    a.report.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result['certificate']))
