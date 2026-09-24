#!/usr/bin/env python3
"""Exact CNF encoding of the necessary conditions listed in ENCODING.md."""
import itertools as it
from pysat.card import CardEnc, EncType as CE
from pysat.pb import PBEnc, EncType as PE
from pysat.formula import IDPool

N=18
V=range(N)
PAIRS=list(it.combinations(V,2))

class Model:
    def __init__(self, positive=False, facet_edges=None, min_cubics=8):
        self.pool=IDPool()
        self.edges={p:self.pool.id(('e',)+p) for p in PAIRS}
        self.fixed={}
        self.clauses=[]
        self.done=set()
        self.solver=None
        self.true=self.pool.id('true'); self.fix(self.true,True)
        for u,v in PAIRS:
            if v<6: self.fix(self.e(u,v), False)
            if u<6 and 6<=v<12: self.fix(self.e(u,v),v==u+6)
        self.b={(v,k):self.pool.id(('b',v,k)) for v in V for k in range(4,8)}
        if facet_edges is not None:
            k=len(facet_edges)
            for a,p in enumerate(facet_edges):
                for r in range(6): self.fix(self.e(a,r+12),r in p)
                for j in range(4,8): self.fix(self.b[a,j],False)
            for a in range(k,6):
                self.fix(self.b[a,4],True); self.fix(self.b[a+6,4],True)
        for v in V:
            es=[self.e(v,u) for u in V if u!=v]
            self.card(es,3,'ge'); self.card(es,7,'le')
            for k in range(4,8):
                b=self.b[v,k]
                self.card(es,k,'ge',[-b]); self.card(es,k-1,'le',[b])
        self.card([self.b[v,4] for v in V],N-min_cubics,'le')
        for v in range(5):
            for k in range(4,8): self.add([-self.b[v,k],self.b[v+1,k]])
        for r in range(12,18): self.card([self.e(a,r) for a in range(6)],2,'ge')
        if facet_edges is None:
            for r in range(12,17):
                self.pb([(1<<a,self.e(a,r)) for a in range(6)]+[(-(1<<a),self.e(a,r+1)) for a in range(6)],0,'le')
        self.tris={}
        incident=[[] for _ in V]
        for t in it.combinations(V,3):
            y=self.conj([self.e(*p) for p in it.combinations(t,2)],('t',)+t)
            self.tris[t]=y
            for v in t: incident[v].append(y)
        weights=[(w,self.b[v,k]) for v in V for k,w in [(4,2),(5,1),(7,-1)]]+[(1,t) for t in self.tris.values()]
        self.pb(weights,15 if not positive else 14,'ge' if not positive else 'le')
        self.pb([(w,self.b[v,k]) for v in V for k,w in [(4,8),(5,5),(6,2),(7,-1)]]+[(3,t) for t in self.tris.values()],90,'le')
        prod={}
        for v in V:
            for u in V:
                if v!=u:
                    for k in range(4,8):
                        prod[v,u,k]=self.conj([self.e(u,v),self.b[u,k]],('p',v,u,k))
        for v in V:
            ts=[(-1,b) for b in self.b.values()]
            ts.extend([(-6,self.b[v,4]),(-4,self.b[v,5]),(-2,self.b[v,6])])
            ts.extend((2,prod[v,u,k]) for u in V if u!=v for k in range(4,8))
            ts.extend((-2,t) for t in incident[v])
            self.pb(ts,-10,'ge')
            self.card(incident[v],1,'le',[self.b[v,4]])
        for u,v in PAIRS:
            cs=[self.conj([self.e(u,w),self.e(v,w)],('c',u,v,w)) for w in V if w not in (u,v)]
            self.card(cs,1,'le',[self.e(u,v),self.b[u,4],self.b[v,4]])

    def e(self,u,v): return self.edges[tuple(sorted((u,v)))]
    def fix(self,v,val):
        self.fixed[v]=val
        self.clauses.append([v if val else -v])
    def add(self,c):
        new=[]
        for x in sorted(set(c),key=lambda x:(abs(x),x<0)):
            if abs(x) in self.fixed:
                if self.fixed[abs(x)]==(x>0): return
            else: new.append(x)
        if any(-x in new for x in new): return
        self.clauses.append(new)
        if self.solver is not None: self.solver.add_clause(new)
    def conj(self,ls,key):
        fresh=[]
        for x in ls:
            if abs(x) in self.fixed:
                if self.fixed[abs(x)]!=(x>0): return -self.true
            else: fresh.append(x)
        ls=fresh
        if not ls: return self.true
        if len(ls)==1: return ls[0]
        y=self.pool.id(key)
        for x in ls: self.add([-y,x])
        self.add([y]+[-x for x in ls])
        return y
    def card(self,ls,k,op,cond=()):
        fresh=[]
        for x in ls:
            if abs(x) in self.fixed:
                k-=int(self.fixed[abs(x)]==(x>0))
            else: fresh.append(x)
        ls=fresh
        if (op=='ge' and k<=0) or (op=='le' and k>=len(ls)): return
        if (op=='ge' and k>len(ls)) or (op=='le' and k<0): self.add(list(cond)); return
        enc=(CardEnc.atleast if op=='ge' else CardEnc.atmost)(ls,bound=k,vpool=self.pool,encoding=CE.seqcounter)
        for c in enc.clauses: self.add(list(cond)+c)
    def pb(self,terms,bound,op):
        totals={}
        for w,l in terms:
            if l<0: bound-=w; l=-l; w=-w
            if l in self.fixed: bound-=w*int(self.fixed[l])
            else: totals[l]=totals.get(l,0)+w
        lits=[]; weights=[]
        for l,w in totals.items():
            if w<0: l=-l; bound-=w; w=-w
            if w: lits.append(l); weights.append(w)
        if bound<0:
            if op=='le': self.add([])
            return
        enc=(PBEnc.atleast if op=='ge' else PBEnc.atmost)(lits,weights=weights,bound=bound,vpool=self.pool,encoding=PE.best)
        for c in enc.clauses: self.add(c)
    def face(self,S):
        key=('f',tuple(S))
        if key in self.done: return False
        self.done.add(key)
        cond=[self.e(*p) for p in it.combinations(S,2)]
        ys=[self.conj([-self.e(u,v) for u in S],('f',tuple(S),v)) for v in V if v not in S]
        if len(S)<=4: self.card(ys,1,'ge',cond)
        elif len(S)==5:
            self.card(ys,2,'ge',cond); self.card(ys,2,'le',cond)
        elif len(S)==7: self.add(cond)
        else: raise ValueError(S)
        return True

def build(facet_edges, *, positive=False):
    """No adaptive cuts, external graph catalogue, or floating arithmetic."""
    m=Model(positive=positive,facet_edges=facet_edges)
    for size in (5,7):
        for S in it.combinations(V,size):
            if not any(m.fixed.get(m.e(*p)) is True for p in it.combinations(S,2)):
                m.face(S)
    return m
