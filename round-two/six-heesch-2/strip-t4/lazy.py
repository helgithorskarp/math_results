"""Independent cell-incidence reconstruction and rejection-DAG reader.

Full conflict matrices are unnecessary for the short late-stage proofs:
rebuild a row only when the certificate branches on its candidate.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from geometry import DIRS, affine, halo, inverse, pose


def sha(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':'),sort_keys=True).encode()).hexdigest()


def touching(a,b):
    """Direct unit-edge incidence, independent of the search's halo masks."""
    return any((x+u,y+v) in b for x,y in a for u,v in DIRS)


def pool(tile,fixed,domain):
    """All whole copies that can help cover the fixed union's halo."""
    fixed=tuple(fixed);domain=set(domain)
    occupied=set().union(*(set(t) for t in fixed))
    required=tuple(sorted(halo(occupied)))
    needed=set(required)
    frames={t:pose(tile,t) for t in fixed}
    transported={t:{affine(u,frames[t]) for u in domain} for t in fixed}
    candidates=set().union(*transported.values())
    oldsets={t:set(t) for t in fixed}
    tiles=tuple(sorted(u for u in candidates
                       if occupied.isdisjoint(u) and not needed.isdisjoint(u)
                       and all(not touching(u,oldsets[t]) or u in transported[t]
                               for t in fixed)))
    return required,tiles


class Instance:
    def __init__(self,tile,required,tiles,domain):
        self.tile=tuple(sorted(tile));self.required=tuple(required);self.tiles=tuple(tiles)
        self.domain=set(domain);self.sets=[set(t) for t in self.tiles]
        self.frames={}
        by_cell={q:j for j,q in enumerate(self.required)}
        self.at=[0]*len(self.required);self.cover=[]
        for i,t in enumerate(self.tiles):
            bits=0
            for q in t:
                if q in by_cell:
                    j=by_cell[q];bits|=1<<j;self.at[j]|=1<<i
            if not bits:raise ValueError('A candidate covers no required cell')
            self.cover.append(bits)
        self.all=(1<<len(self.tiles))-1;self.full=(1<<len(self.required))-1
        self._conflicts={}

    def frame(self,i):
        if i not in self.frames:self.frames[i]=inverse(pose(self.tile,self.tiles[i]))
        return self.frames[i]

    def conflict(self,i):
        if i not in self._conflicts:
            bits=0
            for j,t in enumerate(self.tiles):
                if self.sets[i]&self.sets[j]:
                    bits|=1<<j
                elif touching(self.tiles[i],self.sets[j]):
                    u=affine(self.tiles[i],self.frame(j))
                    v=affine(t,self.frame(i))
                    if u not in self.domain or v not in self.domain:bits|=1<<j
            self._conflicts[i]=bits
        return self._conflicts[i]

    def reject(self,certificate):
        if certificate['pool_sha256']!=sha({'required':self.required,'tiles':self.tiles}):
            raise ValueError('Wrong instance fingerprint')
        root=tuple(int(s,16) for s in certificate['root'])
        if root!=(self.all,self.full):raise ValueError('Wrong rejection root')
        nodes=[(int(a,16),int(r,16),j) for a,r,j in certificate['nodes']]
        if len({(a,r) for a,r,j in nodes})!=len(nodes):raise ValueError('Duplicate certificate states')
        valid=set()
        for available,remaining,j in sorted(nodes,key=lambda v:(v[1].bit_count(),v)):
            if not remaining or available&~self.all or remaining&~self.full:
                raise ValueError('Invalid state masks')
            if type(j) is not int or not 0<=j<len(self.required) or not (remaining>>j)&1:
                raise ValueError('Invalid split cell')
            choices=self.at[j]&available
            while choices:
                bit=choices&-choices;choices^=bit;i=bit.bit_length()-1
                child=(available&~self.conflict(i),remaining&~self.cover[i])
                if child not in valid:raise ValueError('An exhaustive branch has no failed child')
            valid.add((available,remaining))
        if root not in valid:raise ValueError('Root is not certified')
        return len(nodes)


def enumerate_stars(tile,domain,node_guard=100000):
    """Set-based cover recursion on the first uncovered point, without MRV.

This is separate from Cover.solutions and does not read its conflict masks.
Every contacting copy covers a halo cell, so a disjoint full cover has no
redundant additional root neighbors.
"""
    tiles=tuple(sorted(domain));required=set(halo(tile))
    cell_sets=[set(t) for t in tiles];frames=[inverse(pose(tile,t)) for t in tiles]
    adjacency={q:[i for i,t in enumerate(cell_sets) if q in t] for q in required}
    excluded={}
    def compatible(i,j):
        key=tuple(sorted((i,j)))
        if key not in excluded:
            bad=bool(cell_sets[i]&cell_sets[j])
            if not bad and touching(tiles[i],cell_sets[j]):
                bad=affine(tiles[i],frames[j]) not in domain or affine(tiles[j],frames[i]) not in domain
            excluded[key]=bad
        return not excluded[key]
    result=set();nodes=0
    def visit(chosen,remaining,available):
        nonlocal nodes
        nodes+=1
        if nodes>node_guard:raise RuntimeError('Independent inventory node guard')
        if not remaining:
            result.add(tuple(sorted(chosen)));return
        q=min(remaining)
        for i in adjacency[q]:
            if i in available:
                next_available={j for j in available if j!=i and compatible(i,j)}
                visit(chosen+(i,),remaining-cell_sets[i],next_available)
    visit((),required,set(range(len(tiles))))
    return {tuple(tiles[i] for i in ids) for ids in result},nodes
