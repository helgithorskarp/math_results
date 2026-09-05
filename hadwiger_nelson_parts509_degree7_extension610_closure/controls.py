#!/usr/bin/env python3
"""Brute-force soundness controls for the small RUP checker."""
from itertools import product
import json
import rup


def main():
    clauses=[[],[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]]
    assignments=[set((i+1 if x else -(i+1)) for i,x in enumerate(values))
                 for values in product((False,True),repeat=2)]
    checks=accepted=0
    for mask in range(1<<len(clauses)):
        formula=[row for i,row in enumerate(clauses) if mask>>i&1]
        models=[values for values in assignments if all(set(row)&values for row in formula)]
        for clause in clauses:
            if rup.is_rup(formula,clause):
                assert all(set(clause)&values for values in models)
                accepted+=1
            checks+=1
    xor=[[1,2],[1,-2],[-1,2],[-1,-2]]
    assert rup.check(xor,[[1],[]])==2
    assert rup.check([[]],[[]])==1
    rejected=0
    for formula,proof in [([[1]],[[]]),([[1,2]],[[-1],[]]),(xor,[]),(xor,[[1]])]:
        try:rup.check(formula,proof)
        except ValueError:rejected+=1
        else:raise AssertionError('invalid or incomplete proof accepted')
    assert rejected==4
    print(json.dumps(dict(formulas=512,clause_checks=checks,rup_steps_confirmed_by_truth_tables=accepted,
                          invalid_or_incomplete_proofs_rejected=rejected,
                          explicit_valid_refutations=2,status='RUP CONTROLS VERIFIED'),indent=2,sort_keys=True))


if __name__=='__main__':main()
