"""Literal sharpness, hypothesis, encoding and physical-transport controls."""
from pathlib import Path
from itertools import combinations
import json
from encode import formula


def paley_blowup(copies):
    labels = list(range(17))+[0]*(copies-1)
    residues = {x*x%17 for x in range(1,17)}
    n=len(labels); a=[[0]*n for _ in range(n)]
    for u,v in combinations(range(n),2):
        a[u][v]=a[v][u]=int(labels[u]==labels[v] or (labels[u]-labels[v])%17 in residues)
    return a


def literal(a):
    n=len(a)
    red4=[S for S in combinations(range(n),4) if all(a[u][v] for u,v in combinations(S,2))]
    blue4=[S for S in combinations(range(n),4) if all(not a[u][v] for u,v in combinations(S,2))]
    red5=[S for S in combinations(range(n),5) if all(a[u][v] for u,v in combinations(S,2))]
    blue5=[S for S in combinations(range(n),5) if all(not a[u][v] for u,v in combinations(S,2))]
    pairs=[(S,T) for S,T in combinations(red4,2) if set(S).isdisjoint(T)]
    return dict(n=n,red4=len(red4),blue4=len(blue4),red5=len(red5),blue5=len(blue5),red4_disjoint_pairs=len(pairs))


def encode_graph(a):
    n=len(a); word=sum(a[u][v]<<k for k,(u,v) in enumerate(combinations(range(n),2)))
    return dict(n=n,red_hex=format(word,f'0{(n*(n-1)//2+3)//4}x'))


def controls():
    base=literal(paley_blowup(1))
    if base['red4'] or base['blue4']:
        raise ValueError('base Paley graph')
    lower=paley_blowup(2); l=literal(lower)
    if l['red5'] or l['blue4'] or l['red4_disjoint_pairs'] or not l['red4']:
        raise ValueError('sharp order18 control')
    essential=paley_blowup(3); e=literal(essential)
    if e['blue4'] or e['red4_disjoint_pairs'] or not e['red5']:
        raise ValueError('K5 hypothesis control')
    # This is the prior published good19 counterexample, checked without invoking
    # or restarting its discovery computation. It violates the blue-K4-free
    # hypothesis of the present lemma.
    prior=Path(__file__).resolve().parent.parent/'ramsey_r55_good19_packing_bridge_counterexample/graph.json'
    old=json.loads(prior.read_text()); bits=int(old['red_hex'],16); a=[[0]*19 for _ in range(19)]
    for k,(u,v) in enumerate(combinations(range(19),2)):a[u][v]=a[v][u]=(bits>>k)&1
    old_stats=literal(a)
    if old_stats['red5'] or old_stats['blue5'] or not old_stats['blue4'] or old_stats['red4_disjoint_pairs']:
        raise ValueError('prior bridge scope control')
    obj=json.loads((Path(__file__).resolve().parent/'CONTROL_19.json').read_text())
    bits=int(obj['red_hex'],16);aa=[[0]*19 for _ in range(19)]
    for k,(u,v) in enumerate(combinations(range(19),2)):aa[u][v]=aa[v][u]=(bits>>k)&1
    local=literal(aa)
    if local!=obj['literal'] or local['red5'] or local['blue4'] or not local['red4_disjoint_pairs']:
        raise ValueError('positive local control')
    # Truth-table checks compare the specialized CNF with graph definitions;
    # reference.py independently grounds full vertex subsets in the main run.
    trials=0
    for n in (1,2,3):
        for core_bits in range(1<<(n*(n-1)//2)):
            C=[[0]*n for _ in range(n)]
            for k,(u,v) in enumerate(combinations(range(n),2)):C[u][v]=C[v][u]=(core_bits>>k)&1
            clauses=formula(C)
            for word in range(1<<(4*n)):
                aa=[[0]*(n+4) for _ in range(n+4)]
                for u,v in combinations(range(4),2):aa[u][v]=aa[v][u]=1
                for u,v in combinations(range(n),2):aa[4+u][4+v]=aa[4+v][4+u]=C[u][v]
                for w in range(4):
                    for v in range(n):aa[w][4+v]=aa[4+v][w]=(word>>(n*w+v))&1
                truth=literal(aa)
                admissible=not (truth['red5'] or truth['blue4'] or truth['red4_disjoint_pairs'])
                satisfied=all(any(bool((word>>(abs(x)-1))&1)==(x>0) for x in c) for c in clauses)
                if admissible!=satisfied:raise ValueError('definition truth table mismatch')
                trials+=1
    return dict(status='SHARPNESS_AND_HYPOTHESES_VERIFIED',base_paley17=base,order18=l,k5_hypothesis_order19=e,
                positive_local19=local,
                old_good19_counterexample=old_stats,exhaustive_small_assignments=trials,
                order18_graph=encode_graph(lower),k5_hypothesis_graph=encode_graph(essential))


if __name__=='__main__':
    print(json.dumps(controls(),sort_keys=True,indent=2))
