#!/usr/bin/env python3
"""Test the proposed uniform merge criterion before using it for counting."""
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import platform
import resource
from time import perf_counter

from reverse_tree_merges import (boundary_merges, perfect_tree, ReverseWeights,
                                  StateCapExceeded, word_legal)
from tree_dynamics import (insert_maximum_shape, shape_legal_gaps, size, tree_word)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    start = perf_counter()
    weights = {():1}
    reverse = ReverseWeights(cap=200000)
    checked_merges = 0
    rows = []
    stream = sha256()
    for n in range(11):
        for child, weight in weights.items():
            if child == ():
                continue
            cut = size(child[0])
            seen = set()
            for parent, word in boundary_merges(child[0], child[1], False):
                require(parent not in seen, 'duplicate merge parent')
                seen.add(parent)
                require(insert_maximum_shape(parent, cut) == child,
                        'merge does not reconstruct the child split')
                legal = cut in shape_legal_gaps(parent)
                require(legal == word_legal(word),
                        'spine-word criterion failed '+tree_word(child)+' '+word)
                checked_merges += 1
                stream.update((tree_word(child)+':'+word+':'+str(legal)+'\n').encode())
            filtered = {p for p, _ in boundary_merges(child[0], child[1])}
            require(filtered == {p for p, w in boundary_merges(child[0], child[1], False)
                                 if word_legal(w)}, 'filtered generator not complete')
            require(reverse.weight(child) == weight, 'reverse/forward weight mismatch')
        rows.append({'n':n,'states_compared':len(weights),'avoiders':sum(weights.values())})
        if n != 10:
            next_weights=defaultdict(int)
            for tree, weight in weights.items():
                for gap in shape_legal_gaps(tree):
                    next_weights[insert_maximum_shape(tree,gap)] += weight
            weights=dict(next_weights)
    balanced = []
    for height in range(1,5):
        tree=perfect_tree(height)
        try:
            count=reverse.weight(tree)
        except StateCapExceeded:
            balanced.append({'height':height,'n':size(tree),'status':'state cap reached; no complete count'})
            break
        balanced.append({'height':height,'n':size(tree),'avoiding_fiber':count,
                         'status':'exact finite count; no uniform growth inference'})
    result={'actor':'literature-researcher-3','status':'proposed merge criterion finite replay passed; uniform proof/review pending',
            'full_growth_target_solved':False,'all_forward_state_weights_compared_through':10,
            'all_merge_candidates_checked':checked_merges,'merge_stream_sha256':stream.hexdigest(),
            'rows':rows,'perfect_tree_controls':balanced,'reverse_states':len(reverse.states),
            'reverse_transitions':reverse.transitions,'state_cap':reverse.cap,
            'seconds':perf_counter()-start,'peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'python':platform.python_version(),'processes':1,'native_threads':1}
    Path(__file__).with_name('reverse_merges_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
