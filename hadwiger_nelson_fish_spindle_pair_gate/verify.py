"""Replay exact geometry and the full relation on every two-terminal set."""
from pathlib import Path
from hashlib import sha256
from itertools import combinations, product
import json
from model import build, moser, need

HERE=Path(__file__).resolve().parent

def relations(graph, summary, cert):
    need(cert['schema']=='fish-spindle-pair-relations-v1','relation schema')
    need(cert['graph_sha256']==summary['graph_sha256'],'graph identity')
    need(cert['forced']==[],'positive complete-relation certificate expected')
    n=len(graph['classes']);E=set(map(tuple,graph['edges']));pairs=list(combinations(range(n),2))
    same=set();different=set();words=cert['words']
    need(type(words) is list and bool(words),'nonempty colouring certificate')
    for word in words:
        need(type(word) is str and len(word)==n and set(word)<=set('0123'),'colour word shape')
        need(all(word[a]!=word[b] for a,b in E),'physical unit-edge inequality')
        for a,b in pairs:
            if word[a]==word[b]:same.add((a,b))
            else:different.add((a,b))
    need(same==set(pairs)-E,'all and only nonunit pairs permit equality')
    need(different==set(pairs),'all distinct pairs permit inequality')
    return {'status':'EVERY TWO-TERMINAL RELATION IS NEUTRAL','words':len(words),
            'same_colour_nonunit_pairs':len(same),'different_colour_pairs':len(different),
            'bare_feasible_canonical_requests':len(same)+len(different),
            'unit_edge_inequalities_checked':len(words)*len(E),
            'word_sha256':sha256(('\n'.join(words)+'\n').encode()).hexdigest()}

def run():
    graph,geometry=build(HERE/'geometry_certificate.json')
    c=json.loads((HERE/'relation_certificate.json').read_text())
    result=relations(graph,geometry,c)
    # The fibre F_0+M is a physical Moser spindle. Check its known lower bound.
    M,ME=moser()
    for word in product(range(3),repeat=7):
        need(any(word[a]==word[b] for a,b in ME),'Moser has no three-colouring')
    return {'geometry':geometry,'relation':result,'chromatic_number':4,
            'two_copy_order_bound_if_equal_pair_existed':2*len(graph['classes'])-1,
            'equal_pair_forcing_found':False,'record_improvement':False,
            'qualifying_physical_signal':False}

if __name__=='__main__':print(json.dumps(run(),indent=2))
