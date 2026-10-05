#!/usr/bin/env python3
"""A decisive exact lumpability test for a proposed three-statistic quotient."""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

from kernel import boxed_occurrences
from tree_dynamics import size, tree_word, shape_legal_gaps, insert_maximum_shape, cartesian_shape


@lru_cache(maxsize=None)
def abc(tree):
    if tree==(): return 1,1,1
    a,b,c=abc(tree[0]);d,e,f=abc(tree[1])
    return b+d,b+f,b


@lru_cache(maxsize=None)
def shapes(n):
    if n==0: return ((),)
    return tuple((l,r) for k in range(n) for l in shapes(k) for r in shapes(n-k-1))


def leaves(tree,path=''):
    if tree==(): return (path,)
    return leaves(tree[0],path+'L')+leaves(tree[1],path+'R')


def admissible(path):
    seen_l=False; previous=None
    for letter in path:
        if seen_l and previous=='R' and letter=='R': return False
        seen_l=seen_l or letter=='L';previous=letter
    return True


def avoiding_representative(tree):
    if tree==(): return ()
    l,r=tree
    left=avoiding_representative(l);right=avoiding_representative(r)
    return tuple(x+len(right) for x in left)+(len(left)+len(right)+1,)+right


def profile(tree):
    result=Counter(abc(insert_maximum_shape(tree,g)) for g in shape_legal_gaps(tree))
    return [{'ABC':t,'multiplicity':result[t]} for t in sorted(result)]


def main():
    root=Path(__file__).resolve().parent
    output=root/'boundary_automaton_probe_v1.json'
    if output.exists(): raise RuntimeError('Preserve original output; new version required')
    result={'actor':'literature-researcher-3','full_target_solved':False,
            'status':'exact author test, separate check pending','sizes_checked':[],
            'plan_sha256':sha256((root/'BOUNDARY_AUTOMATON_PROBE_V1.md').read_bytes()).hexdigest(),
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    for n in range(8):
        seen={}
        count=0
        for tree in shapes(n):
            paths=leaves(tree)
            legal=tuple(g for g,p in enumerate(paths) if admissible(p))
            assert len(paths)==n+1
            if legal!=shape_legal_gaps(tree) or len(legal)!=abc(tree)[0]:
                raise RuntimeError('External language/count mismatch')
            p=avoiding_representative(tree)
            if boxed_occurrences(p) or cartesian_shape(p)!=tree:
                raise RuntimeError('Representative outside the claimed domain')
            signature=abc(tree); children=profile(tree)
            count+=1
            if signature in seen and seen[signature][1]!=children:
                other,old=seen[signature]
                result['counterexample']={'n':n,'ABC':signature,
                    'first_shape':tree_word(other),'second_shape':tree_word(tree),
                    'first_avoiding_representative':avoiding_representative(other),
                    'second_avoiding_representative':p,'first_child_multiset':old,
                    'second_child_multiset':children,
                    'first_legal_gaps':shape_legal_gaps(other),'second_legal_gaps':legal}
                result['status']='Q refuted by exact author collision; no growth conclusion'
                result['sizes_checked'].append({'n':n,'prefix_shapes_checked':count,'complete':False})
                output.write_text(json.dumps(result,indent=2)+'\n')
                print(json.dumps(result,indent=2));return
            seen.setdefault(signature,(tree,children))
        result['sizes_checked'].append({'n':n,'shapes_checked':count,'complete':True})
    result['status']='finite tests pass; universal Q and growth unresolved'
    output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__': main()
