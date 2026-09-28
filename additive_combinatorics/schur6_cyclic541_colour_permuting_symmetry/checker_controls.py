"""Check watched propagation against full-clause propagation and truth tables."""
import itertools
import random

from rup import RUP


def naive_rup(clauses, proposed):
    assigned = {-x for x in proposed}
    while True:
        if any(-x in assigned for x in assigned):
            return True
        new = set()
        for clause in clauses:
            if any(x in assigned for x in clause):
                continue
            remaining = set(clause) - {-x for x in assigned}
            if not remaining:
                return True
            if len(remaining) == 1:
                new.update(remaining)
        new -= assigned
        if not new:
            return False
        assigned.update(new)


def controls():
    rng = random.Random(54120)
    candidates = [tuple(sign * (i + 1) for i, sign in enumerate(pattern) if sign)
                  for pattern in itertools.product([-1, 0, 1], repeat=4)]
    comparisons = semantic = 0
    for _ in range(80):
        formula = [list(rng.choice(candidates[1:])) for _ in range(rng.randrange(1, 18))]
        checker = RUP(4, formula)
        order = candidates[:]
        rng.shuffle(order)
        for proposed in order:
            got = checker.implied(proposed)
            if got != naive_rup(formula, proposed):
                raise ValueError("watched propagation disagrees with full scanning")
            comparisons += 1
            if got:
                for values in itertools.product([False, True], repeat=4):
                    def truth(lit):
                        return values[abs(lit) - 1] == (lit > 0)
                    if all(any(truth(x) for x in c) for c in formula):
                        if not any(truth(x) for x in proposed):
                            raise ValueError("RUP accepted a nonconsequence")
                    semantic += 1
                if proposed:  # Exercise retained learned clauses and watch state.
                    checker.add(proposed)
                    formula.append(list(proposed))
    unsat = [[1, 2], [-1, 2], [1, -2], [-1, -2]]
    if RUP(2, unsat).check(["1 0", "-1 0", "0"])["additions"] != 3:
        raise ValueError("small proof failed")
    bad = [([[1, 2]], ["0"]), (unsat, ["1 0"]),
           (unsat, ["3 0", "0"]), (unsat, ["1 0 2 0"]),
           ([[1, 2], [-1, 2]], ["-2 0", "0"])]
    rejected = 0
    for formula, proof in bad:
        try:
            RUP(2, formula).check(proof)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("bad certificate was accepted")
    return {"rup_comparisons": comparisons, "semantic_assignments": semantic,
            "malformed_or_invalid_proofs_rejected": rejected}
