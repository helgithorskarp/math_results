"""Two-watch unit propagation and an exact negative-unit RUP reader."""
from collections import defaultdict


class UnitReader:
    def __init__(self, variables, clauses):
        self.variables = variables
        self.clauses = tuple(tuple(c) for c in clauses)
        self.assignment = [0]*(variables+1)
        self.trail = []
        self.head = 0
        self.positions = []
        self.watches = defaultdict(list)
        for i,c in enumerate(self.clauses):
            if not c or any(type(v) is not int or v==0 or abs(v)>variables for v in c):
                raise ValueError('Malformed clause')
            if len(set(c))!=len(c) or any(-v in c for v in c):
                raise ValueError('Unnormalized clause')
            self.positions.append([0,min(1,len(c)-1)])
            if len(c)==1:
                if not self.assign(c[0]):
                    raise ValueError('Contradictory input units')
            else:
                self.watches[c[0]].append(i)
                self.watches[c[1]].append(i)
        if not self.propagate():
            raise ValueError('Input contradicts unit propagation')

    def value(self, literal):
        a = self.assignment[abs(literal)]
        return a if literal>0 else -a

    def assign(self, literal):
        old = self.value(literal)
        if old:
            return old==1
        self.assignment[abs(literal)] = 1 if literal>0 else -1
        self.trail.append(literal)
        return True

    def propagate(self):
        while self.head<len(self.trail):
            false = -self.trail[self.head]
            self.head += 1
            watched = self.watches[false]
            i = 0
            while i<len(watched):
                number = watched[i]
                clause = self.clauses[number]
                positions = self.positions[number]
                side = 0 if clause[positions[0]]==false else 1
                assert clause[positions[side]]==false
                other = clause[positions[1-side]]
                if self.value(other)==1:
                    i += 1
                    continue
                replacement = next((j for j,v in enumerate(clause)
                                    if j not in positions and self.value(v)!=-1),None)
                if replacement is not None:
                    positions[side] = replacement
                    watched[i] = watched[-1]
                    watched.pop()
                    self.watches[clause[replacement]].append(number)
                elif not self.assign(other):
                    return False
                else:
                    i += 1
        return True

    def undo(self, length):
        for literal in self.trail[length:]:
            self.assignment[abs(literal)] = 0
        del self.trail[length:]
        self.head = length

    def read_negative(self, variable):
        if type(variable) is not int or not 1<=variable<=self.variables:
            raise ValueError('Malformed negative unit')
        length = len(self.trail)
        contradiction = not self.assign(variable) or not self.propagate()
        self.undo(length)
        if not contradiction:
            raise ValueError('Negative unit is not RUP')
        assert self.assign(-variable) and self.propagate()

    def add_positive(self, variable):
        if not self.assign(variable) or not self.propagate():
            raise ValueError('Positive anchor contradicted')
