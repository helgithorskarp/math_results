"""Small exhaustive search controls and semantic literal/transport rejections."""
from pathlib import Path
from itertools import combinations
import argparse,json
from carrier import *
from isomorphism import invariant

def reject(name,f):
    try:f()
    except ValueError:return name
    raise ValueError('damage accepted: '+name)

def run(work):
    work=Path(work);result=json.loads((work/'RESULT.json').read_text())
    seed=tuple(json.loads((Path(__file__).parent/'INSTANCE.json').read_text())['classical68_words'])
    controls=[];graphs=0;states=0
    for n in range(6):
        edges=tuple(combinations(range(n),2))
        for mask in range(1<<len(edges)):
            adj=[0]*n
            for i,(a,b)in enumerate(edges):
                if mask>>i&1:adj[a]|=1<<b;adj[b]|=1<<a
            for k in range(n+2):
                direct=tuple(c for c in combinations(range(n),k)if all(adj[a]>>b&1 for a,b in combinations(c,2)))
                got,_=exact_cliques(adj,k)
                require(got==direct,'all small graph/subset literal comparison');states+=1
            graphs+=1
    controls.append(reject('duplicated classical word',lambda:packing(seed[:-1]+(seed[0],))))
    controls.append(reject('wrong weight',lambda:packing(seed[:-1]+(seed[-1]^(seed[-1]&-seed[-1]),))))
    controls.append(reject('wrong cardinality',lambda:packing(seed[:-1])))
    controls.append(reject('out of physical domain',lambda:packing(seed[:-1]+(seed[-1]|1<<18,))))
    # Valid unused-point replacement of one word destroys C5 invariance.
    w=next(x for x in seed if x>>16&1); damaged=tuple(sorted((set(seed)-{w})|{(w^(1<<16))|1<<17}))
    require(admissible(damaged),'positive single-word replacement packing control')
    controls.append(reject('valid packing with broken g symmetry',lambda:packing(damaged)))
    bad=list(G);bad[0]=G[1]
    controls.append(reject('nonbijective point transport',lambda:require(sorted(bad)==list(range(18)),'bijection')))
    # A proper point permutation with different cycle multipliers fails normalization.
    p=list(range(18))
    for i,x in enumerate(CYCLES[0]):p[x]=CYCLES[0][2*i%5]
    require(sorted(p)==list(range(18)),'positive mismatched map bijection')
    def normalizes(p):
        for k in range(1,5):
            power=list(range(18))
            for _ in range(k):power=[G[x]for x in power]
            if all(p[G[x]]==power[p[x]]for x in range(18)):return True
        return False
    controls.append(reject('unequal cycle multipliers',lambda:require(normalizes(p),'no common multiplier')))
    labelled=[tuple(c)for c in json.loads((work/'labelled.json').read_text())]
    keys=Counter(invariant(c)for c in labelled)
    require(len(keys)==5,'five full-isomorphism invariants')
    class0=set(tuple(c)for c in json.loads((work/'centralizer_classes.json').read_text())[0])
    square=list(range(18))
    for cyc in CYCLES:
        for i,x in enumerate(cyc):square[x]=cyc[2*i%5]
    rep=tuple(result['centralizer_representatives'][0]); moved=code_image(rep,square)
    require(moved not in class0 and moved in set(labelled),'strict centralizer versus normalizer positive control')
    z={'exhaustive_small_graphs':graphs,'complete_graph_target_checks':states,'semantic_rejections':controls,'valid_nonsymmetric_packing_control':True,'strict_normalizer_coarsening_control':True,'full_label_free_invariant_keys':len(keys)}
    print(json.dumps(z,sort_keys=True,separators=(',',':')));return z

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--expect');a=p.parse_args();z=run(a.work)
    if a.expect:require(z==json.loads(Path(a.expect).read_text()),'controls expected')
