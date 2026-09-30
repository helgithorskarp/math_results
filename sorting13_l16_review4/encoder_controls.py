"""Independent finite semantic checks of the actual published CNF primitives.

Imports the generator being tested, never its checkers. Small exhaustive
truth tables validate encoding; the general correspondence proof is in REVIEW.md.
"""
import importlib.util
import itertools as it
import json
from pathlib import Path
import tempfile

from audit import require, clauses

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('tested_encoder',ROOT/'sorting13_pure_maximum_exclusions/sequential_sat.py')
encoder=importlib.util.module_from_spec(spec);spec.loader.exec_module(encoder)


def satisfied(rows,bits):
    return all(any(bits[abs(v)-1]==(v>0) for v in c) for c in rows)


def cardinalities(directory):
    count=0;formulas=0
    for n in range(1,5):
        for bound in range(-1,n+1):
            path=directory/'cardinality.cnf';w=encoder.Writer(path)
            variables=[w.var() for _ in range(n)];w.at_most(variables,bound);w.close()
            total,rows=clauses(path);represented=set()
            for bits in it.product((False,True),repeat=total):
                if satisfied(rows,bits):represented.add(bits[:n])
                count+=1
            expected={x for x in it.product((False,True),repeat=n) if sum(x)<=bound}
            require(represented==expected,'at-most semantics');formulas+=1
        path=directory/'one.cnf';w=encoder.Writer(path)
        variables=[w.var() for _ in range(n)];w.exactly_one(variables);w.close()
        total,rows=clauses(path);represented=set()
        for bits in it.product((False,True),repeat=total):
            if satisfied(rows,bits):represented.add(bits[:n])
            count+=1
        require(represented=={x for x in it.product((False,True),repeat=n) if sum(x)==1},
                'exactly-one semantics');formulas+=1
    return {'formulas':formulas,'truth_assignments':count}


def generated_gate(directory):
    # Use all8 three-wire inputs and all3 pairs in one sequential slot.
    # Only sorted-output constants are used by this production encoder.
    # Freeze each pair and compare formula satisfiability with exact replay
    # on singleton targets, including already sorted rows.
    controls=0
    for state in range(8):
        for pair in it.combinations(range(3),2):
            path=directory/'gate.cnf'
            def freeze(w,choices,pairs,bits):
                w.add(choices[0][pairs.index(pair)])
            meta=encoder.generate(3,[state],1,path,commute=False,encode_sorted=True,augment=freeze)
            n,rows=clauses(path);found=False
            for bits in it.product((False,True),repeat=n):
                if satisfied(rows,bits):found=True;break
            output=state
            a,b=pair
            if (state>>a)&1 and not (state>>b)&1:output ^= (1<<a)|(1<<b)
            sorted_mask=((1<<state.bit_count())-1)<<(3-state.bit_count())
            require(found==(output==sorted_mask),'actual generated compare-exchange semantics')
            require(meta['pairs']==list(it.combinations(range(3),2)) and
                    not meta['commute_lexicographic'],'pair cover')
            controls+=1
    return controls


def main():
    with tempfile.TemporaryDirectory(prefix='l16-encoder-') as name:
        directory=Path(name)
        result={'cardinality':cardinalities(directory),'generated_gate_cases':generated_gate(directory)}
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
