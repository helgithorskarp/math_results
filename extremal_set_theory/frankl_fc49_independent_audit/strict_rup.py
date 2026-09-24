#!/usr/bin/env python3
"""Strict, standalone checker for the RUP-only subset of text LRAT.

No SAT solver or external Python package is imported. RAT hints are rejected.
Every addition, including the empty clause, must produce a conflict by the
specified sequence of unit propagations under the negation of that clause.
"""
import argparse
import json
from pathlib import Path


class InvalidProof(ValueError):
    pass


def read_cnf(path):
    clauses={}; current=[]; header=None
    with path.open() as stream:
        for line in stream:
            words=line.split()
            if not words or words[0]=='c': continue
            if words[0]=='p':
                if header is not None or clauses or current or len(words)!=4 or words[1]!='cnf':
                    raise InvalidProof('Malformed CNF header')
                header=tuple(map(int,words[2:])); continue
            if header is None: raise InvalidProof('Missing CNF header')
            for word in words:
                lit=int(word)
                if abs(lit)>header[0]: raise InvalidProof('Literal exceeds declared variable count')
                if lit: current.append(lit)
                else:
                    clauses[len(clauses)+1]=tuple(current); current=[]
    if header is None or current or len(clauses)!=header[1]:
        raise InvalidProof('Incomplete CNF or wrong clause count')
    return clauses,header


def rup(clause,hints,active):
    assigned={}
    for lit in clause:
        var=abs(lit); val=lit<0  # Falsify the proposed clause.
        if var in assigned and assigned[var]!=val:
            return 0  # The proposed clause is a tautology.
        assigned[var]=val
    steps=0
    for cid in hints:
        if cid<=0: raise InvalidProof('RAT or nonpositive hint is unsupported')
        if cid not in active: raise InvalidProof(f'Hint to inactive clause {cid}')
        unit=None
        for lit in active[cid]:
            var=abs(lit)
            if var in assigned:
                if assigned[var]==(lit>0):
                    raise InvalidProof(f'Satisfied hint clause {cid}')
            elif unit is None: unit=lit
            elif unit!=lit:
                raise InvalidProof(f'Nonunit hint clause {cid}')
        steps+=1
        if unit is None: return steps  # A falsified clause: actual conflict.
        assigned[abs(unit)]=unit>0
    raise InvalidProof('Addition has no propagation conflict')


def check(cnf,proof):
    active,(variables,input_count)=read_cnf(cnf)
    last_add=input_count; additions=0; deletions=0; steps=0; empty=False
    with proof.open() as stream:
        for line_number,line in enumerate(stream,1):
            words=line.split()
            if not words or words[0]=='c': continue
            if len(words)<3: raise InvalidProof(f'Short proof line {line_number}')
            cid=int(words[0])
            if words[1]=='d':
                ids=list(map(int,words[2:]))
                if not ids or ids[-1]!=0 or any(i<=0 for i in ids[:-1]):
                    raise InvalidProof('Malformed deletion')
                for old in ids[:-1]:
                    active.pop(old,None); deletions+=1
                continue
            if cid<=last_add or cid in active:
                raise InvalidProof('Addition IDs must strictly increase')
            data=list(map(int,words[1:]))
            if not data or data[-1]!=0 or data.count(0)!=2:
                raise InvalidProof('Expected clause and hint terminators')
            zero=data.index(0); clause=tuple(data[:zero]); hints=data[zero+1:-1]
            if any(abs(lit)>variables for lit in clause):
                raise InvalidProof('Proof introduces an undeclared variable')
            steps+=rup(clause,hints,active)
            active[cid]=clause; last_add=cid; additions+=1
            if not clause: empty=True
    if not empty: raise InvalidProof('No justified empty clause')
    return {'verified':True,'input_clauses':input_count,'additions':additions,
            'deletion_references':deletions,'propagation_hints_checked':steps}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('cnf',type=Path);ap.add_argument('proof',type=Path)
    args=ap.parse_args()
    try: result=check(args.cnf,args.proof)
    except (InvalidProof,ValueError,OSError) as error:
        print(json.dumps({'verified':False,'error':str(error)})); raise SystemExit(1)
    print(json.dumps(result,sort_keys=True)); print('s VERIFIED')


if __name__=='__main__': main()
