"""Check exact-cover rejection DAGs independently of search and MRV order.

Coverage and footprint conflicts are rebuilt by cell incidence. Failed states
are verified in increasing remaining-cell count. No search verdict is trusted.
"""
from collections import defaultdict

class Audit:
    totals={'covers':0,'negative_checks':0,'positive_checks':0,'failed_states':0}
    def __init__(self,cover,extra_conflict=None):
        self.cover=cover;self.valid=set()
        Audit.totals['covers']+=1
        owners=defaultdict(set)
        for i,t in enumerate(cover.tiles):
            for p in t:owners[p].add(i)
        self.at=[]
        for p in cover.required:self.at.append(sum(1<<i for i in owners[p]))
        self.conflicts=[]
        for i,t in enumerate(cover.tiles):
            bad={i}
            for p in t:bad.update(owners[p])
            self.conflicts.append(sum(1<<j for j in bad))
        if extra_conflict is not None:
            for i in range(len(cover.tiles)):
                for j in range(i):
                    if extra_conflict(i,j):
                        self.conflicts[i]|=1<<j;self.conflicts[j]|=1<<i
        self.covers=[sum(1<<j for j,p in enumerate(cover.required) if i in owners[p]) for i in range(len(cover.tiles))]
        assert self.at==cover.at and self.covers==cover.covers
        assert self.conflicts==cover.conflicts

    def certify(self,root):
        c=self.cover
        for available,remaining in sorted(c.failed-self.valid,key=lambda k:(k[1].bit_count(),k)):
            assert remaining and available&~c.all==0 and remaining&~c.full==0
            checked=False;bits=remaining
            while bits and not checked:
                bit=bits&-bits;bits^=bit
                choices=self.at[bit.bit_length()-1]&available
                checked=True
                while choices:
                    choice=choices&-choices;choices^=choice;i=choice.bit_length()-1
                    child=(available&~self.conflicts[i],remaining&~self.covers[i])
                    if child not in self.valid:
                        checked=False;break
            assert checked,'Failed state has no exhaustive certified branch'
            self.valid.add((available,remaining))
            Audit.totals['failed_states']+=1
        assert root in self.valid,'Negative decision has no certified root'
        Audit.totals['negative_checks']+=1

    def witness(self,indices,forced=None):
        c=self.cover
        assert len(indices)==len(set(indices))
        if forced is not None:assert forced in indices
        used=set();cells=set()
        for i in indices:
            assert not cells.intersection(c.tiles[i]);cells.update(c.tiles[i])
            assert all(not (self.conflicts[i]>>j)&1 for j in used)
            used.add(i)
        assert set(c.required)<=cells
        Audit.totals['positive_checks']+=1
