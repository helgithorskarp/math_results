#!/usr/bin/env python3
"""Two blue-triangle-free anchors and complete r=4 equality formulas."""
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent/'ramsey_r55_order3_eleven_cycle_obstruction'
PREVIOUS = ROOT.parent/'ramsey_r55_order3_eleven_four_empty_split'
CLASSIFICATION = ROOT.parent/'ramsey_r55_order3_eleven_empty_signature'/'classification.json'
PARENT_PIN = 'c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f'
CLASSIFICATION_PIN = '163bf5fd836ff5fbd58387182995d9389f85b2d8eade6f6bef4009a313a09f98'
BOUNDARY_PIN = '4e450e3df6f5277612a53baab4e2a8231a800d517566c42d9854d5200e09cf7b'
PAIRS = tuple(combinations(range(3), 2))
REPS = {11:'100110110', 13:'110110101'}
REMOVED = {(-4,7), (-5,8), (-6,9)}
CORE_VARIABLES = (1,2,3,4,5,6,31,32,33)


def require(ok, why):
    if not ok: raise ValueError(why)


def info(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while b := f.read(1<<20): h.update(b)
    return dict(bytes=path.stat().st_size, sha256=h.hexdigest())


def transform(bits, perm, shift, sign):
    def edge(i,j,d):
        if i>j: i,j,d=j,i,-d
        return bits[3*PAIRS.index((i,j))+d%3]
    return ''.join(edge(perm[i],perm[j],sign*d+shift[j]-shift[i])
                   for i,j in PAIRS for d in range(3))


def blue_free(bits):
    return all(bits[(b-a)%3]=='1' or bits[3+(c-a)%3]=='1' or
               bits[6+(c-b)%3]=='1' for a,b,c in product(range(3),repeat=3))


def classify():
    words = [''.join(map(str,w)) for w in product((0,1),repeat=3) if sum(w)<3]
    maps = list(product(permutations(range(3)),product(range(3),repeat=3),(1,-1)))
    free = []
    for ws in product(words,repeat=3):
        bits = ''.join(ws)
        if not blue_free(bits): continue
        hits = []
        for index,rep in REPS.items():
            for perm,shift,sign in maps:
                if transform(bits,perm,shift,sign)==rep:
                    hits.append(dict(type=index,perm=perm,shift=shift,sign=sign)); break
        require(len(hits)==1,'two-type coverage/disjointness')
        free.append(dict(bits=bits,**hits[0]))
    require(info(CLASSIFICATION)['sha256']==CLASSIFICATION_PIN,'classification pin')
    require(info(PREVIOUS/'boundary.json')['sha256']==BOUNDARY_PIN,'boundary pin')
    remaining=json.loads((PREVIOUS/'boundary.json').read_text())['remaining_open']
    cores=json.loads(CLASSIFICATION.read_text())['rows']
    rows=[]; lookup={r['bits']:r for r in free}; pairs4=list(combinations(range(4),2))
    for core in cores:
        if core['index'] not in remaining: continue
        choices=[]
        for omitted in range(4):
            triple=[i for i in range(4) if i!=omitted]
            bits=''.join(core['bits'][3*pairs4.index((i,j))+d]
                         for i,j in combinations(triple,2) for d in range(3))
            if bits in lookup:
                record=lookup[bits]
                choices.append(dict(omitted=omitted,anchor_bits=bits,type=record['type'],
                                    perm=[triple[i] for i in record['perm']]+[omitted],
                                    shift=list(record['shift'])+[0],sign=record['sign']))
        require(choices,'residual core lacks free anchor')
        rows.append(dict(index=core['index'],bits=core['bits'],labeled=core['labeled'],anchors=choices))
    require([r['index'] for r in rows]==remaining,'remaining coverage')
    return dict(format='r55-r4-blue-free-anchor-v1',domain=343,blue_free=free,
                type_counts={str(i):sum(r['type']==i for r in free) for i in REPS},
                residual=rows,remaining_classes=len(rows),remaining_labeled=sum(r['labeled'] for r in rows))


def cases():
    return [dict(id=f'a{i}_equality',type=i,bits=b) for i,b in REPS.items()]


def tail(case):
    units=[v if b=='1' else -v for v,b in zip(CORE_VARIABLES,case['bits'])]
    # Sorted bit vectors, not sorted numeric masks. Fourth red bit stays free.
    masks=(0,4,4,2,2,6,1,1,5,3)
    units += [211+11*f+i if mask>>i&1 else -(211+11*f+i)
              for f,mask in enumerate(masks) for i in range(3)]
    return units


def make(parent, output, case):
    require(info(parent)['sha256']==PARENT_PIN,'complete parent bytes')
    removed=set(); count=0
    with parent.open() as f,output.open('w') as g:
        require(f.readline()=='p cnf 34280 615920\n','parent header')
        g.write('p cnf 34280 615956\n')
        for line in f:
            clause=tuple(map(int,line.split()[:-1]))
            if clause in REMOVED: removed.add(clause);continue
            g.write(line);count+=1
        for unit in tail(case):g.write(f'{unit} 0\n');count+=1
    require(removed==REMOVED and count==615956,'exact removal and total')
    return info(output)
