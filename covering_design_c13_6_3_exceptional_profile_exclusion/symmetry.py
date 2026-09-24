"""Explicit point automorphisms of each fixed through-link system."""
from itertools import permutations,product
from collections import Counter
import json

def automorphisms(columns):
    groups={m:tuple(i for i,c in enumerate(columns) if c==m) for m in set(columns)}
    keys=sorted(groups)
    for perm in permutations(range(5)):
        action={m:sum(1<<perm[i] for i in range(5) if m>>i&1) for m in keys}
        if any(action[m] not in groups or len(groups[action[m]])!=len(groups[m]) for m in keys):continue
        for choices in product(*(permutations(groups[action[m]]) for m in keys)):
            image=[None]*11
            for m,targets in zip(keys,choices):
                for old,new in zip(groups[m],targets):image[old]=new
            yield tuple(image)

def move(block,perm):return sum(1<<perm[p] for p in range(11) if block>>p&1)



def make_templates(records, completions):
    templates=[]
    summary=[]
    for index,covers_list in sorted(completions.items()):
        covers=set(map(tuple,covers_list))
        actions=tuple(automorphisms(records[index]['columns']))
        rows=set(records[index]['rows'])
        for action in actions:
            if len(set(action))!=11 or {move(row,action) for row in rows}!=rows:
                raise ValueError('invalid through-system automorphism')
        left=set(covers);sizes=[]
        while left:
            representative=min(left)
            orbit={tuple(sorted(move(block,action) for block in representative)) for action in actions}
            if not orbit<=covers:raise ValueError('completion orbit leaves the complete census')
            left-=orbit;sizes.append(len(orbit))
            templates.append(dict(type=index,cover=covers_list.index(list(representative)),
                                  a=records[index]['rows'],b=list(representative)))
        summary.append(dict(type=index,automorphisms=len(actions),orbit_sizes=sizes))
    return templates,summary
