"""Independent, coarser R18 one-unary closure; resumable45-second batches.

six-sorting-1, researcher. Uses scalar one-zero rows for kernel enumeration,
scalar two-zero transitions and inverse fibers for a DFS on (phase,max,F).
There is no preparation counter, minimum-root timing, or suffix-depth bound.
Imports no researcher generator, PySAT or other native computation.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

HERE=Path(__file__).resolve().parent
FIXTURE=HERE/'fixture.json'
LOWER=(0,0,1,3,5,9,12,16,19,25,29,35,39,44)
PAIRS=tuple(itertools.combinations(range(10),2))


def scalar(row,word):
    row=list(row)
    high=low=0
    for a,b in word:
        high+=row[a]==1 or row[b]==1
        low+=row[a]==0 or row[b]==0
        row[a],row[b]=min(row[a],row[b]),max(row[a],row[b])
    return row,high,low


def prerequisites(fixture):
    initial={};caps={0:100,1:100,5:100};maximum9_cap=100
    count=0
    for rec in fixture['R137']['prefixes']:
        prefix=rec['prefix26'];image=set()
        for mask in range(8192):
            values=[(mask>>i)&1 for i in range(13)]
            out,high,low=scalar(values,prefix)
            assert out[10:]==sorted(values)[-3:]
            r=sum(v<<i for i,v in enumerate(out[:10]));image.add(r)
            assert scalar(out,fixture['R137']['known19_control'])[0]==sorted(values)
            if r==512:
                maximum9_cap=min(maximum9_cap,44-LOWER[13-mask.bit_count()]-high)
            if mask.bit_count()==12:
                port=out.index(0);assert port in caps
                caps[port]=min(caps[port],5-low)
            if mask.bit_count()==11:
                zeros=sum((v==0)<<i for i,v in enumerate(out[:10]))
                initial[zeros]=max(initial.get(zeros,0),low)
            count+=1
        assert image==set(fixture['R137']['states'])
        assert 256 in image and 512 in image
    assert caps=={0:3,1:2,5:3} and maximum9_cap==1
    initial=tuple(sorted(initial.items()))
    assert initial==tuple(sorted(map(tuple,fixture['initial_two_minimum_profile'])))
    assert sum(2**d for m,d in initial)==208
    return initial,{'original_inputs':count,'two_minimum_profile':initial,'minimum_caps':caps,
                    'maximum9_cap':maximum9_cap,'R_onehot8_and9':True}


def enumerate_kernels():
    initial=tuple(tuple(int(i!=p) for i in range(10)) for p in (0,1,5))
    words=[]
    def visit(rows,q,unaries,word):
        occupied={r.index(0) for r in rows}
        if len(occupied)==1:
            assert occupied=={0}
            if unaries==1 and q[1]==2:
                assert len(word)==3;words.append(word)
            return
        if len(word)==3:return
        for gate in PAIRS:
            touched=occupied.intersection(gate)
            if not touched:continue
            u=unaries+(len(touched)==1)
            costs=tuple(c+(r[gate[0]]==0 or r[gate[1]]==0) for r,c in zip(rows,q))
            if u>1 or any(c>cap for c,cap in zip(costs,(3,2,3))):continue
            next_rows=tuple(tuple(scalar(r,[gate])[0]) for r in rows)
            visit(next_rows,costs,u,word+(gate,))
    visit(initial,(0,0,0),0,())
    assert len(words)==len(set(words))==59
    return sorted(words)


def marker_transitions():
    table={}
    for positions in itertools.combinations(range(10),2):
        mask=sum(1<<i for i in positions)
        row=[int(i not in positions) for i in range(10)]
        for gate in PAIRS:
            out,high,deleted=scalar(row,[gate])
            destination=sum((v==0)<<i for i,v in enumerate(out))
            assert destination.bit_count()==2
            table[mask,gate]=destination,deleted
    assert len(table)==2025
    return table


def binary_controls(initial,table):
    result=[]
    for word,expected in [(((0,1),(0,5)),768),(((1,5),(0,1)),704)]:
        profile=initial
        for gate in word:
            fibers={}
            for mask,d in profile:
                destination,add=table[mask,gate]
                fibers.setdefault(destination,[]).append(d+add)
            profile=tuple(sorted((mask,max(ds)) for mask,ds in fibers.items()))
        weight=sum(2**d for mask,d in profile)
        assert weight==expected and weight>512
        result.append({'kernel':word,'terminal_profile':profile,'weight':weight})
    return result


def close(word,initial,table,deadline):
    if any(9 in gate for gate in word):
        assert all(gate!=(8,9) for gate in word)
        return {'kernel':word,'status':'excluded_by_sole9_gate'}
    rows=tuple(tuple(int(i!=p) for i in range(10)) for p in (0,1,5))
    positions=[]
    for gate in word:
        positions.append(tuple(r.index(0) for r in rows))
        rows=tuple(tuple(scalar(r,[gate])[0]) for r in rows)
    allowed=[tuple(g for g in PAIRS if g==word[i] or all(p not in g for p in positions[i])) for i in range(3)]
    first=(0,False,initial);states={first};stack=[first]
    edges=processed=max_cuts=weight_cuts=terminals=0
    status='independent_complete_empty_coarse_closure'
    while stack:
        if time.monotonic()>=deadline:
            status='operational_limit_incomplete';break
        phase,max_used,profile=stack.pop();processed+=1
        if phase==3:
            terminals+=1;status='coarse_terminal_found';break
        for gate in allowed[phase]:
            edges+=1
            if 9 in gate and (gate!=(8,9) or max_used):
                max_cuts+=1;continue
            fibers={}
            for mask,d in profile:
                destination,add=table[mask,gate]
                fibers.setdefault(destination,[]).append(d+add)
            next_profile=tuple(sorted((mask,max(ds)) for mask,ds in fibers.items()))
            if sum(2**d for mask,d in next_profile)>512:
                weight_cuts+=1;continue
            new=(phase+(gate==word[phase]),max_used or 9 in gate,next_profile)
            if new not in states:
                if len(states)>=50000:
                    status='operational_limit_incomplete';break
                states.add(new);stack.append(new)
        if status=='operational_limit_incomplete':break
    h=hashlib.sha256()
    for state in sorted(states):h.update(json.dumps(state,separators=(',',':')).encode())
    return {'kernel':word,'status':status,'states':len(states),'processed':processed,'queue':len(stack),
            'edges':edges,'maximum_cuts':max_cuts,'weight_cuts':weight_cuts,'terminals':terminals,
            'coarse_state_sha256':h.hexdigest()}


def main():
    from driver import run
    fixture=json.loads(FIXTURE.read_text())
    initial,controls=prerequisites(fixture)
    catalog=enumerate_kernels()
    table=marker_transitions()
    controls['binary_minimum_kernels']=binary_controls(initial,table)
    run('verify',catalog,lambda word,deadline:close(word,initial,table,deadline),controls)

if __name__=='__main__':main()
