#!/usr/bin/env python3
"""Definition-level baseline for a proposed uniform balanced-tree join bound."""
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

from reverse_tree_merges import perfect_tree
from tree_dynamics import cartesian_shape
from verify_kernel import direct_occurrences


def avoiding_fiber(height):
    n=(1<<height)-1
    tree=perfect_tree(height)
    return [p for p in permutations(range(1,n+1))
            if cartesian_shape(p)==tree and not direct_occurrences(p)]


def join(alpha,beta,selected):
    m=len(alpha)
    left=tuple(selected)
    chosen=set(left)
    right=tuple(x for x in range(1,2*m+1) if x not in chosen)
    return tuple(left[x-1] for x in alpha)+(2*m+1,)+tuple(right[x-1] for x in beta)


def pair_count(alpha,beta):
    m=len(alpha)
    good=0
    evidence=sha256()
    for selected in combinations(range(1,2*m+1),m):
        p=join(alpha,beta,selected)
        occurrences=direct_occurrences(p)
        good+=int(not occurrences)
        evidence.update((json.dumps([selected,p,occurrences],separators=(',',':'))+'\n').encode())
    return {'alpha':alpha,'beta':beta,'valid_rank_partitions':good,
            'definition_occurrence_stream_sha256':evidence.hexdigest()}


def main():
    root=Path(__file__).resolve().parent
    rows=[]
    for height in (1,2):
        fiber=avoiding_fiber(height)
        pairs=[pair_count(a,b) for a in fiber for b in fiber]
        rows.append({'height':height,'m':len(fiber[0]),'fiber':fiber,'pair_counts':pairs,
                     'minimum_valid_rank_partitions':min(r['valid_rank_partitions'] for r in pairs),
                     'candidate_lower_bound':1<<((len(fiber[0])-1)//2)})
    for height in (1,2,3):
        fiber=avoiding_fiber(height)
        data=str(len(fiber[0]))+' '+str(len(fiber))+'\n'
        data+=''.join(' '.join(map(str,p))+'\n' for p in fiber)
        (root/f'balanced_fiber_h{height}.txt').write_text(data)
    result={'actor':'literature-researcher-3','status':'finite definition baseline only',
            'full_growth_target_solved':False,'rows':rows}
    (root/'balanced_join_reference.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
