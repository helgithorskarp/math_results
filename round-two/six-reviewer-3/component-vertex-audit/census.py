"""Complete original14-plane basis domain from all14-bit masks of weight3."""
from itertools import combinations
from geometry import LABELS, CONTACTS

PLANES=LABELS+(98,99)
PAIRS=((0,9),(1,8),(2,12),(4,10),(5,6),(7,11),(8,12),(98,99))
CAPS={98:((-8,12,-5),9),99:((-5,-14,20),15)}

def classify(labels=LABELS,contacts=CONTACTS,pairs=PAIRS):
    if tuple(labels)!=LABELS or tuple(contacts)!=CONTACTS or tuple(pairs)!=PAIRS:
        raise ValueError('literal original scope changed')
    edges={frozenset(e) for e in contacts}
    records=[]
    for mask in range(1<<len(PLANES)):
        if mask.bit_count()!=3:continue
        triple=tuple(PLANES[k] for k in range(len(PLANES)) if mask>>k&1)
        bad=[list(p) for p in pairs if set(p)<=set(triple)]
        clique=all(frozenset(p) in edges for p in combinations(triple,2))
        categories=[]
        if bad:categories.append('incompatible_pair')
        if triple==(6,7,9):categories.append('all_low_A')
        if clique:categories.append('original_equilateral')
        if triple==(4,7,99):categories.append('critical_short')
        if len(categories)>1:raise ValueError('claimed disjoint census has overlap')
        records.append({'triple':list(triple),'incompatible_pairs':bad,
                        'case':categories[0] if categories else 'residual'})
    records.sort(key=lambda r:r['triple'])
    if [tuple(r['triple']) for r in records]!=list(combinations(PLANES,3)):
        raise ValueError('entire mask/combinations basis domains differ')
    return records
