"""Check geometry, complete relation, minimal retained core, and correction control."""
import json
from pathlib import Path
from itertools import product, combinations, permutations
from model import POINTS,TERMINALS,FAILED_POINT,need,graph,digest,patterns,check_word

HERE=Path(__file__).resolve().parent

def verify(cert=None):
    if cert is None:
        cert=json.loads((HERE/'certificate.json').read_text())
    need(cert['schema']=='moser-four-terminal-relation-v1','schema')
    edges,distances=graph()
    need(len(edges)==19 and len(distances)==55,'complete graph counts')
    need(not any(a>=7 for a,b in edges),'independent terminal set')
    internal=[e for e in edges if e[1]<7]
    need(len(internal)==11,'Moser interior')
    # The two K4-e diamonds and their joining edge give the written proof.
    left={(0,1),(0,2),(1,2),(1,3),(2,3)}
    right={(0,4),(0,5),(4,5),(4,6),(5,6)}
    need(set(internal)==left|right|{(3,6)},'two diamonds plus joining edge')
    caps={(0,7),(1,7),(2,8),(3,8),(4,9),(6,9),(0,10),(5,10)}
    need(set(edges)-set(internal)==caps,'exact cap incidences')
    need(next(row[2:] for row in distances if row[:2]==(7,8))==(1008,0),
         'first marked pair squared length seven')
    need(next(row[2:] for row in distances if row[:2]==(9,10))==(1008,0),
         'second marked pair squared length seven')
    all_patterns=set(patterns(4))
    forbidden={(0,0,0,0),(0,0,1,1)}
    got=[check_word(w,edges) for w in cert['positive_words']]
    need(len(got)==13 and len(set(got))==13 and set(got)==all_patterns-forbidden,
         'complete canonical positive relation')
    # Certify the negative mechanism locally by all 3^4 diamond colourings.
    diamond_edges=[(0,1),(0,2),(1,2),(1,3),(2,3)]
    diamond_words=[w for w in product(range(3),repeat=4)
                   if all(w[a]!=w[b] for a,b in diamond_edges)]
    need(len(diamond_words)==6 and all(w[0]==w[3] for w in diamond_words),
         'three-colour diamond equality')
    # If both cap pairs are monochromatic, each diamond avoids its cap
    # colour, so 0=3 and 0=6, contradicting the unit edge 3--6.
    need(len(cert['vertex_deletions'])==7,'all interior deletions supplied')
    seen=set()
    for row in cert['vertex_deletions']:
        v=row['deleted'];need(type(v) is int and 0<=v<7 and v not in seen,
                              'unique interior deletion')
        seen.add(v)
        need(len(row['words'])==2,'two formerly forbidden patterns')
        need({check_word(w,edges,removed=v) for w in row['words']}==forbidden,
             'deletion releases both exclusions')
    # Together with restrictions of positive full words, every deletion
    # above now allows all 15 patterns. No smaller retained interior works.
    labelled=set()
    for word in cert['positive_words']:
        pin=tuple(int(word[t]) for t in TERMINALS)
        for perm in permutations(range(4)):
            labelled.add(tuple(perm[c] for c in pin))
    need(len(labelled)==240,'labelled positive patterns')
    formula={w for w in product(range(4),repeat=4)
             if not (w[0]==w[1] and w[2]==w[3])}
    need(labelled==formula,'exact full relation formula')
    for subset in combinations(range(4),3):
        need({tuple(w[i] for i in subset) for w in labelled}
             ==set(product(range(4),repeat=3)),'all three-pin projections neutral')
    failed=list(POINTS);failed[9]=FAILED_POINT
    fe,fd=graph(failed)
    need(len(fe)==18 and (4,9) not in fe,'failed domination formula control')
    fg=[check_word(w,fe) for w in cert['failed_formula_words']]
    need(len(fg)==15 and set(fg)==all_patterns,'failed formula has neutral relation')
    result={
        'status':'EXACT FOUR-TERMINAL RELATION VERIFIED',
        'points':11,'strict_unit_edges':19,'all_pairs':55,'chromatic_number':4,
        'canonical_allowed':13,'canonical_forbidden':['0000','0011'],
        'labelled_allowed':240,'labelled_forbidden':16,
        'neutral_three_terminal_projections':4,
        'neutral_interior_vertex_deletions':7,
        'marked_pair_squared_lengths':[7,7],
        'failed_formula_points_edges':[11,18],
        'failed_formula_allowed_patterns':15,
        'point_sha256':digest(POINTS),'distance_sha256':digest(distances),
        'edge_sha256':digest(edges),'labelled_relation_sha256':digest(sorted(labelled)),
        'qualifying_capped_composition':False,'record_improvement':False,
    }
    return result

if __name__=='__main__':
    print(json.dumps(verify(),indent=2,sort_keys=True))
