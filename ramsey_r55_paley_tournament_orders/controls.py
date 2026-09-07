#!/usr/bin/env python3
import copy
import itertools as it
import json
from pathlib import Path
import random
from build import ordering_clauses
from check import propagation,check_tree,verify as proof_check,need
from extract import graph,extract
from verify import verify as physical_check


def edge_text(matrix):
    edges=[(u,v) for u,v in it.combinations(range(43),2) if matrix[u][v]]
    return f'43 {len(edges)}\n'+''.join(f'{u} {v}\n' for u,v in edges)


def rejected(fn):
    try: fn()
    except (ValueError,TypeError,KeyError): return
    raise ValueError('invalid input accepted')


def run():
    pairs=list(it.combinations(range(5),2)); mask=(1<<10)-1
    index={pair:i for i,pair in enumerate(pairs)}
    physical_good=[]
    for g in range(1<<10):
        ok=True
        for k,c in [(4,1),(5,0)]:
            if any(all((g>>index[u,v]&1)==c for u,v in it.combinations(q,2))
                   for q in it.combinations(range(5),k)): ok=False
        physical_good.append(ok)
    order_bits=[]
    for order in it.permutations(range(5)):
        pos={v:i for i,v in enumerate(order)}
        order_bits.append(sum(1<<i for i,(u,v) in enumerate(pairs) if pos[u]<pos[v]))
    semantic_cases=0
    for tournament in range(1<<10):
        rows=[[False]*5 for _ in range(5)]
        for i,(u,v) in enumerate(pairs):
            rows[u][v]=bool(tournament>>i&1); rows[v][u]=not rows[u][v]
        cs,_=ordering_clauses(rows)
        bit_clauses=[(sum(1<<(x-1) for x in c if x>0),sum(1<<(-x-1) for x in c if x<0)) for c in cs]
        for values in order_bits:
            encoded=all(values&p or (mask^values)&n for p,n in bit_clauses)
            physical=physical_good[mask^(tournament^values)]
            need(bool(encoded)==physical,'order/physical encoding mismatch')
            semantic_cases+=1
    transitive=bit_clauses[:20]
    valid_values=[v for v in range(1<<10) if all(v&p or (mask^v)&n for p,n in transitive)]
    need(valid_values==sorted(order_bits),'comparison transitivity coverage')
    possible=[]
    for pattern in it.product((-1,0,1),repeat=3):
        c=[(i+1)*x for i,x in enumerate(pattern) if x]
        if c: possible.append(c)
    checked=0
    for count in range(4):
        for clauses in it.combinations(possible,count):
            satisfying=[v for v in range(8) if all(any(bool(v>>(abs(x)-1)&1)==(x>0) for x in c) for c in clauses)]
            for initial in it.product((-1,0,1),repeat=3):
                models=[v for v in satisfying if all(x==0 or bool(v>>i&1)==(x>0) for i,x in enumerate(initial))]
                out=propagation(clauses,[0,*initial])
                if out is None: need(not models,'false unit conflict')
                else: need(all(all(x==0 or bool(v>>i&1)==(x>0) for i,x in enumerate(out[1:])) for v in models),'false propagation')
                checked+=1
    case={'order':[],'nodes':[[1,-1,-1]],'root':0}
    need(check_tree([[1,2],[1,-2],[-1,2],[-1,-2]],case,2)==(1,2),'small branching proof')
    rejected(lambda:check_tree([[1]],{'order':[],'nodes':[],'root':-1},1))
    cert=json.loads(Path(__file__).with_name('certificate.json').read_text())
    proof_check(cert)  # The full permutation census is cached only within this process.
    mutations=[]
    def change(fn):
        c=copy.deepcopy(cert); fn(c); mutations.append(c)
    change(lambda c:c.update(prime=41))
    change(lambda c:c['cases'].pop())
    change(lambda c:c['cases'][1].update(order=c['cases'][0]['order']))
    change(lambda c:c['cases'][1].update(nodes=[],root=-1))
    change(lambda c:c['cases'][1]['nodes'][0].__setitem__(0,True))
    change(lambda c:c['cases'][1]['nodes'][0].__setitem__(1,0))
    for c in mutations: rejected(lambda c=c:proof_check(c))
    rng=random.Random(430043); samples=[]
    natural=list(range(43))
    samples.extend([natural,natural[::-1]])
    for _ in range(24):
        order=natural[:]; rng.shuffle(order); samples.extend([order,order[::-1]])
    disjoint=json.loads(Path(__file__).with_name('disjoint_fixture.json').read_text())
    S=disjoint[1:22]; Q=sorted({x*x%43 for x in range(1,43)})
    need(sorted(S)==Q and disjoint==[0]+S+[(-v)%43 for v in S],'boundary fixture structure')
    special_matrix=graph(disjoint)
    need(not any(all(special_matrix[u][v] for u,v in it.combinations(q,2))
                 for q in it.combinations(Q,4)),'boundary fixture has a red K4')
    blue_fives=sum(all(not special_matrix[u][v] for u,v in it.combinations(q,2))
                   for q in it.combinations(Q,5))
    need(blue_fives>0,'boundary fixture needs a blue K5')
    samples.extend([disjoint,[0]+S+sorted((-v)%43 for v in Q),[0]+Q+[(-v)%43 for v in S]])
    outcomes={}
    for order in samples:
        matrix=graph(order); c=extract(order)
        result=physical_check(edge_text(matrix),c)
        key=tuple(result['colors']); outcomes[str(key)]=outcomes.get(str(key),0)+1
    # Under every affine tournament automorphism, verify every physical pair.
    base=samples[2]; matrix=graph(base)
    Q={x*x%43 for x in range(1,43)}; transports=0
    for a,b in it.product(sorted(Q),range(43)):
        labels=[(a*v+b)%43 for v in range(43)]
        changed=graph([labels[v] for v in base])
        need(all(matrix[u][v]==changed[labels[u]][labels[v]] for u,v in pairs43()),'affine transport')
        transports+=1
    for order in [[],[0]*43,[True,*range(1,43)],list(range(42))+[43]]:
        rejected(lambda order=order:graph(order))
    text=edge_text(graph(natural)); c=extract(natural)
    bad=copy.deepcopy(c); bad['witnesses'][0]['color']=1-bad['witnesses'][0]['color']
    rejected(lambda:physical_check(text,bad))
    bad=copy.deepcopy(c); bad['witnesses'][1]=bad['witnesses'][0]
    rejected(lambda:physical_check(text,bad))
    bad=copy.deepcopy(c); bad['witnesses'][0]['vertices'][0]=True
    rejected(lambda:physical_check(text,bad))
    rejected(lambda:physical_check('43 1\n0 43\n',c))
    return {'status':'VERIFIED_PALEY_TOURNAMENT_CONTROLS','all_five_vertex_tournaments':1024,
            'order_encoding_physical_comparisons':semantic_cases,'comparison_assignments':1024,
            'unit_propagation_truth_table_cases':checked,'rejected_proof_certificates':len(mutations),
            'extractor_orders':len(samples),'extractor_color_patterns':outcomes,'affine_transports':transports,
            'transported_physical_pairs':transports*903,'rejected_orders':4,'rejected_physical_certificates_or_graphs':4,
            'red_K4_free_local_boundary_fixture_blue_fives':blue_fives}


def pairs43(): return it.combinations(range(43),2)


if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
