#!/usr/bin/env python3
"""One bounded labeled reverse-tree test of the precise full-growth mechanism L."""
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from kernel import validate_permutation
from verify_kernel import direct_occurrences
from tree_dynamics import cartesian_shape
from reverse_tree_merges import perfect_tree
from publish_tree_join_v1 import barrier


class Incomplete(RuntimeError): pass


def fixture(sigma,state_cap=50000,seconds_cap=30):
    sigma=validate_permutation(sigma);m=len(sigma)
    if m==0 or m&(m-1): raise ValueError('Positive power-of-two input length required')
    n=4*m-1;start=perf_counter();states=set();branches=0
    leaf_values={4*i:m+x for i,x in enumerate(sigma)}
    leaf_values.update({4*i+2:i+1 for i in range(m)})
    def original(offset,length):
        if length==0: return ()
        k=length//2
        return offset+k,original(offset,k),original(offset+k+1,k)
    tree=original(0,n)
    @lru_cache(maxsize=None)
    def maximum_leaf(t):
        if not t: return 0
        return max(leaf_values.get(t[0],0),maximum_leaf(t[1]),maximum_leaf(t[2]))
    def merges(left,right):
        def build(l,r,seen_r,last_l):
            if not l and not r:
                yield ();return
            if l and not (seen_r and last_l):
                for tail in build(l[2],r,seen_r,True):
                    yield l[0],l[1],tail
            if r:
                for tail in build(l,r[1],True,False):
                    yield r[0],tail,r[2]
        yield from build(left,right,False,False)
    @lru_cache(maxsize=None)
    def solve(t):
        nonlocal branches
        if not t: return ()
        states.add(t)
        if len(states)>state_cap: raise Incomplete('state cap; no existence verdict')
        if perf_counter()-start>seconds_cap: raise Incomplete('time cap; no existence verdict')
        root,l,r=t
        if root in leaf_values and leaf_values[root]!=maximum_leaf(t): return None
        for parent in merges(l,r):
            branches+=1
            tail=solve(parent)
            if tail is not None: return (root,)+tail
        return None
    result={'sigma':sigma,'m':m,'n':n,'state_cap':state_cap,'seconds_cap':seconds_cap,
            'full_target_solved':False,'universal_L_proved':False}
    try: history=solve(tree)
    except Incomplete as e:
        result['status']='incomplete:'+str(e);history=None
    else:
        result['status']='complete nonexistence for this fixture' if history is None else 'fixture witness only; uniform existence unproved'
    if history is not None:
        p=[0]*n
        for step,node in enumerate(history): p[node]=n-step
        def st(xs):
            ranks={x:i+1 for i,x in enumerate(sorted(xs))}
            return tuple(ranks[x] for x in xs)
        actual_leaf_order=st(p[::2])
        expected=tuple(x for pair in zip((m+x for x in sigma),range(1,m+1)) for x in pair)
        if actual_leaf_order!=expected or st(p[::4])!=sigma:
            raise RuntimeError('Leaf band/input recovery failed')
        if direct_occurrences(tuple(p)) or cartesian_shape(tuple(p))!=perfect_tree((n+1).bit_length()-1):
            raise RuntimeError('Witness literal avoidance/perfect shape failed')
        result.update({'witness':p,'descending_original_node_history':history,
                       'literal_complete_occurrences':[],'perfect_shape_checked':True,
                       'leaf_band_decode_checked':True,'sigma_decode_checked':True})
    result.update({'states_visited':len(states),'merge_branches':branches,'seconds':perf_counter()-start})
    return result


def main():
    barrier();root=Path(__file__).resolve().parent
    output=root/'leaf_band_first_fixture_v1.json'
    if output.exists(): raise RuntimeError('Preserve existing original')
    answer=fixture((2,1,4,3))
    answer['actor']='literature-researcher-3'
    answer['source_sha256']=sha256(Path(__file__).read_bytes()).hexdigest()
    answer['plan_sha256']=sha256((root/'LEAF_BAND_COMPLETION_PLAN_V1.md').read_bytes()).hexdigest()
    output.write_text(json.dumps(answer,indent=2)+'\n');print(json.dumps(answer,indent=2))


if __name__=='__main__': main()
