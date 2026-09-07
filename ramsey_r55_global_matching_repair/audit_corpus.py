"""Read proofs without importing the producer; literal counts and transports."""
import hashlib
import json
from itertools import combinations
from pathlib import Path
import random
import sys

import verify


def word_of(g):
    return sum(g[u][v] << i for i,(u,v) in enumerate(combinations(range(len(g)),2)))


def transport(proof, permutation):
    n=proof['n'];nodes=[None]*len(proof['nodes']);done={}
    def visit(i, used):
        if i in done:
            verify.require(done[i]==used,'transport shared state')
            return
        done[i]=used
        q, children=proof['nodes'][i]
        labels=[v for v in range(n) if q & (1 << v)]
        available=[(u,v) for u,v in combinations(labels,2) if u not in used and v not in used]
        verify.require(len(available)==len(children),'transport branch coverage')
        mapped=[]
        for (u,v),child in zip(available,children):
            visit(child,used | {u,v})
            mapped.append((tuple(sorted((permutation[u],permutation[v]))),child))
        nodes[i]=[sum(1 << permutation[v] for v in labels),[child for edge,child in sorted(mapped)]]
    visit(0,frozenset())
    return {'status':'UNSAT','n':n,'k':proof['k'],'root':0,'nodes':nodes}


def run(proof_dir):
    proof_dir=Path(proof_dir)
    raw=Path(__file__).with_name('parents.json').read_bytes()
    parents=json.loads(raw)
    verify.require(parents['schema']==1 and parents['edge_order']=='combinations(range(43),2), bit k from least significant bit','parent format')
    verify.require(len(parents['records'])==21,'all references')
    rng=random.Random(2026090704)
    rows=[];total_nodes=total_leaves=total_branches=total_pairs=0
    for i,parent in enumerate(parents['records']):
        word=int(parent['red_edge_bits_hex'],16)
        g=verify.dense(43,word)
        red=[(u,v) for u,v in combinations(range(43),2) if g[u][v]]
        literal_text='43 '+str(len(red))+'\n'+''.join(f'{u} {v}\n' for u,v in red)
        verify.require(hashlib.sha256(literal_text.encode()).hexdigest()==parent['canonical_edge_list_sha256'],'canonical physical edge-list hash')
        count=[0,0]
        for q,color in verify.bad_sets(g,5): count[color]+=1
        verify.require(count==parent['expected_blue_red_five_sets'],'parent advertised counts')
        payload=(proof_dir/f'parent_{i:02}.json').read_bytes()
        proof=json.loads(payload)
        facts=verify.check(43,word,proof)
        verify.require(facts['status']=='VERIFIED_COMPLETE_MATCHING_FAMILY_EXCLUSION','full family verdict')
        verify.require(proof['discovery_nodes']==facts['nodes'],'node count')
        p=list(range(43));rng.shuffle(p)
        h=[[0]*43 for _ in range(43)]
        for u,v in combinations(range(43),2): h[p[u]][p[v]]=h[p[v]][p[u]]=g[u][v]
        changed=transport(proof,p)
        moved_word=word_of(h)
        for w,c in (((1 << 903)-1)^word,proof),(moved_word,changed),(((1 << 903)-1)^moved_word,changed):
            more=verify.check(43,w,c)
            verify.require(more==facts,'transport changed proof facts')
        total_nodes+=facts['nodes'];total_leaves+=facts['leaves']
        total_branches+=facts['branches'];total_pairs+=facts['literal_pair_checks']
        rows.append({'index':i,'name':parent['name'],'blue_red_five_sets':count,
                     'proof_sha256':hashlib.sha256(payload).hexdigest(),'proof_bytes':len(payload),
                     'facts':facts})
    # Independent closed-form count, by each possible matching cardinality.
    counts=[]
    from math import factorial
    for k in range(22): counts.append(factorial(43)//(factorial(43-2*k)*(2**k)*factorial(k)))
    return {'status':'VERIFIED_COMPLETE_GLOBAL_MATCHING_GATE','parents_sha256':hashlib.sha256(raw).hexdigest(),
            'references':21,'distinct_physical_parents':len({r['red_edge_bits_hex'] for r in parents['records']}),
            'canonical_edge_lists_checked':21,
            'literal_five_sets_per_parent':962598,'literal_five_sets_total':21*962598,
            'base_proof_nodes':total_nodes,'base_proof_leaves':total_leaves,'base_proof_branches':total_branches,
            'base_literal_pair_checks':total_pairs,'total_proof_checks_with_transports':84,
            'transported_literal_pair_checks':4*total_pairs,
            'proof_bytes':sum(r['proof_bytes'] for r in rows),
            'matchings_by_size':counts,'matchings_per_fixed_parent':sum(counts),'records':rows}


if __name__=='__main__':
    print(json.dumps(run(sys.argv[1]),indent=2,sort_keys=True))
