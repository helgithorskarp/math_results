#!/usr/bin/env python3
"""Exact prefix-threshold CNF, with explicit constant simplification."""
class Builder:
    def __init__(self, variables):
        self.variables=variables
        self.rows=[]

    def fresh(self):
        self.variables+=1
        return self.variables

    def clause(self, *lits):
        if any(type(v) is bool and v for v in lits):
            return
        row=[v for v in lits if type(v) is not bool]
        if any(-v in row for v in row):
            return
        self.rows.append(list(dict.fromkeys(row)))

    @staticmethod
    def neg(v):
        return not v if type(v) is bool else -v

    def threshold(self, xs, k):
        if k<=0: return True
        if k>len(xs): return False
        old=[True]+[False]*k
        for i,x in enumerate(xs,1):
            current=[True]
            for j in range(1,k+1):
                if j>i:
                    current.append(False);continue
                a,b=old[j],old[j-1]
                z=self.fresh()
                # z iff a OR (x AND b)
                self.clause(self.neg(a),z)
                self.clause(-x,self.neg(b),z)
                self.clause(-z,a,x)
                self.clause(-z,a,b)
                current.append(z)
            old=current
        return old[k]

    def dimacs(self):
        return (f'p cnf {self.variables} {len(self.rows)}\n'+
                ''.join(' '.join(map(str,row))+' 0\n' for row in self.rows)).encode()
