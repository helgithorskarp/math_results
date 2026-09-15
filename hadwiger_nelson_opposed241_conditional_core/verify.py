#!/usr/bin/env python3
"""Exact geometry, complete-input rejection, and relative vertex minimality.

Python 3.11+, standard library only. No imported solver verdict is a premise.
"""
import argparse
import hashlib
import json
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
B_PATH = HERE.parent / 'hadwiger_nelson_nonmono159_214_lowden2/points214.tsv'
B_HASH = '97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f'
BAD = '0121212203'
G = [(0,0,0,0),(36,0,0,0),(18,0,18,0),(-18,0,18,0),
     (-36,0,0,0),(-18,0,-18,0),(18,0,-18,0),(6,0,0,6),
     (-3,-3,3,-3),(-3,3,-3,-3)]
# (a+b sqrt(33)+i(c sqrt(3)+d sqrt(11)))/36.

def need(condition, message):
    if not condition:
        raise ValueError(message)

def digest(rows):
    return hashlib.sha256(('\n'.join(rows)+'\n').encode()).hexdigest()

def unit(p,q):
    a,b,c,d = (x-y for x,y in zip(p,q))
    return a*a+33*b*b+3*c*c+11*d*d == 1296 and a*b+c*d == 0

def all_edges(points):
    return [(i,j) for i,j in combinations(range(len(points)),2) if unit(points[i],points[j])]

def point_hash(points):
    return digest(' '.join(map(str,(a,0,0,b,0,c,d,0))) for a,b,c,d in points)

def geometry():
    need(hashlib.sha256(B_PATH.read_bytes()).hexdigest()==B_HASH,'B214 fixture hash')
    b=[]
    for line in B_PATH.read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        z=list(map(int,line.split()))
        need(len(z)==16 and all(z[i]==0 for i in (1,2,3,4,6,7,8,10,11,13,14,15)), 'B214 coordinate basis')
        b.append((3*z[0],3*z[5],3*z[9],3*z[12]))
    need(len(b)==214,'B214 order')
    left=[(a-18,b,c,d) for a,b,c,d in b]
    right=[(-a+18,-b,c,d) for a,b,c,d in b]
    points=[];index={};maps=[]
    for block in (G,left,right):
        image=[]
        for p in block:
            if p not in index:
                index[p]=len(points);points.append(p)
            image.append(index[p])
        maps.append(image)
    need(len(points)==343,'source collisions')
    need(point_hash(points)=='8e44b5746cc16badb0ddc6db1bb33d5d64baa088f0715a175632977c5d371a13','source point stream')
    return points,maps,b

def proper(word, n, edges, colours='0123', omitted=None):
    need(isinstance(word,str) and len(word)==n,'word length')
    need(all(ch in colours if i!=omitted else ch=='-' for i,ch in enumerate(word)), 'word alphabet')
    need(all(i==omitted or j==omitted or word[i]!=word[j] for i,j in edges),'improper word')

def adjacency(n,edges):
    adj=[set() for _ in range(n)]
    for a,b in edges:
        adj[a].add(b);adj[b].add(a)
    return adj

def components(adj,omitted=None):
    remaining=set(range(len(adj)))-{omitted};count=0
    while remaining:
        todo=[remaining.pop()];count+=1
        while todo:
            u=todo.pop();new=adj[u]&remaining;remaining-=new;todo.extend(new)
    return count

def decide_pinned(n,edges,pins):
    """Finite exhaustive domain search; every branch is a possible next colour.

    Singleton propagation is forced by edge inequalities. A conflict closes
    a branch, never a heuristic. Choosing MRV only changes the branch order.
    """
    adj=adjacency(n,edges);nodes=0;conflicts=0
    def visit(dom,queue):
        nonlocal nodes,conflicts
        nodes+=1
        while queue:
            u=queue.pop();bit=dom[u]
            for v in sorted(adj[u]):
                if dom[v]&bit:
                    new=dom[v]&~bit
                    if new==0:
                        conflicts+=1;return None
                    dom[v]=new
                    if new&(new-1)==0:
                        queue.append(v)
        undec=[v for v in range(n) if dom[v]&(dom[v]-1)]
        if not undec:
            return ''.join(str(d.bit_length()-1) for d in dom)
        v=min(undec,key=lambda v:(dom[v].bit_count(),-sum(bool(dom[u]&(dom[u]-1)) for u in adj[v]),v))
        bits=dom[v]
        while bits:
            bit=bits&-bits;bits-=bit;dd=dom.copy();dd[v]=bit
            found=visit(dd,[v])
            if found is not None:
                return found
        return None
    dom=[15]*n
    for i,c in pins.items():
        need(0<=i<n and 0<=c<4,'pin range');dom[i]=1<<c
    word=visit(dom,sorted(pins))
    return word,nodes,conflicts

def cnf(n,edges,bad=BAD):
    clauses=[]
    for v in range(n):
        clauses.append([4*v+c+1 for c in range(4)])
        clauses.extend([[-4*v-a-1,-4*v-b-1] for a,b in combinations(range(4),2)])
    clauses.extend([[-4*a-c-1,-4*b-c-1] for a,b in edges for c in range(4)])
    clauses.extend([[4*i+int(c)+1] for i,c in enumerate(bad)])
    rows=[f'p cnf {4*n} {len(clauses)}']+[' '.join(map(str,c))+' 0' for c in clauses]
    return ('\n'.join(rows)+'\n').encode()

def native_budget(points):
    """Coordinate accounting only; never inspect a receiver relation table."""
    path=HERE.parent/'hadwiger_nelson_parts373_receiver_relation/points.tsv'
    need(hashlib.sha256(path.read_bytes()).hexdigest()=='f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50','parent fixture hash')
    rows=[tuple(map(int,line.split())) for line in path.read_text().splitlines() if line and not line.startswith('#')]
    need(len(rows)==509 and all(len(r)==16 for r in rows),'parent fixture shape')
    host={tuple(3*x for x in row):i for i,row in enumerate(rows) if i<374 and i!=310}
    need(len(host)==373,'host order')
    need(all(all(r[j]==0 for j in range(16) if j not in (0,5,9,12)) for r in host),'native host field membership')
    overlaps=[]
    for i,(a,b,c,d) in enumerate(points):
        row=[0]*16;row[0]=8*a;row[5]=8*b;row[9]=8*c;row[12]=8*d
        if tuple(row) in host:overlaps.append((i,host[tuple(row)]))
    need([v for i,v in overlaps if i<10]==[0,153,150,169,166,161,158,53,65,59],'Golomb role map')
    need(len(overlaps)==137,'native collision count')
    return {'host_points':373,'shared_points':137,'new_points':104,'merged_points':477,
            'all_points_in_reviewed_four_colour_field':True,
            'scope':'coordinate accounting and known field theorem; no receiver relation query or solve'}

def run(cert):
    need(cert['schema']=='opposed241-conditional-core-v1','schema')
    source,maps,b=geometry();ids=cert['source_ids']
    need(ids==sorted(set(ids)) and ids[:10]==list(range(10)) and len(ids)==241 and ids[-1]<343,'core labels')
    points=[source[i] for i in ids];edges=all_edges(points);n=len(points)
    need(len(set(points))==n and len(edges)==991,'complete core geometry')
    need(point_hash(points)==cert['point_sha256'],'core point stream')
    eh=digest(f'{a} {b}' for a,b in edges);need(eh==cert['edge_sha256'],'core edge stream')
    need(cert['bad_word']==BAD,'specified complete input word')
    ge=all_edges(G);need(len(ge)==18,'Golomb edges');proper(BAD,10,ge)
    words=[]
    for tail in product(range(4),repeat=7):
        w=(0,1,2)+tail
        if all(w[a]!=w[b] for a,b in ge):words.append(''.join(map(str,w)))
    need(len(words)==95,'complete Golomb input count')
    need(not any(all(w[a]!=w[b] for a,b in ge) for tail in product(range(3),repeat=7) for w in [(0,1,2)+tail]),'Golomb lower bound')
    proper(cert['proper4'],n,edges);proper(cert['proper5'],n,edges,'01234')
    need(cert['proper4'][:10]!=BAD,'surviving distinct full input')
    need(set(cert['proper5'])==set('01234'),'five-word uses five colours')
    deletions=cert['deletion_words'];need(set(deletions)=={str(v) for v in range(10,n)},'all private deletion witnesses')
    for v in range(10,n):
        w=deletions[str(v)];need(w[:10]==BAD,'deletion input');proper(w,n,edges,omitted=v)
    source_to_core={v:i for i,v in enumerate(ids)};left=set(maps[1]);right=set(maps[2])
    lm=[source_to_core[v] for v in maps[1] if v in source_to_core]
    rm=[source_to_core[v] for v in maps[2] if v in source_to_core]
    inherited=[(a,b) for a,b in edges if {ids[a],ids[b]}<=left or {ids[a],ids[b]}<=right]
    private=[e for e in edges if e not in set(inherited)]
    need(len(private)==47,'private contacts')
    w=cert['without_private_contacts_word'];need(w[:10]==BAD,'contact-deleted input');proper(w,n,inherited)
    need(any(w[a]==w[b] for a,b in private),'contacts must actually reject witness')
    # Check isolated full B214 words in the original B order and their Golomb images.
    be=all_edges(b)
    for k,name in ((1,'isolated_left_word'),(2,'isolated_right_word')):
        ww=cert[name];proper(ww,214,be)
        locations={v:i for i,v in enumerate(maps[k])}
        need(''.join(ww[locations[i]] for i in range(10))==BAD,'isolated complete input')
    adj=adjacency(n,edges);need(components(adj)==1,'connected core')
    cuts=[v for v in range(n) if components(adj,v)!=1];need(not cuts,'core has a cut vertex')
    word,nodes,conflicts=decide_pinned(n,edges,{i:int(c) for i,c in enumerate(BAD)})
    need(word is None,'forbidden complete input extended')
    ch=hashlib.sha256(cnf(n,edges)).hexdigest();need(ch==cert['core_cnf_sha256'],'conditional CNF')
    return {'status':'VERIFIED_CONDITIONAL_CORE','points':n,'complete_unit_edges':len(edges),'all_pairs':n*(n-1)//2,
        'private_contacts':len(private),'left_points':len(lm),'right_points':len(rm),'shared_points':len(set(lm)&set(rm)),
        'minimum_degree':min(map(len,adj)),'articulations':cuts,'chromatic_number':4,
        'complete_input_patterns':len(words),'excluded_complete_input':BAD,'surviving_complete_input':cert['proper4'][:10],
        'full_core_input_relation_enumerated':False,'private_deletion_witnesses':len(deletions),
        'conditional_search_nodes':nodes,'conditional_conflicts':conflicts,
        'source_points_removed':343-n,'new_points_beyond_golomb':n-10,'parts373_target_145_met':n<=145,
        'point_hash':point_hash(points),'edge_hash':eh,'conditional_cnf_hash':ch,
        'native_role_budget':native_budget(points),'receiver_tested':False,'record_candidate':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');ap.add_argument('--check-expected',action='store_true');ap.add_argument('--emit-cnf',type=Path);args=ap.parse_args()
    c=json.loads(args.certificate.read_text());result=run(c)
    if args.emit_cnf:
        ps,_,_=geometry();ps=[ps[i] for i in c['source_ids']];args.emit_cnf.write_bytes(cnf(len(ps),all_edges(ps)))
    if args.check_expected:
        need(result==json.loads((HERE/'EXPECTED.json').read_text()),'expected result')
    print(json.dumps(result,indent=2,sort_keys=True))
