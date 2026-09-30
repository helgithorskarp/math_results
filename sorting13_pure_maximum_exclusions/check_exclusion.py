"""Standalone RUP/core-membership audit, adapted with credit to six-sorting-1.
Primary published source:
https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_endpoint_frontier/check_exclusion.py
Source commit a65309ebb91b28c66b5e3be1f6fc0f2bf3c22e73.
This file imports neither the mathematical generator nor any SAT library.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def clauses(path):
    result = []
    with path.open() as src:
        head = src.readline().split()
        assert head[:2] == ['p', 'cnf']
        n, expected = map(int, head[2:])
        for line in src:
            values = list(map(int, line.split()))
            assert values[-1] == 0 and all(0 < abs(x) <= n for x in values[:-1])
            result.append(tuple(sorted(set(values[:-1]))))
        assert len(result) == expected
    return n, result


class RUP:
    def __init__(self, n, initial):
        self.n = n
        self.formula = []
        self.occurs = defaultdict(list)
        self.units = []
        self.has_empty = False
        for clause in initial:
            self.add(clause)

    def add(self, clause):
        index = len(self.formula)
        self.formula.append(clause)
        if not clause:
            self.has_empty = True
        if len(clause) == 1:
            self.units.append(clause[0])
        for lit in clause:
            self.occurs[lit].append(index)

    def entails_by_rup(self, clause):
        if self.has_empty:
            return True
        assigned = [0] * (self.n + 1)
        pending = [-lit for lit in clause] + self.units
        remaining = [len(c) for c in self.formula]
        satisfied = [False] * len(self.formula)
        for lit in pending:
            variable, sign = abs(lit), 1 if lit > 0 else -1
            if assigned[variable] == -sign:
                return True
            if assigned[variable] == sign:
                continue
            assigned[variable] = sign
            for index in self.occurs[lit]:
                satisfied[index] = True
            for index in self.occurs[-lit]:
                if satisfied[index]:
                    continue
                remaining[index] -= 1
                if remaining[index] == 0:
                    return True
                if remaining[index] == 1:
                    live = [v for v in self.formula[index] if assigned[abs(v)] == 0]
                    assert len(live) == 1
                    pending.append(live[0])
        return False


def subset_check(core, full_path, expected):
    needed = set(core)
    digest = hashlib.sha256()
    count = 0
    with full_path.open('rb') as src:
        line = src.readline(); digest.update(line)
        assert line.decode().strip() == f"p cnf {expected['variables']} {expected['clauses']}"
        for line in src:
            digest.update(line); count += 1
            literals = list(map(int, line.split()))
            assert literals[-1] == 0
            needed.discard(tuple(sorted(set(literals[:-1]))))
    assert count == expected['clauses'] and not needed
    assert digest.hexdigest() == expected['sha256']
    return count


def self_check():
    # Compare RUP soundness with direct satisfiability of every two-variable
    # clause set; nonempty assumptions leave no propagation gap.
    possible = [tuple((i + 1) * sign for i, sign in enumerate(code) if sign)
                for code in __import__('itertools').product((-1, 0, 1), repeat=2)]
    checked = 0
    for chosen in range(1 << len(possible)):
        formula = [c for i, c in enumerate(possible) if chosen >> i & 1]
        rup = RUP(2, formula)
        for candidate in possible:
            extended = formula + [(-lit,) for lit in candidate]
            sat = any(all(any(bool(mask >> (abs(lit) - 1) & 1) == (lit > 0)
                             for lit in c) for c in extended) for mask in range(4))
            answer = rup.entails_by_rup(candidate)
            assert not answer or not sat
            if candidate:
                # Any nonempty assumptions leave at most one free variable,
                # so unit propagation is complete on this restricted case.
                assert answer == (not sat)
            checked += 1
    return checked


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--full-dir',type=Path)
    args=parser.parse_args()
    meta=json.loads((HERE/'exclusion.json').read_text())
    controls=self_check()
    for case in meta['cases']:
        core_path=HERE/case['core_file'];proof_path=HERE/case['proof_file']
        assert hashlib.sha256(core_path.read_bytes()).hexdigest()==case['core_sha256']
        assert hashlib.sha256(proof_path.read_bytes()).hexdigest()==case['proof_sha256']
        n,core=clauses(core_path)
        assert n==case['full_cnf']['variables'] and len(core)==case['core_clauses']
        rup=RUP(n,core)
        assert not rup.entails_by_rup(()),'Premature empty-clause control failed'
        steps=0;ended=False
        for line in proof_path.read_text().splitlines():
            data=list(map(int,line.split()))
            assert data[-1]==0 and all(0<abs(v)<=n for v in data[:-1])
            clause=tuple(sorted(set(data[:-1])))
            assert rup.entails_by_rup(clause),f"Case{case['case']} non-RUP step{steps+1}"
            rup.add(clause);steps+=1
            if not clause:ended=True;break
        assert ended and steps==case['proof_additions']
        count=subset_check(core,args.full_dir/f"J{case['case']}-size14.cnf",case['full_cnf']) if args.full_dir else None
        print(json.dumps(dict(agent='six-sorting-2',role='researcher',case=case['case'],
            status='RUP_and_requested_source_membership_verified',core_clauses=len(core),
            proof_additions=steps,full_cnf_clauses_checked=count,
            tiny_checker_controls=controls,premature_empty_clause_rejected=True)),flush=True)


if __name__=='__main__':main()
