"""Definition-level finite controls of CNF and the ordered-route bridge."""
import itertools
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
if not (HERE/'sequential_sat.py').exists():sys.path.insert(0,str(HERE.parent))
from sequential_sat import Writer,generate


def scalar(row,word):
    row=list(row)
    for a,b in word:
        if row[a]>row[b]:row[a],row[b]=row[b],row[a]
    return row


def route_controls():
    comparisons=0
    for n,depth in ((3,4),(4,3),(5,2)):
        pairs=list(itertools.combinations(range(n),2))
        rows=[list(v) for v in itertools.product((0,1),repeat=n) if v[1]<=v[-1]]
        for word in itertools.product(pairs,repeat=depth):
            values=[list(v) for v in rows]
            high=[0]*(n-1)+[1]
            low=[1]*n;low[1]=0
            for a,b in word:
                if (high[a] or high[b]) and (not low[a] or not low[b]):
                    assert all(v[a]<=v[b] for v in values)
                    comparisons+=len(values)
                values=[scalar(v,[(a,b)]) for v in values]
                high=scalar(high,[(a,b)]);low=scalar(low,[(a,b)])
    return comparisons


def main():
    from pysat.formula import CNF
    from pysat.solvers import Glucose4
    scratch=HERE/'scratch';scratch.mkdir(exist_ok=True)
    path=scratch/'primitive.cnf'
    truth_controls=0
    for length in range(6):
        for bound in range(-1,length+2):
            w=Writer(path);variables=[w.var() for _ in range(length)]
            w.at_most(variables,bound);w.close()
            with Glucose4(bootstrap_with=CNF(from_file=str(path)).clauses) as solver:
                for mask in range(1<<length):
                    assumptions=[v if mask>>i&1 else -v for i,v in enumerate(variables)]
                    assert solver.solve(assumptions=assumptions)==(mask.bit_count()<=bound)
                    truth_controls+=1
    families=[(2,list(range(4))),(2,[1,2]),(3,list(range(8))),
              (3,[1,2,4]),(3,[3,5,6]),(3,[5])]
    completion_controls=0
    for n,states in families:
        pairs=list(itertools.combinations(range(n),2))
        for gates in range(4):
            expected=any(all(scalar([x>>i&1 for i in range(n)],word)==sorted(x>>i&1 for i in range(n))
                             for x in states) for word in itertools.product(pairs,repeat=gates))
            generate(n,states,gates,path,commute=False,encode_sorted=True)
            with Glucose4(bootstrap_with=CNF(from_file=str(path)).clauses) as solver:
                assert solver.solve()==expected,(n,states,gates)
            completion_controls+=1
    result=dict(status='definition_level_controls_verified',cardinality_assignments=truth_controls,
                complete_small_completion_cases=completion_controls,
                ordered_route_row_events=route_controls())
    (scratch/'primitive-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
