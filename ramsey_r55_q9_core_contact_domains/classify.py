"""Physical q9 admission with either a Ramsey witness or a packing redirect."""
from itertools import combinations
from pathlib import Path
import argparse,json
from inputs import need,parents
from contact_codec import Contacts,PhysicalCarrier
from verify_physical import physical,mono

def classify(obj,cache,contacts):
    carrier=PhysicalCarrier(obj['task'],cache,contacts)
    carrier.old.rank(obj['graph']) # exact original ordered pair/star carrier
    a=physical(obj['graph'])
    for i in range(9):
        bad=mono(a,list(range(4*i,4*i+4))+list(range(36,43)))
        if bad is not None:return dict(status='RAMSEY_REJECT',task=obj['task'],bad_five=bad)
    edges=[];used=set()
    for u,v in combinations(range(36,43),2):
        if a[u][v] and u not in used and v not in used:edges.append((u,v));used.update((u,v))
    need(len(edges)>=2,'core matching');e,f=edges[:2]
    for i in range(carrier.r):
        block=list(range(4*i,4*i+4))
        for s in combinations(block,2):
            t=[u for u in block if u not in s]
            if all(a[u][v] for u in s for v in e) and all(a[u][v] for u in t for v in f):
                cliques=[list(s)+list(e),t+list(f)]
                need(all(a[u][v] for clique in cliques for u,v in combinations(clique,2)),'redirect witness')
                return dict(status='PACKING_REDIRECT_REQUIRED',task=obj['task'],red_block=i,new_red_cliques=cliques,
                    requires_existing_h4045_normalizer=True,ramsey_rejection=False)
    return dict(status='CONTACT_CARRIER_ADMITTED_NOT_A_TARGET',task=obj['task'],code=carrier.rank(obj['graph']))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('tables');p.add_argument('input');a=p.parse_args()
    print(json.dumps(classify(json.loads(Path(a.input).read_text()),a.cache,Contacts(a.cache,a.tables)),sort_keys=True))
