"""One exact physical CNF for the union of the four declared frames.

No degree, codegree, packing, symmetry, or imported-theorem clauses are added.
Every K5 clause is generated, then simplified by the literal frame substitution.
Output and any solver proofs belong in a bulk directory outside this package.
"""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import shutil
import time
from graphs import frame, require


def substitution():
    fixed = frame('5', 'A')
    expr = {}
    variable = 0
    for v in range(1, 43):
        for u in range(v):
            if v < 16 and (u, v) not in ((0, 15), (7, 15), (11, 15)):
                expr[u, v] = bool(fixed[u] >> v & 1)
            elif (u, v) == (11, 15):
                expr[u, v] = -expr[7, 15]
            else:
                variable += 1
                expr[u, v] = variable
    require(variable == 785, 'physical dimension')
    return expr, variable


def clauses(expr):
    for vertices in combinations(range(43), 5):
        values = [expr[e] for e in combinations(vertices, 2)]
        for color in (1, 0):
            out = set()
            satisfied = False
            for value in values:
                if type(value) is bool:
                    if value != bool(color):
                        satisfied = True
                        break
                else:
                    literal = -value if color else value
                    if -literal in out:
                        satisfied = True
                        break
                    out.add(literal)
            if not satisfied:
                require(out, 'a frame already contains a monochromatic K5')
                yield tuple(sorted(out, key=lambda x: (abs(x), x)))


def generate(outdir):
    started = time.monotonic()
    outdir.mkdir(parents=True, exist_ok=True)
    expr, variables = substitution()
    body = outdir / 'four_frames.body.tmp'
    count = 0
    with body.open('w') as f:
        for clause in clauses(expr):
            f.write(' '.join(map(str, clause)) + ' 0\n')
            count += 1
    cnf = outdir / 'four_frames.cnf'
    with cnf.open('wb') as f, body.open('rb') as src:
        f.write(f'p cnf {variables} {count}\n'.encode('ascii'))
        shutil.copyfileobj(src, f)
    body.unlink()
    h = sha256()
    with cnf.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    meta = {'variables': variables, 'clauses': count, 'bytes': cnf.stat().st_size,
            'sha256': h.hexdigest(), 'seconds': time.monotonic() - started,
            'scope': 'Complete physical good43 extensions of all four c13 minimum-five-footprint frames.',
            'additional_necessary_constraints': [],
            'red_A_choice_variable': expr[0, 15],
            'red_seed5_choice_variable': expr[7, 15],
            'decoder': 'substitution() gives every physical edge as a Boolean constant or signed variable.'}
    (outdir / 'INPUT.json').write_text(json.dumps(meta, indent=2) + '\n')
    return meta


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('outdir', type=Path)
    print(json.dumps(generate(parser.parse_args().outdir), indent=2))
