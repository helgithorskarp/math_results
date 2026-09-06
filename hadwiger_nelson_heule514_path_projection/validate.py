#!/usr/bin/env python3
"""Audit emitted formula blocks and decode known positive models; no SAT call."""
import argparse
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path
import time
import verify as V
import relation as R

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('projected_compiler', HERE/'compile.py')
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)


def holds(clauses, true_variables):
    return all(any((abs(x) in true_variables) == (x>0) for x in row) for row in clauses)


def validate(example_out=None):
    start = time.monotonic()
    edges, _, _ = V.geometry(); cert = V.load(HERE/'certificate.json')
    first = V.load(HERE.parent/'hadwiger_nelson_heule514_interface/census.json')['first_residuals'][0]
    states = definitions = positives = 0
    example = None
    for mask in range(16):
        omitted = set(first) | {510+i for i in range(4) if not mask & (1 << i)}
        n,clauses = C.build(edges,omitted,cert)
        kernel = [row for row in clauses if all(x>=2041 for x in row)]
        boundary_defs = [row for row in clauses if any(abs(x)>=2041 for x in row) and row not in kernel]
        old_only = [tuple(row) for row in clauses if all(abs(x)<=2040 for x in row)]
        selected = set(range(510))-omitted
        expected_old = {tuple(4*v+c+1 for c in range(4)) for v in selected} | {(1,)}
        for u,v in edges:
            if u in selected and v in selected:
                expected_old.update((-4*u-c-1,-4*v-c-1) for c in range(4))
        V.need(len(old_only)==len(expected_old) and set(old_only)==expected_old, 'actual complete old formula block')
        V.need(len(boundary_defs)==57, 'actual availability clause count')
        # Check the ACTUAL emitted kernel against the independent assignment oracle.
        assignments = V.colourings(mask)
        for lists in product(range(8), repeat=4):
            true = {2041+3*i+c for i in range(4) for c in range(3) if lists[i] & (1 << c)}
            V.need(holds(kernel,true)==(V.oracle(assignments,lists) is not None), 'actual compiled kernel truth table')
            states += 1
        for i,neighbours in enumerate(V.NEIGHBOURS):
            for c in range(3):
                a = 2041+3*i+c
                rows = [row for row in boundary_defs if a in row or -a in row]
                xs = [4*v+c+2 for v in neighbours]
                V.need(len(rows)==len(xs)+1 and set(abs(x) for row in rows for x in row)=={a,*xs}, 'actual boundary incidence')
                for bits in product((False,True),repeat=len(xs)):
                    for av in (False,True):
                        true = {x for x,b in zip(xs,bits) if b} | ({a} if av else set())
                        V.need(holds(rows,true)==(av==(not any(bits))), 'actual boundary reification truth table')
                        definitions += 1
        if mask==15:
            raw = C.dimacs(n,clauses)
            if example_out:
                example_out.write_bytes(raw)
            example = dict(omitted=first, variables=n,clauses=len(clauses),bytes=len(raw),sha256=sha256(raw).hexdigest(),solver_called=False)
    rows = V.load(HERE.parent/'hadwiger_nelson_heule514_interface/certificate.json')['native']
    for row in rows:
        c = row['colouring']
        V.need(len(c)==514 and all(c[u]=='.' or c[v]=='.' or c[u]!=c[v] for u,v in edges), 'pinned positive model')
        for mask in range(16):
            omitted = {i for i,x in enumerate(c[:510]) if x=='.'} | {510+i for i in range(4) if not mask & (1 << i)}
            _,clauses = C.build(edges,omitted,cert)
            true = {4*v+int(x)+1 for v,x in enumerate(c[:510]) if x!='.'}
            lists = []
            for i,neighbours in enumerate(V.NEIGHBOURS):
                available = {x for x in range(1,4) if str(x) not in {c[v] for v in neighbours}}
                lists.append(sum(1 << (x-1) for x in available))
                true.update(2041+3*i+x-1 for x in available)
            V.need(holds(clauses,true), 'known colouring gives a projected model')
            extension = R.extension(mask,lists)
            V.need(extension is not None, 'reconstruct eliminated vertices')
            decoded = c[:510]+''.join('.' if x<0 else str(x+1) for x in extension)
            V.need(all(decoded[u]=='.' or decoded[v]=='.' or decoded[u]!=decoded[v] for u,v in edges), 'full reconstructed graph colouring')
            positives += 1
    return dict(status='ACTUAL PROJECTED CNF AND WITNESS DECODING VERIFIED',local_states=states,
                actual_definition_assignments=definitions,known_positive_models=positives,
                example_formula=example,native_graph_queries=0,seconds=time.monotonic()-start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--report',type=Path);parser.add_argument('--example-out',type=Path)
    args = parser.parse_args(); result = validate(args.example_out)
    if args.report:
        args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
