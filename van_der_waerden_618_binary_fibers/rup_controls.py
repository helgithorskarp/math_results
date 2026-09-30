"""Definition-level truth-table controls and malformed-certificate rejection."""
import itertools
import json
from pathlib import Path
import random
import tempfile

from check_rup_lrat import check_addition, verify


def controls():
    positive = '5 2 0 1 2 0\n6 -2 0 3 4 0\n7 0 5 6 0\n'
    base = 'p cnf 2 4\n1 2 0\n-1 2 0\n1 -2 0\n-1 -2 0\n'
    bad = [positive.replace('1 2 0', '1 500 0', 1),
           positive.replace('5 2 0', '5 1 0', 1),
           positive.replace('1 2 0', '-1 2 0', 1),
           '\n'.join(positive.splitlines()[:-1])+'\n',
           '4 d 1 0\n'+positive,
           positive.replace('5 2 0', '5 3 0', 1),
           positive.replace('5 2 0', '4 2 0', 1),
           positive.replace('7 0 5 6 0', '7 0 500 6 0')]
    with tempfile.TemporaryDirectory() as directory:
        cnf = Path(directory)/'input.cnf'; proof = Path(directory)/'proof.lrat'
        cnf.write_text(base); proof.write_text(positive)
        assert verify(cnf, proof)['status'] == 'EXACT_RUP_LRAT_VERIFIED'
        for text in bad:
            proof.write_text(text)
            try:
                verify(cnf, proof)
            except ValueError:
                pass
            else:
                raise AssertionError('invalid certificate accepted')
        cnf.write_text('p cnf 2 1\n1 2 0\n'); proof.write_text('2 0 1 0\n')
        try:
            verify(cnf, proof)
        except ValueError:
            pass
        else:
            raise AssertionError('satisfiable formula accepted as UNSAT')
    rng = random.Random(618)
    accepted = rejected = 0
    for _ in range(1000):
        n = rng.randrange(1, 7)
        clauses = {}
        for cid in range(1, rng.randrange(2, 20)):
            vs = rng.sample(range(1, n+1), rng.randrange(1, min(n, 4)+1))
            clauses[cid] = tuple(v*rng.choice([-1, 1]) for v in vs)
        vs = rng.sample(range(1, n+1), rng.randrange(min(n, 3)+1))
        proposed = tuple(v*rng.choice([-1, 1]) for v in vs)
        values = {abs(lit): int(lit < 0) for lit in proposed}
        hints = []
        conflict = False
        while True:
            progress = False
            for cid, clause in clauses.items():
                if any(abs(lit) in values and values[abs(lit)] == int(lit > 0) for lit in clause):
                    continue
                free = [lit for lit in clause if abs(lit) not in values]
                if len(free) <= 1:
                    hints.append(cid)
                    if not free:
                        conflict = True
                    else:
                        values[abs(free[0])] = int(free[0] > 0)
                    progress = True
                    break
            if conflict or not progress:
                break
        try:
            check_addition(proposed, hints, clauses)
        except ValueError:
            assert not conflict
            rejected += 1
            continue
        assert conflict
        accepted += 1
        for word in itertools.product([0, 1], repeat=n):
            valid = all(any(word[abs(lit)-1] == int(lit > 0) for lit in clause) for clause in clauses.values())
            conclusion = any(word[abs(lit)-1] == int(lit > 0) for lit in proposed)
            assert not valid or conclusion
    return {'status': 'RUP_TRUTH_TABLE_AND_REJECTION_CONTROLS_PASSED',
            'random_cases': 1000, 'accepted_semantically_checked': accepted,
            'correct_rejections': rejected, 'bad_certificate_rejections': len(bad)+1}


if __name__ == '__main__':
    result = controls()
    Path('scratch/vdw/pass4-rup-controls.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
