"""Truth tables for three-edge counters, including weights three and seven."""
from itertools import product
import hashlib,json
from pysat.formula import IDPool
from pysat.card import CardEnc,EncType
from pysat.solvers import Solver

records=[]
patterns=[(1,2,3),(1,1,2),(-1,2,2),(-1,-2,3,3),(1,1,2,2,3,3),(1,1,1,-2,3),(-1,-1,-1,2,2,3,3),(-1,)*7+(2,3)]
for mode in ("eq","le","ge"):
    for lits in patterns:
        for bound in range(len(lits)+1):
            pool=IDPool(start_from=5)
            f={"eq":CardEnc.equals,"le":CardEnc.atmost,"ge":CardEnc.atleast}[mode]
            clauses=f(lits=list(lits),bound=bound,vpool=pool,encoding=EncType.seqcounter).clauses
            for guarded in (False,True):
                cnf=[([-4] if guarded else [])+c for c in clauses]
                with Solver(name="g4",bootstrap_with=cnf) as solver:
                    for bits in product((0,1),repeat=4):
                        count=sum(bits[abs(x)-1] if x>0 else 1-bits[abs(x)-1] for x in lits)
                        want={"eq":count==bound,"le":count<=bound,"ge":count>=bound}[mode]
                        want=want or (guarded and not bits[3])
                        answer=solver.solve(assumptions=[i+1 if b else -(i+1) for i,b in enumerate(bits)])
                        if bool(answer)!=bool(want):raise ValueError((mode,lits,bound,guarded,bits))
                        records.append((mode,lits,bound,guarded,bits,bool(answer)))
print(json.dumps({"assignments":len(records),
                  "entry_sha256":hashlib.sha256(json.dumps(records).encode()).hexdigest(),
                  "signed_repeated_literals_and_guards":True},sort_keys=True,indent=2))
