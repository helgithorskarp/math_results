"""Bitmask BFS generator, independent of the scalar inverse-fiber verifier.
Author: six-sorting-1, researcher. Arbitrary nongates, no timing/depth cut.
"""
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
PAIRS=tuple(itertools.combinations(range(10),2))
CAPS=(3,2,3)


def enumerate_kernels():
    words=[]
    def visit(p,q,u,word):
        if len(set(p))==1:
            assert p==(0,0,0)
            if u==1 and q[1]==2:
                assert len(word)==3;words.append(word)
            return
        if len(word)==3:return
        for gate in PAIRS:
            occupied=set(p).intersection(gate)
            if not occupied:continue
            new_u=u+(len(occupied)==1)
            new_q=tuple(c+(position in gate) for position,c in zip(p,q))
            if new_u>1 or any(c>cap for c,cap in zip(new_q,CAPS)):continue
            new_p=tuple(gate[0] if position in gate else position for position in p)
            visit(new_p,new_q,new_u,word+(gate,))
    visit((0,1,5),(0,0,0),0,())
    assert len(words)==len(set(words))==59
    return sorted(words)


def transform(profile,gate):
    a,b=gate;A,B=1<<a,1<<b;result={}
    for mask,d in profile:
        new_d=d+bool(mask&(A|B))
        if mask&B and not mask&A:mask^=A|B
        result[mask]=max(result.get(mask,new_d),new_d)
    return tuple(sorted(result.items()))


def close(word,initial,deadline):
    if any(9 in gate for gate in word):
        assert all(gate!=(8,9) for gate in word)
        return {'kernel':word,'status':'excluded_by_sole9_gate'}
    p=(0,1,5);positions=[]
    for gate in word:
        positions.append(p);p=tuple(gate[0] if v in gate else v for v in p)
    assert p==(0,0,0)
    allowed=[tuple(g for g in PAIRS if g==word[i] or set(positions[i]).isdisjoint(g)) for i in range(3)]
    first=(0,False,initial);states={first};queue=deque([first])
    processed=edges=max_cuts=weight_cuts=terminals=0
    status='complete_empty_closure'
    while queue:
        if time.monotonic()>=deadline:status='operational_limit_incomplete';break
        phase,max_used,profile=queue.popleft();processed+=1
        if phase==3:terminals+=1;status='terminal_found';break
        for gate in allowed[phase]:
            edges+=1
            if 9 in gate and (gate!=(8,9) or max_used):max_cuts+=1;continue
            rows=transform(profile,gate)
            if sum(1<<d for mask,d in rows)>512:weight_cuts+=1;continue
            new=(phase+(gate==word[phase]),max_used or 9 in gate,rows)
            if new not in states:
                if len(states)>=50000:status='operational_limit_incomplete';break
                states.add(new);queue.append(new)
        if status=='operational_limit_incomplete':break
    h=hashlib.sha256()
    for state in sorted(states):h.update(json.dumps(state,separators=(',',':')).encode())
    return {'kernel':word,'status':status,'states':len(states),'processed':processed,'queue':len(queue),
            'edges':edges,'maximum_cuts':max_cuts,'weight_cuts':weight_cuts,'terminals':terminals,
            'state_sha256':h.hexdigest()}


def main():
    from driver import run
    fixture=json.loads((HERE/'fixture.json').read_text())
    assert fixture['minimum_caps']==list(CAPS) and fixture['minimum1_passages']==2
    initial=tuple(sorted(map(tuple,fixture['initial_two_minimum_profile'])))
    assert sum(1<<d for mask,d in initial)==208
    catalog=enumerate_kernels()
    run('generate',catalog,lambda word,deadline:close(word,initial,deadline),{'catalog_count':59,'initial_weight':208})


if __name__=='__main__':main()
