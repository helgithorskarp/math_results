#!/usr/bin/env python3
"""Separate exact star enumeration from the literal four-clique CNF."""
from itertools import combinations,product
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def require(ok,msg):
    if not ok:raise ValueError(msg)


def matrix():
    a=[[False]*24 for _ in range(24)]
    outer_edges={frozenset((i,(i+1)%5)) for i in range(5)}
    for i in range(5):
        group=list(range(5*i,min(5*i+5,24)))
        for j in range(5):
            u=5*i+j;v=5*i+(j+1)%5
            if u<24 and v<24:a[u][v]=a[v][u]=True
        for k in range(i+1,5):
            if frozenset((i,k)) in outer_edges:
                for u in group:
                    for v in range(5*k,min(5*k+5,24)):a[u][v]=a[v][u]=True
    return a


def model_set(n,clauses):
    """Enumerate every complete model by unit propagation and two-way splits."""
    full=(1<<n)-1; models=set();nodes=0
    for pos,neg in clauses:
        require(type(pos) is int and type(neg) is int and pos>=0 and neg>=0 and
                not(pos&neg) and not((pos|neg)&~full),'clause format')
    def visit(ones,zeros):
        nonlocal nodes
        nodes+=1
        while True:
            fresh1=fresh0=0;shortest=None
            for pos,neg in clauses:
                if pos&ones or neg&zeros:continue
                unset=(pos|neg)&~(ones|zeros)
                if not unset:return
                if unset&(unset-1)==0:
                    if pos&unset:fresh1|=unset
                    else:fresh0|=unset
                elif shortest is None or unset.bit_count()<shortest.bit_count():shortest=unset
            if fresh1&fresh0 or fresh1&zeros or fresh0&ones:return
            if not(fresh1|fresh0):break
            ones|=fresh1;zeros|=fresh0
        remaining=full&~(ones|zeros)
        if not remaining:
            models.add(ones);return
        pivot=(shortest if shortest is not None else remaining)
        pivot &= -pivot
        visit(ones|pivot,zeros);visit(ones,zeros|pivot)
    visit(0,0)
    return models,nodes


def verify(cert):
    a=matrix();pairs=list(combinations(range(24),2))
    require(cert['core_order']==24 and cert['free_pairs_at_43']==903-len(pairs),'family dimensions')
    require(cert['core_red_edges']==[[u,v] for u,v in pairs if a[u][v]],'literal core identity')
    qs=[[],[]]
    for q in combinations(range(24),4):
        colors={a[u][v] for u,v in combinations(q,2)}
        if len(colors)==1:qs[int(next(iter(colors)))].append(sum(1<<u for u in q))
    for five in combinations(range(24),5):
        require(len({a[u][v] for u,v in combinations(five,2)})==2,'core is not Ramsey')
    require([len(q) for q in qs]==cert['core_four_cliques_blue_red'],'four-clique census')
    clauses=[(m,0) for m in qs[0]]+[(0,m) for m in qs[1]]
    models,nodes=model_set(24,clauses)
    digest=hashlib.sha256(''.join(f'{m}\n' for m in sorted(models)).encode()).hexdigest()
    require(len(models)==cert['complete_star_count'] and digest==cert['star_set_sha256'],'complete star set')
    # Independently reconstruct each of the short bag tables from actual pairs.
    tables={}
    for n in (4,5):
        classes=[[],[],[],[]]
        for m in range(1<<n):
            r=any(a[i][j] and m>>i&1 and m>>j&1 for i,j in combinations(range(n),2))
            b=any(not a[i][j] and not(m>>i&1) and not(m>>j&1) for i,j in combinations(range(n),2))
            classes[int(r)+2*int(b)].append(m)
        tables[str(n)]=classes
    require(tables==cert['bag_status_masks'],'bag tables')
    weights=[];words=[];rejected=0;expected=set()
    for w in product(range(4),repeat=5):
        weight=1
        for i,s in enumerate(w):weight*=len(tables[str(4 if i==4 else 5)][s])
        good=True
        for i,j in combinations(range(5),2):
            if a[5*i][5*j]:good &= not(w[i]&1 and w[j]&1)
            else:good &= not(w[i]&2 and w[j]&2)
        weights.append([list(w),weight,bool(good)])
        if good and weight:
            words.append([list(w),weight])
            for blocks in product(*(tables[str(4 if i==4 else 5)][s] for i,s in enumerate(w))):
                expected.add(sum(x<<(5*i) for i,x in enumerate(blocks)))
        else:rejected+=weight
    require(models==expected,'entrywise factor versus DPLL equality')
    require(words==cert['feasible_positive_weight_words'] and cert['status_words_checked']==len(weights),'complete status words')
    require(rejected==cert['rejected_star_count'] and len(models)+rejected==1<<24,'all24-bit stars covered')
    require(hashlib.sha256(json.dumps(weights,separators=(',',':')).encode()).hexdigest()==cert['signature_table_sha256'],'signature digest')
    require(cert['forced_red']==[20,23] and cert['forced_blue']==[21,22],'forced incidence scope')
    require(all(all(m>>v&1 for v in cert['forced_red']) and all(not(m>>v&1) for v in cert['forced_blue']) for m in models),'every star forces incidences')
    phi=[5*((2*(v//5)+1)%5)+(2*(v%5)+1)%5 for v in range(24)]
    require(sorted(phi)==list(range(24)) and all(a[u][v]!=a[phi[u]][phi[v]] for u,v in pairs),'self-complement isomorphism')
    return {'status':'VERIFIED_COMPLETE_H24_ATTACHMENT_KERNEL','stars':len(models),'rejected_stars':rejected,
            'literal_clauses':len(clauses),'dpll_nodes':nodes,'star_set_sha256':digest,
            'core_edges':sum(map(sum,a))//2,'core_five_sets_checked':42504,
            'self_complement_pairs_checked':len(pairs)}

if __name__=='__main__':
    print(json.dumps(verify(json.loads((ROOT/'certificate.json').read_text())),indent=2))
